from __future__ import annotations

import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.api.petstore_client import PetstoreClient
from src.config.settings import settings


def _resolve_browser_executable(browser_name: str) -> str | None:
    candidates = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ],
        "firefox": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            os.path.expandvars(r"%LocalAppData%\Mozilla Firefox\firefox.exe"),
            os.path.expandvars(r"%LocalAppData%\Programs\Mozilla Firefox\firefox.exe"),
        ],
    }
    for candidate in candidates[browser_name]:
        if os.path.exists(candidate):
            return candidate
    return None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser-name",
        action="store",
        default=settings.default_browser,
        choices=["chrome", "firefox"],
        help="Browser to run UI tests with.",
    )


def pytest_configure() -> None:
    Path("test-results").mkdir(parents=True, exist_ok=True)
    Path(settings.screenshot_dir).mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def selected_browser_name(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("browser_name"))


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, selected_browser_name: str) -> Browser:
    if selected_browser_name == "chrome":
        chrome_path = _resolve_browser_executable("chrome")
        try:
            if chrome_path:
                browser = playwright_instance.chromium.launch(
                    executable_path=chrome_path, headless=settings.headless
                )
            else:
                browser = playwright_instance.chromium.launch(
                    channel="chrome", headless=settings.headless
                )
        except Exception:
            browser = playwright_instance.chromium.launch(headless=settings.headless)
    else:
        try:
            browser = playwright_instance.firefox.launch(headless=settings.headless)
        except Exception:
            firefox_path = _resolve_browser_executable("firefox")
            browser = playwright_instance.firefox.launch(
                executable_path=firefox_path, headless=settings.headless
            )
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=not settings.verify_ssl,
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page


@pytest.fixture(scope="session")
def petstore_client() -> PetstoreClient:
    return PetstoreClient(settings.petstore_base_url)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    page = item.funcargs.get("page")
    if not page:
        return
    screenshot_dir = Path(settings.screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{item.name}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
