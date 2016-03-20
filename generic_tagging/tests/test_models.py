from django.test.testcases import TestCase
from generic_tagging.models import Tag, TaggedItem, TagManager, TaggedItemManager
from generic_tagging.tests.factories import TagFactory


class TagTestCase(TestCase):
    def test_manager(self):
        self.assertIsInstance(Tag.objects, TagManager)

    def test_str(self):
        tag = TagFactory(label='Test')
        self.assertEqual(tag.label, str(tag))

    def test_order(self):
        tag0 = TagFactory(label='banana')
        tag1 = TagFactory(label='apple')
        tag2 = TagFactory(label='cherry')
        tags = Tag.objects.all()
        self.assertEqual(tags[0], tag1)
        self.assertEqual(tags[1], tag0)
        self.assertEqual(tags[2], tag2)
