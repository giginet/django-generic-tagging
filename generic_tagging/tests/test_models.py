from django.test.testcases import TestCase
from generic_tagging.models import Tag, TaggedItem, TagManager, TaggedItemManager
from generic_tagging.tests.factories import TagFactory, TaggedItemFactory


class TagTestCase(TestCase):
    def test_manager(self):
        self.assertIsInstance(Tag.objects, TagManager)

    def test_str(self):
        tag = TagFactory(label='Test')
        self.assertEqual(str(tag), tag.label)

    def test_order(self):
        tag0 = TagFactory(label='banana')
        tag1 = TagFactory(label='apple')
        tag2 = TagFactory(label='cherry')
        tags = Tag.objects.all()
        self.assertEqual(tags[0], tag1)
        self.assertEqual(tags[1], tag0)
        self.assertEqual(tags[2], tag2)


class TaggedItemTestCase(TestCase):
    def test_manager(self):
        self.assertIsInstance(TaggedItem.objects, TaggedItemManager)

    def test_str(self):
        item = TaggedItemFactory(tag__label='Label')
        self.assertEqual(str(item), 'Label TagTestArticle object')

    def test_order(self):
        item0 = TaggedItemFactory(order=2)
        item1 = TaggedItemFactory(order=5)
        item2 = TaggedItemFactory(order=0)
        items = TaggedItem.objects.all()
        self.assertEqual(items[0], item2)
        self.assertEqual(items[1], item0)
        self.assertEqual(items[2], item1)

