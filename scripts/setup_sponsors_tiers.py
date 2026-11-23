#!/usr/bin/env python3
"""Configure GitHub Sponsors tiers for @Ablation-Tool via official GitHub GraphQL API.

Requires `gh` authenticated with the `user` scope:
    gh auth refresh -h github.com -s user
    python3 scripts/setup_sponsors_tiers.py --dry-run
    python3 scripts/setup_sponsors_tiers.py --apply
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

OLD_TIER_IDS = (
    ("ST_kwDOE9q5TM4ACion", "$5 a month (old)"),
    ("ST_kwDOE9q5TM4ACioo", "$10 one time (old)"),
    ("ST_kwDOE9q5TM4ACiou", "$10 a month (old)"),
    ("ST_kwDOE9q5TM4ACiot", "$25 one time (old)"),
    ("ST_kwDOE9q5TM4ACiov", "$100 a month (old)"),
    ("ST_kwDOE9q5TM4ACiop", "$200 one time (old)"),
    ("ST_kwDOE9q5TM4ACios", "$500 one time (old)"),
    ("ST_kwDOE9q5TM4ACior", "$1,000 one time (old)"),
    ("ST_kwDOE9q5TM4ACiow", "$1,000 a month (old)"),
    ("ST_kwDOE9q5TM4ACioq", "$5,000 one time (old)"),
)

NEW_TIERS = (
    # Monthly recurring tiers
    {
        "amount": 5,
        "isRecurring": True,
        "title": "Open Research Backer",
        "description": (
            "- Helps keep Zoe, Dorothy 3D Human Brain Observatory, Dual-Peer Zoe & Clara, "
            "Ablation AIARE, and SafeConvert 100% free, ad-free, and open-source.\n"
            "- Supports continuous offline verification, open documentation, and public releases."
        ),
        "welcomeMessage": (
            "Thank you for backing independent open-source research. Every release, proof, "
            "and tool remains free and verifiable offline."
        ),
    },
    {
        "amount": 25,
        "isRecurring": True,
        "title": "Instrument & Device Supporter",
        "description": (
            "- Funds local compute, cross-platform test hardware (Android, Apple, Linux, Windows, macOS), "
            "and offline verification infrastructure.\n"
            "- Optional sponsor credit in Ablation-Tool/zoe release notes and priority issue triage "
            "for Ablation and Zoe."
        ),
        "welcomeMessage": (
            "Thank you for supporting independent instrument engineering and cross-platform testing."
        ),
    },
    {
        "amount": 100,
        "isRecurring": True,
        "title": "Neuroscience & Metacognition Patron",
        "description": (
            "- Directly supports open work on Operational Metacognition (A_tau(p)), "
            "Dorothy 3D Human Brain Observatory anatomy tools, and zero-telemetry personal safety software (SafeConvert).\n"
            "- Optional patron acknowledgment in release notes plus quarterly written research digests "
            "covering new theorems, benchmarks, and verifiers."
        ),
        "welcomeMessage": (
            "Thank you for patronizing independent open science, Operational Metacognition, "
            "and Dorothy Brain Observatory research."
        ),
    },
    {
        "amount": 500,
        "isRecurring": True,
        "title": "Research & Defensive Security Partner",
        "description": (
            "- Sustains full-time independent research across AI uncertainty/metacognition, "
            "reverse engineering (Ablation AIARE), and defensive infrastructure hardening.\n"
            "- Optional monthly technical architecture discussion (defensive open-source scope aligned "
            "with CONSTITUTION.md) and opt-in organizational acknowledgment."
        ),
        "welcomeMessage": (
            "Thank you for partnering with independent open-source intelligence and security research."
        ),
    },
    # One-time tiers
    {
        "amount": 10,
        "isRecurring": False,
        "title": "One-Time Thank You",
        "description": (
            "- A quick one-time thank-you supporting free, ad-free, open-source software and "
            "offline-verifiable research."
        ),
        "welcomeMessage": "Thank you for the support!",
    },
    {
        "amount": 50,
        "isRecurring": False,
        "title": "Cross-Platform Testing & Build Fund",
        "description": (
            "- Helps cover test devices, storage, and build tooling across Android, Apple, "
            "Linux, Windows, and macOS releases."
        ),
        "welcomeMessage": "Thank you for helping keep every platform tested and open.",
    },
    {
        "amount": 250,
        "isRecurring": False,
        "title": "Local Compute & Hardware Milestone",
        "description": (
            "- Contributes directly toward local workstation GPUs, RAM, and offline model evaluation "
            "hardware so research stays zero-cloud-lock-in and reproducible."
        ),
        "welcomeMessage": "Thank you for fueling local, independent compute.",
    },
    {
        "amount": 1000,
        "isRecurring": False,
        "title": "Open Science Hardware / Module Grant",
        "description": (
            "- Funds dedicated workstation upgrades, neuroimaging visualization tooling, or a focused "
            "open-source research module released publicly under GPL-3.0 / MIT."
        ),
        "welcomeMessage": "Thank you for funding open-source scientific infrastructure.",
    },
)


def _gh_graphql(query: str, variables: dict) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, val in variables.items():
        if isinstance(val, (bool, int)):
            cmd.extend(["-F", f"{key}={json.dumps(val)}"])
        else:
            cmd.extend(["-f", f"{key}={val}"])
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    data = json.loads(proc.stdout)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up clean GitHub Sponsors tiers for @Ablation-Tool.")
    parser.add_argument("--apply", action="store_true", help="Retire old tiers and publish the 8 new tiers live.")
    parser.add_argument("--keep-old", action="store_true", help="Do not retire existing published tiers.")
    parser.add_argument("--draft", action="store_true", help="Create new tiers as drafts instead of publishing immediately.")
    args = parser.parse_args()

    print(f"Planned tiers: {len(NEW_TIERS)} (4 monthly + 4 one-time)")
    for t in NEW_TIERS:
        kind = "monthly" if t["isRecurring"] else "one-time"
        print(f"  - ${t['amount']:,} {kind:8s} | {t['title']}")

    if not args.apply:
        print("\nDry run complete. To apply live:")
        print("  1. gh auth refresh -h github.com -s user")
        print("  2. python3 scripts/setup_sponsors_tiers.py --apply")
        return 0

    if not args.keep_old:
        retire_q = "mutation($tierId: ID!) { retireSponsorsTier(input: {tierId: $tierId}) { sponsorsTier { id name } } }"
        for tid, label in OLD_TIER_IDS:
            try:
                _gh_graphql(retire_q, {"tierId": tid})
                print(f"[RETIRED] {label} ({tid})")
            except RuntimeError as exc:
                print(f"[SKIP/WARN] {label}: {exc}")

    create_q = """
    mutation($amount: Int!, $isRecurring: Boolean!, $description: String!, $welcomeMessage: String!, $publish: Boolean!) {
      createSponsorsTier(input: {
        amount: $amount,
        isRecurring: $isRecurring,
        description: $description,
        welcomeMessage: $welcomeMessage,
        publish: $publish
      }) {
        sponsorsTier { id name monthlyPriceInDollars isOneTime }
      }
    }
    """
    for t in NEW_TIERS:
        res = _gh_graphql(
            create_q,
            {
                "amount": t["amount"],
                "isRecurring": t["isRecurring"],
                "description": t["description"],
                "welcomeMessage": t["welcomeMessage"],
                "publish": not args.draft,
            },
        )
        tier = res["data"]["createSponsorsTier"]["sponsorsTier"]
        state = "DRAFT" if args.draft else "PUBLISHED"
        print(f"[{state}] {tier['name']} ({tier['id']})")

    print("\nAll GitHub Sponsors tiers updated cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
