import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # LLM
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.anthropic.com/v1")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "claude-sonnet-4-6")
    DEEPINFRA_API_KEY: str = os.getenv("DEEPINFRA_API_KEY", "")
    DEEPINFRA_BASE_URL: str = os.getenv("DEEPINFRA_BASE_URL", "https://api.deepinfra.com/v1/openai")
    DEEPINFRA_MODEL_NAME: str = os.getenv("DEEPINFRA_MODEL_NAME", "meta-llama/Meta-Llama-3.1-70B-Instruct")

    # Solana
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    SOLANA_WS_URL: str = os.getenv("SOLANA_WS_URL", "wss://api.mainnet-beta.solana.com")
    HELIUS_API_KEY: str = os.getenv("HELIUS_API_KEY", "")
    HELIUS_RPC_URL: str = os.getenv("HELIUS_RPC_URL", "")

    # Price data
    COINGECKO_API_KEY: str = os.getenv("COINGECKO_API_KEY", "")
    COINGECKO_BASE_URL: str = os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3")

    # Bonding curve
    CURVE_VIRTUAL_SOL: float = float(os.getenv("CURVE_VIRTUAL_SOL", "30.0"))
    CURVE_VIRTUAL_TOKENS: float = float(os.getenv("CURVE_VIRTUAL_TOKENS", "1073000000"))
    TOKEN_TOTAL_SUPPLY: float = float(os.getenv("TOKEN_TOTAL_SUPPLY", "1000000000"))
    GRADUATION_MARKET_CAP_SOL: float = float(os.getenv("GRADUATION_MARKET_CAP_SOL", "85.0"))
    TRADE_FEE_BPS: int = int(os.getenv("TRADE_FEE_BPS", "100"))

    # Launch
    LAUNCH_FEE_SOL: float = float(os.getenv("LAUNCH_FEE_SOL", "0.02"))
    MAX_NAME_LENGTH: int = int(os.getenv("MAX_NAME_LENGTH", "32"))
    MAX_TICKER_LENGTH: int = int(os.getenv("MAX_TICKER_LENGTH", "10"))

    # Flask
    DEBUG: bool = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    PORT: int = int(os.getenv("FLASK_PORT", "5001"))

    @classmethod
    def validate(cls) -> None:
        if not cls.LLM_API_KEY:
            raise ValueError("LLM_API_KEY is required. Copy .env.example to .env")
