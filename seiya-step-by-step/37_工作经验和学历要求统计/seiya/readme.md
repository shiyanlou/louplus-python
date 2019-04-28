### matplotlib 画图显示中文：

1、安装 SimHei 字体

```
cd /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/ttf
sudo wget https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf
```

2、清除 matplotlib 缓存

```
sudo rm -rf ~/.cache/matplotlib
```
