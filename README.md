# Lista de produtos favoritos

Este projeto simula um serviço de lista de produtos favoritos, para teste de habilidades de programação


## Índice

- [Sobre](#sobre)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Pré requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Autenticação](#Autenticação)
- [Testes](#testes)

## Sobre

Neste projeto é possivel fazer o cadastro de cliente com perfils distintos, também é posspvel cadastrar produtos e viculá-los a lista de produtos favoritos do usuário.

Para a construção deste projeto foram utlizados os conceitos de arquitetura hexagonal, DDD, clean code e SOLID

## Tecnologias Utilizadas
A aplicação foi desenvolvida utilizando as Tecnologias abaixo, segue links para consultas de documentação:

- [Python v3.10.12](https://www.python.org/downloads/release/python-31012/)
- [FastApi v0.115.8](https://fastapi.tiangolo.com/release-notes) 
- [Docker](https://docs.docker.com/)

## Pré requisitos

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

- Git
- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose


## Instalação

Siga estes passos para instalar o projeto:

Clone o repositório:

```bash
   git clone git@github.com:leandrogoncalves/fastapi_wishlist.git
```
Entre no diretório do projeto

```bash
   cd fastapi_wishlist
```

Crie o .env
```bash
    cp .env.example .env
```

Suba os containers
```bash
    docker compose up
```

Crie as tabelas do banco de dados
```bash
     docker exec -it wishlist-app sh -c "python database/migrations.py"
```

Popule o banco de dados com os dados de exemplo
```bash
    docker exec -it wishlist-app sh -c "python database/seeder.py"
```

## Como Usar

Após subir os containers, acesse a url http://localhost:8000 seu navegador. Se a instalação foi bem sucedida, você terá o seguinte retorno:

<img src="/docs/images/home.png">

Você pode acessar documentação dos endpoints do projeto acesse o link http://localhost:8000/docs

<img src="/docs/images/docs.png">


## Autenticação

As rotas principais da API estão protegidas por autenticação e autorização, para isso é necessário gerar um token de acesso. Para gerar um token de acesso é preciso realizar o login através da rota /api/auth/login. Utilize os dados de teste abaixo após ter populado o banco de dados com os dado de teste:

username: admin@test.com

password: 123456

<img src="/docs/images/token.png">

Com o token em mãos basta fazer a autorização na API através do header Authorization: Bearer <token> para utlizar os demais endpoints.

<img src="/docs/images/auth.png">

<img src="/docs/images/products.png">


## Testes

Esse projeto possui alguns testes que garantem a validação dos dados obrigatórios nos endpoints e a comunição com os MOCs de notificação e validação de transações.

Pra executar os testes:

Rode os testes:
```bash
   make test
```

Ou se preferir, rode os testes com o comando abaixo:
```bash
   docker compose up test --abort-on-container-exit --exit-code-from test
```