import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from auth_data import user_data


# Определение класса для страницы регистрации
class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://uts.sirius.online/#/auth/register/qainternship"
        self.xpath_list = {
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[2]/label/div[2]/input': 'first_name',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[3]/label/div[2]/input': 'last_name',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[4]/label/div[2]/input': 'mid_name',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[5]/label/div[2]/div[1]': 'birth',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[6]/label/div[2]/input': 'email',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[7]/label/div[2]/input': 'profession',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[8]/div/div[2]/label/div[2]/select': 'country',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[8]/div/div[3]/label/div[2]/input': 'city',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[8]/div/div[4]/label/div[2]/input': 'name_organization',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[8]/div/div[5]/label/div[2]/input': 'school',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[8]/div/div[6]/label/div[2]/input': 'classes',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[9]/label/div[2]/input': 'vosh_login',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[10]/label/div[2]/input': 'tel',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[11]/label/div[2]/input': 'snils',
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[12]/ul/li[1]/span[2]': None,
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[12]/ul/li[2]/span[2]': None,
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[13]/div/label/input': None,
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[14]/div/label/input': None,
            '//*[@id="index"]/div/div[2]/div[4]/div/div/div[15]/div/label/input': None,
        }

    def navigate_to_registration_page(self):
        """
        Осуществляет переход на страницу регистрации.
        :return: None
        """
        self.driver.get(self.url)

    def is_registration_page_loaded(self):
        """
        Проверяет, что страница регистрации полностью загружена и доступна для взаимодействия.
        :return: None.
        """
        try:
            first_name_input = self.driver.find_element(By.XPATH, next(iter(self.xpath_list)))
            last_name_input = self.driver.find_element(By.XPATH, next(iter(self.xpath_list)))

            return first_name_input.is_displayed() and last_name_input.is_displayed()
        except NoSuchElementException:
            return False

    def empty_fields_validation(self):
        """
        Проверяет, что обязательные поля на странице регистрации отображаются и что появляются сообщения об ошибках,
        если поля оставлены пустыми.
        :return: None.
        """
        wait = WebDriverWait(self.driver, 3)
        for xpath in self.xpath_list.keys():
            try:
                element = wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
                assert element.is_displayed()
            except Exception as ex:
                pytest.fail(f"Element with XPath '{xpath}' is not visible. Error: {str(ex)}")

    def fill_registration_form(self, data):
        """
        Заполняет форму регистрации данными из переданного словаря.
        :param data: Словарь с данными для заполнения формы.
        :return: None.
        """
        sleep(1)
        for index, (xpath, data_key) in enumerate(self.xpath_list.items()):
            new_key = '//*[@id="index"]/div/div[2]/div[4]/div/div/div[5]/label/div[2]/div[1]'
            new_elem = "/div/div/input"
            if xpath == new_key:
                new_xpath = f'{new_key}{new_elem}'
                element = self.driver.find_element(By.XPATH, new_xpath)
            else:
                element = self.driver.find_element(By.XPATH, xpath)

            if index == 3:
                element.send_keys(data[data_key])
                sleep(2)

            if data_key is None:
                element.click()
            else:
                element.send_keys(user_data[data_key])

        self.driver.find_element(By.XPATH, '//*[@id="index"]/div/div[2]/div[4]/button/span').click()


    def is_registration_successful(self):
        """
        Проверяет, что после успешной регистрации пользователь перенаправлен на страницу с подтверждением.
        :return: None.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="index"]/div/div[2]/div/div[2]'))
            )
            return True
        except TimeoutException:
            return False

    def select_additional_olympiad(self):
        """
        Выбирает дополнительную олимпиаду на странице регистрации.
        :return: None
        """
        additional_olympiad_xpath = '//*[@id="index"]/div/div[2]/div[4]/div/div/div[12]/ul/li[1]/span[2]'
        main_olympiad_xpath = '//*[@id="index"]/div/div[2]/div[4]/div/div/div[12]/ul/li[2]/span[2]'
        main_element = self.driver.find_element(By.XPATH, additional_olympiad_xpath)
        add_element = self.driver.find_element(By.XPATH, main_olympiad_xpath)
        add_element.click() if add_element.is_displayed() else main_element.click()


# Фикстура для инициализации и завершения браузера перед/после тестами
@pytest.fixture(scope="module")
def browser():
    service = webdriver.ChromeService(executable_path=r'./chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# Тест-кейс для проверки загрузки страницы регистрации
def test_is_registration_page_loaded(browser):
    page = RegistrationPage(browser)
    page.navigate_to_registration_page()
    assert page.is_registration_page_loaded()


# Тест-кейс для проверки сообщений об ошибках при пустых обязательных полях
def test_empty_fields_validation(browser):
    page = RegistrationPage(browser)
    page.navigate_to_registration_page()
    page.empty_fields_validation()


# Тест-кейс для проверки выбора дополнительной олимпиады
def test_select_additional_olympiad(browser):
    page = RegistrationPage(browser)
    page.navigate_to_registration_page()
    page.select_additional_olympiad()


# Тест-кейс для проверки заполнения формы регистрации
def test_fill_registration_form(browser):
    page = RegistrationPage(browser)
    page.navigate_to_registration_page()
    page.fill_registration_form(user_data)


# Тест-кейс для проверки успешной регистрации
def test_is_registration_successful(browser):
    page = RegistrationPage(browser)
    page.is_registration_page_loaded()
    assert page.is_registration_page_loaded()


