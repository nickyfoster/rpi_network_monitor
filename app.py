import subprocess
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


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
        res = subprocess.check_output(['speedtest', '--format=json']).decode()
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
