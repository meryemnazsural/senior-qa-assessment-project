from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://useinsider.com/")
    careers_qa_url: str = os.getenv(
        "CAREERS_QA_URL", "https://useinsider.com/careers/quality-assurance/"
    )
    petstore_base_url: str = os.getenv(
        "PETSTORE_BASE_URL", "https://petstore.swagger.io/v2"
    )
    n11_base_url: str = os.getenv("N11_BASE_URL", "https://www.n11.com")
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    default_browser: str = os.getenv("DEFAULT_BROWSER", "chrome")
    screenshot_dir: str = os.getenv("SCREENSHOT_DIR", "test-results/screenshots")
    verify_ssl: bool = os.getenv("VERIFY_SSL", "false").lower() == "true"


settings = Settings()
