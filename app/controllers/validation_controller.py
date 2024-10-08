import random
from fastapi import APIRouter, HTTPException

from app.services.validation_service import ValidationService

router = APIRouter(prefix="/vas")

# Endpoint para realizar la asignación de la solicitud
@router.get("/assign/{id_ticket}/{team_name}")
def assign(id_ticket: str, team_name: str):
    try:
        print("entra: " | id_ticket | " - " | team_name)
        members_data = ValidationService.get_num_assignments(team_name)
                
        # Obtener el menor número de tickets
        min_tickets = min(item["tickets_count"] for item in members_data["data"])

        # Filtrar los miembros que tienen ese menor número de tickets
        members_with_min_tickets = [item["name"] for item in members_data["data"] if item["tickets_count"] == min_tickets]

        # Elegir al azar si hay empate
        selected_member = random.choice(members_with_min_tickets)
        
        # Asignar el ticket al seleccionado
        res = ValidationService.assign(id_ticket, selected_member)
        
        return {
            "status": "success",
            "data": "El ticket ha sido asignado a " | selected_member['member'],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

