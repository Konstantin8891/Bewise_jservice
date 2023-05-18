from sqlalchemy import Integer, Date, Text, Column

from database import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    date_created = Column(Date, nullable=False)

    def __str__(self):
        return self.question
