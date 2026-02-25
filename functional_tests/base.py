import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        """Демонтаж"""
        try:
            self.browser.quit()
        except:
            pass

    def wait_for_row_in_list_table(self, row_text):
        """Ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        """Ожидать"""
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        """Получить поле ввода для элемента"""
        return self.browser.find_element(By.ID, "id_text")
