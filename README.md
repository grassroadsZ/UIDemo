# Python3 + Pytest +selenium + allure

本地运行
 ```shell script
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt
python run_local.py
```
## 真实数据地址已被替换，项目无法运行，仅提供参考思路

每个Case可独立运行，case运行前先将参数化需要用到的动态数据生成保存至yaml文件,case运行前数据从yaml文件中加载读取，解决使用pytest-xdist
进行多进程同时运行时各个进程加载到的数据不一致导致多进程运行失败的问题。前置依赖数据使用接口进行生成

由于web中无windows系统自带弹窗的场景，将case放在linux服务器的docker容器中运行，减少本地电脑的占用

case运行结束后使用多线程查询case运行后产生的有特定名称的数据，使用for循环进行删除(此处多线程进行删除处理过于麻烦，且多线程查询数据时也需要优化)，
由于接口未遵循restful风格，目前想到的只能一个接口一个方法。


allure 报告需本地安装allure

# 部署


## java安装

```shell
yum install java
```

## Maven安装

```shell
wget http://mirrors.hust.edu.cn/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz

tar -xvf  apache-maven-3.3.9-bin.tar.gz

sudo mv -f apache-maven-3.3.9 /usr/local/

sudo vim /etc/profile
# 添加到最后两行
export MAVEN_HOME=/usr/local/apache-maven-3.3.9
export PATH=${PATH}:${MAVEN_HOME}/bin

source /etc/profile
mvn -v
```

## Jenkins安装

```shell
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo

sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

yum install jenkins -y
```

修改端口(未被占用可不修改)

```shell
vi /etc/sysconfig/jenkins
:/PORT
# 改为其它未被占用的端口8088

sudo systemctl daemon-reload
```

启动停止重启

```shell
service jenkins start/stop/restart
```

查看安装密码

```shell
cat /var/lib/jenkins/secrets/initialAdminPassword
```

修改jenkins执行命令的用户

```shell
vim /etc/sysconfig/jenkins
# 将$JENKINS_USER="jenkins"修改为$JENKINS_USER="root"

# 修改目录权限
chown -R root:root /var/lib/jenkins
chown -R root:root /var/cache/jenkins
chown -R root:root /var/log/jenkins

# 将jenkins加入docker 的用户组

sudo gpasswd -a jenkins docker && sudo service jenkins restart 
```

修改docker 运行容器的host地址

```shell
vi /etc/hosts
#添加如下无域名要求忽略这步
1.2.3.4 www.baidu.com
```


安装jenkins的allure插件

![](https://gitee.com/grassroadsZ/MarkDownImage/raw/master/img/20200320114906.png)
UI项目jenkins配置参考

![](https://gitee.com/grassroadsZ/MarkDownImage/raw/master/img/20200320110232.png)



![](https://gitee.com/grassroadsZ/MarkDownImage/raw/master/img/20200320110318.png)



![](https://gitee.com/grassroadsZ/MarkDownImage/raw/master/img/20200320110445.png)



## 必要条件

虚拟环境命令

```shell
yum install python3
python3 -m venv 路径/虚拟环境名

docker pull elgalu/selenium

docker pull dosel/zalenium
```






## 注意

关于jenkins 相关的配置请尽量原封不动，否则会遇到如下问题

- jenkins无法启动docker容器的问题（通过将jenkins加docker组，实际改成root这步可以忽略）

- jenkins的执行用户尽量改成root，否则pip依赖包时可能加sudo依然会存在无权限无法安装依赖包
- 建议jenkins中在tarsUI的工程上加一个stop selenium的docker容器命令在TarsUI项目构建完成后再进行容器停止



[selenium docker 容器启动参数参考](https://opensource.zalando.com/zalenium/#faq)


