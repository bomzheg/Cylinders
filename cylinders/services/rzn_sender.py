from time import sleep
import re

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec

Driver = webdriver.Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

PATTERN_VOLUME_CYLINDER = re.compile(r"(?<=газ сжатый 1 шт\. \()\d+\.\d+(?= м3\), баллоны/ ~)")
PATTERN_VOLUME_MONOBLOCK = re.compile(r"(?<=газ сжатый 1 шт\. \()(\d+\.\d+) м3\), баллоны \((\d+)\)(?=, моноблоки/ ~)")


class RZNGeneral:
    BASE_URL = "http://vk.roszdravnadzor.ru/"
    NAME_LOGIN_FIELD = 'login'
    NAME_PASSWORD_FIELD = 'password'
    # кнопка для аутентификации
    CLASS_LOGIN_SUBMIT = "grey-submit"
    # ссылка с "ввод данных" в верхнем меню
    ID_MAIN_MENU = "main_menu_vk_lines_new"
    # комбобокс с фильтрами
    XPATH_COMBOBOX = "/html/body/div[1]/div[3]/form/table/tbody/tr[4]/td[12]/button/span"

    FS_CHECK_BOXES = tuple()
    # кнопка отфильтровать
    FILTER_BUTTON_XPATH = "/html/body/div[1]/div[3]/form/div/table/tbody/tr/td[3]"
    # первая строка, которую будем копировать
    FIRST_ROW_XPATH = "/html/body/div[1]/form/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[2]/td[6]/nobr/a"
    # кнопка "скопировать"
    ADD_BUTCH_BUTTON = "/html/body/div[1]/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table"
    # поле для ввода номера серии
    BUTCH_NUMBER_FIELD_NAME = "_series"
    # поле для ввода количества
    COUNT_FIELD_NAME = "_quantity"
    # чекбокс который нужно отметить чтобы появилось поле для ввода количества по заданному адресу
    BUTCH_LOCATION_CHECK_BOX = "/html/body/div[1]/form/table/tbody[12]/tr[2]/td[2]/div/table/tbody/tr/td[1]/input"
    # поле для ввода количества по заданному адресу
    COUNT_BUTCH_CURRENT_LOCATION = "/html/body/div[1]/form/table/tbody[12]/tr[2]/td[2]/div/table/tbody/tr/td[2]/input"
    # кнопка "сохранить"
    CONFIRM_BUTTON_XPATH = "/html/body/div[1]/table[4]/tbody/tr/td/table/tbody/tr[2]/td[2]/table"
    ALERT_TEXT = "Сохранить данные?"

    def __init__(self, login: str, password: str, timeout: int = 10, headless: bool = False):
        self.timeout = timeout
        if headless:
            options.add_argument('headless')
        self.driver = Driver(
            executable_path=ChromeDriverManager().install(),
            chrome_options=options,
            service_log_path='NUL',
        )
        self.web_wait = WebDriverWait(self.driver, self.timeout, ignored_exceptions=StaleElementReferenceException)

        self.login = login
        self.password = password
        self.load_main_page()

    def load_main_page(self):
        self.driver.get(self.BASE_URL)
        self.web_wait.until(ec.element_to_be_clickable((By.NAME, self.NAME_LOGIN_FIELD)))

        login = self.driver.find_element_by_name(name=self.NAME_LOGIN_FIELD)
        login.send_keys(self.login)
        password = self.driver.find_element_by_name(name=self.NAME_PASSWORD_FIELD)
        password.send_keys(self.password)
        submit = self.driver.find_element_by_class_name(self.CLASS_LOGIN_SUBMIT)
        submit.click()
        self.web_wait.until(
            ec.element_to_be_clickable((By.ID, self.ID_MAIN_MENU))
        )

        input_data_btn = self.driver.find_element_by_id(self.ID_MAIN_MENU)
        input_data_btn.click()

    def load_last_batch_page(self):
        """
        in inherit class you have to specify FS_CHECK_BOXES.
        :return:
        """

        self.web_wait.until(ec.element_to_be_clickable((By.XPATH, self.XPATH_COMBOBOX)))

        combobox = self.driver.find_element_by_xpath(self.XPATH_COMBOBOX)
        combobox.click()
        for checkbox_xpath in self.FS_CHECK_BOXES:
            fs_checkbox = self.driver.find_element_by_xpath(checkbox_xpath)
            fs_checkbox.click()
        filter_button = self.driver.find_element_by_xpath(self.FILTER_BUTTON_XPATH)
        filter_button.click()
        self.web_wait.until(ec.element_to_be_clickable((By.XPATH, self.FIRST_ROW_XPATH)))

        first_row = self.driver.find_element_by_xpath(self.FIRST_ROW_XPATH)
        first_row.click()

    def save_new_batch(self, butch_number: str, count: int, *args, **kwargs):
        self.web_wait.until(
            ec.element_to_be_clickable((By.XPATH, self.ADD_BUTCH_BUTTON))
        )

        add_button = self.driver.find_element_by_xpath(self.ADD_BUTCH_BUTTON)
        add_button.click()

        self.web_wait.until(ec.element_to_be_clickable((By.XPATH, self.BUTCH_LOCATION_CHECK_BOX)))

        self.specify_info_product(*args, **kwargs)

        batch_number = self.driver.find_element_by_name(self.BUTCH_NUMBER_FIELD_NAME)
        batch_number.send_keys(butch_number)
        count_butch = self.driver.find_element_by_name(self.COUNT_FIELD_NAME)
        count_butch.send_keys(str(count))
        location_checkbox = self.driver.find_element_by_xpath(self.BUTCH_LOCATION_CHECK_BOX)
        location_checkbox.click()
        count_butch_location = self.driver.find_element_by_xpath(self.COUNT_BUTCH_CURRENT_LOCATION)
        count_butch_location.send_keys(count)
        confirm = self.driver.find_element_by_xpath(self.CONFIRM_BUTTON_XPATH)
        confirm.click()
        self.confirm_alert()

    def specify_info_product(self, *args, **kwargs):
        raise NotImplemented

    def confirm_alert(self):
        self.web_wait.until(ec.alert_is_present())

        alert = self.driver.switch_to.alert
        assert alert.text == self.ALERT_TEXT
        alert.accept()
        logger.debug("accepting alert")
        # костыльное ожидание закрытия алерта TODO исправить (как?)
        sleep(2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


class RZNLiquid(RZNGeneral):
    FS_CHECK_BOXES = (
        "/html/body/div[2]/ul/li[3]/label/input",  # ФС
        "/html/body/div[2]/ul/li[4]/label/input",  # ФС
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_last_batch_page()

    def specify_info_product(self):
        pass


class RZNGaseous(RZNGeneral):
    FS_CHECK_BOXES = ("/html/body/div[2]/ul/li[2]/label/input",)
    TABLE_VOLUMES = "/html/body/div[1]/form/table/tbody[3]/tr[5]/td[2]/div/table"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_last_batch_page()

    def specify_info_product(self, volume: str, fp_passport=None, fp_approve=None, ul_data=None):
        if ul_data is not None:
            raise NotImplemented("Current version don't support change info about \"Уполномоченное лицо\"")
        table_volumes = self.driver.find_element_by_xpath(self.TABLE_VOLUMES)
        for element in table_volumes.find_element_by_tag_name('nobr'):
            element: WebElement
            if check_text_equal_volume(element.text, volume):
                pass


def check_text_equal_volume(text, volume):
    if PATTERN_VOLUME_CYLINDER.match(text) == volume:
        return True
    if PATTERN_VOLUME_MONOBLOCK.match(text):
        return True
