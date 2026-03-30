from __future__ import annotations

import re

from playwright.sync_api import expect

from src.pages.base_page import BasePage


class HomePage(BasePage):
    block_texts = [
        "Trusted by 2,000+ customers",
        "Why more teams choose Insider One",
        "What brands achieve with Insider One",
    ]

    def open(self, url: str) -> None:
        self.goto(url)

    def accept_cookies_if_present(self) -> None:
        cookie_button = self.page.get_by_role("button", name="Accept")
        if cookie_button.count():
            cookie_button.click()

    def verify_home_page_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"https://(www\.)?(useinsider|insiderone)\.com/?"))
        for block_text in self.block_texts:
            expect(self.page.get_by_text(block_text, exact=False).first).to_be_visible()
