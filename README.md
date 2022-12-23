nonebot-plugin-gocqhttp-cross-machine-upload-file
========

为go-cqhttp与nonebot部署于不同机器的系统提供上传群文件、私聊文件的能力。

## 配置

### callback_host

回调HOST，设置为nonebot所在的主机名/IP。务必保证go-cqhttp所在主机可访问，用于让go-cqhttp下载本机文件。

默认值：127.0.0.1

### callback_port

回调端口，保持默认值即可。

默认值：与PORT保持一致即可