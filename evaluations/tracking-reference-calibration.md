# 跟踪参考校准与原生制作记录

日期：2026-11-06。本报告保留校准和失败过程；最新三输入验收见tracking-verified.json。

真实输出由AE26.0x67内置3D Camera Tracker从扁平MP4求解。源场景没有导入求解工程。截图确认三点和原生参考平面后替换原创图像，重开AEP，用aerender生成MP4。

## 修复与校准

自动Mostly Flat原生误差标签0.50像素；改Typical+Detailed后0.09像素。标签不是贴图漂移指标。单点实底朝向摄影机，锚点稳定但平面错误；独立光流/源场景真值分别测得四角最大3.32/3.42像素，均失败。实际Shift三点选面修复了方向。

最初48像素半径ROI未包围贴图四角，局部单应外推产生约3像素假漂移。旧drift.json全部保留。原创源场景临时导出back平面投影仅用于验算，源工程未保存改动，摄影机从未进入求解。真值显示三点平面四角最大约0.26像素。扩大到同墙面120像素半径、120个稳定特征后，光流四角最大0.16像素，参考锚点与真值最大差0.067像素。

检测器新增逐帧特征凸包覆盖四角的门槛，不满足时inconclusive。区域仍须目视同一刚性平面；凸包不能证明平面语义。RMSE≤1、最大≤2像素门槛未变，仅适用于960×540实验。回归实测：正确平面通过；单点错误平面在充分参考支持下仍失败；小ROI变为inconclusive。

## 当前输出

|镜头与变化|samples下目录|检查|
|---|---|---|
|原创房间、几何图标100%|tracking-fixture-001/solve-calibrated-001/composite-001|96帧完整解码；四角最大0.162像素；真值最大0.257像素|
|同镜头、文字80%|tracking-fixture-001/solve-calibrated-001/composite-typography|96帧完整解码；四角最大0.119像素|
|原创画廊、前景展板、纹理目标宽100像素|tracking-gallery-001/solve-001/composite-pixel-sized|120帧完整解码；四角最大0.256像素|
|原创走廊、前进运镜、文字目标宽220像素|tracking-corridor-001/solve-001/composite-pixel-sized|84帧完整解码；四角RMSE1.526、最大2.822像素，失败|
|同一走廊，输入已知水平视角重新求解，文字仍220像素|tracking-corridor-001/solve-calibrated-001/composite-pixel-sized|84帧完整解码；四角RMSE0.223、最大0.783像素，通过|

目录保留project.aep、final.mp4、receipt.json、projection-trace.json和quality.json。built/reopened为构建回执，rendered:false保留构建时状态，实际渲染以quality和视频为准。

GUI归属检查拒绝了非AE前台的物理点击；随后用AE实测app.activate()激活宿主，不操作遮挡应用。右键必须命中可见点或实际目标，三点几何质心不一定命中；ContextX/Y允许指定已观察命中点。坐标须每次截图确定。

## 视觉与边界

已查看房间和画廊原版本2fps整段接触表及贴图局部，未见黑帧、跳变。画廊55%世界比例贴图太小，不是理想演示；现已增加画面像素宽度参数并重新原生制作100像素版本，数值通过，最终画面审查待完成。视觉审美与数值分开，不将测试场景当作电影质感作品。

后续已完成走廊精度修复、最终画面审查、四个原生工程编辑恢复、独立技能封装和实际复制调用，证据见tracking-suite-001及tracking-verified.json。真实拍摄素材仍未验证；未覆盖遮挡、模糊、滚动快门、畸变、变焦。
