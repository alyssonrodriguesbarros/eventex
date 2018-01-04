from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeGet(TestCase):
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
        tags = (('<form',1),
                ('<input',6),
                ('type="text"',3),
                ('type="email"',1),
                ('type="submit"',1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html deve conter csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context deve ter subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    
class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Alysson Barros', cpf='12345678901',
                    email='arb35@yahoo.com.br', phone='31-99618-6180')
        self.resp = self.client.post('/inscricao/', data)
    def test_post(self):
        """O post válido deve redirecionar para /inscricao"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1,len(mail.outbox))

class SubscribePostInvalid(TestCase):
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