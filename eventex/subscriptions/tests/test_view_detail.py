from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name = 'Alysson Barros',
            cpf = '123454678901',
            email = 'alysson@barros.net',
            phone = '31-996186180'
        )
        self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk))
    def test_get(self):
        """Get/inscricao/1/ deve retornar status code 200"""
        self.assertEqual(200,self.resp.status_code)

    def test_template(self):
        """Deve retornar subscriptions/subscription_detail.html"""
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name,self.obj.cpf,self.obj.email,self.obj.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)

class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEqual(404,resp.status_code)