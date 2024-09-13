import os
import sys
from asyncpg import create_pool
from auth import *
from .views.user import *

# Читаем переменные из файла auto.py
sys.path.append(os.path.dirname(os.path.abspath('auth.py')))


# Создаем пул соединений с базой данных PostgreSQL
async def init_app():
    # Создаем пул соединений с базой данных
    pool = await create_pool(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)

    app = web.Application()
    app['db'] = pool
    app.router.add_post('/users', create_user)
    app.router.add_get('/users/{id}', get_user)
    app.router.add_get('/users', get_users)
    app.router.add_put('/users/{id}', update_user)
    app.router.add_get('/user_count', get_user_count)
    app.router.add_get('/users_filtered', get_users_filtered)
    return app