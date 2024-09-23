import os
import sys
from asyncpg import create_pool
from auth import *
from .views.user import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sys.path.append(os.path.dirname(os.path.abspath('auth.py')))


async def chek_table_exists(conn, table_name):
    result = await conn.fetchval(
        "SELECT to_regclass($1)", table_name
    )
    return result is not None


async def create_table(pool):
    async with pool.acquire() as conn:
        table_exists = await chek_table_exists(conn, "public.users")
        if table_exists:
            logger.info('Таблица "public.users" существует')
        else:
            with open('deploy/createdb.sql', 'r') as file:
                sql_script = file.read()
            try:
                logger.info('Выполнение SQL-скрипта создания таблицы')
                await conn.execute(sql_script)
                logger.info('Таблица успешно создана')
            except Exception as e:
                logger.error(f'Ошибка при создании таблицы: {e}')

async def init_app():
    """
    Функция создания пула соединений с базой данных
    Создание новой таблицы в базе данных
    """
    try:
        pool = await create_pool(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        logger.info('Успешное подключение к базе данных')
    except Exception as e:
        logger.error(f'Ошибка при подключении к базе данных: {e}')
        return None
    await create_table(pool)
    app = web.Application()
    app['db'] = pool
    app.router.add_post('/users', create_user)
    app.router.add_get('/users/{id}', get_user)
    app.router.add_get('/users', get_users)
    app.router.add_put('/users/{id}', update_user)
    app.router.add_get('/user_count', get_user_count)

    logger.info('Инициализация успешна, приложение готово получать запросы')
    return app