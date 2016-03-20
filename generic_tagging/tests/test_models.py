from django.test.testcases import TestCase
from generic_tagging.models import Tag, TaggedItem, TagManager, TaggedItemManager


class TagTestCase(TestCase):
    def test_manager(self):
        self.assertIsInstance(Tag.objects, TagManager)
