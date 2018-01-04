from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Alysson Barros', cpf='12345678901',
                    email='arb35@yahoo.com.br', phone='31-99618-6180')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br','arb35@yahoo.com.br']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Alysson Barros',
            '12345678901',
            'arb35@yahoo.com.br',
            '31-99618-6180'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
