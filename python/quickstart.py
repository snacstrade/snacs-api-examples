"""SNACS Data API quickstart: verify your key, then pull a dilution snapshot and a quote.

Usage:
    export SNACS_API_KEY=snacs_sk_live_...
    python quickstart.py [TICKER]

Docs: https://data.snacs.trade/docs
"""
import os
import sys

import requests

BASE = "https://data.snacs.trade/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['SNACS_API_KEY']}"}


def get(path: str, **params):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "GPUS").upper()

    me = get("/auth/whoami")
    print(f"Authenticated: tier={me['tier']} rate_limit={me['rate_limit_per_min']}/min")

    cov = get(f"/coverage/{ticker}")
    print(f"\n{ticker} coverage: {cov}")

    dil = get(f"/dilution/{ticker}")
    print(f"\nDilution snapshot for {ticker}:")
    for k, v in list(dil.items())[:12]:
        print(f"  {k}: {v}")

    quote = get(f"/market/{ticker}/quote")
    print(f"\nQuote ({quote.get('source')}): {quote}")


if __name__ == "__main__":
    main()
