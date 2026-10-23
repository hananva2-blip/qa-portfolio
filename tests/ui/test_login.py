import allure
import pytest
from playwright.sync_api import expect

from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.feature("UI")]

# Public demo accounts published on saucedemo.com
PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page):
    login = LoginPage(page)
    login.open()
    return login


def test_valid_login_opens_inventory(login_page, page):
    login_page.login("standard_user", PASSWORD)

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize("user, password, error", [
    ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
    ("standard_user", "wrong", "Username and password do not match"),
    ("", PASSWORD, "Username is required"),
    ("standard_user", "", "Password is required"),
])
def test_invalid_login_shows_error(login_page, user, password, error):
    login_page.login(user, password)

    expect(login_page.error).to_contain_text(error)


def test_add_item_updates_cart_badge(login_page, page):
    login_page.login("standard_user", PASSWORD)
    inventory = InventoryPage(page)

    inventory.add_to_cart("Sauce Labs Backpack")

    expect(inventory.cart_badge).to_have_text("1")
