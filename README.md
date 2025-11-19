## 环境信息

见 [pyproject.toml](./src/pyproject.toml)

## 运行方法

**1.安装 uv**

```bash
pip install uv # 或者用其他方法
```

**2.运行**

（1）通过执行启动脚本直接运行

Linux

```bash
./start-service.sh
```

Windows

```bash
start-service.bat
```

初次运行涉及到依赖下载与模型下载，请稍作等候

若要终止，使用`Ctrl + C`

（2）使用 docker compose

```bash
docker compose up
```

## API 定义

### （1）请求执行相似视频查找

**REQUEST**

| 属性     | 值                                          |
| -------- | ------------------------------------------- |
| Endpoint | http://127.0.0.1:6590/api/va/similar-videos |
| Method   | GET                                         |

查询参数

| 参数      | 必需 | 范围  | 说明                                                            | 示例                                                       |
| --------- | ---- | ----- | --------------------------------------------------------------- | ---------------------------------------------------------- |
| threshold | 否   | [0,1] | 指定两个视频应达到什么样的相似度才会被视为“相似”，默认值为 0.95 | http://127.0.0.1:6590/api/va/similar-videos?threshold=0.95 |

Curl 请求示例

```bash
curl -X GET http://127.0.0.1:6590/api/va/similar-videos \
    -w "\n响应状态码: %{http_code}\n"
```

**RESPONSE**

```json
{
    "success": true,
    "message": "",
    "data": [
        {
            "referenceVideo": "aow05202",
            "similarVideos": {
                "0x0fa9ax": 0.92,
                "ab90s9fa": 0.85,
                "aof09sa0": 0.95
            }
        },
        {
            "referenceVideo": "f2fafaow",
            "similarVideos": {
                "jfoeia9e": 0.85,
                "ojfs9909": 0.95
            }
        }
    ]
}
```

data 为一个数组，表示相似的视频组，该值保证不为 null，至多为空数组

| 字段           | 类型        | 说明                                                                |
| -------------- | ----------- | ------------------------------------------------------------------- |
| referenceVideo | str         | 参考视频的 id                                                       |
| similarVideos  | {str:float} | 一个视频 id -> 相似度的字典，表示对应视频和 referenceVideo 的相似度 |
