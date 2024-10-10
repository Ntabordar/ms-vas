import requests
import random
from typing import Any

from fastapi import HTTPException

from app.services.common import URL_MOTOR

class ValidationService:
    @staticmethod
    def get_num_assignments(team_name: str):
        # Consumir el servicio de teams para obtener los tickets por team
        
        # URL del servicio de Teams para obtener los tickets por equipo
        url = f"{URL_MOTOR}/teams/{team_name}/members/assigned"  # Actualiza con la URL real
        
        # Cabeceras con la autenticación
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET
        response = requests.get(url, headers=headers)

        # Verificar si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Convertir la respuesta a JSON
            data = response.json()

            # Imprimir los datos de los tickets por equipo
            print("Tickets por miembro:", data)
            
            teams_tickets = [{"member": member["member"], "count": member["count"]} for member in data["data"]]
            print("Equipos y número de tickets:", teams_tickets)
            return {
                "data": teams_tickets
            }
        else:
            print(f"Error: {response.status_code} - {response.text}") 
            raise HTTPException(status_code=400, detail=f"Error al obtener los tickets: {response.status_code} - {response.text}")    
    
    @staticmethod
    def choose_team_member(members_data:list[dict[str, Any]]):
        # Obtener el menor número de tickets
        min_tickets = min(item["count"] for item in members_data)
        
        # Filtrar los miembros que tienen ese menor número de tickets
        members_with_min_tickets = [item["member"] for item in members_data if item["count"] == min_tickets]
        
        # Elegir al azar si hay empate
        return random.choice(members_with_min_tickets)
        
    
    @staticmethod
    def assign(id_ticket: str, user_email:str):
        # TODO: Cambiar para que sea dinamico
        url = f"{URL_MOTOR}/reversals/{id_ticket}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "new_state": "Asignado",
            "user_email": user_email,
        }

        response = requests.put(url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code in [200, 201]:
            return response_data["data"]

        else:
            raise HTTPException(status_code=400, detail=f"Error al asignar el ticket: {response.status_code} - {response.content.decode()}")
