import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    show_hide_password_button = (By.XPATH, './/div[contains(@class, "icon")]')
    password_field = (By.XPATH, './/div[./div[contains(@class, "icon")]]')

    @allure.step('Проверить активность поля ввода пароля по нажатию на кнопку показать/скрыть пароль')
    def check_active_password_field_on_button_click(self):
        self.wait_for_load_element(self.show_hide_password_button)
        self.wait_for_load_page()  # от души добавил, но всё равно через раз работает для firefox
        # можно ждать исчезновения элемента loader.svg
        try:
            self.click_on_element(self.show_hide_password_button)
            self.wait_for_load_element(self.password_field)
            self.wait_for_load_page()  # от души добавил, но всё равно через раз работает для firefox
            return "input_status_active" in self.get_attribute_value(self.password_field, "class")
        except WebDriverException:
            ValueError("Проблема с функционированием кнопки показать/скрыть пароль!")
