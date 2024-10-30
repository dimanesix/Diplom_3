import allure
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import test_data
from pages.base_page import BasePage


class AccountPage(BasePage):
    order_history_button = (By.XPATH, './/a[@href="/account/order-history"]')
    exit_button = (By.XPATH, './/button[text()="Выход"]')
    personal_account_button = (By.XPATH, './/a[@href="/account"]')
    orders_history_list = (By.XPATH, './/p[@class="text text_type_digits-default"]')

    @allure.step('Кликнуть на кнопку "История заказов"')
    def click_on_button_order_history(self):
        self.wait_for_load_element(self.order_history_button)
        # также можно подождать исчезновение (wait_for_invisible..) элемента loader.svg
        try:
            self.click_on_element(self.order_history_button)
        except WebDriverException:
            ValueError("Проблемы с кнопкой 'История заказов'!")

    @allure.step('Кликнуть на кнопку "Личный Кабинет"')
    def click_on_personal_account_button(self):
        self.wait_for_load_element(self.personal_account_button)
        self.click_on_element(self.personal_account_button)

    @allure.step('Проверить переход в раздел с историей заказов')
    def check_transfer_to_order_history(self):
        self.click_on_button_order_history()
        self.wait_url_to_be(test_data.ORDER_HISTORY_PAGE)
        return self.get_current_url() == test_data.ORDER_HISTORY_PAGE

    @allure.step('Кликнуть на кнопку "Выход"')
    def click_on_exit_button(self):
        self.wait_for_load_element(self.exit_button)
        self.click_on_element(self.exit_button)

    @allure.step('Проверить выход из аккаунта')
    def check_logout(self):
        self.click_on_exit_button()
        self.wait_url_to_be(test_data.LOGIN_PAGE_URL)
        # костыль для firefox надо дождаться загрузки всей страницы
        # да и то не всегда работает...
        self.wait_for_load_page()
        # можно подождать исчезновения элемента loader.svg
        try:
            self.click_on_personal_account_button()
        except WebDriverException:
            ValueError("Проблемы с кнопкой 'Личный кабинет'!")
        self.wait_url_to_be(test_data.LOGIN_PAGE_URL)
        return self.get_current_url() == test_data.LOGIN_PAGE_URL

    @allure.step('Получить все заказы пользователя из "Истории заказов"')
    def return_orders_from_history(self):
        self.wait_for_load_elements(self.orders_history_list)
        order_elements = self.find_elements(self.orders_history_list)
        orders = []
        for element in order_elements:
            orders.append(element.text.split('#0')[1])  # .slit('#')
        return orders
