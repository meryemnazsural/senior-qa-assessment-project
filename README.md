# Senior QA Engineer Assessment Project

Single Python project covering the requested UI automation, API testing, and load testing scope.

## Stack

- pytest for test execution
- Playwright for browser automation with Chrome and Firefox support
- requests for API testing
- Locust for load testing

## Project Structure

- `src/pages`: page objects for UI automation
- `src/api`: API client wrappers
- `src/config`: runtime configuration
- `src/utils`: test data builders
- `tests/ui`: Insider UI test cases
- `tests/api`: Swagger Petstore CRUD test cases
- `load`: Locust scenario for n11 search
- `docs`: supporting test scenario notes

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chrome firefox
copy .env.example .env
```

If `python` is shadowed by the Windows Store alias on your machine, use the installed interpreter directly to create the virtual environment first, then run the rest through `.venv\Scripts\python.exe`.

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