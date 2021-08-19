from core.models import Tag
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import *

class TestModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
    
    def test_user_created(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('12345'))
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)

    def test_user_login(self):
        self.client.login(username='testuser', password='12345')
        self.assertTrue(self.client.login(username='testuser', password='12345'))
        self.assertFalse(self.client.login(username='testuser', password='123456'))

    def test_production_created(self):
        Production.objects.create(
            name='testprod',
            CN='MILK',
        )
        self.assertEqual(Production.objects.count(), 1)
        self.assertEqual(Production.objects.first().name, 'testprod')
        self.assertEqual(Production.objects.first().CN, 'MILK')
    
    def test_customization_created(self):
        cust = Customization.objects.create(
            name='testcustom',
            slug='testcustom',
            production=Production.objects.create(name='testprod', CN='MILK')
        )
        self.assertEqual(Customization.objects.count(), 1)
        self.assertEqual(Customization.objects.first().name, 'testcustom')

    def test_tag_created(self):
        cust = Customization.objects.create(
            name='testcustom',
            slug='testcustom',
            production=Production.objects.create(name='testprod', CN='MILK')
        )
        Tag.objects.create(
            name='testtag',
            slug='testtag',
            customization=cust
        )
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, 'testtag'.upper())