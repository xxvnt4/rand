from django.test import TestCase
from ..models import Topics


class TopicsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Topics.objects.create(title='Big')

    def test_title_label(self):
        topic = Topics.objects.get(id=1)
        field_label = topic._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_subtitle_label(self):
        topic = Topics.objects.get(id=1)
        field_label = topic._meta.get_field('subtitle').verbose_name
        self.assertEqual(field_label, 'subtitle')

    def test_description_label(self):
        topic = Topics.objects.get(id=1)
        field_label = topic._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_object_name_is_title_slash_subtitle(self):
        topic = Topics.objects.get(id=1)

        if topic.subtitle:
            expected_object_name = f'{topic.title} / {topic.subtitle}'
        else:
            expected_object_name = f'{topic.title}'

        self.assertEqual(str(topic), expected_object_name)

    def test_get_absolute_url(self):
        topic = Topics.objects.get(id=1)

        self.assertEqual(topic.get_absolute_url(), '/topic_info/1/')