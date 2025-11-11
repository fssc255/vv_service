## 环境信息

Python 版本: 3.13.9
依赖第三方包：见 [requirements.txt](./requirements.txt)

## 项目结构

**目录结构说明**

| 目录名 | 说明                                                    |
| ------ | ------------------------------------------------------- |
| errors | 异常类                                                  |
| models | 关系型数据库（MySql）中的数据模型定义                   |
| utils  | 工具类                                                  |
| my_va  | [IVideoAnalyzer.py](./src/IVideoAnalyzer.py) 的实现样例 |

**关键文件说明**

| 文件名                                       | 说明                     |
| -------------------------------------------- | ------------------------ |
| [\_\_main\_\_.py](./src/__main__.py)         | 程序入口                 |
| [IVideoAnalyzer.py](./src/IVideoAnalyzer.py) | 进行相似度匹配的算法接口 |
| [Config.py](./src/Config.py)                 | 程序配置信息             |

**工具类（utils）说明**

| 文件                                                   | 说明                              |
| ------------------------------------------------------ | --------------------------------- |
| [DbAccessor.py](./src/utils/DbAccessor.py)             | 访问关系型数据库（MySql）中的数据 |
| [Logger.py](./src/utils/Logger.py)                     | 用于打印日志信息                  |
| [KeyframesSampler.py](./src/utils/KeyframesSampler.py) | 用于对视频文件中进行帧采样        |

## 命名规则

1. 目录名使用 snake_case
2. 文件名以主类名命名，使用 PascalCase
3. 以\*\_example 结尾的文件名表示对应类的使用示例
