# 阵列布局：第21节四滑杆实现

这是既有阵列/自由指向单元的另一实现，与第33节固定间距+atan2朝向保留区别，不按视频再建独立Skill。来源：https://www.bilibili.com/video/BV1c7GTzMEh5/?p=21 。0.14.1仍candidate，人工整体反馈待答。

## 课程明确内容

01:10与08:40：320×240、方形像素、25fps、10秒。满画幅红Solid，中心ADD圆形Mask、锚点/初始Position160/120。02:28的400%预览用于推定最终圆直径约25；准确Mask坐标与RGB未完整读出，当前纯红和Bezier圆为重建，羽化0/Opacity100采用默认值，不冒充源数值。

10:00–11:00最终固定式：

```javascript
hang=Math.ceil(index/5);
lie=index-(hang-1)*5;
x=lie*64-32;
y=hang*48-24;
[x,y]
```

早期lie减hang而缺−1、漏分号、遗漏半格偏移是制作过程错误，不保留为最终算法。course口述/自动转录里的乘除和加减误说，以最终画面代码为准。

11:45之后添加Null并禁用、放在所有圆层下面。四Slider语义依次为x_距离、x_初始位置、y_距离、y_初始位置，14:00/14:55最终：

```javascript
hang=Math.ceil(index/5);
lie=index-(hang-1)*5;
x=lie*thisComp.layer("Null 1").effect("x_距离")(1)
 -thisComp.layer("Null 1").effect("x_初始位置")(1);
y=hang*thisComp.layer("Null 1").effect("y_距离")(1)
 -thisComp.layer("Null 1").effect("y_初始位置")(1);
[x,y]
```

(1)是本机已实测属性槽位适配，避免假设中文宿主支持原视频英文Slider显示名；控制器语义及减法保留。最终54/28/57/34使第五行中心Y251，仍保留25层，不自动改成四行或居中。四个滑杆不会改变列数5。

## 独立调用

使用已有安装Pillow的Python运行scripts/build_index_array.py；本机已验证C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe，无新增安装。Pillow仅用于快速逐帧图像包围框/像素探针检查，底层Adobe执行和渲染继续复用run_ae.py/render_ae.py、既有AE与FFmpeg。

- --layout fixed：原固定式；默认25层/5列、10秒。无Null。
- 默认controller：四控件末态54/28/57/34；--values依次改四数值。
- --controller-profile examples/p21-controller-replay.json：5秒源手动操作重放。JSON有duration与升序keyframes，每点time和values四数；4..10秒、完整25fps帧。有Profile时逐点values优先于--values；改变整段须改Profile，而非只改某一时刻的滑杆键。
- --columns2..7、--count1..49、--duration4..10及四值−100..160是显式泛化。固定式仍使用64/32/48/24，不擅按新列数自动重排画布；controller按指定数值直接算。
- --asset自有透明PNG，16..2048像素，需有可见高亮不透明探针；最长边适配25，复制到assets且原生PAR设1。黑底上的纯黑/极暗素材不在已验范围。三种不同PNG已实际制作，未承诺所有素材/尺寸组合均已验。
- --point-profile配合PNG与显式--heading-offset，组合第33节sub(self,target)/atan2/radiansToDegrees。朝上PNG用−90；方向语义见free-pointing.md。目标几何是新组合设定，不能当第21节原片存在目标。目标Profile时长须与制作时长一致。

示例先构建全新输出目录，再运行同目录run_ae.py <build.jsx> --ae <AfterFX.exe>，最后render_ae.py <目录> --aerender <aerender.exe> --reuse。640×480连续显示包装为交付适配，内部保持320×240方形像素。输出含真正AEP、MP4、参数/计划、复制素材和验证记录。跨机器重建或重链接assets。

## 源重放的边界

原课是暂停时间线后拖滑杆，没有作者的时间轴动画。14:30–14:35的125帧已抽取，125个Y值局部图和25个场景图直接查看。X64/初始32/Y初始28与若干Y值明确；逐帧Y轨迹根据末行边缘相对清晰47值的位移推算，受重影及预览刷新滞后影响。输入逐点线性重放是自制适配，不冒充源关键帧、缓动或精确原工程状态。

固定与末态是有意静态布局，不以冻结动画替代教程。五次不同原生时间点导出PNG字节相同、250帧原生变换一致、无制作运动键，成片相邻帧亮度差实际0。通用静态校验新增的非文字路径仅限index-array及上述实证，不伪造text_layers；原文字校验条件仍保留。移动影片强制标静态被拒绝，实际原生末帧经FFmpeg冻结的错误重放也被专用像素检查拒绝。

## 诊断与组合

Null必须在底部，阵列层indices1..N连续。Null移到上面会挤走index，先恢复层序，不随手给公式补index−1。移动Null的Position不会平移阵列；改变初始值，且增大会向负方向移动。层复制用原生duplicate，位置不写死25组值。

数值导致重叠或越界时按课程直接保留。若整片不可见，检查距离与初始值，不把检测失败解释成已成功渲染视觉效果。没有自动clamp、居中或不经说明的重布局。

重开工程后必须重新查找Comp/Layer对象；旧引用实际曾报“对象无效”，失败回执已保存。脚本只处理未父级化二维图层，脏或非本实验工程会停止保留。入库后临时渲染帧删除，重新制作使用全新目录，不复用旧回执或尝试打包不存在的帧。

验证见tests/index-array-results.json：原生位置/控制器/Mask编辑保存重开、125/250帧影片全解码与每帧包围框和像素探针、朝向组合主轴、依赖审计。包围框与探针不是整幅原片像素身份或审美通过；课程原片在左、复刻在右的人工评审单独绑定SHA。
