from django.test.testcases import TestCase
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient
from generic_tagging.tests.factories import TagFactory
from generic_tagging.models import Tag, TaggedItem


class TagViewSetTestCase(TestCase):
    def setUp(self):
        self.tags = [
            TagFactory(label='aaa 0'),
            TagFactory(label='bbb 1'),
            TagFactory(label='ccc 2')
        ]
        self.client = APIClient()

    def test_list(self):
        r = self.client.get('/tags/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, [
            {'id': self.tags[0].pk, 'label': self.tags[0].label},
            {'id': self.tags[1].pk, 'label': self.tags[1].label},
            {'id': self.tags[2].pk, 'label': self.tags[2].label},
        ])

    def test_retrieve(self):
        r = self.client.get('/tags/{}/'.format(self.tags[0].pk))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, {'id': self.tags[0].pk, 'label': self.tags[0].label})

    def test_create(self):
        self.assertRaises(ObjectDoesNotExist, Tag.objects.get, label='new label')
        r = self.client.post('/tags/', {'label': 'new label'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertIsNotNone(Tag.objects.get(label='new label'))

    def test_delete(self):
        tag = TagFactory()
        count = Tag.objects.count()
        r = self.client.delete('/tags/%d/' % tag.pk)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(Tag.objects.count(), count - 1)

    def test_update(self):
        tag = TagFactory()
        r = self.client.patch('/tags/%d/' % tag.pk, {'label': 'new name'})
        self.assertEqual(r.status_code, 405)

