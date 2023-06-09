import logging
import os
from functools import wraps
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

X_API_KEY = os.getenv("X_API_KEY", "MYAPIKEY")


class ServiceNotReadyException(Exception):
    ...


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if kws["header"] != X_API_KEY:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail='wrong app key',
                                headers={"WWW-Authenticate": "Bearer"})

        return f(*args, **kws)

    return decorated_function


def handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        try:
            resp = f(*args, **kws)
            return resp
        except ServiceNotReadyException:
            raise HTTPException(status_code=422,
                                detail=f"Prediction Service is not instantiated. Please use endpoint "
                                       f"PUT  /prediction-server/model/<model_name> "
                                       f"to instantiate it with a prediction model.")
        except FileNotFoundError as e:
            raise HTTPException(status_code=404,
                                detail=str(e))
        except Exception as ex:
            logging.error(str(ex))
            raise HTTPException(status_code=500,
                                detail=str(ex))

    return decorated_function
