from pydantic import BaseModel


class QuestionSchema(BaseModel):
    questions_num: int
