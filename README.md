从事Zabbix课程教学快两年了，给上千名学生讲解过Zabbix的使用，对于熟练使用Zabbix网页的操作人来说，Zabbix
网页添加监控很简单。但是对于初学者来说，Zabbix网页操作比较繁琐，添加一个主机需要很多步骤，添加完后还要等很长时间才能确定是否能监控上，浪费时间，发现监控不了，又不能很快的排查故障。

# 设计功能
1. Zabbix网页默认添加新的主机只能等待网页变绿（能够监控）或变红（不能监控），浪费时间。本产品第一个功能，主动检查是否能够获取客户端主机名，获取不到数据则检查客户端配置文件。
2. 通过上面的功能获取到主机名，并结合用户填入的其他数据调用Zabbix API添加主机。
3. 通过web管理本平台和Zabbix后台的会话保持。
4. 左侧是控制面板，右侧是具体内容，使用ajax动态加载右侧页面，这样提高页面加载速度，像共用的js/css静态资源就不用重复向服务器建立连接。

# 代码结构

```html
ZyZabbix
	ZyZabbix           核心配置目录
	  |--settings.py   Django主配置文件
	  |--urls.py       url规则
	  |--zabbix_get.py 获取zabbix相关信息
	  |--pyzabbix.py   调用Zabbix API
	  |--zabbix_info.conf   包含Zabbix的账号，密码等信息的配置文件
	  |--zbconfig.py   操作zabbix_info.conf配置文件
	hostmanager        功能实现app
	  |--views.py      业务逻辑处理：首页/添加主机
	statics            静态资源目录
	  |--css           样式
	  |--fonts         字体
	  |--images        图片
	  |--js            引入的js
	templates          网页模板目录
	  |--hostadd.html  添加用户网页
	  |--index.html    首页
	  |--settings.html Zabbix连接配置页面
	manage.py
```

# 安装环境
1. Python3
2. Django 1.10.4
3. 第三方模块requests

# 产品功能展示
1. 主机添加页面

![image](https://github.com/zhangyao8/ZyZabbix/statics/images/hostadd.jpg)

2. 配置管理页面

![image](https://github.com/zhangyao8/ZyZabbix/statics/images/settings.jpg)