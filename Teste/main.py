import datetime

from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow

from google.auth.transport.requests import Request

import pickle

import os.path


# Credenciais do Google Calendar

SCOPES = ['https://www.googleapis.com/auth/calendar']


def criar_evento(titulo, descricao, data, localizacao):

    # Autenticação com o Google Calendar

    creds = None

    if os.path.exists('token.pickle'):

        with open('token.pickle', 'rb') as token:

            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:

            pickle.dump(creds, token)


    service = build('calendar', 'v3', credentials=creds)


    # Criar evento

    evento = {

        'summary': titulo,
    
        'description': descricao,

        'start': {'date': data},

        'end': {'date': data},

        'location': localizacao

    }


    # Inserir evento no calendário

    evento = service.events().insert(calendarId='primary', body=evento).execute()

    print(f'Evento criado: {evento.get("htmlLink")}')

SCOPES = ['https://www.googleapis.com/auth/calendar']


def remover_evento(titulo):

    # Autenticação com o Google Calendar

    creds = None

    if os.path.exists('token.pickle'):

        with open('token.pickle', 'rb') as token:

            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(

                'credentials.json', SCOPES)

            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'w') as token:

            pickle.dump(creds, token)


    service = build('calendar', 'v3', credentials=creds)


    # Buscar evento com base no título

    events_result = service.events().list(calendarId='primary', q=titulo).execute()
    
    events = events_result.get('items', [])


    print(f"Eventos encontrados: {events}")


    # Remover evento

    if events:

        for event in events:

            event_id = event['id']

            try:

                service.events().delete(calendarId='primary', eventId=event_id).execute()

                print(f"Evento '{titulo}' removido com sucesso!")

            except Exception as e:

                print(f"Erro ao remover evento: {e}")

    else:

        print(f"Evento '{titulo}' não encontrado.")


def main():


    while True:
        opcao = int(input("Digite 1 para inserir evento no calendário | Digite 2 para remover um evento | Digite 3 para fechar a aplicação: "))

        if opcao == 1:
            titulo = input("Digite o título do evento: ")
            descricao = input("Digite a descrição do evento: ")
            data = input("Digite a data do evento (YYYY-MM-DD): ")
            localizacao = input("Digite o localizacao desse evento: ")

            criar_evento(titulo, descricao, data, localizacao)
        elif opcao == 2:
            titulo = input("Digite o título do evento: ")

            remover_evento(titulo)

        elif opcao == 3:
            print("Obrigado por usar")
            break

if __name__ == '__main__':

    main()