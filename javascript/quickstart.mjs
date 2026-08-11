// SNACS Data API quickstart (Node 18+, no dependencies).
//
// Usage:
//   export SNACS_API_KEY=snacs_sk_live_...
//   node quickstart.mjs [TICKER]
//
// Docs: https://data.snacs.trade/docs

const BASE = "https://data.snacs.trade/v1";
const headers = { Authorization: `Bearer ${process.env.SNACS_API_KEY}` };

async function get(path, params = {}) {
  const url = new URL(`${BASE}${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

const ticker = (process.argv[2] || "GPUS").toUpperCase();

const me = await get("/auth/whoami");
console.log(`Authenticated: tier=${me.tier} rate_limit=${me.rate_limit_per_min}/min`);

const dil = await get(`/dilution/${ticker}`);
console.log(`\n${ticker} dilution snapshot:`, {
  shares_outstanding: dil.shares_outstanding,
  cash_runway_months: dil.cash_runway_months,
  going_concern: dil.going_concern,
});

const quote = await get(`/market/${ticker}/quote`);
console.log(`\nQuote (${quote.source}): ${quote.price} (${(quote.change_percent * 100).toFixed(1)}%)`);

const bars = await get(`/market/${ticker}/bars`, { limit: 5 });
console.log(`\nLast 5 daily bars:`);
for (const b of bars.data ?? bars) console.log(`  ${b.date} O=${b.open} H=${b.high} L=${b.low} C=${b.close} V=${b.volume}`);
