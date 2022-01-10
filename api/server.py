from typing import Optional
from fastapi import FastAPI, UploadFile, File
import uvicorn
import aiofiles
from os.path import splitext
from json import dumps
from transform.parser import Parser


application = FastAPI()


@application.get("/version")
def version():
    return {"Hello": "World"}


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


def run(app: str = "server:application", port: int = 5000):
    uvicorn.run(app=app, host="127.0.0.1", port=port, log_level="info", reload=True)


if __name__ == "__main__":
    run()
