import logging
from typing import cast

import random
from app.Exceptions.APIException import APIException
from database.DBConnection import AlchemyEncoder, get_session
from utils.http_utils import build_response, get_paginate_params
from app.Data.Enum.http_status_code import HTTPStatusCode
from app.Data.Interfaces.PaginationResult import PaginationResult
from app.Services.AnswerService import AnswerService
from app.Core.Controllers.BaseController import index, find, store, update, delete

def get_by_question(service, event: dict):
    session = get_session()
    (page, per_page) = get_paginate_params(event['queryStringParameters'])
    path_params = event['pathParameters']
    quizId = int(path_params['questionId'])
    
    try:
        elements = cast(AnswerService, service).filter_by_column(session, "IdQuestion", quizId, True)
        random.shuffle(elements)
        total_elements = cast(AnswerService, service).count_elements(session)
        body = PaginationResult(elements, page, per_page, total_elements).to_dict()
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        body = e.to_dict()
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        body = dict(message="Cannot make the request")
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)