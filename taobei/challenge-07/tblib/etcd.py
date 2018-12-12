import time

import etcd


def init_etcd_service(app, name):
    host, port = app.config['ETCD_ADDR'].split(':')
    port = int(port)
    client = etcd.Client(host=host, port=port)

    key = '/taobei/services/{}'.format(name)
    value = 'http://{}:{}'.format(
        app.config['LISTENER'][0], app.config['LISTENER'][1])
    while True:
        client.write(key, value, append=True, ttl=5)
        time.sleep(4)


def init_etcd_client(app):
    host, port = app.config['ETCD_ADDR'].split(':')
    port = int(port)
    client = etcd.Client(host=host, port=port)

    key = '/taobei/services'
    while True:
        time.sleep(1)

        try:
            client.read(key, recursive=True, wait=True)
            r = client.read(key, recursive=True, sorted=True)
        except Exception as e:
            print(e)
            continue

        d = {}
        for child in r.children:
            if child.value is None:
                continue

            name = child.key.split('/')[-2].upper()
            if d.get(name) is None:
                d[name] = []

            if child.value not in d[name]:
                d[name].append(child.value)
        print('Current service addresses:')
        print(d)

        for name, addresses in d.items():
            app.config['SERVICE_{}'.format(name)]['addresses'] = addresses
