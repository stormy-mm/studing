from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .container_commands import create_session_on_server  # (1)
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):
    """Тест приложения 'Мои списки'"""

    def create_pre_authenticated_session(self, email):
        if self.test_server:  # (2)
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/",
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """Тест: списки зарегистрированных пользователей сохраняются как 'Мои списки'"""
        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_session('edith@example.com')

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_item_list("Reticulate splines")
        self.add_item_list("Immnat")
        first_list_url = self.browser.current_url

        # Она замечает ссылку на мои списки в первый раз
        self.browser.find_element(By.LINK_TEXT, "My lists").click()

        # Она видит, что её список находится там, и он назван на основе первого элемента списка
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "Reticulate splines"))
        self.browser.find_element(By.LINK_TEXT, "Reticulate splines").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # Она решает начать ещё один список, чтобы только убедиться
        self.browser.get(self.live_server_url)
        self.add_item_list("clock rows")
        second_list_url = self.browser.current_url

        # Под заголовком Мои списки появляется её новый список
        self.browser.find_element(By.LINK_TEXT, "My lists").click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, "clock rows"))
        self.browser.find_element(By.LINK_TEXT, "clock rows").click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # Она выходит из системы. опция мои списки исчезает
        self.browser.find_element(By.LINK_TEXT, "Log out").click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.LINK_TEXT, "My lists"), []))
