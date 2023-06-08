from datetime import date
from typing import Optional

import aiohttp

# Встречается текст загрязнённый html тегами, поэтому решил очистить
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext import asyncio as sea

from database import get_async_session
from schemas import QuestionSchema
from models import Question


router = APIRouter(prefix='', tags=['main_router'])


@router.post('/')
async def questions(
    question_number: QuestionSchema,
    db: sea.AsyncSession = Depends(get_async_session)
) -> Optional[str]:
    try:
        url = (
            'https://jservice.io/api/random?count='
            f'{question_number.questions_num}'
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                quiz = await response.json()
    except Exception:
        raise HTTPException(status_code=503, detail='Service is unavailable')
    while_loop_counter = 0
    for i in range(len(quiz)):
        question_instance = await db.execute(select(Question).where(
            Question.question == quiz[i]['question']
        ))
        question_instance = question_instance.scalar_one_or_none()
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
                    url = 'https://jservice.io/api/random?count=1'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            quiz_resp = await response.json()[0]
                            quiz[i] = quiz_resp
                except Exception:
                    raise HTTPException(
                        status_code=503, detail='Service is unavailable'
                    )
                question_instance = await db.execute(select(Question).where(
                    Question.question == quiz[i]['question']
                ))
                question_instance = question_instance.scalar_one_or_none()

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
        await db.commit()
    if question_number.questions_num == 1:
        return
    return quiz[len(quiz) - 2]['question']
