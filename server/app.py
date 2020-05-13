import subprocess

from fastapi import FastAPI


def speedtest_view(app):
    @app.get("/speedtest")
    def speedtest():
        res = subprocess.check_output(['speedtest', '--format=json']).decode()
        return res

    return speedtest


def health_check_view(app):
    @app.get("/healthCheck")
    def health_check():
        return "Ok"

    return health_check


def prepare() -> FastAPI:
    app = FastAPI()
    health_check_view(app=app)
    speedtest_view(app=app)
    return app


APP = prepare()
