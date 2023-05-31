from os import PathLike
from typing import Union, AsyncIterable, Iterator
from uuid import uuid4

from fastapi import FastAPI, Path
from nonebot import get_app
from starlette.responses import Response, FileResponse, StreamingResponse

from .errors import UnsupportedDriverError

try:
    _app: FastAPI = get_app()
except AssertionError as e:
    raise UnsupportedDriverError() from e

_files = {}


@_app.get("/file_center/{file_id}")
async def get_file(file_id: str = Path()):
    data = _files.get(file_id, None)
    if data is None:
        return Response(status_code=404)

    data, path = data

    if data is not None:
        if isinstance(data, (bytes, str)):
            return Response(data)
        else:
            return StreamingResponse(data)
    else:
        return FileResponse(path)


def put_file(data: Union[None, bytes, str,
                         AsyncIterable[Union[str, bytes]],
                         Iterator[Union[str, bytes]]] = None,
             path: Union[None, str, PathLike[str]] = None):
    if not data and not path:
        raise ValueError("either data or path must be provided")

    file_id = str(uuid4()).replace('-', '')
    _files[file_id] = (data, path)
    return file_id


def del_file(file_id: str):
    if file_id in _files:
        del _files[file_id]
