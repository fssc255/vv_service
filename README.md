## 环境信息

Python 版本: 3.13.9
依赖第三方包：见 [requirements.txt](./requirements.txt)

## 项目结构

**目录结构说明**

| 目录名 | 说明                                                    |
| ------ | ------------------------------------------------------- |
| errors | 异常类定义                                              |
| models | 关系型数据库（MySql）中的数据模型定义                   |
| my_va  | [IVideoAnalyzer.py](./src/IVideoAnalyzer.py) 的实现样例 |

**关键文件说明**

| 文件名                                       | 说明                          |
| -------------------------------------------- | ----------------------------- |
| [\_\_main\_\_.py](./src/__main__.py)         | 程序入口                      |
| [IVideoAnalyzer.py](./src/IVideoAnalyzer.py) | 进行相似度匹配的算法接口      |
| [Config.py](./src/Config.py)                 | 程序配置信息                  |
| [DbAccessor.py](./src/DbAccessor.py)         | 关系型数据库（MySql）的访问器 |
