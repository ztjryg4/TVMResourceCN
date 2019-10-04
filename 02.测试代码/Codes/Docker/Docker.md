# Nvida-docker2
当你在用TVM-GPU时，你要先安装nvida-docker2不然无法安装GPU版本的docker。

    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
        sudo apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)

    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update

    sudo apt-get install -y nvidia-docker2
    sudo pkill -SIGHUP dockerd

但是呢，事情不是那么简单的。我遇了到这个问题

    sudo apt-get install -y nvidia-docker2
    
    The following packages have unmet dependencies:
    nvidia-docker2 : Depends: docker-ce (= 5:18.09.0~3-0~ubuntu-bionic) but 5:18.09.0~3-0~ubuntu-xenial is to be installed or
                                docker-ee (= 5:18.09.0~3-0~ubuntu-bionic) but it is not installable
    E: Unable to correct problems, you have held broken packages.

说是docker-rc没安装，解决办法安装指定版本的docker-rc:

    sudo apt-get install docker-ce = 5：18.09.0~3-0~ubuntu-bionic
    sudo apt-get install -y nvidia-docker2

但这对我并没有用。我查阅资料后发现可能是我需要重启下docker

    sudo systemctl daemon-reload
    sudo systemctl restart docker

但这个常规的方法对我无效了,看来是要清除docker并重新安装：

    sudo apt remove docker-ce
    sudo apt autoremove
    sudo apt-get install docker-ce=5:18.09.0~3-0~ubuntu-bionic
    sudo apt install nvidia-docker2

以上操作结束后，nvidia-docker2成功安装

# Docker

安装上依赖时遇到

    E: Unable to correct problems, you have held broken packages.

可能是网络问题，解决方法:

    sudo apt-get upgrade
    sudo apt-get update

在启动docker时遇到如下状况

    Failed to start docker.service: Unit docker.service is masked.

应该是系统服务的管理问题，解决方法：

    systemctl unmask docker.service
    systemctl unmask docker.socket
    systemctl start docker.service


最开始使用docker来装cuda的，因为从源编译总是遇到莫名其妙的问题，但是安装完后发现并不能从OS调用，遂产生了全部从docker来实现的想法

开始我是在找下载的镜像的地址

    Sudo dockers images

运行即

    docker start d9b100f2f63  ##后面那串数字就是ID

查看docker容器

    docker ps -a

但是很重要一点你退出是直接 Control+D，但其并不保留你的更改操作，你需要新创建个image来保存

    docker commit +ID

而ID通过docker ps -l 找到


# 安装docker上的tvm篇

Clone下来

    git clone --recursive https://github.com/dmlc/tvm 
    ./docker/bash.sh tvmai/demo-cpu    ##gpu版本就换gpu
    apt-get update
    apt-get upgrade
    apt-get install -y python python-dev python-setuptools gcc libtinfo-dev zlib1g-dev vim

然后安装LLVM 
在build文件里修改一下编译tvm。
但你在python3中import tvm失败

这里我们不能像平时一样修改~/.bashrc，解决方法：

    ENV PYTHONPATH=/usr/tvm/python:/usr/tvm/topi/python:/usr/tvm/nnvm/python/:/usr/tvm/vta/python:${PYTHONPATH}

还有一点在github 的问答中作者建议用python3.6但给的image里的是python3.5

重装python3

    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    cd /usr/bin/
    sudo rm python3  
    sudo ln -s python3.6 python3 
    sudo apt-get install python3-pip

但在更新python版本后又出现
    
    Error after upgrading pip: cannot import name 'main'

又要再重装一遍

    python3 -m pip uninstall pip && sudo apt install python3-pip –reinstall

最后我测试几个例子发现存在着

    can‘t import relay

查阅官方社区发现也存在有相同问题，已向问题楼层下提问，等待回复。

>https://discuss.tvm.ai/t/error-docker-tutotial-example-tensorflow/1787

