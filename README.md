
ip代理池：proxy_pool-master
=======

### 启动:

```
程序分为: schedule 调度程序 和 webserver Api服务

# 进入proxy_pool-master的cli目录
# 首先启动调度程序
>>>python proxyPool.py schedule

# 然后启动webApi服务
>>>python proxyPool.py webserver

```

# 若使用Redis：
## 下载Redis
* [下载地址](https://blog.csdn.net/liangxw1/article/details/82864581)
## 下载RedisDesktopManager
* [下载地址](https://www.cnblogs.com/zlslch/p/8563627.html)




# 若使用SSDB：
## SSDB数据库：ssdb-bin-master
### 启动
```
* 1.进入ssdb-bin-master目录
* 2.ssdb-server-1.9.4.exe ssdb.conf
```

## SSDB可视化工具：SSDBAdmin-master
```
* 1.进入SSDBAdmin-master目录
* 2.python run.py
```


