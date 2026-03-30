from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from src.config.settings import settings
from src.pages.home_page import HomePage
from src.pages.qa_careers_page import QACareersPage


def test_insider_home_page_blocks_loaded(page: Page) -> None:
    home_page = HomePage(page)
    home_page.open(settings.base_url)
    home_page.accept_cookies_if_present()
    home_page.verify_home_page_loaded()


def test_qa_jobs_are_filterable_and_redirect_to_lever(page: Page) -> None:
    qa_page = QACareersPage(page)
    qa_page.open(settings.careers_qa_url)
    qa_page.open_all_jobs()
    expect(page).to_have_url(re.compile(r".*(open-positions|careers/#open-roles|jobs\.lever\.co).*"))

    if qa_page.has_filter_controls():
        qa_page.filter_jobs(location="Istanbul, Turkiye", department="Quality Assurance")
        qa_page.verify_filtered_jobs(
            expected_title="Quality Assurance",
            expected_department="Quality Assurance",
            expected_location="Istanbul, Turkiye",
        )
        with page.expect_popup() as popup_info:
            qa_page.click_view_role()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        expect(popup).to_have_url(re.compile(r"https://jobs\.lever\.co/useinsider/.+"))
    else:
        qa_page.open_quality_assurance_team_jobs()
        qa_page.verify_lever_quality_assurance_jobs()
