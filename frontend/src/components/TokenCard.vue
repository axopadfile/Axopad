<template>
  <div class="token-card" @click="$router.push(`/token/${token.id}`)">
    <div class="tc-head">
      <div class="tc-avatar">{{ token.ticker.slice(0, 2) }}</div>
      <div class="tc-id">
        <span class="tc-ticker">{{ token.ticker }}</span>
        <span class="tc-name">{{ token.name }}</span>
      </div>
      <span class="tc-status" :class="token.status">{{ token.status }}</span>
    </div>
    <p v-if="token.description" class="tc-desc">{{ token.description }}</p>
    <div class="tc-stats">
      <div class="tc-stat"><span class="tl">MCap</span><span class="tv accent">◎{{ fmt(token.market_cap_sol) }}</span></div>
      <div class="tc-stat"><span class="tl">Vol</span><span class="tv">◎{{ fmt(token.volume_sol) }}</span></div>
      <div class="tc-stat"><span class="tl">Trades</span><span class="tv">{{ token.trade_count }}</span></div>
    </div>
    <div v-if="token.graduation_progress !== undefined" class="tc-progress">
      <div class="tc-bar"><div class="tc-fill" :style="{ width: (token.graduation_progress * 100) + '%' }"></div></div>
      <span class="tc-pct">{{ (token.graduation_progress * 100).toFixed(0) }}% to graduation</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ token: { type: Object, required: true } });
const fmt = (v) => (v ?? 0).toLocaleString("en", { maximumFractionDigits: 2 });
</script>

<style scoped>
.token-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 10px; cursor: pointer; transition: border-color 0.2s; }
.token-card:hover { border-color: var(--accent); }
.tc-head { display: flex; align-items: center; gap: 10px; }
.tc-avatar { width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, var(--accent), var(--accent2)); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #000; font-size: 12px; }
.tc-id { display: flex; flex-direction: column; }
.tc-ticker { font-weight: 700; font-size: 13px; }
.tc-name { font-size: 11px; color: var(--muted); }
.tc-status { margin-left: auto; font-size: 9px; padding: 2px 6px; border-radius: 3px; text-transform: uppercase; }
.tc-status.bonding { background: rgba(192,132,252,0.1); color: var(--accent); }
.tc-status.graduated { background: rgba(74,222,128,0.1); color: var(--green); }
.tc-desc { font-size: 11px; color: var(--muted); overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.tc-stats { display: flex; gap: 16px; }
.tc-stat { display: flex; flex-direction: column; gap: 1px; }
.tl { font-size: 9px; color: var(--muted); text-transform: uppercase; }
.tv { font-size: 12px; }
.accent { color: var(--accent); }
.tc-progress { display: flex; flex-direction: column; gap: 3px; }
.tc-bar { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.tc-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--green)); border-radius: 2px; }
.tc-pct { font-size: 9px; color: var(--muted); }
</style>
