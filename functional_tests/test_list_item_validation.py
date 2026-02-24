from unittest import skip

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элементов списка"""

    def test_cannot_add_empty_list(self):
        """Тест: нельзя добавить пустой список"""
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент. Она нажимает энтер на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке,
        # которое говорит, что элементы списка не должны быть пустыми
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, ".has-error").text,
            "You can't have an empty list item"
        ))

        # Она пробует снова, теперь с неким текстом для элемента, и теперь это срабатывает
        self.browser.find_element(By.ID, "id_new_item").send_keys("Buy milk")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Как ни странно, Эдит решает отправить пустой элемент списка
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        # Она получает аналогичное предупреждение на странице списка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, ".has-error").text,
            "You can't have an empty list item"
        ))

        # И она может меня исправить, заполнив поле неким тестом
        self.browser.find_element(By.ID, "id_new_item").send_keys("Make tea")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
