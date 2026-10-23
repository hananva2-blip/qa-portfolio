import allure
import requests


class ApiClient:
    """Thin wrapper over requests: one base URL, a timeout, and an Allure step per call."""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        with allure.step(f"{method} {path}"):
            response = self.session.request(method, self.base_url + path, timeout=self.timeout, **kwargs)
            allure.attach(response.text, name=f"response {response.status_code}",
                          attachment_type=allure.attachment_type.JSON)
            return response

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()
