import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeedOrderPage(BasePage):
    orders_feed = (By.XPATH, './/ul[contains(@class, "OrderFeed_list")]/li/a')
    order_details_window = (By.XPATH, './/div[contains(@class, "Modal_orderBox")]')
    orders_feed_list = (By.XPATH, './/p[@class="text text_type_digits-default"]')
    order_feed_counters = (By.XPATH, './/p[contains(@class, "OrderFeed_number")]')
    orders_in_work_section = (By.XPATH, './/ul[contains(@class, "OrderFeed_orderListReady")]/li')
    orders_ready_message = (By.XPATH, './/li[contains(@class, "text text_type_main-small")]')

    @allure.step('Нажать на заказ')
    def click_on_order(self):
        self.wait_for_load_element(self.orders_feed)
        self.click_on_elements(self.orders_feed, 1)

    @allure.step('Проверить появление окна с деталями заказа')
    def check_appearance_order_detail_window(self):
        self.click_on_order()
        self.wait_for_load_element(self.order_details_window)
        return self.is_element_displayed(self.order_details_window)

    @allure.step('Получить последние 50 заказов Ленты')
    def return_orders_from_feed(self):
        self.wait_for_load_elements(self.orders_feed_list)
        order_elements = self.find_elements(self.orders_feed_list)
        orders = []
        for element in order_elements:
            orders.append(element.text.split("#0")[1])
        return orders

    @allure.step('Проверить видимость всех заказов в Ленте')
    def check_orders_display_in_feed(self):
        orders = self.find_elements(self.orders_feed)
        for order in orders:
            if order.is_displayed() is True:
                continue
            else:
                return False
        return True

    @allure.step('Получить значения счётчиков')
    def get_the_counters_value(self):
        counters_value = []
        self.wait_for_load_elements(self.order_feed_counters)
        counters = self.find_elements(self.order_feed_counters)
        for counter in counters:
            counters_value.append(counter.text)
        return counters_value

    @allure.step('Проверить увеличение счётчиков')
    def check_increase_counters_after_order(self, counters_before: list, counters_after: list):
        return ((int(counters_after[0]) - int(counters_before[0]) >= 1) and
                (int(counters_after[1]) - int(counters_before[1]) >= 1))

    @allure.step('Получить заказы, находящиеся в работе')
    def get_orders_in_work_section(self):
        orders_in_work = []
        self.wait_for_load_elements(self.orders_in_work_section)
        self.wait_for_invisible_element(self.orders_ready_message)
        orders = self.find_elements(self.orders_in_work_section)
        for order in orders:
            orders_in_work.append(order.text)
        return orders_in_work

    @allure.step('Проверить, что заказ пользователя появляется в разделе В работе')
    def check_user_order_in_work_section(self, user_order: str):
        user_order = "0" + user_order
        orders_in_work = self.get_orders_in_work_section()
        return user_order in orders_in_work
