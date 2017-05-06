>   2017-5-5

部署
```docker
docker run --name css -d -p 0.0.0.0:2000:5000 -v /docker/css:/code --link mysql:mysql css:1
```

>   2017-5-6

修复容器时区错误导致，时间显示差8小时
```bash
TZ=Asia/Shanghai
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
date
```
