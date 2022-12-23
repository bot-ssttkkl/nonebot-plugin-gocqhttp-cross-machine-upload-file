nonebot-plugin-gocqhttp-cross-machine-upload-file
========

为go-cqhttp与nonebot部署于不同机器的系统提供上传群文件、私聊文件的能力。

## 用法

```python
from io import StringIO

from nonebot import on_startswith, require
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

require("nonebot_plugin_gocqhttp_cross_machine_upload_file")

from nonebot_plugin_gocqhttp_cross_machine_upload_file import upload_file


@on_startswith("test").handle()
async def handle(bot: Bot, event: MessageEvent):
    # 上传指定路径文件
    await upload_file(bot, event, "image.png", path="image.png")

    # 上传打开的IO流
    with StringIO() as f:
        f.write("Hello World")
        f.seek(0)
        await upload_file(bot, event, "hello.txt", f)

    # 上传bytes
    await upload_file(bot, event, "hello.txt", "Hello World".encode())
```


## 配置

### callback_host

回调HOST，设置为nonebot所在的主机名/IP。务必保证go-cqhttp所在主机可访问，用于让go-cqhttp下载本机文件。

默认值：127.0.0.1

### callback_port

回调端口，保持默认值即可。

默认值：与PORT保持一致即可