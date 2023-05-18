# Bewise_jservice

 API, который вытаскивает вопросы для квизов из API jservice и сохраняет их в базе данных
 
 ## Пререквизиты
 
 На компьютере должен быть установлен Docker
 
 ## Стек
 
 FastAPI
 
 PostgreSQL
 
 ## Запуск
 
 git clone git@github.com:Konstantin8891/Bewise_jservice.git

 cd Bewise_jservice

 cd backend

 nano .env

 содержание .env файла:

 POSTGRES_DB=postgres

 POSTGRES_USER=postgres

 POSTGRES_PASSWORD=postgres

 HOST=db

 cd ..

 cd infra

 docker-compose up --build -d

 docker-compose exec backend alembic upgrade head
 
 ## Запрос к API
 
 POST http://localhost:8000/
 
 Запрос:
 
 {
 
    "questions_num": 10
    
 }
 
 Ответ:
 
 "While could be a 5th W, joining who, what, where & why; traditionally, it's this synonym"
 
