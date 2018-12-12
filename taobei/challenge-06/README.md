# 挑战解析

## 启动说明

### 启动 Redis 服务

在默认端口 6379 上启动 Redis 服务，如果使用不同端口，请对应修改配置文件里的 Redis 连接地址。

### 添加推荐数据

使用 Redis 客户端工具 `redis-cli` 连接上 Redis 服务，然后使用 `rpush` 命令分别往 Key `recommend.products` 和  `recommend.shops` 里写入被推荐的商品和店铺 ID 。

### 启动应用服务

执行 `supervisord` 命令来启动所有服务，然后访问 `http://localhost:5050/` 即可查看首页推荐内容。
