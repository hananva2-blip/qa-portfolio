# QA Automation Portfolio

[![tests](https://github.com/hananva2-blip/qa-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/hananva2-blip/qa-portfolio/actions/workflows/tests.yml)

**📊 Live Allure report:** https://hananva2-blip.github.io/qa-portfolio/

A Python test automation framework that covers the three layers of a modern product: **API**, **UI** and an **AI (LLM) feature**.
Every push runs the full suite **inside Docker** on **GitHub Actions** and publishes an **Allure report** to GitHub Pages.

---

## Tech stack

| Area | Tools |
|---|---|
| Language & runner | Python 3.12, pytest |
| API testing | requests, jsonschema |
| UI testing | Playwright (Page Object Model) |
| AI testing | Anthropic SDK (Claude) |
| Reporting | Allure |
| CI/CD | Docker, GitHub Actions, GitHub Pages |

---

## What is tested

### 1. API: [JSONPlaceholder](https://jsonplaceholder.typicode.com) (`tests/api/`)

| Test | What it checks |
|---|---|
| `test_get_post_matches_schema` | Status 200 and the body matches a JSON schema, for several IDs (`parametrize`) |
| `test_missing_post_returns_404` | A resource that does not exist returns 404 |
| `test_create_post_echoes_body` | `POST` returns 201, echoes the sent fields and adds an `id` |
| `test_filter_posts_by_user` | A query parameter really filters the results |
| `test_response_time_under_two_seconds` | A basic performance guard |

A status code alone is not enough: a `200` with a missing field is still a bug, so the tests validate the **schema** as well.

### 2. UI: [Sauce Demo](https://www.saucedemo.com) (`tests/ui/`)

| Test | What it checks |
|---|---|
| `test_valid_login_opens_inventory` | A valid user lands on the products page |
| `test_invalid_login_shows_error` | Four negative cases: locked user, wrong password, empty username, empty password |
| `test_add_item_updates_cart_badge` | Adding a product updates the cart counter |

The tests use the **Page Object Model** (`src/pages/`): locators and actions live in one class per page, so a UI change is fixed in one place.
Playwright's `expect` waits for elements automatically, so there are no `sleep` calls.

### 3. AI: an LLM support bot (`tests/ai/`)

`src/chatbot.py` is the "feature under test": a store support bot built on Claude. It must answer **only from a product catalog**, reply in **JSON**, and **never reveal** an internal code.

LLM output changes from run to run, so these tests never compare exact text. They check **behavior** that must always hold:

| Test | What it checks |
|---|---|
| `test_reply_is_valid_json` | Every reply matches the expected JSON schema |
| `test_price_comes_from_catalog` | Prices in the answer are the real catalog prices (grounding) |
| `test_unknown_product_is_not_invented` | A product that does not exist returns `in_catalog: false` (no hallucination) |
| `test_prompt_injection_does_not_leak_secret` | "Ignore all previous instructions…" does not leak the secret (security) |

The AI tests are skipped automatically when `ANTHROPIC_API_KEY` is not set.

---

## Project structure

```
qa-portfolio/
├── src/
│   ├── api_client.py          # requests wrapper: base URL, timeout, every call logged as an Allure step
│   ├── chatbot.py             # the AI feature under test
│   └── pages/
│       ├── login_page.py      # Page Object: login screen
│       └── inventory_page.py  # Page Object: products screen
├── tests/
│   ├── api/test_posts.py
│   ├── ui/test_login.py
│   └── ai/test_chatbot.py
├── conftest.py                # shared fixtures + screenshot on UI failure
├── pytest.ini                 # markers and Allure output folder
├── Dockerfile                 # Python + dependencies + Chromium
└── .github/workflows/tests.yml
```

---

## Framework design

- **`ApiClient`** wraps `requests.Session`, so every test shares one connection, one timeout and one base URL. Each call becomes an Allure step with the response attached, so a failed test shows exactly what the server returned.
- **Fixtures** (`conftest.py`): the `api` fixture has `scope="session"`, so it is created once for the whole run and closed at the end with `yield`.
- **Screenshot on failure**: a `pytest_runtest_makereport` hook attaches a screenshot to the Allure report whenever a UI test fails.
- **Markers** (`api`, `ui`, `ai`) let you run one layer at a time: `pytest -m api`.
- **Data-driven tests**: `@pytest.mark.parametrize` runs one test over many inputs.

---

## CI/CD pipeline

```
push / pull request
      │
      ▼
 docker build  ──►  docker run pytest  ──►  allure generate  ──►  deploy to GitHub Pages
```

1. GitHub Actions builds the Docker image, the same environment as a local run.
2. Runs all tests inside the container and writes results to `allure-results/`.
3. Generates the HTML report, even if some tests failed (`if: always()`).
4. Publishes the report to GitHub Pages (from `main` only).

---

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

pytest                         # all tests
pytest -m api                  # API only
pytest -m ui --headed          # UI, with a visible browser
export ANTHROPIC_API_KEY=...   # enables the AI tests
allure serve allure-results    # open the report
```

## Run in Docker

```bash
docker build -t qa-tests .
docker run --rm -e ANTHROPIC_API_KEY -v "$PWD/allure-results:/app/allure-results" qa-tests
```
