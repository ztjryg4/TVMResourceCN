# 安装Nvidia1070ti驱动
    sudo add-apt-repository ppa:graphics-drivers/ppa  
    sudo apt-get update  
    sudo apt-get install nvidia-390 #此处要根据上面查询到的版本适当更改
    sudo apt-get install mesa-common-dev  
    sudo apt-get install freeglut3-dev
    
    nvidia-smi  #若出现电脑GPU列表，即安装成功

# 服务器备份
    我是先给这个服务器备份了一下，这几天搞了不少小问题出来

## 备份命令：
    sudo -i
    cd /
    tar cvpzf backup.tgz --exclude=/proc --exclude=/lost+found --exclude=/backup.tgz --exclude=/mnt --exclude=/sys --exclude=/media /

## 恢复指令：
    sudo rm -rf /media/磁盘名称/分区名称*

    将备份文件”backup.tgz”拷入该分区； 
    sudo cp -i backup.tgz /media/磁盘名/分区名sdaX

    进入分区并将压缩文件解压缩，参数x是告诉tar程序解压缩备份文件。 
    sudo tar xvpfz backup.tgz

    重新创建那些在备份时被排除在外的目录； 
    sudo mkdir proc lost+found mnt sys media 

# 在Android上的部署
## Requirements：
    JDK、Android NDK、Android设备，LLVM在构建shared library已装

### Gradle的安装  
    
    requires only a Java JDK or JRE version 8 or higher to be installed. To check, run java -version
    java -version
    
#### 要装个sdkman！

    https://sdkman.io/install
    curl -s "https://get.sdkman.io" | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
##### 检查版本
    sdk version
    sdk install gradle 5.5.1


### NDK安装
    我是通过Android Studio来装的

    但AS在Linux x64 上要先安装32位库
    sudo apt-get install lib32z1 lib32ncurses5 lib32bz2-1.0 lib32stdc++6


装好AS后注意安装Android SDK路径 ，在sdk manager那里把NDK也要选中，选好路径

AS网络连接不是很好要下好几次。

#### PATH 导入
    sudo vim /etc/profile
    export PATH=$PATH:/home/s5/android-stuudio/bin
    export PATH=$PATH:/home/s5/Android/SDK/ndk-bundle/
    export ANDROID_HOME=~/Android/Sdk/
##### 刷新
    source /etc/profile
### JDK安装
 TVM目前只支持openjdk8

 换Ubuntu 下切换 JDK 版本

    sudo update-alternatives --config java  

    java -version  

### Maven 3
    sudo apt-get install maven

    mvn --version

    
# 编译安装TVM4J
## jvmkg
    make jvmpkg
    

    Reactor Summary for TVM4J Package - Parent 0.0.1-SNAPSHOT:
    [INFO] 
    [INFO] TVM4J Package - Parent ............................. SUCCESS [  1.510 s]
    [INFO] TVM4J Package - Core ............................... SUCCESS [  3.713 s]
    [INFO] TVM4J Package - Native Parent ...................... SUCCESS [  0.025 s]
    [INFO] TVM4J Package - Native Linux-x86_64 ................ SUCCESS [ 58.494 s]
    [INFO] TVM4J Package - Full Parent ........................ SUCCESS [  0.028 s] 
    [INFO] TVM4J Package - Full Linux-x86_64 .................. SUCCESS [01:47 min]
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS


## jvminstall
    make jvminstall

#### 我前面是用sudo make jvmpkg 导致后面的依赖装到/root/.m2
解决办法：
    sudo cp /root/.m2 /home/s5 -R 
    
    sudo make jvminstall


## 安装RPC App到Android手机
### 换目录 
    cd tvm/app/android_rpc/
    
### PATH设定
    export ANDROID_HOME=~/Android/Sdk/
    export PATH=$PATH:/home/s5/Android/Sdk/ndk-bundle/

### 编译RPC的apk
    gradle clean build or gradle clean build --no-daemon

### 编译完成后 
    find . -name "*.apk" -exec ls -l {} \+
#### 会看到
    ./app/build/outputs/apk/release/app-release-unsigned.apk
## 密钥和签名
#### 你要生成签名，不然不能通过adb安装
    keytool -genkey -keystore /home/s5/tvm/apps/android_rpc/dev_tools/tvmrpc.keystore -alias tvmrpc -keyalg RSA -validity 10000
    
#### 为apk生成签名
    jarsigner -keystore /home/s5/tvm/apps/android_rpc/dev_tools/tvmrpc.keystore \
          -signedjar 
            /home/s5/tvm/apps/android_rpc/dev_tools/../app/build/outputs/apk/release/tvmrpc-release.apk \
            /home/s5/tvm/apps/android_rpc/dev_tools/../app/build/outputs/apk/release/app-release-unsigned.apk 'tvmrpc'

### 通过adb装上去
    adb install -r /home/s5/tvm/apps/android_rpc/dev_tools/../app/build/outputs/apk/release/tvmrpc-release.apk
    
    Success

### Android机上调试RPC 
    python -m tvm.exec.rpc_tracker --port 7030 开放在7030端口
    
### 在TVMRPC上调试
    Address：192.168.xxx.xxx
    Port：7030
    Key：android

### 宿主机上查看RPC连接 
    python -m tvm.exec.query_rpc_tracker --port 7030

    Server List
    ----------------------------
    server-address	key
    ----------------------------
    10.66.79.132:47700	server:android
    ----------------------------

    Queue Status
    -------------------------------
    key       total  free  pending
    -------------------------------
    android   1      1     0      


#### 测试
    tests/android_rpc_test.py

    Run CPU test ...
    



# 编译安装android_deploy示例

### 安装ninja：
    sudo apt install ninja-build

    cd  tvm/apps/android_deploy

### setup env
    export PATH=$PATH:/home/s5/Android/Sdk/ndk-bundle/
    export ANDROID_HOME=~/Android/Sdk/

## 和构建RPC一样构建Deploy
### build
    gradle clean build --no-daemon

#### 出现一个错误
    Execution failed for task ':app:packageDebug'.

开始以为是zip损坏了，后来发现应该是在每次构建执行都要启动一个新JVM

#### 解决办法：在编译目录下创建gradle.properties

    Just create a file called gradle.properties in your root project:
    root
    |--gradle.properties
    |--build.gradle
    |--settings.gradle
    |--app
    |----build.gradle
    Then add inside the file:
    org.gradle.jvmargs=-Xmx2048m

#### 密钥和签名和安装

    find . -name "*.apk" -exec ls -l {} \+

##### 再生成密钥和签名

    jarsigner -keystore /home/s5/tvm/apps/android_deploy/dev_tools/tvmrpc.keystore \
          -signedjar /home/s5/tvm/apps/android_deploy/dev_tools/../app/build/outputs/apk/release/tvmrpc-release.apk \
          /home/s5/tvm/apps/android_deploy/dev_tools/../app/build/outputs/apk/release/app-release-unsigned.apk 'tvmrpc'

##### 再通过adb安装

    adb install -r /home/gemfield/projects/tvm/apps/android_deploy/dev_tools/../app/build/outputs/apk/release/tvmdemo-release.apk