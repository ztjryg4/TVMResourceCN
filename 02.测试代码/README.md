# 测试代码  

## 杂项及说明  
1. 部分测试代码源自TVM官方Tutorial，部分经过更改以满足测试需求。  
2. 部分测试代码中的required file下载部分已被注释，改为本地地址。  
3. 移步“相关”一栏中给出的链接，可以看到有关测试代码更详细的实现细节和解读。  

## 内容  
### 在TVM上部署TensorFlow模型  
**链接：**[Codes/TensorFlow](Codes/TensorFlow)  
**说明：**  
`from_tensorflow.py` TensorFlow测试代码  
**相关：**  
英文Introduction（官方）：[Compile Tensorflow Models](https://docs.tvm.ai/tutorials/frontend/from_tensorflow.html#sphx-glr-tutorials-frontend-from-tensorflow-py)  
中文Blog（章天杰）：[TVM部署TensorFlow模型](http://imztj.cn/?p=3020)  

### TVM上的YOLO-Darknet单图、多图测试  
**链接：**[Codes/YOLO-Darknet](Codes/YOLO-Darknet)  
**说明：**  
`single_from_darknet.py` YOLO-Darknet单图测试代码  
`from_darknet_multi.py` YOLO-Darknet多图测试代码  
`*.jpg`测试用图片  
`darknet_single` Darknet目录（用于单图测试）  
`darknet` Darknet目录（经过更改，用于多图测试）  
`filelist.txt`多图测试文件列表  
**相关：**  
英文Introduction（官方）：[Compile YOLO-V2 and YOLO-V3 in DarkNet Models](https://docs.tvm.ai/tutorials/frontend/from_darknet.html)  
单图测试中文Blog（章天杰）：[TVM上部署YOLO-DarkNet及单图性能对比](http://imztj.cn/?p=3023)  
多图测试中文Blog（章天杰）：[TVM上YOLO-DarkNet多图性能对比](http://imztj.cn/?p=3041)  

## TVM与mssd-GlounCV测试  
**链接：**[Codes/mssd-glouncv](Codes/mssd-glouncv)  
**说明：**  
`demo_ssd.py`GlounCV上直接跑mssd  
`deploy_ssd_gluoncv.py` TVM上跑单图测试  
`deploy_ssd_gluoncv_multi.py` TVM上跑多图测试  