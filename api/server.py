from fastapi import FastAPI, UploadFile, File
import uvicorn
from os.path import splitext
from json import dumps
from transform.parser import Parser
from datetime import datetime
from cli.command import __version__

application = FastAPI()
initial_uptime = datetime.now()


@application.get("/version")
def version():
    data = {
        "doc": "https://fiware-orion.readthedocs.org/en/master/",
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


def run(app: str = "server:application", port: int = 5000, uptime: datetime = datetime.utcnow()):
    initial_uptime = uptime
    uvicorn.run(app=app, host="127.0.0.1", port=port, log_level="info", reload=True)


if __name__ == "__main__":
    run()
