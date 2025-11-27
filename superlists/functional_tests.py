from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн приложение со списком неотложных дел
        # она решает оценить его домашнюю страницу
        self.browser.get("http://localhost:8000")

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
        input_box.send_keys("Купить павлиньи перья")

        # когда она нажимает на enter, страница обновляется, и теперь страница содержит
        # "1: купить павлиньи перья" в качестве элемента списка
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(
            any(row.text == "1: Купить павлиньи перья" for row in rows),
            "Новый элемент списка не появился в таблице"
        )

        # текстовое поле по прежнему приглашает её добавить ещё один элемент
        # она вводит "сделать мушку из павлиньих перьев"
        # (Эдит очень методична)

        self.fail("Закончить тест!")

        # страница снова обновляется, и теперь показывает оба элемента в её списке

        # Эдит интересно, запомнит ли её сайт список. Далее она видит, что сайт сгенерировал для неё уникальный url-адрес
        # об этом вводится небольшое сообщение с объяснениями

        # она посещает url-адрес - её список по прежнему там

        # удовлетворённая, она ложится спать

if __name__ == '__main__':
    unittest.main(warnings="ignore")
