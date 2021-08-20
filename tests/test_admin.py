from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from core.models import *


class TestCustomAdmin(TestCase):
    def setUp(self):        
        self.order_admin = admin.site._registry.get(Order)
        self.tag_admin = admin.site._registry.get(Tag)
        self.cust_admin = admin.site._registry.get(Customization)

    def test_order_models_is_registered(self):
        self.assertTrue(Order in admin.site._registry)
        self.assertTrue(Tag in admin.site._registry)
        self.assertTrue(Customization in admin.site._registry)
    
    def test_fieldsets_identification(self):
        answer_id = self.order_admin.fieldsets
        expected_id = (
                    ('Client', {'fields': ('owner',)
                        }),
                    ('Order', {'fields': ('status', 'product', 'quantity', 'price', 'tag', 'customization')
                        }),
                    ('Customizations', {
                        'fields': ('MILK', 'SIZE', 'SHOTS', 'KIND')
                        })
                    )
        self.assertEqual(expected_id, answer_id)


class TestObjectsAdmin(TestCase):
    def setUp(self):
        # register an admin user and login
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.client.login(username='admin', password='admin')

    def test_create_tag_adminpage(self):
        response = self.client.get('/admin/core/tag/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_customization_adminpage(self):
        response = self.client.get('/admin/core/customization/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_order_adminpage(self):
        response = self.client.get('/admin/core/order/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_production_adminpage(self):
        response = self.client.get('/admin/core/production/add/')
        self.assertEqual(response.status_code, 200)
