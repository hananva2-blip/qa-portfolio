import allure


class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    @allure.step("Add '{name}' to cart")
    def add_to_cart(self, name):
        self.items.filter(has_text=name).get_by_role("button", name="Add to cart").click()
