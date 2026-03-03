from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List


class ItemFormTest(TestCase):
    """Тест формы для элемента списка"""

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """Тест: поле ввода имеет placeholder и css-классы"""
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """Тест валидации формы для пустых элементов"""
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_handles_saving_to_a_list(self):
        """Тест: метод save формы обрабатывает сохранение в список"""
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, "do me")
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
    """Тест формы для существующего списка"""

    def setUp(self):
        """Создание экземпляра списка"""
        self.list_ = List.objects.create()

    def test_form_renders_item_text_input(self):
        """Тест: форма отображает текстовый ввод элемента"""
        form = ExistingListItemForm(for_list=self.list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """Тест: валидация формы для пустых элементов"""
        form = ExistingListItemForm(for_list=self.list_, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        """Тест: валидация формы для повторных элементов"""
        Item.objects.create(list=self.list_, text="to do")
        form = ExistingListItemForm(for_list=self.list_, data={"text": "to do"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        """Тест сохранения формы"""
        form = ExistingListItemForm(for_list=self.list_, data={"text": "to do"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])