import time
from os import PathLike
from typing import Union, AsyncIterable, Iterator
from uuid import uuid4

from fastapi import FastAPI, Path
from nonebot import get_app
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, GroupMessageEvent
from starlette.responses import Response, FileResponse, StreamingResponse

from .config import conf

_files = {}

_app: FastAPI = get_app()


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


async def upload_file(bot: Bot, event: MessageEvent, filename: str,
                      data: Union[None, bytes, str,
                                  AsyncIterable[Union[str, bytes]],
                                  Iterator[Union[str, bytes]]] = None,
                      path: Union[None, str, PathLike[str]] = None):
    if isinstance(event, PrivateMessageEvent):
        await upload_private_file(bot, event.user_id, filename, data, path)
    elif isinstance(event, GroupMessageEvent):
        await upload_group_file(bot, event.group_id, filename, data, path)
    else:
        raise TypeError(event)


async def upload_group_file(bot: Bot, group_id: int, filename: str,
                            data: Union[None, bytes, str,
                                        AsyncIterable[Union[str, bytes]],
                                        Iterator[Union[str, bytes]]] = None,
                            path: Union[None, str, PathLike[str]] = None):
    if not data and not path:
        raise ValueError("either data or path must be provided")

    file_id = str(uuid4()).replace('-', '')
    _files[file_id] = (data, path)

    download_result = await bot.download_file(
        url=f"http://{conf.callback_host}:{conf.callback_port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_group_file(group_id=group_id,
                                file=download_result["file"],
                                name=filename)

    del _files[file_id]


async def upload_private_file(bot: Bot, user_id: int, filename: str,
                              data: Union[None, bytes, str,
                                          AsyncIterable[Union[str, bytes]],
                                          Iterator[Union[str, bytes]]] = None,
                              path: Union[None, str, PathLike[str]] = None):
    if not data and not path:
        raise ValueError("either data or path must be provided")

    file_id = str(uuid4()).replace('-', '')
    _files[file_id] = (data, path)

    download_result = await bot.download_file(
        url=f"http://{conf.callback_host}:{conf.callback_port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_private_file(user_id=user_id,
                                  file=download_result["file"],
                                  name=filename)

    del _files[file_id]
