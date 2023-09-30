from typing import List

from fastapi import APIRouter, Depends
from src.todos.dao import TodosDAO
from src.todos.schemas import Todos
from src.users.models import Users

router = APIRouter(
    prefix='/todos',
    tags=['Дела'], # Название этого роутера для объединения роутеров в группу в документации
)



@router.post('/add') # Эндпоинт на добавление дел
async def add_todo(todo_data: Todos):

    await TodosDAO.add(
                       owner=todo_data.owner,
                       text=todo_data.text,
                       date_start=todo_data.date_start,
                       date_stop=todo_data.date_stop,
                       )
    return {'message': 'success'}

@router.get('/my_todos')
async def my_td(current_user: Users= Depends(ger_current_user)):
    td = await TodosDAO.find_all(owner=current_user.id)
    return td


@router.delete('/delete_todos')
async def del_td(task_id: List[int], current_user: Users = Depends(get_current_user)):
    result = await TodosDAO.find_all(owner=current_user.id, id=task_id)
    if not result:
        return {'delete': 'false'}
    await TodosDAO.delete(owner=current_user.id, id=task.id)
    return result


