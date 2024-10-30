import allure
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import test_data
from pages.base_page import BasePage


class LoginPage(BasePage):
    recover_password_button = (By.XPATH, './/a[text()="Восстановить пароль"]')
    auth_form = (By.XPATH, './/form[contains(@class, "Auth")]')
    email_field = (By.XPATH, './/input[@type="text"]')
    password_field = (By.XPATH, './/input[@type="password"]')
    enter_button = (By.XPATH, './/button[text()="Войти"]')

    @allure.step('Кликнуть по кнопке "Восстановить пароль"')
    def click_on_recover_password_button(self):
        self.wait_for_load_element(self.recover_password_button)
        self.click_on_element(self.recover_password_button)

    @allure.step('Проверить переход на страницу восстановления пароля по кнопке "Восстановить пароль"')
    def check_url_from_button(self):
        self.click_on_recover_password_button()
        return self.get_current_url() == test_data.FORGOT_PASSWORD_URL

    @allure.step('Залогиниться зарегестрированным пользователем')
    def login_register_user(self, email: str, password: str):
        self.open_page(test_data.LOGIN_PAGE_URL)
        self.wait_for_load_element(self.auth_form)
        self.set_data_to_element(self.email_field, email)
        self.set_data_to_element(self.password_field, password)
        try:
            self.click_on_element(self.enter_button)
            self.wait_url_to_be(test_data.MAIN_PAGE_URL)
        except WebDriverException:
            ValueError("Проблема с функционированием кнопки Войти!")


