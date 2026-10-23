import allure


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator("[data-test='error']")

    @allure.step("Open login page")
    def open(self):
        self.page.goto(self.URL)

    @allure.step("Log in as {user}")
    def login(self, user, password):
        self.username.fill(user)
        self.password.fill(password)
        self.login_button.click()
