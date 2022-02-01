from fastapi import FastAPI, UploadFile, Request, Response, status, HTTPException
from uvicorn import run
from os.path import splitext
from transform.parser import Parser
from datetime import datetime
from cli.command import __version__
from secure import Server, ContentSecurityPolicy, StrictTransportSecurity, \
    ReferrerPolicy, PermissionsPolicy, CacheControl, Secure
from logging import getLogger
from pathlib import Path
from api.custom_logging import CustomizeLogger


server = Server().set("Secure")

csp = (
    ContentSecurityPolicy()
    .default_src("'none'")
    .base_uri("'self'")
    .connect_src("'self'" "api.spam.com")
    .frame_src("'none'")
    .img_src("'self'", "static.spam.com")
)

hsts = StrictTransportSecurity().include_subdomains().preload().max_age(2592000)

referrer = ReferrerPolicy().no_referrer()

permissions_value = (
    PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
)

cache_value = CacheControl().must_revalidate()

secure_headers = Secure(
    server=server,
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    permissions=permissions_value,
    cache=cache_value,
)


initial_uptime = datetime.min


logger = getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='IoTAgent-Turtle', debug=False)
    config_path = Path(__file__).with_name("logging_config.json")
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


application = create_app()


@application.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


@application.get("/version", status_code=status.HTTP_200_OK)
def version(request: Request):
    request.app.logger.info("Request version information")
    data = {
        "doc": "...",
        "git_hash": "nogitversion",
        "iotagent-turtle version": __version__,
        "release_date": "no released",
        "uptime": get_uptime()
    }

    return data


@application.post("/parse", status_code=status.HTTP_201_CREATED)
async def parse(request: Request, file: UploadFile, response: Response):
    request.app.logger.info(f'Request parse file "{file.filename}"')

    # check if the post request has the file part
    if splitext(file.filename)[1] != '.ttl':
        resp = {'message': 'Allowed file type is only ttl'}
        response.status_code = status.HTTP_400_BAD_REQUEST
        request.app.logger.error(f'POST /parse 400 Bad Request, file: "{file.filename}"')
    else:
        # Start parsing the file
        myparser = Parser()

        try:
            content = await file.read()
        except Exception as e:
            request.app.logger.error(f'POST /parse 500 Problem reading file: "{file.filename}"')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        else:
            request.app.logger.info(f'File readed')


        try:
            myparser.parsing(content=content.decode("utf-8"))
        except Exception as e:
            request.app.logger.error(f'POST /parse 500 Problem parsing file: "{file.filename}"')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        else:
            request.app.logger.info(f'File successfully parsed')

        # Send the data to a FIWARE Context Broker instance

        resp = {'message': 'File successfully sent'}

    return resp


def get_uptime():
        now = datetime.now()
        delta = now - initial_uptime

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


def launch(app: str = "server:application", port: int = 5000, uptime: datetime = datetime.utcnow()):
    global initial_uptime

    initial_uptime = uptime

    run(app=app, host="127.0.0.1", port=port, log_level="info", reload=True, server_header=False)


if __name__ == "__main__":
    launch()
