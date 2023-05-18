import requests

from datetime import date

# Встречается текст загрязнённый html тегами, поэтому решил очистить
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

import sys
sys.path.append('..')

from database import SessionLocal
from schemas import QuestionSchema
from models import Question


router = APIRouter(prefix='', tags=['main_router'])


def get_db() -> None:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/')
async def questions(
    question_number: QuestionSchema, db: Session = Depends(get_db)
) -> Optional[str]:
    try:
        quiz = requests.get(
            'https://jservice.io/api/random?count='
            f'{question_number.questions_num}'
        ).json()
    except Exception:
        raise HTTPException(status_code=503, detail='Service is unavailable')
    while_loop_counter = 0
    for i in range(len(quiz)):
        question_instance = db.query(Question).filter(
            Question.question == quiz[i]['question']
        ).first()
        # встречаются записи у которых вместо ответа и вопроса "="
        # не уверен что такие записи нужны в бд
        if question_instance or quiz[i]['question'] == '=':
            while True:
                while_loop_counter += 1
                if while_loop_counter == 1000:
                    raise HTTPException(
                        status_code=508, detail='Exceed max cycles of loop'
                    )
                try:
                    quiz[i] = requests.get(
                        'https://jservice.io/api/random?count=1'
                    ).json()[0]
                except Exception:
                    raise HTTPException(
                        status_code=503, detail='Service is unavailable'
                    )
                question_instance = db.query(Question).filter(
                    Question.question == quiz[i]['question']
                ).first()
                if question_instance:
                    continue
                else:
                    break
        date_cr = date.today()
        question_instance = Question(
            question=quiz[i]['question'],
            answer=BeautifulSoup(quiz[i]['answer'], "lxml").text,
            date_created=date_cr
        )
        db.add(question_instance)
        db.commit()
    if question_number.questions_num == 1:
        return
    return quiz[len(quiz) - 2]['question']
