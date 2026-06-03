from dataclasses import dataclass
from typing import Optional
import httpx

from app.config import Config
from app.utils.logger import get_logger
from app.utils.retry import retry
from app.utils.rate_limiter import llm_limiter
from app.utils.helpers import trim_context

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are Axopad Analyst — a token analyst for a Solana fair-launch launchpad.

You provide concise, honest commentary on newly launched tokens trading on a bonding curve.
You assess: momentum, holder distribution, volume quality, and risk signals.

You are NOT a shill. You call out obvious risks (low holders, single-buyer volume, suspicious
patterns). You do NOT give financial advice. This is a research tool for degens who want
a clear read before aping.

Respond in this exact format:
MOMENTUM: [cold/warming/hot/euphoric]
RISK: [low/medium/high]
SIGNAL: [2-3 sentences citing specific data — market cap, volume, trades, holders]
VERDICT: [one punchy sentence]
GRADUATION_ODDS: [0.0-1.0]"""


@dataclass
class TokenAnalysis:
    momentum: str
    risk: str
    signal: str
    verdict: str
    graduation_odds: float
    raw: str

    def to_dict(self) -> dict:
        return {
            "momentum": self.momentum,
            "risk": self.risk,
            "signal": self.signal,
            "verdict": self.verdict,
            "graduation_odds": self.graduation_odds,
        }


class LLMAnalyst:
    def __init__(self, config: type = Config):
        self._api_key = config.LLM_API_KEY
        self._base_url = config.LLM_BASE_URL.rstrip("/")
        self._model = config.LLM_MODEL_NAME
        self._http = httpx.Client(timeout=30.0)

    def close(self) -> None:
        self._http.close()

    @retry(max_attempts=3, delay=2.0)
    def analyze(self, token_summary: str) -> TokenAnalysis:
        llm_limiter.acquire()
        user_msg = f"Analyze this token on the Axopad bonding curve:\n\n{trim_context(token_summary)}"

        is_anthropic = "anthropic" in self._base_url
        if is_anthropic:
            payload = {"model": self._model, "max_tokens": 400, "system": SYSTEM_PROMPT,
                       "messages": [{"role": "user", "content": user_msg}]}
            headers = {"x-api-key": self._api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
            resp = self._http.post(f"{self._base_url}/messages", headers=headers, json=payload)
        else:
            payload = {"model": self._model, "max_tokens": 400,
                       "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_msg}]}
            headers = {"Authorization": f"Bearer {self._api_key}", "content-type": "application/json"}
            resp = self._http.post(f"{self._base_url}/chat/completions", headers=headers, json=payload)

        resp.raise_for_status()
        data = resp.json()
        raw = data["content"][0]["text"] if is_anthropic else data["choices"][0]["message"]["content"]
        return self._parse(raw)

    def _parse(self, raw: str) -> TokenAnalysis:
        momentum, risk, signal, verdict, odds = "", "", "", "", 0.5
        for line in raw.strip().split("\n"):
            line = line.strip()
            if line.startswith("MOMENTUM:"): momentum = line.split(":", 1)[1].strip()
            elif line.startswith("RISK:"): risk = line.split(":", 1)[1].strip()
            elif line.startswith("SIGNAL:"): signal = line.split(":", 1)[1].strip()
            elif line.startswith("VERDICT:"): verdict = line.split(":", 1)[1].strip()
            elif line.startswith("GRADUATION_ODDS:"):
                try: odds = float(line.split(":", 1)[1].strip())
                except: pass
        return TokenAnalysis(momentum=momentum, risk=risk, signal=signal,
                             verdict=verdict, graduation_odds=odds, raw=raw)
