from fastapi import FastAPI, UploadFile, File
from uvicorn import run
from os.path import splitext
from json import dumps
from transform.parser import Parser
from datetime import datetime
from cli.command import __version__
import secure

'''
script-src 'strict-dynamic' 'nonce-rAnd0m123' 'unsafe-inline' http: https:;
object-src 'none';
base-uri 'none';
require-trusted-types-for 'script';
report-uri https://csp.example.com;
'''
server = secure.Server().set("Secure")

csp = (
    secure.ContentSecurityPolicy()
    .default_src("'none'")
    .base_uri("'self'")
    .connect_src("'self'" "api.spam.com")
    .frame_src("'none'")
    .img_src("'self'", "static.spam.com")
)

hsts = secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000)

referrer = secure.ReferrerPolicy().no_referrer()

permissions_value = (
    secure.PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
)

cache_value = secure.CacheControl().must_revalidate()

secure_headers = secure.Secure(
    server=server,
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    permissions=permissions_value,
    cache=cache_value,
)


application = FastAPI()
initial_uptime = datetime.min


@application.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


@application.get("/version")
def version():
    data = {
        "doc": "...",
        "git_hash": "nogitversion",
        "iotagent-turtle version": __version__,
        "release_date": "no released",
        "uptime": get_uptime()
    }

    return data


@application.post("/parse")
async def parse(file: UploadFile = File(...)):
    print("filename = ", file.filename)  # getting filename

    # check if the post request has the file part
    if splitext(file.filename)[1] != '.ttl':
        resp = dumps({'message': 'Allowed file type is only ttl'})
        resp.status_code = 400
    else:
        # Start parsing the file
        myparser = Parser()
        content = await file.read()
        myparser.parsing(content=content)

        resp = dumps({'message': 'File successfully uploaded'})
        resp.status_code = 201

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
    # uvicorn --no-server-header
    run(app=app, host="127.0.0.1", port=port, log_level="info", reload=True, server_header=False)


if __name__ == "__main__":
    launch()
