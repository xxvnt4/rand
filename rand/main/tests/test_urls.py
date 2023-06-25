from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .. import views


class TestUrls(SimpleTestCase):

    def test_signup_url_resolves(self):
        url = reverse('signup')

        self.assertEqual(resolve(url).func, views.signup)

    def test_index_url_resolves(self):
        url = reverse('index')

        self.assertEqual(resolve(url).func, views.index)

    def test_user_list_url_resolves(self):
        url = reverse('user_list')

        self.assertEqual(resolve(url).func.view_class, views.TopicsList)

    def test_add_topic_url_resolves(self):
        url = reverse('add_topic')

        self.assertEqual(resolve(url).func.view_class, views.TopicsCreate)

    def test_random_url_resolves(self):
        url = reverse('random')

        self.assertEqual(resolve(url).func, views.random)

    def test_settings_url_resolves(self):
        url = reverse('settings')

        self.assertEqual(resolve(url).func, views.settings)

    def test_change_username_url_resolves(self):
        url = reverse('change_username')

        self.assertEqual(resolve(url).func, views.change_username)

    def test_confirm_delete_profile_url_resolves(self):
        url = reverse('confirm_delete_profile')

        self.assertEqual(resolve(url).func, views.confirm_delete_profile)

    def test_delete_profile_url_resolves(self):
        url = reverse('delete_profile')

        self.assertEqual(resolve(url).func, views.delete_profile)

    def test_confirm_reset_random_url_resolves(self):
        url = reverse('confirm_reset_random')

        self.assertEqual(resolve(url).func, views.confirm_reset_random)

    def test_reset_random_url_resolves(self):
        url = reverse('reset_random')

        self.assertEqual(resolve(url).func, views.reset_random)

    def test_do_with_selected_url_resolves(self):
        url = reverse('do_with_selected')

        self.assertEqual(resolve(url).func, views.do_with_selected)

    def test_topic_info_url_resolves(self):
        url = reverse('topic_info', args=[1])

        self.assertEqual(resolve(url).func.view_class, views.TopicInfoView)

    def test_edit_topic_url_resolves(self):
        url = reverse('edit_topic', args=[1])

        self.assertEqual(resolve(url).func.view_class, views.TopicsUpdate)

    def test_confirm_delete_topic_url_resolves(self):
        url = reverse('confirm_delete_topic', args=[1])

        self.assertEqual(resolve(url).func, views.confirm_delete_topic)

    def test_delete_topic_url_resolves(self):
        url = reverse('delete_topic', args=[1])

        self.assertEqual(resolve(url).func.view_class, views.TopicsDelete)

    def test_logout_url_resolves(self):
        url = reverse('logout')

        self.assertEqual(resolve(url).func.view_class, views.MyLogoutView)
