"""Point-in-time dilution state: what did the company look like on a past date?

The /v1/dilution/{ticker}/as-of/{date} endpoint returns the share-count
checkpoint effective on or before the date, the facilities in force, and the
corporate events up to it - no lookahead bias, safe for backtests.

Usage:
    export SNACS_API_KEY=snacs_sk_live_...
    python point_in_time.py GPUS 2025-12-31

Docs: https://data.snacs.trade/docs
"""
import os
import sys

import requests

BASE = "https://data.snacs.trade/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['SNACS_API_KEY']}"}


def main():
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "GPUS").upper()
    as_of = sys.argv[2] if len(sys.argv) > 2 else "2025-12-31"

    r = requests.get(f"{BASE}/dilution/{ticker}/as-of/{as_of}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    state = r.json()

    cp = state.get("checkpoint") or {}
    print(f"{ticker} as of {as_of}:")
    print(f"  share checkpoint ({cp.get('as_of_date')}): total_shares={cp.get('total_shares')}")

    facs = state.get("facilities") or []
    active = [f for f in facs if f.get("status") == "active"]
    print(f"  facilities on file: {len(facs)} ({len(active)} active)")
    for f in active[:5]:
        print(f"    - {f['facility_type']} {f.get('file_number')} "
              f"capacity=${f.get('capacity_usd')} used=${f.get('used_usd')} status={f['status']}")

    events = state.get("events") or []
    print(f"  corporate events up to {as_of}: {len(events)}")
    for e in events[-3:]:
        print(f"    - {e['event_date']} {e['event_type']}: {e.get('title')} "
              f"(source: {e.get('source_form')} {e.get('source_accession')})")


if __name__ == "__main__":
    main()
