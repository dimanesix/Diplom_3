import pytest
import allure
import test_data
from pages.main_page import MainPage


@pytest.mark.parametrize('browser', ["chrome", "firefox"], indirect=True)
class TestMainFunctionality:
    @allure.title('Проверка переходов с кнопок "Конструктор" и "Лента Заказов" верхнего меню')
    def test_transfers_from_top_menu_buttons(self, browser):
        main_page = MainPage(browser)
        main_page.open_page(test_data.MAIN_PAGE_URL)
        assert main_page.check_transfer_to_constructor_button() is True, f'Должен быть переход на страницу {test_data.CONSTRUCTOR_PAGE_URL}'
        assert main_page.check_transfer_to_feed_order() is True, f'Должен быть переход на страницу {test_data.FEED_PAGE_URL}'

    @allure.title('Проверка функционирования всплывающего окна с деталями ингредиента')
    def test_test_pop_up_ingredient_window(self, browser):
        main_page = MainPage(browser)
        main_page.open_page(test_data.MAIN_PAGE_URL)
        assert main_page.check_appearance_ingredient_detail_window() is True, ('Должно появится всплывающее окно с '
                                                                               'деталями ингредиента')
        assert main_page.check_disappearance_ingredient_detail_window() is True, ('Окно с деталями ингедиента должно '
                                                                                  'пропасть')

    @allure.title('Проверка увеличения счётчика ингредиента при добавлении в корзину')
    def test_increase_ingredient_counter(self, browser):
        main_page = MainPage(browser)
        main_page.open_page(test_data.MAIN_PAGE_URL)
        assert main_page.check_is_increase_ingredient_counter() is True, ('При добавлении ингредиента в корзину '
                                                                          'счётчик ингредиента должен увеличиваться')

    @allure.title('Авторизованный пользователь может сделать заказ')
    def test_auth_user_can_create_order(self, browser, login_user):
        login_user.open_page(test_data.MAIN_PAGE_URL)
        login_user.add_ingredient_to_basket()
        assert login_user.check_create_order() is True, 'Не получается оформить заказ от авторизованного пользователя'
