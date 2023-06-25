from django.test import SimpleTestCase
from django.urls import resolve, reverse

from ..views import index, TopicsList, TopicsCreate, random, settings, change_username, confirm_delete_profile, \
    delete_profile, confirm_reset_random, reset_random, do_with_selected, signup, TopicInfoView, TopicsUpdate, \
    confirm_delete_topic, TopicsDelete, MyLogoutView


class TestUrls(SimpleTestCase):

    def test_signup_url_resolves(self):
        url = reverse('signup')

        self.assertEqual(resolve(url).func, signup)

    def test_index_url_resolves(self):
        url = reverse('index')

        self.assertEqual(resolve(url).func, index)

    def test_user_list_url_resolves(self):
        url = reverse('user_list')

        self.assertEqual(resolve(url).func.view_class, TopicsList)

    def test_add_topic_url_resolves(self):
        url = reverse('add_topic')

        self.assertEqual(resolve(url).func.view_class, TopicsCreate)

    def test_random_url_resolves(self):
        url = reverse('random')

        self.assertEqual(resolve(url).func, random)

    def test_settings_url_resolves(self):
        url = reverse('settings')

        self.assertEqual(resolve(url).func, settings)

    def test_change_username_url_resolves(self):
        url = reverse('change_username')

        self.assertEqual(resolve(url).func, change_username)

    def test_confirm_delete_profile_url_resolves(self):
        url = reverse('confirm_delete_profile')

        self.assertEqual(resolve(url).func, confirm_delete_profile)

    def test_delete_profile_url_resolves(self):
        url = reverse('delete_profile')

        self.assertEqual(resolve(url).func, delete_profile)

    def test_confirm_reset_random_url_resolves(self):
        url = reverse('confirm_reset_random')

        self.assertEqual(resolve(url).func, confirm_reset_random)

    def test_reset_random_url_resolves(self):
        url = reverse('reset_random')

        self.assertEqual(resolve(url).func, reset_random)

    def test_do_with_selected_url_resolves(self):
        url = reverse('do_with_selected')

        self.assertEqual(resolve(url).func, do_with_selected)

    def test_topic_info_url_resolves(self):
        url = reverse('topic_info', args=[1])

        self.assertEqual(resolve(url).func.view_class, TopicInfoView)

    def test_edit_topic_url_resolves(self):
        url = reverse('edit_topic', args=[1])

        self.assertEqual(resolve(url).func.view_class, TopicsUpdate)

    def test_confirm_delete_topic_url_resolves(self):
        url = reverse('confirm_delete_topic', args=[1])

        self.assertEqual(resolve(url).func, confirm_delete_topic)

    def test_delete_topic_url_resolves(self):
        url = reverse('delete_topic', args=[1])

        self.assertEqual(resolve(url).func.view_class, TopicsDelete)

    def test_logout_url_resolves(self):
        url = reverse('logout')

        self.assertEqual(resolve(url).func.view_class, MyLogoutView)


