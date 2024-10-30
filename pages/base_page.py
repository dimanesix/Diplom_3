import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step('Открыть страницу')
    def open_page(self, page_url: str):
        self.driver.get(page_url)

    @allure.step('Найти элемент')
    def find_element(self, page_object: tuple[str, str]):
        return self.driver.find_element(*page_object)

    @allure.step('Найти элементы')
    def find_elements(self, page_object: tuple[str, str]):
        return self.driver.find_elements(*page_object)

    @allure.step('Выполнить скрипт')
    def execute_script(self, script: str, args):
        self.driver.execute_script(script, args)

    @allure.step('Получить URL активной страницы')
    def get_current_url(self):
        return self.driver.current_url

    # иногда требуется повышать timeout >10 для работы в firefox
    @allure.step('Дождаться, когда появится страница')
    def wait_url_to_be(self, page_url: str):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_to_be(page_url))

    # иногда требуется повышать timeout >10 для работы в firefox
    @allure.step('Дождаться появления элемента')
    def wait_for_load_element(self, page_object: tuple[str, str]):
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(page_object))

    @allure.step('Дождаться появления всех элементов')
    def wait_for_load_elements(self, page_object: tuple[str, str]):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_all_elements_located(page_object))

    # костыль для firefox, но иногда и он не помогает...
    @allure.step('Дождаться загрузки страницы полностью')
    def wait_for_load_page(self):
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))

    @allure.step('Дождаться когда элемент исчезнет')
    def wait_for_invisible_element(self, page_object: tuple[str, str]):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.invisibility_of_element_located(page_object))

    @allure.step('Кликнуть по элементу')
    def click_on_element(self, page_object: tuple[str, str]):
        self.driver.find_element(*page_object).click()

    @allure.step('Кликнуть по элементу')
    def click_on_elements(self, page_object: tuple[str, str], number):
        self.find_elements(page_object)[number - 1].click()

    @allure.step('Заполнить элемент данными')
    def set_data_to_element(self, page_object: tuple[str, str], data: str):
        self.driver.find_element(*page_object).send_keys(data)

    @allure.step('Получить значение аттрибута')
    def get_attribute_value(self, page_object: tuple[str, str], attrib: str):
        return self.driver.find_element(*page_object).get_attribute(attrib)

    @allure.step('Получить значение')
    def get_element_text(self, page_object: tuple[str, str]):
        return self.driver.find_element(*page_object).text

    @allure.step('Проверить видимость элемента')
    def is_element_displayed(self, page_object: tuple[str, str]):
        return self.driver.find_element(*page_object).is_displayed()

    @allure.step('Перетянуть элемент в место назначения')
    def drag_and_drop_element(self, source: tuple[str, str], dest: tuple[str, str], number):
        source = self.find_elements(source)[number - 1]
        dest = self.find_elements(dest)[number - 1]
        ActionChains(self.driver).drag_and_drop(source, dest).perform()
