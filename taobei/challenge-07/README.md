# 挑战解析

## 启动说明

### 安装并启动 Etcd 服务

下载并解压预编译好的二进制程序包，然后执行 `etcd` 命令即可启动服务，默认在 2379 端口监听客户端连接请求。

### 创建服务地址目录

为每个服务创建一个目录，该目录下存放该服务的所有节点访问地址。可通过 Etcd Python 客户端来完成。

```bash
$ ipython
Python 3.7.1 (default, Nov  6 2018, 18:46:03)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.1.1 -- An enhanced Interactive Python. Type '?' for help.

In [2]: import etcd

In [3]: client = etcd.Client(port=2379)

In [9]: client.write('/taobei/services/tbbuy', None, dir=True)
Out[9]: <class 'etcd.EtcdResult'>({'action': 'set', 'key': '/taobei/services/tbbuy', 'value': None, 'expiration': None, 'ttl': None, 'modifiedIndex': 215, 'createdIndex': 215, 'newKey': True, 'dir': True, '_children': [], 'etcd_index': 215, 'raft_index': 806})

In [10]: client.write('/taobei/services/tbmall', None, dir=True)
Out[10]: <class 'etcd.EtcdResult'>({'action': 'set', 'key': '/taobei/services/tbmall', 'value': None, 'expiration': None, 'ttl': None, 'modifiedIndex': 216, 'createdIndex': 216, 'newKey': True, 'dir': True, '_children': [], 'etcd_index': 216, 'raft_index': 807})

In [11]: client.write('/taobei/services/tbuser', None, dir=True)
Out[11]: <class 'etcd.EtcdResult'>({'action': 'set', 'key': '/taobei/services/tbuser', 'value': None, 'expiration': None, 'ttl': None, 'modifiedIndex': 217, 'createdIndex': 217, 'newKey': True, 'dir': True, '_children': [], 'etcd_index': 217, 'raft_index': 808})

In [12]: client.write('/taobei/services/tbfile', None, dir=True)
Out[12]: <class 'etcd.EtcdResult'>({'action': 'set', 'key': '/taobei/services/tbfile', 'value': None, 'expiration': None, 'ttl': None, 'modifiedIndex': 218, 'createdIndex': 218, 'newKey': True, 'dir': True, '_children': [], 'etcd_index': 218, 'raft_index': 809})

In [13]:
```

### 启动应用服务

执行 `supervisord` 命令来启动所有服务，然后访问 `http://localhost:5050/` 即可查看首页推荐内容。

此时每个服务有两个节点在同时提供服务，可使用 `supervisorctl` 工具停止掉某个服务的一个节点来确认前台网站是否能正确感知到服务地址变化。
