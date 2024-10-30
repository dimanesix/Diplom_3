import pytest
import allure
import test_data
from pages.account_page import AccountPage
from pages.feed_order_page import FeedOrderPage
from pages.main_page import MainPage


@pytest.mark.parametrize('browser', ["chrome", "firefox"], indirect=True)
class TestFeedOrder:
    @allure.title('Проверка, что если кликнуть на заказ, откроется всплывающее окно с деталями')
    def test_click_on_order_open_window_with_details(self, browser):
        feed_order_page = FeedOrderPage(browser)
        feed_order_page.open_page(test_data.FEED_PAGE_URL)
        assert feed_order_page.check_appearance_order_detail_window() is True, 'Должно появиться окно с деталями заказа'

    @allure.title(
        'Проверка, что заказы пользователя из раздела «История заказов» отображаются на странице «Лента заказов»')
    def test_orders_in_user_history_in_feed(self, browser, login_user):
        # сделаем 2 заказа пользователем
        user_orders = []
        for _ in range(1, 3):
            login_user.open_page(test_data.MAIN_PAGE_URL)
            login_user.add_ingredient_to_basket()
            user_orders.append(login_user.create_order_and_return_order_number())
        # перейдём в аккаунт в раздел Истории заказов
        login_user.click_on_personal_account_button()
        account_page = AccountPage(browser)
        account_page.click_on_button_order_history()
        # получим список всех заказов из Истории заказов
        history_orders = account_page.return_orders_from_history()
        # перейдём в Ленту заказов
        feed_order_page = FeedOrderPage(browser)
        feed_order_page.open_page(test_data.FEED_PAGE_URL)
        # получим 50 последних заказов Ленты
        feed_orders = feed_order_page.return_orders_from_feed()
        # проверим, что все заказ видны (среди них наши два) - впринципе избыточно, но пусть будет...
        orders_is_visible = feed_order_page.check_orders_display_in_feed()
        # проверяем, чтобы заказы из истории пользователя находились в ленте, при этом
        # это должны быть именно те заказы, которые оформил пользователь и все заказы видны
        assert ((user_orders == history_orders) and (set(history_orders) <= set(feed_orders)) and orders_is_visible is
                True), "Заказы из Истории заказов должны быть в Ленте"

    @allure.title('Проверка, что при создании заказа значения счётчиков заказов За все время и Сегодня увеличиваются')
    def test_change_counters_after_user_order(self, browser, login_user):
        # зологинились, открыли Ленту заказов
        login_user.open_page(test_data.FEED_PAGE_URL)
        # запомнили значения счётчиков
        feed_order_page = FeedOrderPage(browser)
        old_counters_value = feed_order_page.get_the_counters_value()
        # перешли на главную страницу
        main_page = MainPage(browser)
        main_page.open_page(test_data.MAIN_PAGE_URL)
        # сделали заказ
        main_page.open_page(test_data.MAIN_PAGE_URL)
        main_page.add_ingredient_to_basket()
        main_page.create_order_and_return_order_number()
        # перешли снова в Ленту
        main_page.open_page(test_data.FEED_PAGE_URL)
        # получили новое значение счётчиков после сделанного закза
        new_counters_value = feed_order_page.get_the_counters_value()
        # проверяем разность - должна быть >= 1 (> - из-за того,что все тестят на одном стенде)
        with allure.step("Проверяем увеличение счётчиков после оформления заказа"):
            assert feed_order_page.check_increase_counters_after_order(old_counters_value, new_counters_value) is True, (
                                                'Сделанный заказ должен влиять наизменение счётчиков в большую сторону')

    @allure.title('Проверка, что после оформления заказа его номер появляется в разделе В работе')
    def test_appearance_order_in_work_section(self, browser, login_user):
        # оформим заказ и получим его номер
        login_user.open_page(test_data.MAIN_PAGE_URL)
        login_user.add_ingredient_to_basket()
        order_number = login_user.create_order_and_return_order_number()
        # перейдём в Ленту заказов
        feed_order_page = FeedOrderPage(browser)
        feed_order_page.open_page(test_data.FEED_PAGE_URL)
        # проверим, что наш заказ в работе
        with allure.step("Проверяем появление заказа в разделе В работе"):
            assert feed_order_page.check_user_order_in_work_section(order_number) is True, ('Заказ пользователя должен '
                                                                                            'появляться в разделе В работе')
