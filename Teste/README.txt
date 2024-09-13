Antes de ir direto para a criação da API tentei criar uma logica de criação de eventos e remoção dos mesmos, como vocês podem ver no arquivo main.py,
esse codigo me fez ter uma base para a criação da API, e não me perder durante a sua criação, ele é um codigo que funciona no terminal mas, faz a mesma função da API.


Este projeto foi criado usando Django e Django Rest Framework (DRF) para integrar uma API que cria e remove eventos no Google Calendar. Abaixo está o passo a passo de como a API foi construída.
Estrutura Geral da API
Endpoints principais:

    Criar Evento: Permite criar um evento no Google Calendar usando os dados fornecidos no corpo da requisição (título, descrição, data e localização).
    Deletar Evento: Permite deletar um evento existente no Google Calendar, passando o ID do evento como parâmetro na URL.

Etapas do Desenvolvimento:
1. Criação do Projeto Django

Primeiro, foi criado um projeto Django e um aplicativo específico chamado events, onde a lógica para interação com o Google Calendar foi implementada.

bash

django-admin startproject mycalendar
cd mycalendar
python manage.py startapp events

2. Configuração da Google Calendar API

No Google Developers Console, foi habilitada a Google Calendar API. Depois disso:

    Foram geradas credenciais OAuth 2.0.
    O arquivo credentials.json foi baixado e colocado na raiz do projeto para ser usado na autenticação da API.

3. Autenticação com o Google Calendar

Para autenticar e interagir com a API do Google Calendar, foi implementada a função get_google_calendar_service.
Esta função autentica a aplicação usando o arquivo credentials.json e armazena tokens de autenticação em token.pickle. O token é reutilizado para evitar a necessidade de autenticação sempre que a API for acessada.


4. Implementação das Views para Criar e Deletar Eventos
a) Criar Evento

A view CreateEventView recebe os dados do evento via POST (título, descrição, data e localização) e cria um evento no Google Calendar. O ID, título e link do evento são retornados na resposta.

5. Configuração das URLs:
As rotas da API foram configuradas no arquivo events/urls.py. As rotas permitem criar e deletar eventos:

6. Configuração Final:
No arquivo principal de URLs do projeto (mycalendar/urls.py), foi adicionado o events.urls:

7. Testando a API:

Com a API configurada, é possível testá-la utilizando ferramentas como Postman ou Insomnia para realizar as seguintes ações:

Criar um Evento:
POST para http://127.0.0.1:8000/api/events/
Corpo da requisição (JSON):

json

{
 "title": "Reunião de Projeto",
 "description": "Discussão sobre o progresso do projeto",
 "date": "2024-09-15",
 "location": "Escritório Central"
}

Deletar um Evento:
 DELETE para http://127.0.0.1:8000/api/events/{event_id}/

Conclusão

Este código integra uma API RESTful com o Google Calendar utilizando Django e Django Rest Framework. Ele permite que o usuário crie e remova eventos de forma programática e automatizada.
A autenticação é realizada via OAuth 2.0 e tokens são armazenados para facilitar a reutilização da sessão com o Google Calendar.