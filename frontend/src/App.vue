<template>
  <div id="axopad">
    <nav class="navbar">
      <div class="brand">
        <span class="logo">🚀</span>
        <span class="brand-name">Axopad</span>
        <span class="brand-sub">Fair Launchpad · Solana</span>
      </div>
      <div class="nav-links">
        <router-link to="/">Discover</router-link>
        <router-link to="/launch" class="launch-btn">+ Launch</router-link>
      </div>
      <div class="status">
        <span class="dot" :class="online ? 'ok' : 'err'"></span>
        <span>{{ online ? "Live" : "Offline" }}</span>
      </div>
    </nav>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
const online = ref(false);
onMounted(async () => {
  try { await axios.get("/health"); online.value = true; } catch { online.value = false; }
});
</script>

<style>
:root {
  --bg: #0a0710;
  --surface: #14101c;
  --border: #241a30;
  --accent: #c084fc;
  --accent2: #f0abfc;
  --green: #4ade80;
  --red: #f87171;
  --text: #ede9fe;
  --muted: #6b5b7e;
  --font: "JetBrains Mono", "Cascadia Code", monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--font); font-size: 13px; line-height: 1.6; }
#axopad { min-height: 100vh; display: flex; flex-direction: column; }
.navbar { display: flex; align-items: center; gap: 24px; padding: 12px 24px; background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }
.brand { display: flex; align-items: center; gap: 8px; }
.logo { font-size: 16px; }
.brand-name { font-size: 16px; font-weight: 700; color: var(--accent); }
.brand-sub { font-size: 11px; color: var(--muted); border-left: 1px solid var(--border); padding-left: 10px; }
.nav-links { display: flex; gap: 16px; margin-left: auto; align-items: center; }
.nav-links a { color: var(--muted); text-decoration: none; font-size: 12px; transition: color 0.2s; }
.nav-links a:hover, .nav-links a.router-link-active { color: var(--accent); }
.launch-btn { background: var(--accent); color: #000 !important; padding: 6px 14px; border-radius: 6px; font-weight: 700; }
.status { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--muted); }
.dot { width: 7px; height: 7px; border-radius: 50%; }
.dot.ok { background: var(--green); }
.dot.err { background: var(--red); }
.main { flex: 1; padding: 24px; max-width: 1400px; width: 100%; margin: 0 auto; }
</style>
