from app.Controllers.PersonController import index, find, store, update, delete
from app.Services.PersonService import PersonService

service = PersonService()

def route_index(event, context):
    return index(service, event)

def route_find(event, context):
    return find(service, event)

def route_insert(event, context):
    return store(service, event)

def route_update(event, context):
    return update(service, event)

def route_delete(event, context):
    return delete(service, event)

