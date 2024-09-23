from aiohttp import web
import pandas as pd
import logging
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_user(request):
    """
    Функция для создания пользователя и записи его в базу данных
    """
    try:
        logger.info("Получен запрос на создание нового пользователя")
        data = await request.json()
        logger.info(f"Получены данные: {data}")
        async with request.app['db'].acquire() as connection:
            await connection.execute("""
                INSERT INTO public.users (first_name, last_name, phone_number, age)
                VALUES ($1, $2, $3, $4)
                """, data['first_name'], data['last_name'], data['phone_number'], data['age'])
            logger.info(f"Пользователь {data['first_name']} {data['last_name']} успешно записан в базу данных")
        return web.Response(body=json.dumps({"success": "Пользователь успешно зарегистрирован"}), status=201)
    except Exception as e:
        logger.error(e)
        return web.Response(
            body=json.dumps({"error": e}), status=400)


async def get_user(request):
    """
    Функция для получения id пользователя по запросу
    """
    try:
        logger.info('Получен запрос на получение пользователя из базы данных')
        user_id = int(request.match_info['id'])
        logger.info(f'Получен id: {user_id}')
        async with request.app['db'].acquire() as connection:
            user = await connection.fetchrow('SELECT * FROM public.users WHERE id = $1', user_id)
        if user is not None:
            logger.info(f"Найден пользователь под номером {user['id']}: {user['first_name']} {user['last_name']}")
            return web.json_response(dict(user), status=200)
        else:
            logger.warning(f"Пользователь под номером {user_id} не найден")
            return web.json_response({"warning": "Пользователь не найден"}, status=404)
    except Exception as e:
        logger.error(e)
        return web.Response(body=json.dumps({"error": e}), status=400)


async def get_users(request):
    """
    Функция для получения списка пользователей в удобном формате, json или excel
    С дополнительной необязательной фильтрацией по столбцу first_name
    """
    format_type = request.rel_url.query.get('format', 'json')
    first_name = request.rel_url.query.get('first_name', None)

    try:
        async with request.app['db'].acquire() as conn:
            if first_name:
                users = await conn.fetch('SELECT * FROM public.users WHERE first_name ILIKE $1', f'%{first_name}%')
            else:
                users = await conn.fetch('SELECT * FROM public.users')

        users_list = [dict(user) for user in users]

        if format_type == 'excel':
            df = pd.DataFrame(users_list)
            file_path = 'users_filtered.xlsx' if first_name else 'users.xlsx'
            df.to_excel(file_path, index=False)

            logger.info(f"Excel файл {file_path} успешно создан и отправлен.")

            return web.FileResponse(file_path, status=200)

        return web.json_response(users_list, status=200)

    except Exception as e:
        logger.error(f"Ошибка при получении списка пользователей: {str(e)}")
        return web.Response(body=json.dumps({"error": "Ошибка при получении данных пользователей"}), status=400)


async def update_user(request):
    """
    Функция для обновления данных пользователя по его id в базе данных
    """
    try:
        logger.info('Получен запрос на обновление данных пользователя по его id в базе данных')
        user_id = int(request.match_info['id'])
        logger.info(f'Получен id: {user_id}')
        data = await request.json()
        logger.info(f'')
        async with request.app['db'].acquire() as connection:
            await connection.execute("""
                UPDATE public.users
                SET first_name = $1, last_name = $2, phone_number = $3, age = $4
                WHERE id = $5
            """, data['first_name'], data['last_name'], data['phone_number'], data['age'], user_id)
        return web.Response(body=json.dumps({"success": "Данные успешно обновлены"}), status=200)
    except Exception as e:
        logger.error(e)
        return web.Response(body=json.dumps({"error": e}), status=400)

async def get_user_count(request):
    """
    Функция для получения количества пользователей в таблице
    """
    logger.info("Получен запрос на получение количества пользователей в таблице")
    async with request.app['db'].acquire() as connection:
        count = await connection.fetchval('SELECT COUNT(*) FROM public.users')
    logger.info(f"Ответ по количеству пользователей отправлен и составил {count}")
    return web.json_response({'count': count}, status=200)