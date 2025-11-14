## 环境信息

见 [pyproject.toml](./src/pyproject.toml)

## 运行方法

**1.安装 uv**

```bash
pip install uv # 或者用其他方法
```

**2.运行**

执行脚本

```bash
./start-service.sh
```

初次运行涉及到依赖下载与模型下载，请稍作等候

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

### （2）添加视频

**REQUEST**

| 属性     | 值                                  |
| -------- | ----------------------------------- |
| Endpoint | http://127.0.0.1:6590/api/va/videos |
| Method   | POST                                |

```json
{
    "videoId": "f2fafaow",
    "videoFilePath": "/full/qualified/path/to/video/file.mp4"
}
```

| 参数          | 说明                           |
| ------------- | ------------------------------ |
| videoId       | 视频 id                        |
| videoFilePath | 视频文件上传到本地后的完整路径 |

Curl 请求示例

```bash
curl -X POST http://127.0.0.1:6590/api/va/videos \
  -H "Content-Type: application/json" \
  -d '{
    "videoId": "f2fafaow",
    "videoFilePath": "/full/qualified/path/to/video/file.mp4"
  }' \
  -w "\n响应状态码: %{http_code}\n"
```

**RESPONSE**

```json
{
    "success": true,
    "message": "",
    "data": {
        "id": -1,
        "videoId": "",
        "width": 1920,
        "height": 1080,
        "fps": 30.0,
        "duration": 120,
        "fileType": "mp4",
        "fileSize": 10485760,
        "createTime": 1698765432,
        "modifyTime": 1698765432,
        "md5": "5d41402abc4b2a76b9719d911017c592"
    }
}
```

| 字段       | 类型          | 说明                                              |
| ---------- | ------------- | ------------------------------------------------- |
| id         | int           | 记录 id，总是为-1                                 |
| videoId    | str           | 视频的 Id，总是为请求参数中的 videoId             |
| width      | int \| null   | 视频画面宽度                                      |
| height     | int \| null   | 视频画面高度                                      |
| fps        | float \| null | 视频帧率                                          |
| duration   | int \| null   | 视频时长，单位秒                                  |
| fileType   | string        | 视频文件类型，确保全小写                          |
| fileSize   | int           | 视频文件大小，单位为字节                          |
| createTime | int           | 视频文件的创建时间，unix 时间戳（秒单位，秒精度） |
| modifyTime | int           | 视频文件的修改时间，unix 时间戳（秒单位，秒精度） |
| md5        | string        | 视频文件的 md5，全小写                            |

### （3）删除视频

**REQUEST**

| 属性     | 值                                            |
| -------- | --------------------------------------------- |
| Endpoint | http://127.0.0.1:6590/api/va/videos/{videoId} |
| Method   | DELETE                                        |

路径参数

| 参数名  | 范围          | 说明                  | 示例                                          |
| ------- | ------------- | --------------------- | --------------------------------------------- |
| videoId | 有效的视频 Id | 指明要删除的视频的 Id | http://127.0.0.1:6590/api/va/videos/abc114514 |

Curl 请求示例

```bash
curl -X DELETE http://127.0.0.1:6590/api/va/videos/abc114514 \
  -w "\n响应状态码: %{http_code}\n"
```

**RESPONSE**

```json
{
    "success": true,
    "message": ""
}
```

## 项目结构

**目录结构说明**

| 目录名   | 说明                                                    |
| -------- | ------------------------------------------------------- |
| errors   | 异常类                                                  |
| models   | 关系型数据库（MySql）中的数据模型定义                   |
| utils    | 工具类                                                  |
| storages | 持久化相关类                                            |
| my_va    | [IVideoAnalyzer.py](./src/IVideoAnalyzer.py) 的实现样例 |

**关键文件说明**

| 文件名                               | 说明         |
| ------------------------------------ | ------------ |
| [\_\_main\_\_.py](./src/__main__.py) | 程序入口     |
| [VAService.py](./src/VAService.py)   | 功能汇聚点   |
| [Config.py](./src/Config.py)         | 程序配置信息 |

**工具类（utils）说明**

| 文件                                                   | 说明                       |
| ------------------------------------------------------ | -------------------------- |
| [Logger.py](./src/utils/Logger.py)                     | 用于打印日志信息           |
| [KeyframesSampler.py](./src/utils/KeyframesSampler.py) | 用于对视频文件中进行帧采样 |

**存储类（storages）说明**

| 文件                                                      | 说明                              |
| --------------------------------------------------------- | --------------------------------- |
| [DbAccessor.py](./src/storages/DbAccessor.py)             | 访问关系型数据库（MySql）中的数据 |
| [VectorDbAccessor.py](./src/storages/VectorDbAccessor.py) | 访问向量数据库中的数据            |

## 命名规则

1. 目录名使用 snake_case
2. 文件名以主类名命名，使用 PascalCase
3. 以\*\_example.py 结尾的文件名表示对应类的使用示例
