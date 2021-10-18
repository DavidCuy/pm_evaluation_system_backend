import json
import logging
from typing import cast

import random
from app.Exceptions.APIException import APIException
from database.DBConnection import AlchemyEncoder, get_session
from utils.http_utils import build_response
from app.Data.Enum.http_status_code import HTTPStatusCode
from app.Data.Interfaces.PaginationResult import PaginationResult
from app.Data.Models.Question import Question
from app.Data.Models.Answer import Answer
from app.Data.Models.Person import Person
from app.Data.Models.PersonAnswer import PersonAnswer

def index(event: dict):
    session = get_session()
    path_params = event['pathParameters']
    personId = int(path_params['personId'])
    quizId = int(path_params['quizId'])
    
    try:
        questions = Question.filter_by(session, "IdQuiz", quizId)
        question_ids = list(map(lambda q: q.id, questions))
        answers = session.query(Answer).filter(Answer.IdQuestion.in_(question_ids))
        answer_ids = list(map(lambda a: a.id, answers))
        person_answers = session.query(PersonAnswer).filter(PersonAnswer.IdAnswer.in_(answer_ids)).all()
        print(person_answers)

        body = []

        for q in json.loads(json.dumps(questions, cls=AlchemyEncoder)):
            print(q)
            q_answers = list(filter(lambda a: a.IdQuestion == q['IdQuestion'], answers))
            qp_answer = list(filter(lambda a: a.IdQuestion == q['IdQuestion'], answers))
            if len(q_answers) > 0:
                q['answers'] = json.loads(json.dumps(q_answers, cls=AlchemyEncoder))
                for q_answer in q_answers:
                    qp_answer = list(filter(lambda qp: qp.IdAnswer == q_answer.id, person_answers))
                    if len(qp_answer) > 0:
                        q['person_answer'] = json.loads(json.dumps(qp_answer[0], cls=AlchemyEncoder))

            body.append(q)

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