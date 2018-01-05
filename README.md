#Eventex

Sistema de eventos encomendado pela morena

[![Build Status](https://travis-ci.org/alyssonrodriguesbarros/eventex.svg?branch=master)](https://travis-ci.org/alyssonrodriguesbarros/eventex)
[![Code Health](https://landscape.io/github/alyssonrodriguesbarros/eventex/master/landscape.svg?style=flat)](https://landscape.io/github/alyssonrodriguesbarros/eventex/master)

##Como desenvolver?
1. Clone o repositporio
2. Crie um virtualenv com python 3.5
3. Ative o seu virtualenv
4. Instale as dependências
5. Configure a instãncia com o .env
6. Execute os testes

```console
git clone git@github.com:alyssonrodriguesbarros/eventex.git wttd
cd wttd
python -m venv .wttd
windows: .wttd\scripts\activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```
##Como fazer o deploy?

1. Crie uma instãncia no heroku
2. Envie as configurações para o heroku
3. Defina uma SECRET_KEY segura para a instãncia
4. Defina DEBUG=False
5. Configure o serviço de email
6. Envie o código pára o heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=python contrib/secret_gen.py
heroku config:set DEBUG=False
#Configurar o email
git push heroku master --force
```

