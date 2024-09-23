from testapi.testapi import init_app
from aiohttp.web import run_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StartApp:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8080

    def run(self):
        try:
            logger.info('Запуск сервера')
            app = init_app()
            run_app(app, host=self.host, port=self.port)
        except Exception as ex:
            logger.error(ex)
if __name__ == '__main__':
    StartApp().run()