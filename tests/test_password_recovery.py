import pytest
import allure
from faker import Faker
import test_data
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage


@pytest.mark.parametrize('browser', ["chrome", "firefox"], indirect=True)
class TestPasswordRecovery:
    @allure.title('Проверка, что при нажатии на кнопку "Восстановить пароль" происходит переход на страницу '
                  'восстановления пароля')
    def test_transfer_to_recovery_password_page(self, browser):
        login_page = LoginPage(browser)
        login_page.open_page(test_data.LOGIN_PAGE_URL)
        assert login_page.check_url_from_button() is True, (f'Должен быть переход на страницу '
                                                            f'{test_data.FORGOT_PASSWORD_URL}')

    @allure.title('Проверка ввода почты и клика по кнопке "Восстановить"')
    def test_enter_email_and_click_recover_button(self, browser):
        some_email = Faker().free_email()
        forgot_password_page = ForgotPasswordPage(browser)
        forgot_password_page.open_page(test_data.FORGOT_PASSWORD_URL)
        forgot_password_page.send_data_to_email_field(some_email)
        assert (forgot_password_page.check_text_is_display_in_email_field() is True and
                forgot_password_page.check_input_email_text_is_correct(
                    some_email) is True), ('Вводимый адрес электронной почты должен быть виден и корректно '
                                           'отображаться')

        assert forgot_password_page.check_clickable_recover_button() is True, ('Кнопка "Восстановить" должна '
                                                                               'кликаться')

    # в firefox в большинстве запусков падает, но бывало проходил...Modal_modal_overlay__x2ZCr - перекрыает нужные
    # кнопки
    @allure.title('Проверка, что клик по кнопке показать/скрыть пароль делает поле активным — подсвечивает его"')
    def test_click_on_show_pwd_button_email_field_is_active(self, browser):
        some_email = Faker().free_email()
        forgot_password_page = ForgotPasswordPage(browser)
        forgot_password_page.open_page(test_data.FORGOT_PASSWORD_URL)
        forgot_password_page.send_data_to_email_field(some_email)
        forgot_password_page.click_on_recover_button()
        assert ResetPasswordPage(browser).check_active_password_field_on_button_click() is True, ('По нажатию на '
                                                                                                  'кнопку '
                                                                                                  'скрыть/показать '
                                                                                                  'пароль поле ввода '
                                                                                                  'должно '
                                                                                                  'подсвечиваться')