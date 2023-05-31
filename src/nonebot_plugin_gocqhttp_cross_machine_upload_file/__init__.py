from os import PathLike
from typing import Union, AsyncIterable, Iterator

from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event

from .config import conf
from .errors import UnsupportedDriverError

try:
    from .file_manager import put_file, del_file

    init_failed = False
except UnsupportedDriverError as e:
    logger.error(e)
    put_file = None
    del_file = None
    init_failed = True


async def upload_file(bot: Bot, event: Event, filename: str,
                      data: Union[None, bytes, str,
                                  AsyncIterable[Union[str, bytes]],
                                  Iterator[Union[str, bytes]]] = None,
                      path: Union[None, str, PathLike[str]] = None):
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)

    if group_id is not None:
        await upload_group_file(bot, group_id, filename, data, path)
    elif user_id is not None:
        await upload_private_file(bot, user_id, filename, data, path)
    else:
        raise TypeError(event)


async def upload_group_file(bot: Bot, group_id: int, filename: str,
                            data: Union[None, bytes, str,
                                        AsyncIterable[Union[str, bytes]],
                                        Iterator[Union[str, bytes]]] = None,
                            path: Union[None, str, PathLike[str]] = None):
    if init_failed:
        raise UnsupportedDriverError()

    file_id = put_file(data, path)

    download_result = await bot.download_file(
        url=f"http://{conf.callback_host}:{conf.callback_port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_group_file(group_id=group_id,
                                file=download_result["file"],
                                name=filename)

    del_file(file_id)


async def upload_private_file(bot: Bot, user_id: int, filename: str,
                              data: Union[None, bytes, str,
                                          AsyncIterable[Union[str, bytes]],
                                          Iterator[Union[str, bytes]]] = None,
                              path: Union[None, str, PathLike[str]] = None):
    if init_failed:
        raise UnsupportedDriverError()

    file_id = put_file(data, path)

    download_result = await bot.download_file(
        url=f"http://{conf.callback_host}:{conf.callback_port}/file_center/{file_id}",
        thread_count=1
    )

    await bot.upload_private_file(user_id=user_id,
                                  file=download_result["file"],
                                  name=filename)

    del_file(file_id)
