from django.shortcuts import render

import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse

# Escopo do Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Função para autenticação do Google Calendar
def get_google_calendar_service():
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
    return service

# View para criar evento
class CreateEventView(APIView):
    def post(self, request):
        data = request.data
        titulo = data.get('title')
        descricao = data.get('description')
        data_evento = data.get('date')
        localizacao = data.get('location')

        service = get_google_calendar_service()

        evento = {
            'summary': titulo,
            'description': descricao,
            'start': {'date': data_evento},
            'end': {'date': data_evento},
            'location': localizacao
        }

        try:
            evento_criado = service.events().insert(calendarId='primary', body=evento).execute()
            
            return Response({
                "message": "Evento criado com sucesso!",
                "id": evento_criado.get('id'),
                "title": evento_criado.get('summary'),
                "event_link": evento_criado.get('htmlLink')
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View para remover evento
class DeleteEventView(APIView):
    def delete(self, request, event_id):
        # Autenticação com o Google Calendar
        service = get_google_calendar_service()
        try:
            # Tentativa de deletar o evento com base no event_id
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            return Response({"message": "Evento removido com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Se houver um erro (como evento não encontrado), retorna um erro 404
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
def listar_eventos():
    service = get_google_calendar_service()

    # Lista os próximos 10 eventos
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
    eventos = events_result.get('items', [])

    if not eventos:
        print("Nenhum evento encontrado.")
        return

    # Exibe os eventos e seus IDs
    for event in eventos:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"ID: {event['id']}, Título: {event['summary']}, Data: {start}")
