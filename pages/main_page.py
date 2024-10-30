import allure
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import test_data
from pages.base_page import BasePage


class MainPage(BasePage):
    personal_account_button = (By.XPATH, './/a[@href="/account"]')
    constructor_button = (By.XPATH, './/a[@href="/"]')
    feed_order_button = (By.XPATH, './/a[@href="/feed"]')
    ingredient = (By.XPATH, './/a[@href="/ingredient/61c0c5a71d1f82001bdaaa6d"]')
    ingredient_details_window = (By.XPATH, './/div[contains(@class, "Modal_modal__container")]')
    close_ingredient_details_button = (By.XPATH, './/button[contains(@class, "Modal_modal__close")]')
    ingredient_counter = (By.XPATH, './/p[contains(@class, "counter_counter")]')
    basket = (By.XPATH, './/section[contains(@class, "BurgerConstructor_basket")]')
    create_order_button = (By.XPATH, './/button[contains(@class, "button_button")]')
    order_window = (By.XPATH, './/div[contains(@class, "Modal_modal__contentBox")]')
    close_order_button = (By.XPATH, './/button[contains(@class, "Modal_modal")]')
    orders_number_element = (By.XPATH, './/h2[contains(@class, "Modal_modal")]')
    loading_order_animation = (By.XPATH, './/img[@alt="loading animation"]')

    @allure.step('Кликнуть по кнопке "Личный Кабинет"')
    def click_on_personal_account_button(self):
        self.wait_for_load_element(self.personal_account_button)
        try:
            self.click_on_element(self.personal_account_button)
            self.wait_url_to_be(test_data.ACCOUNT_PAGE_URL)
        except WebDriverException:
            ValueError("Проблемы с кнопкой 'Личный кабинет'")

    @allure.step('Нажать на кнопку "Конструктор"')
    def click_on_constructor_button(self):
        self.wait_for_load_element(self.constructor_button)
        # self.click_on_element(self.constructor_button)
        self.click_on_elements(self.constructor_button, 1)

    @allure.step('Проверить переход по клику на "Конструктор"')
    def check_transfer_to_constructor_button(self):
        self.click_on_constructor_button()
        self.wait_url_to_be(test_data.CONSTRUCTOR_PAGE_URL)
        return self.get_current_url() == test_data.CONSTRUCTOR_PAGE_URL

    @allure.step('Нажать на кнопку "Лента Заказов"')
    def click_on_feed_order_button(self):
        self.wait_for_load_element(self.feed_order_button)
        self.click_on_element(self.feed_order_button)

    @allure.step('Проверить переход по клику на "Ленту Заказов"')
    def check_transfer_to_feed_order(self):
        self.click_on_feed_order_button()
        self.wait_url_to_be(test_data.FEED_PAGE_URL)
        return self.get_current_url() == test_data.FEED_PAGE_URL

    @allure.step('Нажать на ингредиент')
    def click_on_ingredient(self):
        self.wait_for_load_element(self.ingredient)
        self.click_on_element(self.ingredient)

    @allure.step('Проверить появление всплывающего окна с деталями ингредиента')
    def check_appearance_ingredient_detail_window(self):
        self.click_on_ingredient()
        self.wait_for_load_element(self.ingredient_details_window)
        return self.is_element_displayed(self.ingredient_details_window)

    @allure.step('Нажать на кнопку закрытия окна с деталями ингредиента')
    def click_on_close_ingredient_details_button(self):
        self.wait_for_load_element(self.close_ingredient_details_button)
        self.click_on_elements(self.close_ingredient_details_button, 1)

    @allure.step('Проверить закрытие окна с деталями ингредиента')
    def check_disappearance_ingredient_detail_window(self):
        self.click_on_close_ingredient_details_button()
        self.wait_for_load_element(self.ingredient_details_window)
        self.wait_for_invisible_element(self.ingredient_details_window)
        return not self.is_element_displayed(self.ingredient_details_window)

    @allure.step('Добавить ингредиент в корзину')
    def add_ingredient_to_basket(self):
        self.wait_for_load_element(self.ingredient)
        self.wait_for_load_element(self.basket)
        self.drag_and_drop_element(self.ingredient, self.basket, 1)
        self.wait_for_load_element(self.ingredient)

    @allure.step('Проверить увеличивается ли счётчик ингредиента при добавлении в корзину')
    def check_is_increase_ingredient_counter(self):
        self.wait_for_load_element(self.ingredient_counter)
        old_value = self.get_element_text(self.ingredient_counter)
        self.add_ingredient_to_basket()
        self.wait_for_load_element(self.ingredient_counter)
        new_value = self.get_element_text(self.ingredient_counter)
        return int(new_value) - int(old_value) > 0

    @allure.step('Нажать на кнопку "Оформить заказ"')
    def click_on_create_order_button(self):
        self.wait_for_load_element(self.create_order_button)
        self.click_on_element(self.create_order_button)

    @allure.step('Проверить создание заказа')
    def check_create_order(self):
        self.create_order()
        return self.is_element_displayed(self.order_window)

    @allure.step('Cоздать заказ')
    def create_order(self):
        self.click_on_create_order_button()
        self.wait_for_invisible_element(self.loading_order_animation)

    @allure.step('Создать заказ и вернуть его номер')
    def create_order_and_return_order_number(self):
        self.create_order()
        order_number = self.get_element_text(self.orders_number_element)
        self.click_on_element(self.close_order_button)
        return order_number
