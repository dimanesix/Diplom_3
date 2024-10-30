import pytest
import requests
from faker import Faker
from selenium import webdriver
import test_data
from pages.login_page import LoginPage
from pages.main_page import MainPage


@pytest.fixture
def browser(request):
    driver = None
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")
        driver = webdriver.Chrome(options)
    elif request.param == "firefox":
        driver = webdriver.Firefox()
        driver.fullscreen_window()
    else:
        ValueError("Неверное значение!")
    yield driver
    driver.quit()


# в задании не требуется проверять регистрацию пользователя,
# поэтому выполним регистрацию пользователя через ручку
@pytest.fixture
def register_user():
    data = {
        "email": Faker().free_email(),
        "password": Faker().password(),
        "name": Faker().first_name()
    }
    response = requests.post(url=test_data.REGISTER_PAGE_URL, json=data)
    #print(f'register: {response.status_code}, {data}')
    yield data
    if response.status_code == 200:
        response = requests.delete(url=test_data.USER_DATA_ENDPOINT, headers={"Authorization": f"{response.json()["accessToken"]}"})
    else:
        ValueError("Ошибка регистрации пользователя!")
    #print(f'delete: {response.status_code}')


# в задании не требуется проверять процедуру логина пользователя,
# поэтому считаем, что это всё работает и выносим в фикстуру
@pytest.fixture
def login_user(browser, register_user):
    test_account = register_user
    test_auth_data = {
        "email": test_account["email"],
        "password": test_account["password"]
    }
    login_user_page = LoginPage(browser)
    login_user_page.login_register_user(test_auth_data["email"], test_auth_data["password"])
    main_page = MainPage(browser)
    main_page.click_on_personal_account_button()
    return main_page
