<template>
  <div class="launch">
    <h1>Launch a Token</h1>
    <p class="sub">Deploy in seconds. Starts on the bonding curve. Fair for everyone.</p>

    <div class="form">
      <label>Name *</label>
      <input v-model="form.name" class="inp" maxlength="32" placeholder="Axolotl Coin" />

      <label>Ticker *</label>
      <input v-model="form.ticker" class="inp" maxlength="10" placeholder="AXO" style="text-transform: uppercase" />

      <label>Description</label>
      <textarea v-model="form.description" class="inp" rows="3" placeholder="What's the story?"></textarea>

      <label>Image URL</label>
      <input v-model="form.image_url" class="inp" placeholder="https://..." />

      <div class="socials">
        <input v-model="form.twitter" class="inp" placeholder="Twitter" />
        <input v-model="form.telegram" class="inp" placeholder="Telegram" />
        <input v-model="form.website" class="inp" placeholder="Website" />
      </div>

      <label>Creator wallet *</label>
      <input v-model="form.creator" class="inp" placeholder="Your Solana address" />

      <button class="btn-launch" @click="launch" :disabled="launching">
        {{ launching ? "Launching..." : "🚀 Launch Token" }}
      </button>
      <span v-if="err" class="err">{{ err }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { launchToken } from "@/api/index.js";

const router = useRouter();
const launching = ref(false), err = ref(null);
const form = ref({ name: "", ticker: "", description: "", image_url: "", twitter: "", telegram: "", website: "", creator: "" });

async function launch() {
  if (!form.value.name || !form.value.ticker || !form.value.creator) {
    err.value = "Name, ticker, and creator wallet are required."; return;
  }
  launching.value = true; err.value = null;
  try {
    const res = await launchToken({ ...form.value, ticker: form.value.ticker.toUpperCase() });
    router.push(`/token/${res.data.id}`);
  } catch (e) { err.value = e.response?.data?.error || e.message; }
  finally { launching.value = false; }
}
</script>

<style scoped>
.launch { max-width: 560px; margin: 0 auto; display: flex; flex-direction: column; gap: 8px; }
h1 { font-size: 22px; color: var(--accent); }
.sub { font-size: 12px; color: var(--muted); margin-bottom: 12px; }
.form { display: flex; flex-direction: column; gap: 6px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
label { font-size: 11px; color: var(--muted); text-transform: uppercase; margin-top: 8px; }
.inp { background: var(--bg); border: 1px solid var(--border); color: var(--text); font-family: var(--font); font-size: 12px; padding: 8px 12px; border-radius: 6px; width: 100%; }
.socials { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }
.btn-launch { margin-top: 16px; background: var(--accent); border: none; color: #000; font-weight: 700; padding: 10px; border-radius: 6px; cursor: pointer; font-family: var(--font); font-size: 13px; }
.btn-launch:disabled { opacity: 0.4; cursor: not-allowed; }
.err { color: var(--red); font-size: 11px; margin-top: 6px; }
</style>
