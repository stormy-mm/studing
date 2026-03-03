from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Item, List


class ItemModelTest(TestCase):
    """Тест модели элемента"""

    def test_default_text(self):
        """Тест: используется текст по умолчанию"""
        item = Item()
        self.assertEqual(item.text, "")

    def test_string_representation(self):
        """Тест: строковое представление"""
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


class ListModelTest(TestCase):
    """Тест модели списка"""
    
    def setUp(self):
        """Создание экземпляра списка"""
        self.list_ = List.objects.create()

    def test_item_is_related_to_list(self):
        """Тест: элемент связан со списком"""
        item = Item()
        item.list = self.list_
        item.save()
        self.assertIn(item, self.list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """Тест: нельзя добавить пустой список"""
        item = Item(list=self.list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        """Тест: получение абсолютного URL"""
        self.assertEqual(self.list_.get_absolute_url(), f"/lists/{self.list_.id}/")

    def test_duplicate_items_are_invalid(self):
        """Тест: повторы элементов недопустимы"""
        Item.objects.create(list=self.list_, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list=self.list_, text="bla")
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        """Тест: МОЖЕТ сохранить тот же элемент в разные списки"""
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean() # не должно вызывать исключение

    def test_list_ordering(self):
        """Тест: упорядочивание списков"""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )