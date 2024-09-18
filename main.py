from testapi.testapi import init_app
from aiohttp.web import run_app


class StartApp:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8080

    def run(self):
        try:
            app = init_app()
            print('Успешный запуск')
            run_app(app, host=self.host, port=self.port)
        except Exception as ex:
            print(ex)
if __name__ == '__main__':
    StartApp().run()