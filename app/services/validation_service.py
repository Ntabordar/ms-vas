import requests

from app.services.common import TEAMS_URL, ASSIGN_URL

class ValidationService:
    @staticmethod
    def get_num_assignments(team_name: str):
        # Consumir el servicio de teams para obtener los tickets por team
        
        # URL del servicio de Teams para obtener los tickets por equipo
        url = f"{TEAMS_URL}/{team_name}"  # Actualiza con la URL real
        
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
            
            teams_tickets = [(member["name"], member["tickets_count"]) for member in data["data"]]
            print("Equipos y número de tickets:", teams_tickets)
            return {
                "status": "success",
                "data": teams_tickets
            }
        else:
            print(f"Error: {response.status_code} - {response.text}") 
            raise ValueError(f"Error al obtener los tickets: {response.status_code} - {response.text}")    
    
    @staticmethod
    def assign(id_ticket: str, user_email:str):
        # Crear un nuevo ticket en Azure DevOps
        url = f"{ASSIGN_URL}/${id_ticket}"
        
        params = {
            "new_state": "En evaluacion",
            "user_email": user_email
        }
        
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.put(url, headers=headers, json=params)
        response_data = response.json()

        if response_data.status_code in [200, 201]:
            return {
                "status": "success",
                "data": response_data["data"]
            } 
        else:
            raise ValueError(f"Error al crear el ticket: {response.status_code} - {response.content.decode()}")
