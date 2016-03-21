from urllib.parse import quote
from django.test.testcases import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from rest_framework.test import APIClient
from generic_tagging.tests.factories import TagFactory, TaggedItemFactory, UserFactory, TagTestArticle0Factory
from generic_tagging.models import Tag, TaggedItem


class TagViewSetTestCase(TestCase):
    def setUp(self):
        self.tags = [
            TagFactory(label='aaa 0'),
            TagFactory(label='bbb 1'),
            TagFactory(label='ccc 2')
        ]
        self.client = APIClient()

    @staticmethod
    def _dict_for_tag(tag):
        return {'id': tag.pk,
                'label': tag.label,
                'url': 'http://testserver/api/tags/%d/' % tag.pk,
                'absolute_url': 'http://testserver/%s/' % quote(tag.label)}

    def test_list(self):
        r = self.client.get('/api/tags/')
        self.assertEqual(r.status_code, 200)

        self.assertEqual(r.data, [
            self._dict_for_tag(self.tags[0]),
            self._dict_for_tag(self.tags[1]),
            self._dict_for_tag(self.tags[2]),
        ])

    def test_retrieve(self):
        r = self.client.get('/api/tags/{}/'.format(self.tags[0].pk))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, self._dict_for_tag(self.tags[0]))

    def test_create(self):
        self.assertRaises(ObjectDoesNotExist, Tag.objects.get, label='new label')
        r = self.client.post('/api/tags/', {'label': 'new label'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertIsNotNone(Tag.objects.get(label='new label'))

    def test_delete(self):
        tag = TagFactory()
        count = Tag.objects.count()
        r = self.client.delete('/api/tags/%d/' % tag.pk)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(Tag.objects.count(), count - 1)

    def test_update(self):
        tag = TagFactory()
        r = self.client.patch('/api/tags/%d/' % tag.pk, {'label': 'new name'})
        self.assertEqual(r.status_code, 405)


class TaggedItemViewSet(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_list_with_no_parameter(self):
        r = self.client.get('/api/tagged_items/')
        self.assertEqual(r.status_code, 400)

    def test_list_with_object_id_only(self):
        article0 = TagTestArticle0Factory()
        TaggedItemFactory(content_object=article0)
        r = self.client.get('/api/tagged_items/', {'object_id': article0.pk})
        self.assertEqual(r.status_code, 400)

    def test_list_with_content_type_only(self):
        article0 = TagTestArticle0Factory()
        TaggedItemFactory(content_object=article0)
        ct = ContentType.objects.get_for_model(article0)
        r = self.client.get('/api/tagged_items/', {'content_type': ct.pk})
        self.assertEqual(r.status_code, 400)

    def test_list_with_object(self):
        article0 = TagTestArticle0Factory()
        article1 = TagTestArticle0Factory()
        tagged_item0 = TaggedItemFactory(content_object=article0)
        tagged_item1 = TaggedItemFactory(content_object=article0)
        tagged_item2 = TaggedItemFactory(content_object=article1)

        ct = ContentType.objects.get_for_model(article0)
        r = self.client.get('/api/tagged_items/', {'content_type': ct.pk, 'object_id': article0.pk})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)
        self.assertEqual(r.data[0]['id'], tagged_item0.pk)
        self.assertEqual(r.data[1]['id'], tagged_item1.pk)

    def test_retrieve(self):
        tagged_item = TaggedItemFactory()
        r = self.client.get('/api/tagged_items/%d/' % tagged_item.pk)
        self.assertEqual(r.status_code, 405)

    def test_create_with_new_tag(self):
        item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)

        r = self.client.post('/api/tagged_items/', {'tag': 'new tag', 'object_id': article.pk, 'content_type': ct.pk})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(TaggedItem.objects.count(), item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count + 1)
        tagged_item = TaggedItem.objects.all()[0]
        self.assertIsNone(tagged_item.author)

    def test_create_with_exist_tag(self):
        TagFactory(label='exist tag')
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)
        item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()

        r = self.client.post('/api/tagged_items/', {'tag': 'exist tag', 'object_id': article.pk, 'content_type': ct.pk})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(TaggedItem.objects.count(), item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count)
        tagged_item = TaggedItem.objects.all()[0]
        self.assertIsNone(tagged_item.author)

    def test_create_with_author(self):
        self.client.login(username=self.user.username, password='password')
        item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)

        r = self.client.post('/api/tagged_items/', {'tag': 'new tag', 'object_id': article.pk, 'content_type': ct.pk})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(TaggedItem.objects.count(), item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count + 1)
        tagged_item = TaggedItem.objects.all()[0]
        self.assertEqual(tagged_item.author, self.user)

    def test_update(self):
        item = TaggedItemFactory()
        r = self.client.patch('/api/tagged_items/%d/' % item.pk, {'locked': False})
        self.assertEqual(r.status_code, 405)

    def test_delete(self):
        item = TaggedItemFactory()
        count = TaggedItem.objects.count()
        r = self.client.delete('/api/tagged_items/%d/' % item.pk)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(TaggedItem.objects.count(), count - 1)

    def test_lock(self):
        lock_permission = Permission.objects.get(codename='lock_tagged_item')
        self.user.user_permissions.add(lock_permission)
        self.client.login(username=self.user.username, password='password')

        item = TaggedItemFactory()
        r = self.client.patch('/api/tagged_items/%d/lock/' % item.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(TaggedItem.objects.get(pk=item.pk).locked)

    def test_lock_without_permission(self):
        item = TaggedItemFactory()
        r = self.client.patch('/api/tagged_items/%d/lock/' % item.pk)
        self.assertEqual(r.status_code, 403)
        self.assertFalse(TaggedItem.objects.get(pk=item.pk).locked)

    def test_lock_for_locked_item(self):
        lock_permission = Permission.objects.get(codename='lock_tagged_item')
        self.user.user_permissions.add(lock_permission)
        self.client.login(username=self.user.username, password='password')

        item = TaggedItemFactory(locked=True)
        r = self.client.patch('/api/tagged_items/%d/lock/' % item.pk)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(TaggedItem.objects.get(pk=item.pk).locked)

    def test_unlock(self):
        unlock_permission = Permission.objects.get(codename='unlock_tagged_item')
        self.user.user_permissions.add(unlock_permission)
        self.client.login(username=self.user.username, password='password')

        item = TaggedItemFactory(locked=True)
        r = self.client.patch('/api/tagged_items/%d/unlock/' % item.pk)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(TaggedItem.objects.get(pk=item.pk).locked)

    def test_unlock_without_permission(self):
        item = TaggedItemFactory(locked=True)
        r = self.client.patch('/api/tagged_items/%d/unlock/' % item.pk)
        self.assertEqual(r.status_code, 403)

    def test_unlock_for_unlocked_item(self):
        unlock_permission = Permission.objects.get(codename='unlock_tagged_item')
        self.user.user_permissions.add(unlock_permission)
        self.client.login(username=self.user.username, password='password')

        item = TaggedItemFactory()
        r = self.client.patch('/api/tagged_items/%d/unlock/' % item.pk)
        self.assertEqual(r.status_code, 400)
        self.assertFalse(TaggedItem.objects.get(pk=item.pk).locked)
