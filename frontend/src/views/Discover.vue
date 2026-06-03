<template>
  <div class="discover">
    <div class="hero">
      <h1>The fair launchpad for Solana.</h1>
      <p>Every token starts on the curve. No presale. No insiders.</p>
    </div>

    <div class="tabs">
      <button v-for="t in tabs" :key="t.key" :class="{ active: tab === t.key }" @click="tab = t.key; load()">
        {{ t.label }}
      </button>
    </div>

    <div v-if="loading" class="empty">Loading...</div>
    <div v-else-if="tokens.length === 0" class="empty">
      No tokens here yet. <router-link to="/launch" class="link">Launch the first one →</router-link>
    </div>
    <div class="token-grid">
      <TokenCard v-for="t in tokens" :key="t.id" :token="t" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { feedTrending, feedNew, feedGraduating, feedGraduated } from "@/api/index.js";
import TokenCard from "@/components/TokenCard.vue";

const tab = ref("trending"), loading = ref(false), tokens = ref([]);
const tabs = [
  { key: "trending", label: "🔥 Trending" },
  { key: "new", label: "✨ New" },
  { key: "graduating", label: "🎓 Graduating" },
  { key: "graduated", label: "✅ Graduated" },
];

const loaders = { trending: feedTrending, new: feedNew, graduating: feedGraduating, graduated: feedGraduated };

async function load() {
  loading.value = true;
  try { tokens.value = (await loaders[tab.value]()).data.tokens; }
  catch {} finally { loading.value = false; }
}
onMounted(load);
</script>

<style scoped>
.discover { display: flex; flex-direction: column; gap: 20px; }
.hero { text-align: center; padding: 30px 0 10px; }
.hero h1 { font-size: 28px; color: var(--accent); margin-bottom: 8px; }
.hero p { font-size: 13px; color: var(--muted); }
.tabs { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.tabs button { background: var(--surface); border: 1px solid var(--border); color: var(--muted); padding: 7px 16px; border-radius: 6px; cursor: pointer; font-family: var(--font); font-size: 12px; }
.tabs button.active { border-color: var(--accent); color: var(--accent); }
.empty { color: var(--muted); text-align: center; padding: 60px 0; }
.link { color: var(--accent); }
.token-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
</style>
