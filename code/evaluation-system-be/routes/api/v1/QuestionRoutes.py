from app.Controllers.QuestionController import index, find, store, update, delete, get_by_quiz
from app.Services.QuestionService import QuestionService

service = QuestionService()

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

def route_get_by_quiz(event, context):
    return get_by_quiz(service, event)

