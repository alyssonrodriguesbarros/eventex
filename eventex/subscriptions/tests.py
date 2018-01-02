from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
    def test_get(self):
        """Get/inscricao/ deve retornar status code 200"""
        self.assertEqual(200,self.resp.status_code)
    def test_template(self):
        """Deve retornar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    def test_html(self):
        """O html deve conter input tags"""
        self.assertContains(self.resp,'<form')
        self.assertContains(self.resp,'<input',6)
        self.assertContains(self.resp,'type="text"',3)
        self.assertContains(self.resp,'type="email"')
        self.assertContains(self.resp,'type="submit"')
    def test_csrf(self):
        """Html deve conter csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context deve ter subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form deve conter 4 campos"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Alysson Barros', cpf='12345678901',
                    email='arb35@yahoo.com.br', phone='31-99618-6180')
        self.resp = self.client.post('/inscricao/', data)
    def test_post(self):
        """O post válido deve redirecionar para /inscricao"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1,len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br','arb35@yahoo.com.br']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Alysson Barros', email.body)
        self.assertIn('12345678901',email.body)
        self.assertIn('arb35@yahoo.com.br', email.body)
        self.assertIn('31-99618-6180', email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
    def test_post(self):
        """A postagem inválida não deve redirecionar"""
        self.assertEqual(200,self.resp.status_code)
    def test_template(self):
        """Deve retornar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    def test_has_form(self):
        """Context deve ter subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    def test_form_has_errors(self):
        """Context deve ter subscription form"""
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Alysson Barros', cpf='12345678901',
                    email='arb35@yahoo.com.br', phone='31-99618-6180')
        response = self.client.post('/inscricao/',data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')