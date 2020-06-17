# Agriness Developer Backend Challenge - Thamires S. F.
## Overview
Este projeto é uma API em Django para contemplar o desafio proposto pela Agriness 

## Get started:
### Requisitos:
* Python 3.8
* Pip
* Ter o python adicionado ao *path*

### Setup
* instalar os pacotes com `python -m pip install -r requirements.txt`
* execute o comando `python manage.py migrate`

### Como rodar
* execute o comando `python manage.py runserver` - rodar o servidor no host *localhost:8000* 

## Endpoints expostos:
	'/Books' : suporta o crud de livros com os principais métodos http oferecidos pelo Django Rest Framework.

	'/Accounts' : suporta o crud de usuários com os principais métodos http oferecidos pelo Django Rest Framework.

	'client/{id_client}/books' : retorna livros emprestados por um usuário pelo id do usuário.

	'books/{id_book}/reserve/{id_client}' : reserva um livro com o id de um usuário e o id de um livro

	
## Também é possível acessar esse projeto com uma interface através dos endpoints:
	'/Books': interface do Django Rest Framework

	'/Accounts': interface do Django Rest Framework

	'/admin': interface do Django Admin
