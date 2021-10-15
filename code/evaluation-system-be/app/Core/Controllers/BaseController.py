from typing import cast

from ...Data.Interfaces.PaginationResult import PaginationResult
from ..Services.BaseService import BaseService
from ....database.DBConnection import AlchemyEncoder, get_session
from ....utils.http_utils import build_response, get_paginate_params
from ...Data.Enum.http_status_code import HTTPStatusCode

def index(service, event: dict):
    session = get_session()
    (page, per_page) = get_paginate_params(event['queryStringParameters'])
    
    try:
        elements = cast(BaseService, service).get_all(session, True, page, per_page)
        total_elements = cast(BaseService, service).count_elements(session)
        body = PaginationResult(elements, page, per_page, total_elements).to_dict()
        status_code = HTTPStatusCode.OK.value
    except Exception as e:
        print("Cannot make the request")
        print(e)
        body = dict(message="Cannot make the request")
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)

def find(service, event: dict, id: int):
    session = get_session()
    
    try:
        body = cast(BaseService, service).get_one(session, id)
        status_code = HTTPStatusCode.OK.value
    except Exception as e:
        print("Cannot make the request")
        print(e)
        body = dict(message="Cannot make the request")
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)
