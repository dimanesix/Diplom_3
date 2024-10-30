import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import test_data
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    recover_password_button = (By.XPATH, './/button[text()="Восстановить"]')
    email_field = (By.XPATH, './/input[contains(@class, "text")]')

    @allure.step('Ввести произвольный email в поле ввода почтового адреса')
    def send_data_to_email_field(self, email):
        self.wait_for_load_element(self.email_field)
        self.set_data_to_element(self.email_field, email)

    @allure.step('Проверить кликабельность кнопки "Восстановить"')
    def check_clickable_recover_button(self):
        self.wait_for_load_element(self.recover_password_button)
        try:
            self.click_on_element(self.recover_password_button)
            return True
        except WebDriverException:
            return False

    @allure.step('Нажать на кнопку "Восстановить и дождаться перехода на страницу с формой сброса пароля"')
    def click_on_recover_button(self):
        self.wait_for_load_element(self.recover_password_button)
        try:
            self.click_on_element(self.recover_password_button)
            self.wait_url_to_be(test_data.RESET_PASSWORD_URL)
        except WebDriverException:
            ValueError("Проблема с функционированием кнопки 'Восстановить'")

    @allure.step('Проверить видимость текста в поле ввода электронной почты')
    def check_text_is_display_in_email_field(self):
        return self.is_element_displayed(self.email_field)

    @allure.step('Проверить, что текст отображается так как его вводит пользователь')
    def check_input_email_text_is_correct(self, email):
        return self.get_attribute_value(self.email_field, "value") == email
