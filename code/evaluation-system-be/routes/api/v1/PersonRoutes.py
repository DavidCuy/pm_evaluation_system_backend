from app.Controllers.PersonController import index, find
from app.Services.PersonService import PersonService

service = PersonService()

def route_index(event, context):
    return index(service, event)

def route_find(event, context):
    return find(service, event)

