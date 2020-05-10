# TFlite Benchmark  
   ~~ 和TVM的优化进行对比  ~~

## System：
    Ubuntu18.04

## Require：
JDK,NDK,SDK,bazel,adb

### JDK
    apt-get install openjdk-8-jdk

### SDK,NDK,Platform tools
mkdir ~/Android
cd Android

#### NDK
    wget https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip
    unzip android-ndk-r17c-linux-x86_64.zip
    mkdir Sdk
    mv android-ndk-r17c Sdk/ndk-bundle


If you had read an old Tutorial, install the NDKr14b , C++11 will be wrong.
reference:https://github.com/tensorflow/tensorflow/issues/20830
 
#### SDK tools
    wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
    unzip sdk-tools-linux-4333796.zip 
    mv tools/ Sdk/

#### Platform tools
    wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
    unzip platform-tools-latest-linux.zip 
    mv platform-tools Sdk/

Chinese developer is better to use proxy.


### Bazel

#### install the prerequisites
    sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python

#### Next, download the Bazel binary installer named bazel-<version>-installer-linux-x86_64.sh from the Bazel releases page on GitHub.
    wget https://github.com/bazelbuild/bazel/releases/download/0.24.1/bazel-0.24.1-installer-linux-x86_64.sh


#### run the installer 0.24.1
    chmod +x bazel-0.24.1-installer-linux-x86_64.sh
    ./bazel-0.24.1-installer-linux-x86_64.sh --user

#### setup environment
    export PATH="$PATH:$HOME/bin"

#### Caution
It's better to use 0.24.1，I meet something wrong with the 0.30 version.
If you apt-get install bazel the version will be 0.30

### TFlite benchmark
#### download tensorflow code
    git clone https://github.com/tensorflow/tensorflow.git

#### build benchmark for android
    bazel build -c opt \
        --config=android_arm \
        --cxxopt='--std=c++11' \
        tensorflow/lite/tools/benchmark:benchmark_model


### adb use
#### app_51
if you are not the app_51 user,you may no have the permission to adb push or adb shell.

    adb devices
        
    List of devices attached
    46463b0a	device

use this command to find you ID
    
    lsusb

    Bus 001 Device 007: ID 2717:ff48  
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

My IdProduct is 2717 and it's time to configure the app_51
    
    vim /etc/udev/rules.d/51-android.rules

add 

    SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666"

then

    chmod a+rx /etc/udev/rules.d/51-android.rules
    vim ~/.android/adb_usb.ini

add your IdProduct
    0x2717

restart adb 
    adb kill-server
    adb start-server

check
    adb devices

### Run with adb shell
    adb push bazel-bin/tensorflow/lite/tools/benchmark/benchmark_model /data/local/tmp

    adb shell chmod +x /data/local/tmp/benchmark_model

    adb push mobilenet_v2_1.0_224_quant.tflite /data/local/tmp

    /data/local/tmp/benchmark_model \
        --graph=/data/local/tmp/mobilenet_v1_1.0_224_quant.tflite \
        --num_threads=1

    adb shell taskset f0 /data/local/tmp/benchmark_model \
        --graph=/data/local/tmp/mobilenet_v1_1.0_224_quant.tflite \
        --enable_op_profiling=true


#### Result
 Please see the ternimal.txt