# Python数据可视化

嵌入式开发中，数据可视化对于可以直观的显示出数据，ADC滤波又或者是其他数据，目前有一个小应用，电子秤通过RS232接口将重量数据发送至串口,我们需要自己写一个小程序来将数据接收至日志文件进行分析，数据可视化就非常方便

## 1.安装虚拟串口助手并虚拟一对com口

首先使用虚拟串口软件虚拟出一对串口用于调试，我这里虚拟的为 COM1 COM2

- 安装过程见使用声明，安装好后测试下两个串口是否互通

![image-20241126134429333](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126134429333.png)

## 2.编写从机串口程序并验证

编写从机串口程序，接收到指令R, 返回重量的数据，重量数据格式如下： xxxx.xx      整数四位，小数两位

- 见slave程序，start.bat为运行该程序

![image-20241126134650861](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126134650861.png)

运行程序

![image-20241126134805941](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126134805941.png)

打开任意串口助手，连接COM口，发送 ‘R’ ，串口助手中返回重量数据

![image-20241126135045318](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126135045318.png)

## 3.编写主机串口程序并验证

master文件夹下该bat文件为启动master程序，点击后输入 发送R的时间，程序开始将接收的数据加上时间戳写入日志文件

![image-20241126135357571](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126135357571.png)

master程序验证过程，首先确保slave程序开启，启动master程序，下图可以看到每隔1s发送一次R,接收的数据获取到了

![image-20241126140050280](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126140050280.png)

查看日志文件，日志文件放在master->src 目录下，可以看到接收的数据被加上时间戳保存

![image-20241126140320760](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126140320760.png)

## 4.python数据可视化

首先安装python解释器与matplotlib库

安装python解释器   https://www.python.org/downloads/

安装依赖库：打开cmd窗口使用命令行安装

E:/software/python3.13/python.exe -m pip install matplotlib    (其中software/python3.13为python解释器的路径，需依据自己的环境更改)

可视化数据分析，横轴应该为时间，纵轴应该为数据，同时显示的数据应该可以设置显示时间间隔，与在screen显示的时间段

- 横轴时间   
- 纵轴数据
- 时间间隔调整 
- 显示时间段调整  

![image-20241126141521856](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20241126141521856.png)



