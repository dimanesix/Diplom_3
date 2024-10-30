import pytest
import allure
import test_data
from pages.account_page import AccountPage


@pytest.mark.parametrize('browser', ["chrome", "firefox"], indirect=True)
class TestPersonalAccount:
    # firefox работает через раз при проверке 2 и 3 (идёт перекрытие элементом Modal_modal_overlay__x2ZCr...)
    @allure.title('Проверка фукциональности "Личного кабинета"')
    def test_personal_account(self, browser, register_user, login_user):
        account_page = AccountPage(browser)
        # 1-ая проверка
        with allure.step("Проверяем переход по клику на кнопку 'Личный кабинет'"):
            assert login_user.get_current_url() == test_data.ACCOUNT_PAGE_URL, ('Переход по клику на "Личный кабинет" '
                                                                                'не работает!')
        # 2-ая проверка
        with allure.step("Проверяем переход в раздел 'История заказов'"):
            assert account_page.check_transfer_to_order_history() is True, ('Переход в раздел "История заказов" не '
                                                                            'работает!')
        # 3-я проверка
        with allure.step("Проверяем выход из аккаунта"):
            assert account_page.check_logout() is True, 'Выход из аккаунта не работает!'


