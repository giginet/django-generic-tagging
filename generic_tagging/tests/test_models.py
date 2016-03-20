from django.core.exceptions import PermissionDenied, ValidationError
from django.test.testcases import TestCase

from generic_tagging.exceptions import CannotDeleteLockedTagException
from generic_tagging.models import Tag, TaggedItem, TagManager, TaggedItemManager
from generic_tagging.tests.factories import TagFactory, TaggedItemFactory

from .factories import UserFactory

from .compatibility import patch


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
    def setUp(self):
        self.user = UserFactory()

    def test_manager(self):
        self.assertIsInstance(TaggedItem.objects, TaggedItemManager)

    def test_str(self):
        item = TaggedItemFactory(tag__label='Label')
        self.assertEqual(str(item), 'Label TagTestArticle0 object')

    def test_order(self):
        item0 = TaggedItemFactory(order=2)
        item1 = TaggedItemFactory(order=5)
        item2 = TaggedItemFactory(order=0)
        items = TaggedItem.objects.all()
        self.assertEqual(items[0], item2)
        self.assertEqual(items[1], item0)
        self.assertEqual(items[2], item1)

    def test_lock_without_permission(self):
        tag = TaggedItemFactory()
        self.assertRaises(PermissionDenied, tag.lock, self.user)

    def test_lock(self):
        item = TaggedItemFactory()
        self.assertFalse(item.locked)

        with patch.object(self.user, 'has_perm', and_return=True) as user:
            item.lock(user)
            user.has_perm.assert_called_with('generic_tagging.lock_tagged_item', obj=item)
        self.assertTrue(item.locked)

    def test_lock_with_locked_item(self):
        item = TaggedItemFactory(locked=True)
        self.assertTrue(item.locked)

        with patch.object(self.user, 'has_perm', and_return=True):
            self.assertRaises(ValidationError, item.lock, self.user)

    def test_unlock_without_permission(self):
        tag = TaggedItemFactory(locked=True)
        self.assertRaises(PermissionDenied, tag.unlock, self.user)

    def test_unlock(self):
        item = TaggedItemFactory(locked=True)
        self.assertTrue(item.locked)

        with patch.object(self.user, 'has_perm', and_return=True) as user:
            item.unlock(user)
            user.has_perm.assert_called_with('generic_tagging.unlock_tagged_item', obj=item)
        self.assertFalse(item.locked)

    def test_unlock_with_not_locked_item(self):
        item = TaggedItemFactory()
        self.assertFalse(item.locked)

        with patch.object(self.user, 'has_perm', and_return=True):
            self.assertRaises(ValidationError, item.unlock, self.user)

    def test_delete_for_unlocked_item(self):
        item = TaggedItemFactory()
        self.assertIn(item, TaggedItem.objects.all())

        item.delete()
        self.assertNotIn(item, TaggedItem.objects.all())

    def test_delete_for_locked_item(self):
        item = TaggedItemFactory(locked=True)
        self.assertIn(item, TaggedItem.objects.all())

        self.assertRaises(CannotDeleteLockedTagException, item.delete)
        self.assertIn(item, TaggedItem.objects.all())
