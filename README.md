# Senior QA Engineer Assessment Project

Submission-ready Python QA automation project covering the requested UI automation, API testing, and load testing scope in a single repository.

## Overview

This repository consolidates the three requested assessment areas into one maintainable Python test project:

- UI automation for the Insider careers journey
- API automation for Swagger Petstore CRUD operations
- Load testing for n11 search behavior

The implementation is structured to stay close to production-style QA automation practices: page objects for UI flows, reusable API client abstractions, environment-driven configuration, and runnable VS Code tasks for repeatable execution.

## Assessment Coverage

- UI automation for the Insider/Insider One careers flow using Playwright and Page Object Model design
- CRUD API tests for Swagger Petstore using pytest and requests
- Headless n11 search load scenario using Locust
- Browser execution verified in Chrome and Firefox

## Verified Execution

- `pytest` passes locally for the full suite
- UI tests pass in Chrome and Firefox
- API tests pass against Swagger Petstore
- Locust scenario completes successfully against n11 with 1 user

## Project Design

- `src/pages`: Page Object Model implementation for the UI layer
- `src/api`: API client abstraction for Petstore endpoints
- `src/config`: Centralized runtime settings from environment variables
- `src/utils`: Reusable data builders and shared helpers
- `tests/ui`: UI scenarios for Insider
- `tests/api`: Positive and negative API scenarios for Petstore
- `load`: Locust scenario for n11 search behavior
- `.vscode/tasks.json`: Runnable workspace tasks for install, UI, API, full suite, and load execution

## Stack

- pytest for test execution
- Playwright for browser automation with Chrome and Firefox support
- requests for API testing
- Locust for load testing

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chrome firefox
copy .env.example .env
```

If `python` is shadowed by the Windows Store alias on your machine, use the installed interpreter directly to create the virtual environment first, then run the rest through `.venv\Scripts\python.exe`.

## Executed Scenarios

### UI

- Verify the Insider home page opens successfully and core content blocks are visible
- Navigate from the QA careers entry point to open roles
- Validate the Quality Assurance job flow against the live site behavior
- Confirm the role journey redirects to the Lever job listing flow

### API

- Create a pet
- Read the created pet
- Update the pet
- Delete the pet
- Validate negative retrieval scenarios

### Load

- Exercise n11 search with common keywords such as `iphone` and `samsung`
- Exercise a low-result search scenario
- Run headless with a single user as requested in the assessment

## Run UI Tests

Chrome:

```bash
pytest tests/ui --browser-name=chrome
```

Firefox:

```bash
pytest tests/ui --browser-name=firefox
```

## Run API Tests

```bash
pytest tests/api
```

## Run All Tests

```bash
pytest
```

## Run Load Test

```bash
locust -f load/locustfile.py --headless -u 1 -r 1 -t 1m
```

## Notes

- UI implementation follows a Page Object Model structure.
- Failed UI tests capture a screenshot into `test-results/screenshots`.
- Browser selection is parameterized with `--browser-name`.
- The n11 case requested one user, so the provided Locust command keeps a single virtual user.
- Insider currently redirects from `useinsider.com` to `insiderone.com`, so URL assertions allow either domain.
- The live careers experience has changed over time; the UI flow is implemented against the original assessment steps with selectors made as tolerant as possible.
- `VERIFY_SSL=false` is included for environments with corporate TLS interception; set it to `true` if your machine trusts the target certificates normally.
- The generated pytest HTML report is written to `report.html` in the repository root.

## Practical Assumptions

- The Insider careers experience has evolved since the original case definition, so the UI implementation preserves the intent of the scenario while adapting to the current live site.
- SSL verification is configurable because some enterprise environments intercept HTTPS traffic with local certificates.
- The repository favors reliability and clarity over excessive framework layering.

## Author

Meryem Naz Sural