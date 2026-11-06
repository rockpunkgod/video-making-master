# 首次跟踪合成：失败记录

已由原生3D Camera Tracker创建摄影机及参考实底，并把独立图标贴到该实底上，保存并重开工程，通过aerender生成960×540、24fps、4秒合成。96帧全部可解码。画面见tracking-composite-001-frames/contact-1.jpg。

但独立漂移检查未通过：RMSE 1.865px，最大3.649px，P95 3.363px。验收线在检测前固定为RMSE≤1px且最大≤2px，未根据结果调整。原生内部平均误差0.50px不能替代外部附着稳定性。

方法：仅使用输入MP4的图像，初帧在贴图锚点附近检测27个Shi-Tomasi角点，以前后向Lucas-Kanade光流及局部RANSAC单应性拟合整段平面运动。27个点均存活。AE每帧投影只用于定义初始锚点和最后比较，未用于驱动参考轨迹。该指标只验证一个局部平面，不证明整个三维场景正确。

本机已有OpenCV与NumPy，因此复用它们做独立验收；没有重写AE跟踪器，也未用检测轨迹改写原生摄影机数据。

已观察的可能原因是Auto Detect采用Mostly Flat Scene，而输入包含三个不同深度平面。下一步按[Adobe原生跟踪器说明](https://helpx.adobe.com/after-effects/desktop/work-with-3d-composition/3d-camera-tracker-effect/tracking-3d-camera-movement.html)尝试Typical与详细分析。是否改善以新一次独立测量为准，不提前标记成功。

诊断中的一个假错误已排除：本机直接把向量值与字符串相加会报数值错误；逐个读取分量后确认摄影机和实底位置均为有限数。不能把日志格式化错误当成原生求解产生NaN。
