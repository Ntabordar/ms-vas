from pydantic import BaseModel

class ResourceSchema(BaseModel):
    workItemId: int

class MessageSchema(BaseModel):
    text: str

class AssignReversalSchema(BaseModel):
    subscriptionId: str
    message: MessageSchema
    resource: ResourceSchema
