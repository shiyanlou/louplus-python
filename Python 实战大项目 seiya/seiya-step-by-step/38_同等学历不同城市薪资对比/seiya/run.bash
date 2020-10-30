python3 -m seiya.db                         # 创建数据表
scrapy crawl jobs -s LOG_LEVEL='WARNING'    # 爬取数据
export FLASK_DEBUG=1 FLASK_APP=manage.py FLASK_ENV='development'  # 设置环境变量
