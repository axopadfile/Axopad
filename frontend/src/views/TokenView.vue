<template>
  <div class="token-view" v-if="token">
    <div class="header">
      <div class="t-avatar">{{ token.ticker.slice(0, 2) }}</div>
      <div class="t-id">
        <h1>{{ token.ticker }} <span class="t-name">{{ token.name }}</span></h1>
        <span class="t-status" :class="token.status">{{ token.status }}</span>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat"><span class="sl">Price</span><span class="sv accent">◎{{ token.price?.toExponential(4) }}</span></div>
      <div class="stat"><span class="sl">Market Cap</span><span class="sv accent">◎{{ fmt(token.market_cap_sol) }}</span></div>
      <div class="stat"><span class="sl">Volume</span><span class="sv">◎{{ fmt(token.volume_sol) }}</span></div>
      <div class="stat"><span class="sl">Trades</span><span class="sv">{{ token.trade_count }}</span></div>
    </div>

    <div v-if="token.graduation_progress !== undefined" class="grad">
      <div class="grad-bar"><div class="grad-fill" :style="{ width: (token.graduation_progress * 100) + '%' }"></div></div>
      <span class="grad-pct">{{ (token.graduation_progress * 100).toFixed(1) }}% to graduation (◎85 mcap)</span>
    </div>

    <div class="grid-2">
      <div class="panel">
        <h2>Trade</h2>
        <div class="trade-tabs">
          <button :class="{ active: side === 'buy' }" @click="side = 'buy'">Buy</button>
          <button :class="{ active: side === 'sell' }" @click="side = 'sell'">Sell</button>
        </div>
        <input v-model="amount" class="inp" :placeholder="side === 'buy' ? 'SOL amount' : 'Token amount'" @input="quote" />
        <input v-model="trader" class="inp" placeholder="Your wallet" />
        <div v-if="quoteResult" class="quote">
          <div class="q-row"><span>You {{ side === 'buy' ? 'get' : 'receive' }}</span>
            <span class="accent">{{ side === 'buy' ? fmt(quoteResult.output_amount) + ' ' + token.ticker : '◎' + fmt(quoteResult.output_amount) }}</span></div>
          <div class="q-row"><span>Price impact</span><span :class="quoteResult.price_impact_pct > 5 ? 'red' : ''">{{ quoteResult.price_impact_pct?.toFixed(2) }}%</span></div>
          <div class="q-row"><span>Fee</span><span>◎{{ quoteResult.fee?.toFixed(6) }}</span></div>
        </div>
        <button class="btn-trade" :class="side" @click="execute" :disabled="trading">
          {{ trading ? "..." : (side === "buy" ? "Buy " + token.ticker : "Sell " + token.ticker) }}
        </button>
        <span v-if="tradeErr" class="err">{{ tradeErr }}</span>
      </div>

      <div class="panel">
        <div class="panel-hdr"><h2>AI Analyst</h2><span class="badge">LLM</span></div>
        <button class="btn-analyze" @click="analyze" :disabled="analyzing">{{ analyzing ? "Analyzing..." : "Analyze Token" }}</button>
        <div v-if="analysis" class="analysis">
          <div class="a-row"><span class="al">Momentum</span><span class="av accent">{{ analysis.momentum }}</span></div>
          <div class="a-row"><span class="al">Risk</span><span class="av" :class="riskClass(analysis.risk)">{{ analysis.risk }}</span></div>
          <div class="a-row"><span class="al">Grad Odds</span><span class="av">{{ (analysis.graduation_odds * 100).toFixed(0) }}%</span></div>
          <div class="a-signal">{{ analysis.signal }}</div>
          <div class="a-verdict">💬 {{ analysis.verdict }}</div>
        </div>
      </div>
    </div>

    <div class="panel">
      <h2>Recent Trades</h2>
      <div v-if="trades.length === 0" class="empty">No trades yet.</div>
      <div v-for="t in trades" :key="t.id" class="trade-row" :class="t.side">
        <span class="tr-side" :class="t.side">{{ t.side }}</span>
        <span class="tr-trader muted">{{ t.trader?.slice(0, 8) }}...</span>
        <span class="tr-amt">◎{{ fmt(t.sol_amount) }}</span>
        <span class="tr-tok">{{ fmt(t.token_amount) }} {{ token.ticker }}</span>
        <span class="tr-time muted">{{ fmtTime(t.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getToken, getQuote, buyToken, sellToken, tradeHistory, analyzeToken } from "@/api/index.js";

const route = useRoute();
const token = ref(null), trades = ref([]), analysis = ref(null);
const side = ref("buy"), amount = ref(""), trader = ref("");
const quoteResult = ref(null), trading = ref(false), analyzing = ref(false);
const tradeErr = ref(null);

const fmt = (v) => (v ?? 0).toLocaleString("en", { maximumFractionDigits: 4 });
const fmtTime = (iso) => { try { return new Date(iso).toLocaleTimeString(); } catch { return ""; } };
const riskClass = (r) => ({ high: "red", medium: "warn", low: "accent" }[r] || "");

async function load() {
  token.value = (await getToken(route.params.id)).data;
  trades.value = (await tradeHistory(route.params.id)).data.trades;
}

async function quote() {
  if (!amount.value || parseFloat(amount.value) <= 0) { quoteResult.value = null; return; }
  try { quoteResult.value = (await getQuote(route.params.id, side.value, parseFloat(amount.value))).data; }
  catch { quoteResult.value = null; }
}

async function execute() {
  if (!amount.value || !trader.value) { tradeErr.value = "Amount and wallet required"; return; }
  trading.value = true; tradeErr.value = null;
  try {
    if (side.value === "buy") await buyToken({ token_id: route.params.id, trader: trader.value, sol_in: parseFloat(amount.value) });
    else await sellToken({ token_id: route.params.id, trader: trader.value, tokens_in: parseFloat(amount.value) });
    amount.value = ""; quoteResult.value = null;
    await load();
  } catch (e) { tradeErr.value = e.response?.data?.error || e.message; }
  finally { trading.value = false; }
}

async function analyze() {
  analyzing.value = true; analysis.value = null;
  try { analysis.value = (await analyzeToken(route.params.id)).data; }
  catch (e) { analysis.value = { momentum: "error", risk: "?", signal: e.message, verdict: "", graduation_odds: 0 }; }
  finally { analyzing.value = false; }
}

onMounted(load);
</script>

<style scoped>
.token-view { display: flex; flex-direction: column; gap: 16px; }
.header { display: flex; align-items: center; gap: 12px; }
.t-avatar { width: 48px; height: 48px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent2)); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #000; }
.t-id h1 { font-size: 20px; }
.t-name { font-size: 13px; color: var(--muted); font-weight: 400; }
.t-status { font-size: 10px; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; }
.t-status.bonding { background: rgba(192,132,252,0.1); color: var(--accent); }
.t-status.graduated { background: rgba(74,222,128,0.1); color: var(--green); }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.stat { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; }
.sl { font-size: 10px; color: var(--muted); text-transform: uppercase; }
.sv { font-size: 18px; font-weight: 700; margin-top: 4px; display: block; }
.accent { color: var(--accent); }
.grad { display: flex; flex-direction: column; gap: 4px; }
.grad-bar { height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
.grad-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--green)); }
.grad-pct { font-size: 11px; color: var(--muted); }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 18px; display: flex; flex-direction: column; gap: 10px; }
.panel-hdr { display: flex; align-items: center; gap: 8px; }
.panel h2 { font-size: 14px; }
.badge { font-size: 10px; padding: 2px 8px; border-radius: 4px; background: rgba(192,132,252,0.2); color: var(--accent); }
.trade-tabs { display: flex; gap: 6px; }
.trade-tabs button { flex: 1; background: var(--bg); border: 1px solid var(--border); color: var(--muted); padding: 8px; border-radius: 6px; cursor: pointer; font-family: var(--font); font-size: 12px; }
.trade-tabs button.active { border-color: var(--accent); color: var(--accent); }
.inp { background: var(--bg); border: 1px solid var(--border); color: var(--text); font-family: var(--font); font-size: 12px; padding: 8px 12px; border-radius: 6px; }
.quote { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 10px; display: flex; flex-direction: column; gap: 4px; font-size: 11px; }
.q-row { display: flex; justify-content: space-between; }
.btn-trade { padding: 10px; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; font-family: var(--font); font-size: 13px; }
.btn-trade.buy { background: var(--green); color: #000; }
.btn-trade.sell { background: var(--red); color: #000; }
.btn-trade:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-analyze { background: var(--accent); border: none; color: #000; font-weight: 700; padding: 8px; border-radius: 6px; cursor: pointer; font-family: var(--font); font-size: 12px; }
.analysis { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 12px; display: flex; flex-direction: column; gap: 5px; }
.a-row { display: flex; gap: 12px; font-size: 12px; }
.al { color: var(--muted); min-width: 80px; }
.a-signal { font-size: 11px; line-height: 1.6; border-top: 1px solid var(--border); padding-top: 6px; }
.a-verdict { font-size: 12px; color: var(--accent); }
.err { color: var(--red); font-size: 11px; }
.empty { color: var(--muted); text-align: center; padding: 20px 0; font-size: 12px; }
.trade-row { display: flex; gap: 12px; align-items: center; font-size: 11px; padding: 6px 0; border-bottom: 1px solid var(--border); }
.tr-side { font-size: 10px; padding: 1px 6px; border-radius: 3px; text-transform: uppercase; min-width: 40px; text-align: center; }
.tr-side.buy { background: rgba(74,222,128,0.1); color: var(--green); }
.tr-side.sell { background: rgba(248,113,113,0.1); color: var(--red); }
.tr-amt { min-width: 80px; }
.tr-time { margin-left: auto; }
.muted { color: var(--muted); }
.warn { color: #fbbf24; }
.red { color: var(--red); }
</style>
