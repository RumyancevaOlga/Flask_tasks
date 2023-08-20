# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# БАЗА ДАННЫХ БУДЕТ ТОЛЬКО НА СЛЕДУЮЩЕМ ЗАНЯТИИ
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа.
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Создайте маршрут для удаления информации о пользователе (метод DELETE).
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='./Home_Work_5/templates')


# Создайте класс User с полями id, name, email и password.
class User(BaseModel):
    name: str
    email: str
    password: str


class UserId(User):
    id: int


# Создайте список users для хранения пользователей.
users = [
    UserId(id=1, name='Ivan', email='ivan@mail.ru', password='1234'),
    UserId(id=2, name='Petr', email='petr@mail.ru', password='5678')
]


# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja
@app.get('/', response_class=HTMLResponse)
async def show_users(request: Request):
    return templates.TemplateResponse('user.html', {'request': request, 'users': users})


# Создайте маршрут для добавления нового пользователя (метод POST).
@app.post('/user/', response_model=UserId)
async def add_user(item: User):
    id_ = len(users) + 1
    user = UserId
    user.id = id_
    user.name = item.name
    user.email = item.email
    user.password = item.password
    users.append(user)
    return user


# Создайте маршрут для обновления информации о пользователе (метод PUT).
@app.put('/user/{id}', response_model=UserId)
async def update_user_information(id_: int, update_user: User):
    for user in users:
        if user.id == id_:
            user.name = update_user.name
            user.email = update_user.email
            user.password = update_user.password
            return user
    raise HTTPException(status_code=404, detail='User not found')


# Создайте маршрут для удаления информации о пользователе (метод DELETE).
@app.delete('/user/{id}')
async def delete_user(id_: int):
    for user in users:
        if user.id == id_:
            users.remove(user)
            return users
    raise HTTPException(status_code=404, detail='User not found')
