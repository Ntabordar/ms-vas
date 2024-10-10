from fastapi import APIRouter, HTTPException

from app.schemas.validation_schema import AssignReversalSchema
from app.services.validation_service import ValidationService

router = APIRouter(prefix="/vas")

def extract_text_between_markers(text: str, start_marker: str, end_marker: str) -> str:
    try:
        start_index = text.index(start_marker) + len(start_marker)
        end_index = text.index(end_marker, start_index)
        return text[start_index:end_index].strip()
    except ValueError:
        return ""

# Endpoint para realizar la asignación de la solicitud
@router.post("/assign")
def assign(schema: AssignReversalSchema):
    try:
        state = extract_text_between_markers(schema.message.text, "transitioned to", "by")
        if state != "Solicitado":
            return {
                "status": "success",
                "data": "Ticket ignorado",
            }
        
        team_name = "AX - Grupo 1"
        id_ticket = str(schema.resource.workItemId)
        
        members_data = ValidationService.get_num_assignments(team_name).get("data", [])
        selected_member = ValidationService.choose_team_member(members_data)
        result = ValidationService.assign(id_ticket, selected_member)
        
        print(f"El ticket '{id_ticket}' ha sido asignado a {selected_member}")
        
        return {
            "status": "success",
            "data": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

