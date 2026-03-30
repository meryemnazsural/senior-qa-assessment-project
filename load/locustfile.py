from __future__ import annotations

import urllib3

from locust import HttpUser, between, task

from src.config.settings import settings


class N11SearchUser(HttpUser):
    host = settings.n11_base_url
    wait_time = between(1, 2)

    def on_start(self) -> None:
        self.client.verify = settings.verify_ssl
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
                "Referer": settings.n11_base_url,
            }
        )
        if not settings.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @task(3)
    def search_iphone(self) -> None:
        self.client.get("/arama", params={"q": "iphone"}, name="Search: iphone")

    @task(2)
    def search_samsung(self) -> None:
        self.client.get("/arama", params={"q": "samsung"}, name="Search: samsung")

    @task(1)
    def search_negative_phrase(self) -> None:
        self.client.get("/arama", params={"q": "zzzz-not-found-term"}, name="Search: no result")
