

// Aldebaran includes.
#include <alproxies/alvideodeviceproxy.h>   
#include <alvision/alimage.h>   
#include <alvision/alvisiondefinitions.h>  
#include <alproxies\albehaviormanagerproxy.h>
#include <alerror/alerror.h>
#include <alproxies/almotionproxy.h>




#include <opencv\cv.h>
#include <opencv\highgui.h>
#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\core\core.hpp>

# include <math.h>
#include <windows.h>
#include <iostream>
#include <stdlib.h>   
#include <string>


using namespace AL;  
using namespace cv;
using namespace std;

IplImage* img0 ;
IplImage* inputimg = cvCreateImage( cvSize(320,240), 8, 3 );





/*
获取球中心坐标距离图像中心的竖向应该偏转角度 输入参数为球中心坐标的y值  注：应保证图像大小为320*240
*/
float GetHeadPitchRadians(int bally){
	int xzd=bally-120;
	float xzd1=xzd*23.82;
	float xzd2=xzd1/120;
	float Radians=xzd2/180;//头的竖向校准
	return Radians;
}


/*
获取球中心坐标距离图像中心的横向应该偏转角度 输入参数为球中心坐标的x值  注：应保证图像大小为320*240
*/
float GetHeadYawRadians(int ballx){
	int xzd=160-ballx;
	float xzd1=xzd*30.48;
	float xzd2=xzd1/160;
	float Radians=xzd2/180;
	return Radians;
}

/*
获取球中心坐标距离图像中心的横向应该偏转角度 输入参数为球中心坐标的x值  注：应保证图像大小为320*240
*/
float GetBodyRadians(int ballx){
	int xzd=160-ballx;
	float xzd1=xzd*30.48;
	float xzd2=xzd1/160;
	float Radians=xzd2/180;
	return Radians;
}

/*
获取球中心y坐标函数  输入的src 应该为单通道经过pretreatment函数处理过的图像  showimg置为true显示直方图图像  返回求中心点y坐标 如果没有球则返回0
*/
int getbally(IplImage* src,bool showimg){

	IplImage* paintx31;
	IplImage* paintx3=cvCreateImage( cvSize(240,320),IPL_DEPTH_8U, 1 );  
	cvZero(paintx3);  
	int* v=new int[src->width]; 
	int* q=new int[src->width]; 
	memset(v,0,src->width*4);
	IplImage *img3=0,*imageresize3=0;   
	int x,y;  
	CvScalar s,t,u,line;//  存ä?储ä¡é指?针?
	for(y=0;y<src->height;y++)  
	{  
		for(x=0;x<src->width;x++)  
		{  
			s=cvGet2D(src,y,x);           
			if(s.val[0]==0)  
				v[y]++;                   
		}       

	}  

	for(y=0;y<src->height;y++)  
	{  
		for(x=0;x<v[y];x++)  
		{         
			t.val[0]=255;  
			cvSet2D(paintx3,x,y,t);   
		}  
	}  

	
	paintx31=cvCloneImage(paintx3);
	for(y=0;y<src->height;y++)
	{  
		line.val[0]=100;
		cvSet2D(paintx31,312,y,line);
	
	}

	if(showimg==true){
		cvNamedWindow("y的垂直积分投影");  
		cvShowImage("y的垂直积分投影",paintx31); 
	}


	CvScalar xr;
	int xxk=0;
	int xxc=0;
	for(int xxz=0;xxz<paintx3->width;xxz++) {
		for(int  xxu=312;xxu<313;xxu++){
			xr= cvGet2D(paintx3,xxu,xxz);
			if(xr.val[0]==0)
			{
				xxk++;
				xxc=xxc+xxz;
			}
		}
	}

	int pointy=0;
	if(xxk!=0)
	{
		pointy=xxc/xxk;
	}
	return pointy;

}


/*
获取球直径函数  输入的src 应该为单通道经过pretreatment函数处理过的图像  showimg置为true显示直方图图像  返回球的像素直径 如果没有球则返回0
*/
int getballsize(IplImage*  src,bool showimg)
{
	IplImage* paintx1=cvCreateImage( cvGetSize(src),IPL_DEPTH_8U, 1 );  
	cvZero(paintx1);  
	int* v=new int[src->width]; 
	int* q=new int[src->width]; 
	memset(v,0,src->width*4);
	IplImage *img2=0,*imageresize2=0;   
	int x,y;  
	CvScalar s,t,u;

	for(x=0;x<src->width;x++)  
	{  
		for(y=0;y<src->height;y++)  
		{  
			s=cvGet2D(src,y,x);           
			if(s.val[0]==0) 
				v[x]++; 
		}
	}


	for(x=0;x<src->width;x++)  
	{  
		for(y=0;y<v[x];y++)  
		{         
			t.val[0]=255;  
			cvSet2D(paintx1,y,x,t);    
		}  

	} 


	CvScalar r;
	float k=0.0;
	for(int z=0;z<paintx1->width;z++) {
		for(int  u=230;u<231;u++){
			r= cvGet2D(paintx1,u,z);
			if(r.val[0]==0)
				k++;
		}
	}





	if(showimg!=false){
		cvNamedWindow("垂直投影");  
		cvShowImage("垂直投影",paintx1); 
	}


	return k;
} 

/*
获取球中心x坐标函数  输入的src 应该为单通道经过pretreatment函数处理过的图像 showimg置为true显示直方图图像 返回求中心点x坐标 如果没有球则返回0
*/
int getballx(IplImage* src,bool showimg){
	IplImage* paintx2=cvCreateImage( cvGetSize(src),IPL_DEPTH_8U, 1 );  
	IplImage* paintx21;
	cvZero(paintx2);  
	int* v=new int[src->width]; 
	int* q=new int[src->width]; 
	memset(v,0,src->width*4);
	IplImage *img3=0,*imageresize3=0;   
	int x,y;  
	CvScalar s,t,u,line;

	for(x=0;x<src->width;x++)  
	{  
		for(y=0;y<src->height;y++)  
		{  
			s=cvGet2D(src,y,x);           
			if(s.val[0]==0) 
				v[x]++; 
		}
	}


	for(x=0;x<src->width;x++)  
	{  
		for(y=0;y<v[x];y++)  
		{         
			t.val[0]=255;  
			cvSet2D(paintx2,y,x,t);
		}  

	} 

	paintx21=cvCloneImage(paintx2);
	for(x=0;x<src->width;x++)  
	{  
		line.val[0]=100;
		cvSet2D(paintx21,232,x,line);
	
	}


	CvScalar xr;
	int xk=0;
	int xc=0;
	for(int xz=0;xz<paintx2->width;xz++) {
		for(int  xu=232;xu<233;xu++){
			xr= cvGet2D(paintx2,xu,xz);
			if(xr.val[0]==0)
			{
				xk++;
				xc=xc+xz;
			}
		}
	}


	if(showimg==true)
	{
		cvNamedWindow("x的垂直积分投影");  
		cvShowImage("x的垂直积分投影",paintx21); 
	}


	int pointx=0;
	if(xk!=0){
		pointx=xc/xk;
	}	
	return pointx;

}

/*
*预处理函数 第一个参数为输入图像 为彩色三通道  第二个参数为输出图像 为单通道图像 两者大小完全相等
*/
void pretreatment(IplImage *inputim,IplImage *resultimg){
	cvCopy(inputim,inputimg); 
	CvScalar pixel= {};  

	for (int i=0;i<inputimg->height;i++)  
	{  
		for (int j=0;j<inputimg->width;j++)  
		{              
			pixel=cvGet2D(inputimg,i,j);  
			if ( pixel.val[0]>50 && pixel.val[0]<130&&pixel.val[1]>100 && pixel.val[1]<140 && pixel.val[2]>150 && pixel.val[2]<205)  
			{  

				pixel.val[0]=255;  
				pixel.val[1]=255;  
				pixel.val[2]=255;  
				cvSet2D(inputimg, i, j, pixel); 
			}  
			else  
			{  
				pixel.val[0]= 0;  
				pixel.val[1] = 0;  
				pixel.val[2] = 0;  
				cvSet2D(inputimg, i, j, pixel);  
			}  

		}  
	}  //二值化 


	cvCvtColor(inputimg, resultimg, CV_BGR2GRAY );  
	cvSmooth(resultimg, resultimg, CV_MEDIAN, 3,3,0); 

}

/*
球门识别的预处理函数
*/
void pretreatmentforgate(IplImage *inputim,IplImage *resultimg){
	cvCopy(inputim,inputimg); 
	CvScalar pixel= {};  

	for (int i=0;i<inputimg->height;i++)  
	{  
		for (int j=0;j<inputimg->width;j++)  
		{              
			pixel=cvGet2D(inputimg,i,j);  
			if ( pixel.val[0]>120&& pixel.val[0]<200&&pixel.val[1]>60 && pixel.val[1]<110 && pixel.val[2]>110 && pixel.val[2]<140)  
			{  

				pixel.val[0]=255;  
				pixel.val[1]=255;  
				pixel.val[2]=255;  
				cvSet2D(inputimg, i, j, pixel); 
			}  
			else  
			{  
				pixel.val[0]= 0;  
				pixel.val[1] = 0;  
				pixel.val[2] = 0;  
				cvSet2D(inputimg, i, j, pixel);  
			}  

		}  
	}  //二值化 


	cvCvtColor(inputimg, resultimg, CV_BGR2GRAY );  
	cvSmooth(resultimg, resultimg, CV_MEDIAN, 3,3,0); 

}


/*
鼠标事件  下面的MouseHandleTest方法调用它
*/
void mouseHandler(int event, int x, int y, int flags, void* param)
{
	if (event == CV_EVENT_LBUTTONDOWN)
	{
		CvFont    font;
		uchar*    ptr;
		char      label[30];
		img0 = (IplImage*) param;
		cvInitFont(&font, CV_FONT_HERSHEY_PLAIN, .85, .85, 0, 1, 8);

		ptr = cvPtr2D(img0, y, x, NULL);

		sprintf(label, "  (%d, %d, %d, %d, %d)",x,y, ptr[0], ptr[1], ptr[2]);
		cout<<"B&G&R"<<label<<endl;
	}
}

/*
踢球函数
*/
void Shoot(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	behaveior.runBehavior("LowestHead");
	AL::ALMotionProxy motion(robotIp);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage*  imgHeader2;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	int PositionX;

	ALValue img = camProxy.getImageRemote(clientName);
	imgHeader->imageData = (char*)img[6].GetBinary();
	imgHeader1=cvCloneImage(imgHeader);
	pretreatment(imgHeader1,resultimg);
	PositionX =getballx(resultimg,false);
	if(PositionX>160){
		behaveior.runBehavior("RShoot");
	}else{
		behaveior.runBehavior("LShoot");
	}

	camProxy.releaseImage(clientName); 
	camProxy.unsubscribe(clientName);
}
/*
近距离测距
*/
void ClosedDistanceMeasure(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	behaveior.runBehavior("LowestHead");
	AL::ALMotionProxy motion(robotIp);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage*  imgHeader2;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	int PositionY;
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		imgHeader2=cvCloneImage(imgHeader);
		pretreatment(imgHeader1,resultimg);
		PositionY =getbally(resultimg,false);

		if(PositionY <170){
			motion.moveTo(0.02,0.0,0.0);	
		}
		else{
			break;
		}
		cvShowImage("result", resultimg);
		camProxy.releaseImage(clientName); 
	}

	camProxy.unsubscribe(clientName);
	Shoot(robotIp);
}

/*
进行机器人位置的横向校准
*/
void HorizonalDetect(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	behaveior.runBehavior("LowerHead");
	AL::ALMotionProxy motion(robotIp);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	float Radians;
	int PositionX;
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		pretreatment(imgHeader1,resultimg);
		PositionX =getballx(resultimg,false);
		if(PositionX==0){
			printf("找不到球\n");
		}else{
			if(PositionX >160){
				if(PositionX>170&&PositionX<185){
					printf("跳转前右脚踢球\n");
					break;
				}
				motion.moveTo(0.0,-0.02,0.0);
				printf("右脚踢球\n");
			}else{
				if(PositionX<150&& PositionX>135){
					printf("跳转前左脚踢球\n");
					break;
				}

				motion.moveTo(0.0,0.02,0.0);
				printf("左脚踢球\n");
			}
		}
		cvShowImage("result", resultimg);
		camProxy.releaseImage(clientName); 
	}

	camProxy.unsubscribe(clientName);
	ClosedDistanceMeasure(robotIp);
}



/*
球门识别函数
*/
void GateDetected(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	behaveior.runBehavior("UperHead");
	AL::ALMotionProxy motion(robotIp);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	float Radians;
	int PositionX;
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		pretreatmentforgate(imgHeader1,resultimg);
		PositionX =getballx(resultimg,false);
		if(PositionX>190&&PositionX<220)
		{
			break;
		}
		if(PositionX!=0)
		{
			if(PositionX>160){
				Radians= GetBodyRadians(PositionX)-0.1;
			}else{
				Radians= GetBodyRadians(PositionX)+0.1;
			}


			motion.moveTo(0.0,0.0,Radians);
			if(PositionX>140&&PositionX<180)
			{
				break;
			}
			printf("%d\n",PositionX );
		}else{
			printf("找不到球门");

		}
		cvShowImage("result", resultimg);
		camProxy.releaseImage(clientName); 
	}

	camProxy.unsubscribe(clientName);
	HorizonalDetect(robotIp);
}


/*
此函数为以防机器人看不到球门所做的调整
*/
void BallCorrected(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	behaveior.runBehavior("LowerHead");
	AL::ALMotionProxy motion(robotIp);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	float Radians;
	int PositionX;
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		pretreatment(imgHeader1,resultimg);
		PositionX =getballx(resultimg,false);
		if(PositionX>140&&PositionX<180)
		{
			break;
		}
		if(PositionX!=0)
		{
			if(PositionX>160){
				Radians= GetBodyRadians(PositionX)-0.1;
			}else{
				Radians= GetBodyRadians(PositionX)+0.1;
			}


			motion.moveTo(0.0,0.0,Radians);
			if(PositionX>140&&PositionX<180)
			{
				break;
			}
			printf("%d\n",PositionX );
		}else{
			printf("找不到球");

		}
		cvShowImage("result", resultimg);
		camProxy.releaseImage(clientName); 
	}

	camProxy.unsubscribe(clientName);
	GateDetected(robotIp);

}

/*
此方法为远距离逼近球的方法  由main（）调用 
*/
void LongDistanceMeasure(const std::string& robotIp){
	AL::ALBehaviorManagerProxy behaveior(robotIp,9559);
	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	AL::ALMotionProxy motion(robotIp);
	behaveior.runBehavior("StandUp");
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	IplImage* resultimg1 ;
	IplImage*  imgHeader1;

	cvNamedWindow("result");
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		pretreatment(imgHeader1,resultimg);
		resultimg1=cvCloneImage(resultimg);
		int k1=getballx(resultimg,false);
		int k=getbally(resultimg1,false);
		printf("%d\n",k);
		if(k!=0)
		{
			float xzd3= GetHeadPitchRadians(k);
			if(k>117&&k<123)
			{
				float xzd31= GetHeadYawRadians(k1);	
				motion.moveTo(0.1,0.0,xzd31);
			}
			else
			{	
				motion.changeAngles("HeadPitch", xzd3, 1.0f);
			}


			float angle=motion.getAngles("HeadPitch",true)[0];
			if(angle>0.37)
			{
				printf("%f\n",angle);
				break;
			}

		}
		cvShowImage("result",resultimg); 

		camProxy.releaseImage(clientName);


	}

	camProxy.unsubscribe(clientName);
	BallCorrected(robotIp);
}



/*
鼠标事件测试方法  建议获取值时把其他需要相机的函数屏蔽掉
*/
void MouseHanderTest(const std::string& robotIp){

	ALVideoDeviceProxy camProxy(robotIp, 9559);//声明设置模块
	const std::string clientName = camProxy.subscribe("test", kQVGA, kYUVColorSpace, 30);//test 订阅模块的名称，kQVGAS图像大小320*240，30fps帧数（图像播放速度）预定义一些摄像机参数
	camProxy.setColorSpace("test",kYUVColorSpace);
	IplImage* imgHeader = cvCreateImageHeader(cvSize(320, 240), 8, 3);//建立暂存区，图像大小，建立三通道（彩色），单通道（灰色）

	camProxy.setCameraParameter(clientName,18,1);

	IplImage*  imgHeader1;
	IplImage* resultimg = cvCreateImage( cvSize(320,240), 8, 1 );
	IplImage* resultimg1 = cvCreateImage( cvSize(320,240), 8, 1 );
	cvNamedWindow("result");
	while (cvWaitKey(300) != 64)
	{
		ALValue img = camProxy.getImageRemote(clientName);
		imgHeader->imageData = (char*)img[6].GetBinary();
		imgHeader1=cvCloneImage(imgHeader);
		pretreatment(imgHeader1,resultimg);
		cvShowImage("result",resultimg); 
		int test=getbally(resultimg,true);
		printf("%d\n",test);

		cvSetMouseCallback("mouse", mouseHandler,(void*)imgHeader1 );
		cvShowImage("mouse",imgHeader1);
		camProxy.releaseImage(clientName); 
	}

	camProxy.unsubscribe(clientName);
}


int main(int argc, char* argv[])
{
	const std::string robotIp("169.254.199.170");

	try
	{
		// HorizonalDetect(robotIp);
		//GateDetected(robotIp);
		MouseHanderTest(robotIp);
		//LongDistanceMeasure(robotIp);
	}
	catch (const AL::ALError& e)
	{
		std::cerr << "Caught exception " << e.what() << std::endl;
	}

	return 0;
}





