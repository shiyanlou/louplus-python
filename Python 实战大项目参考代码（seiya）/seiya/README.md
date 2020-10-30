# Seiya 数据分析系统

> 本项目是 [实验楼](https://www.shiyanlou.com/) 课程 [楼+ 之 Python 实战](https://www.shiyanlou.com/louplus/python) 的实战项目之一，仅供学习和研究使用。如有转载，请注明出处。

Seiya 数据分析系统可用于分析热门互联网网站的数据，比如拉勾网职位数据、链家网租房数据和点评网餐馆数据等。当前支持拉勾网职位数据分析，其它待实现。对于每类数据，首先通过爬虫抓取回数据并存放到数据库表中，然后通过 SQL 查询或者 Pandas 进行数据分析，最后将分析得到的结果采用图表形式展示出来。图表采用 Antv G2 在前端生成，或者使用 Matplotlib 在服务端生成。

## 项目目录结构

Seiya 系统包含 `spider`、`analysis` 和 `web` 三个子系统，另外公共的数据库访问抽取到了 `db` 包里。每个子系统下，不同类别的数据分析代码分开到不同的模块文件里。

```text
.
├── scrapy.cfg // Scrapy 配置文件
└── seiya // 项目顶级包目录
    ├── __init__.py
    ├── analysis // 分析子系统
    │   ├── __init__.py
    │   ├── house.py
    │   ├── job.py
    │   └── restaurant.py
    ├── db // 公共的数据库访问层
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── base.py
    │   ├── house.py
    │   ├── job.py
    │   └── restaurant.py
    ├── spider  // 爬虫子系统
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       ├── houses.py
    │       ├── jobs.py
    │       └── restaurants.py
    └── web // web 子系统
        ├── __init__.py
        ├── app.py // 应用入口，以及路由定义
        ├── static // 静态资源文件，包括 JS、CSS 等
        └── templates // 页面模板
            ├── 404.html
            ├── base.html
            ├── house
            ├── index.html
            ├── job
            └── restaurant
```

## 准备数据库

Seiya 使用 SQLAlchemy 来访问 MySQL 数据库，默认地址为 `mysql://root@localhost:3306/seiya?charset=utf8`。如有不同，可修改 Python 模块文件 `seiya.db.base`。

## 创建 Python 虚拟环境

为了防止跟其它项目出现依赖包版本冲突，可为项目创建一个独立的 Python 3 虚拟环境。创建好虚拟环境后，激活虚拟环境并安装项目依赖包。

```bash
python -m venv seiya
cd seiya && source bin/activate
pip install scrapy mysqlclient sqlalchemy numpy pandas matplotlib flask
```

最后拷贝或克隆项目代码到该虚拟环境目录下。

## 爬取数据

在项目根目录下执行以下命令来爬取数据（jobs 为爬虫名称）：

```bash
scrapy crawl jobs
```

## 运行 Web 服务

在项目根目录下执行以下命令来以开发模式启动 web 服务：

```bash
$ FLASK_APP=seiya/web/app.py FLASK_ENV=development python -m flask run
 * Serving Flask app "seiya/web/app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 122-599-353

```

## 分析结果截图

系统首页：

![系统首页](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1535702446126.png/wm)

拉勾网职位数据分析首页：

![拉勾网职位数据分析首页](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1535702446359.png/wm)

职位数排名前十的城市：

![职位数排名前十的城市](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1535956636180.png/wm)

薪资排名前十的城市：

![薪资排名前十的城市](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1535956636579.png/wm)

热门职位标签页面：

![热门职位标签页面](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1535961267882.png/wm)

工作经验统计：

![工作经验统计](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1536200391432.png/wm)

学历要求统计：

![学历要求统计](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1536200391916.png/wm)

同等学历不同城市薪资对比：

![同等学历不同城市薪资对比](https://doc.shiyanlou.com/document-uid606277labid6277timestamp1536201664855.png/wm)
