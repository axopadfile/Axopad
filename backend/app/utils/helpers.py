import re
import uuid
from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)

def utcnow_iso() -> str:
    return utcnow().isoformat()

def new_id() -> str:
    return str(uuid.uuid4())

def short_id(full_id: str) -> str:
    return full_id[:8] if len(full_id) >= 8 else full_id

def fake_mint_address() -> str:
    """Generate a plausible-looking Solana mint address (stub)."""
    import secrets
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return "".join(secrets.choice(alphabet) for _ in range(44))

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))

def safe_div(num: float, den: float, default: float = 0.0) -> float:
    return default if den == 0 else num / den

def pct_change(old: float, new: float) -> float:
    return 0.0 if old == 0 else (new - old) / abs(old) * 100.0

def format_sol(value: float, decimals: int = 4) -> str:
    return f"◎{value:.{decimals}f}"

def trim_context(text: str, max_tokens: int = 4000) -> str:
    max_chars = max_tokens * 4
    return text if len(text) <= max_chars else text[:max_chars] + "\n...[truncated]"

def validate_ticker(ticker: str, max_len: int = 10) -> bool:
    return bool(re.fullmatch(rf"[A-Z0-9]{{1,{max_len}}}", ticker.upper()))
