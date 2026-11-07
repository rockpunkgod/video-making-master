# 距离控制二维缩放或原生 Fast Blur

[第35节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=35)的两个实现共用距离，但输出属性维度不同。不要把靠近后变模糊改成靠近后变清晰，也不增加弹簧或缓动。

## 原法

四个 a.ai/b.ai/c.ai/d.ai 的锚点在图案中心，和可见圆形“控制”同一合成、二维、无父级。Scale 原式：

```javascript
point1=transform.position;
point2=thisComp.layer("控制").transform.position;
distance=length(point1,point2);
linear(distance,0,70,[250,250],[70,70])
```

03:00–05:45计算距离；06:00–08:10写linear。远端先试75、100，08:05后最终70，08:30后复制给其余字母。09:10–09:50的等价实现是chazhi=sub(point1,point2); distance=length(chazhi)，保留两种方法。距离大于等于70时保持70%，不是继续线性外推。

10:00后在原始未加效果的新合成给每个字母加Fast Blur；直接粘贴Scale的二维结果导致维度报错。12:00后最终改为linear(distance,0,70,40,0)：最近40，最远0。Blur Dimensions为Horizontal and Vertical、RepeatEdgePixels关闭。不把原课Fast Blur替换为其他模糊算法；宿主没有ADBE Fast Blur时记录缺失。

## 输入与执行

用已有Pillow/NumPy的Python调用scripts/build_distance_controller.py --out全新目录 --mode scale或blur，再用同目录run_ae.py和render_ae.py实际执行Adobe。输入和计划写入request/plan；原生AEP、最终MP4、回执、质量JSON、五时点PNG及两个原生开关PNG为交付物。

默认四个可编辑自制圆徽章，替代不可得的AI素材；Arial34、44像素预合成、42像素轮廓不是读出的源素材。--assets接四个自有44×44PNG，须同时有透明背景和不透明前景，复制到输出assets并明确解释为PAR1。不自动放缩其他尺寸或裁切素材。三种实际新素材是数字、几何和箭头，各自四图；任意影片、任意尺寸、带父级或3D坐标未验证。

--radius20..120；--near-scale150..300；--far-scale50..100；--near-blur5..60；--duration3..10、整25fps帧；--distance-method two-point或sub-length。允许边界不代表所有组合均已测。目标位置固定41/121/201/281、Y120，本候选不声称可自动排任意数量。

--control-time默认为0.6秒，仅用于真实表达式开/关诊断；改变速度、路径或半径后该时点可能所有目标都在半径外，导致开/关完全相同。此时根据实际轨迹选择有响应的时点重做，不删除开关差异检查。本次独立8秒镜像案例使用1.8秒。

--profile接受从0开始的严格递增time/position键列表；时长改变按比例重映射整段时间。默认examples/p35-scale-replay-inferred.json或p35-blur-replay-inferred.json来自原片08:50–08:55和13:05–13:10的10fps测量，含选择框读数、颜色中心和七个人工补读点。原课明确没有K运动关键帧，当前控制器键是演示重放适配，目标Scale/Blurriness仍零关键帧。不得说恢复了原课时间轴。

控制器二维Position在本机脚本读回为三元素，空间切线同样要求三元素。相邻采样间采用共线三等分切线，避免零切线在宿主空间采样中产生约0.02像素的非匀速数值误差；这是线性重放的数值实现，不是添加缓动。必须独立按Profile线性插值核对真实位置和输出值，不能只验证目标公式相对于错误的控制器轨迹正确。

## 推定与验证边界

源录屏把整个软件缩小，300×225裁片不能直接当原生尺寸。结合Position41/120和控制器140/209提出原生320×240、显示比例约0.95、目标间距80；仍未读到源合成设置。PAR1与25fps是明确适配，29.97仅源Preview设置。深绿底色近似源录屏，额外底部Solid是保持可交付背景的适配，不冒称原课有该层。原AI尺寸、字体和精确RGB未恢复。

先实际保存重开，修改首个控制器位置、确认目标表达式响应、再保存重开恢复。每帧独立计算控制器线性插值、欧氏距离及clamp后的输出，核对零目标动画键、二维无父级、FastBlur真实matchName和两个选项。实际电影全帧解码；缩放逐帧检查独立变换的边界支持点并排除控制器覆盖；模糊检查同一目标在高模糊/零模糊的实际梯度能量，排除控制器圆区。五个原生PNG与电影对应帧比较，原生表达式开/关真实图像须不同。

像素检查不是精确源对齐：重叠素材可共享支持，源鼠标、选择框和预览重影未复刻，测量重放也有偏差。人工总体效果和客观检查分别记录。失败时先查属性维度、同坐标空间、居中锚点、控制器名称、API切线维度和实际媒体；不能改造课程算法来掩盖偏差。结果见../tests/distance-controller-results.json。
