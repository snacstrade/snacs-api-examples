"""Dilution screener: find low-runway companies with active dilution capacity.

Walks the cursor-paginated /v1/screener and prints tickers with less than
`--max-runway` months of cash and an active ATM or shelf on file.

Usage:
    export SNACS_API_KEY=snacs_sk_live_...
    python dilution_screener.py --max-runway 6 --max-price 5

Docs: https://data.snacs.trade/docs
"""
import argparse
import os

import requests

BASE = "https://data.snacs.trade/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['SNACS_API_KEY']}"}


def screen(max_runway: float, max_price: float):
    cursor = None
    hits = []
    while True:
        params = {"limit": 500}
        if cursor:
            params["cursor"] = cursor
        r = requests.get(f"{BASE}/screener", headers=HEADERS, params=params, timeout=30)
        r.raise_for_status()
        page = r.json()
        for row in page["data"]:
            runway = row.get("cash_runway_months")
            price = row.get("last_price")
            if runway is None or runway > max_runway:
                continue
            if price is not None and max_price and price > max_price:
                continue
            if not (row.get("has_active_atm") or row.get("has_active_shelf")):
                continue
            hits.append(row)
        cursor = page.get("next_cursor")
        if not page.get("has_more") or not cursor:
            break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-runway", type=float, default=6.0, help="months of cash")
    ap.add_argument("--max-price", type=float, default=5.0, help="0 disables the price filter")
    args = ap.parse_args()

    hits = screen(args.max_runway, args.max_price)
    print(f"{len(hits)} tickers with <= {args.max_runway}mo runway and an active ATM/shelf:\n")
    for row in sorted(hits, key=lambda r: r["cash_runway_months"]):
        cap = row.get("market_cap_usd")
        print(f"  {row['ticker']:<6} runway={row['cash_runway_months']:>5}mo "
              f"price={row.get('last_price')} "
              f"atm={'Y' if row.get('has_active_atm') else 'n'} "
              f"shelf={'Y' if row.get('has_active_shelf') else 'n'} "
              f"mcap={f'${cap/1e6:.0f}M' if cap else 'n/a'}")


if __name__ == "__main__":
    main()
