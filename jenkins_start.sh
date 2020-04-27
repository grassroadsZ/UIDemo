#!/bin/bash
#Author:grassraodsZ
#description:jenkins启动UI自动化环境脚本

# 第一次使用需要linux服务器存在python3虚拟环境，命令为python3 -m venv 虚拟环境名称

# 激活虚拟环境source 虚拟环境目录/bin/activate
source /home/TarsUI/env/bin/activate

# 查看selenium 的docker容器镜像是否在运行

docker ps|grep TarsUI

if [[ $? -eq 1 ]];
then
  echo "selenium的docker 容器没有启动,正在启动"
  docker run --rm -id --name TarsUI -p 4444:4444  --add-host 'www.tars.test2.com:193.112.207.190'   -v /var/run/docker.sock:/var/run/docker.sock -v /home/TarsUI/selenium/videos:/home/seluser/videos --privileged dosel/zalenium start
else
  echo 'selenium的docker 容器已经启动'
fi
# 删除60分钟前的MP4文件
find /home/TarsUI/selenium/videos/ -name "*.mp4" -type f -mmin +60 -exec rm {} \;

pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt

# 确保docker 容器启动成功
sleep 10

python run.py
