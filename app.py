import subprocess
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import speedtest

app = FastAPI()

security = HTTPBasic()
st = speedtest.Speedtest()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "nimda")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def speedtest_view(app):
    @app.get("/speedtest")
    def speedtest(_=Depends(get_current_username)):
        download_speed = round(st.download() / 1000000, 3)
        upload_speed = round(st.upload() / 1000000, 3)
        ping = round(st.results.ping, 2)
        res = {"download_speed": download_speed,
               "upload_speed": upload_speed,
               "ping": ping}
        return res

    return speedtest


def health_check_view(app):
    @app.get("/healthCheck")
    def health_check(_=Depends(get_current_username)):
        return "Ok"

    return health_check


def prepare():
    app = FastAPI()
    health_check_view(app=app)
    speedtest_view(app=app)
    return app


APP = prepare()
