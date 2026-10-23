import allure
import pytest

from src.api_client import ApiClient

API_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api():
    client = ApiClient(API_URL)
    yield client
    client.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page")
    if report.when == "call" and report.failed and page:
        allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
