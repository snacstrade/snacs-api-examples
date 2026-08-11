# SNACS Data API Examples

Runnable examples for the [SNACS Data API](https://snacs.trade/api): SEC dilution forensics, live market data, news, and fundamentals for U.S. equities, plus an [MCP server](https://github.com/snacstrade/snacs-mcp) for AI assistants.

Every example runs against the live API. You need an API key: [snacs.trade/api](https://snacs.trade/api) -> subscribe -> account settings -> API keys.

```bash
export SNACS_API_KEY=snacs_sk_live_...
```

## Python

```bash
pip install requests
python python/quickstart.py GPUS          # auth check, coverage, dilution snapshot, quote
python python/dilution_screener.py --max-runway 6 --max-price 5
python python/point_in_time.py GPUS 2025-12-31
```

- **[quickstart.py](python/quickstart.py)** - verify your key, pull a ticker's coverage flags, forensic dilution snapshot (share counts, cash runway, going concern), and a composite quote.
- **[dilution_screener.py](python/dilution_screener.py)** - walk the cursor-paginated screener and surface companies with under N months of cash runway and an active ATM or shelf on file.
- **[point_in_time.py](python/point_in_time.py)** - the as-of endpoint: share-count checkpoint, facilities in force, and corporate events (each sourced to a SEC accession number) as they stood on any historical date. No lookahead bias.

## JavaScript (Node 18+, zero dependencies)

```bash
node javascript/quickstart.mjs GPUS
```

- **[quickstart.mjs](javascript/quickstart.mjs)** - auth check, dilution snapshot, quote, and recent daily bars with plain `fetch`.

## Rate limits and errors

- Edge: 50 req/min. Alpha: 1,000 req/min. HTTP 429 with a `Retry-After` header when exceeded.
- Errors are RFC 9457 problem documents (`application/problem+json`).
- Metered families report usage via `X-Data-Cap-Bytes` / `X-Data-Used-Bytes` headers.

## Links

[API docs](https://data.snacs.trade/docs) · [OpenAPI spec](https://data.snacs.trade/v1/openapi.json) · [MCP server](https://github.com/snacstrade/snacs-mcp) · [SNACS](https://snacs.trade)
