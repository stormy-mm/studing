import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

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


    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список для одного пользователя"""
        # Эдит слышала про крутое новое онлайн приложение со списком неотложных дел
        self.browser.get(self.live_server_url)
        # она решает оценить его домашнюю страницу
        # она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # ей сразу же предлагается ввести элемент списка
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute("placeholder"),
            "Enter a to-do item",
        )

        # она набирает в текстовом поле "купить павлиньи перья" (вязанье рыболовных мушек)
        # когда она нажимает на enter, страница обновляется, и теперь страница содержит
        # "1: Купить павлиньи перья" в качестве элемента списка
        input_box.send_keys("Купить павлиньи перья", Keys.ENTER)

        # текстовое поле по прежнему приглашает её добавить ещё один элемент
        # она вводит "сделать мушку из павлиньих перьев"
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys("Сделать мушку из павлиньих перьев", Keys.ENTER)

        # (Эдит очень методична)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")
        self.wait_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")

        # Эдит интересно, запомнит ли её сайт список. Далее она видит, что сайт сгенерировал для неё уникальный url-адрес
        # об этом вводится небольшое сообщение с объяснениями
        self.fail("Закончить тест!")

        # удовлетворённая, она ложится спать


    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys("Купить павлиньи перья")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить павлиньи перья")

        # она замечает, что её список имеет уникальный url адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")


        # теперь новый пользователь, Френсис, приходит на сайт

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр

        self.browser = webdriver.Firefox()

        # Френсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertNotIn("Сделать мушку", page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он меннее интересен, чем список Эдит..
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys("Купить молоко")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Купить молоко")

        # Фрэнсис получает уникальный url - адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ли следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertIn("Сделать молоко", page_text)

        # удовлетворённые, они оба ложатся спать
