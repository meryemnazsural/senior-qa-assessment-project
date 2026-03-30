from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from src.pages.base_page import BasePage


class QACareersPage(BasePage):
    see_all_jobs_button = "a[href*='open-positions'], a:has-text('See all QA jobs'), a:has-text('Explore open roles')"
    location_filter = "#filter-by-location"
    department_filter = "#filter-by-department"
    job_cards = "div.position-list-item-wrapper"
    lever_job_cards = ".posting"
    qa_team_jobs_url = "https://jobs.lever.co/insiderone?team=Quality%20Assurance"
    lever_apply_url_fragment = "jobs.lever.co/useinsider"

    def open(self, url: str) -> None:
        self.goto(url)

    def open_all_jobs(self) -> None:
        expect(self.page.locator(self.see_all_jobs_button).first).to_be_visible()
        self.page.locator(self.see_all_jobs_button).first.click()

    def has_filter_controls(self) -> bool:
        return self.page.locator(self.location_filter).count() > 0 and self.page.locator(
            self.department_filter
        ).count() > 0

    def filter_jobs(self, location: str, department: str) -> None:
        self.page.locator(self.location_filter).select_option(label=location)
        self.page.locator(self.department_filter).select_option(label=department)
        self.page.wait_for_load_state("networkidle")

    def listed_jobs(self) -> Locator:
        return self.page.locator(self.job_cards)

    def open_quality_assurance_team_jobs(self) -> None:
        qa_heading = self.page.get_by_role("heading", name="Quality Assurance")
        if qa_heading.count():
            qa_jobs_link = qa_heading.locator(
                "xpath=ancestor::div[contains(@class, 'insiderone-icon-cards-grid-item')][1]//a[contains(@href, 'jobs.lever.co/insiderone?team=Quality%20Assurance')]"
            )
            if qa_jobs_link.count():
                qa_jobs_link.click()
                return
        self.goto(self.qa_team_jobs_url)

    def verify_filtered_jobs(self, expected_title: str, expected_department: str, expected_location: str) -> None:
        cards = self.listed_jobs()
        expect(cards.first).to_be_visible()
        count = cards.count()
        for index in range(count):
            card = cards.nth(index)
            expect(card).to_contain_text(expected_title)
            expect(card).to_contain_text(expected_department)
            expect(card).to_contain_text(expected_location)

    def click_view_role(self) -> None:
        self.listed_jobs().first.hover()
        self.listed_jobs().first.get_by_role("link", name="View Role").click()

    def verify_redirected_to_lever(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page).to_have_url(re.compile(r"https://jobs\.lever\.co/useinsider/.+"))

    def verify_lever_quality_assurance_jobs(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r"https://jobs\.lever\.co/(useinsider|insiderone).*(Quality%20Assurance|team=Quality)")
        )
        cards = self.page.locator(self.lever_job_cards)
        expect(cards.first).to_be_visible()
        count = cards.count()
        for index in range(count):
            job_text = cards.nth(index).inner_text().upper()
            assert "QA" in job_text or "QUALITY ASSURANCE" in job_text
