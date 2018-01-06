from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name = 'Alysson Barros',
            cpf = '12345678901',
            email = 'alysson@barros.net',
            phone = '31-9988997842'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """A inscrição deve ter um atributo automatico criado em"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Alysson Barros', str(self.obj))

