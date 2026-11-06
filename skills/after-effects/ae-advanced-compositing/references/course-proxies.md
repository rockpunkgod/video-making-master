# 第18节：原生高质量Alpha代理

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=18 ，00:31–07:10。目标是在保留原始图层可编辑性的前提下，预渲染昂贵的平面预合成，再挂回AE代理。此分支不重做课程结尾的相机或文字，也不把组件测试当完整片头验收。

01:13附近Create Proxy→Movie默认Draft/Half。作者在01:50–02:38改用Best/Full、QuickTime Apple ProRes4444、RGB+Alpha、预乘颜色；02:48–03:45手动Set Proxy→File、开关及重做后换文件。04:15–06:35重复用于100层核心，并提醒只渲染所需时长。06:46–07:10明确指出折叠变换依赖内部三维数据，平面MOV不能替代它。

先读request/profile，选择examples/course-proxy-lines.json、course-proxy-core.json或course-proxy-type.json。默认输入是本Skill自制总装和自制原生输出模板，SHA锁定；不读取其他仓库。模板在本机AE GUI设为Trillions of Colors+，实际原生渲染后FFprobe已确认prores/4444/yuva444p12le。不是把H264改后缀，也不重编码课程视频。

```powershell
python scripts/build_proxy.py --profile examples/course-proxy-core.json --out E:/自媒体/video-skills-lab/samples/runs/proxy-new
python scripts/run_ae.py E:/自媒体/video-skills-lab/samples/runs/proxy-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe' --timeout 600
python scripts/render_proxy.py E:/自媒体/video-skills-lab/samples/runs/proxy-new --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe' --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe'
```

上例在Skill目录运行；路径按目标机器修改。输出目录必须全新。输入参数为目标合成名、实际宽高/fps/时长、两份原生AEP及SHA、检查帧和final_policy。另一目标先建明确profile，不能根据相似层名猜测。现有测试只覆盖1080方形与1280×720、30fps、5秒及151帧组件。

准备阶段先扫描输入工程中所有引用目标的层；任一collapseTransformation=true就拒绝。不能先reduceProject移除父合成、再假称没有折叠依赖。不要为通过检查关闭折叠或删除父层。实际负例P13_NOISE被拒绝，见tests/proxy-results.json。

原生模板使用2D包装层PROXY_SOURCE保持原合成尺寸、时间、位置和原始内容，作为只读烘焙适配。它不会把内部3D数据送进其他主场景。诊断合成加深色/白色底板用于检验Alpha，底板不进入MOV，也不是课程画面设计。原始目标全部图层仍留在project.aep。

渲染后先验证真实ProRes4444、Alpha像素格式、尺寸、fps、完整帧数和全帧解码；之后才setProxy。按原生预乘输出明确设AlphaMode.PREMULTIPLIED/黑底解释。切换禁用/启用都保存并重开，再修改真实原图层Opacity为99、重开读回、恢复原值。之后比较代理前后7个深色底、2个白底检查帧。最终视频再逐帧解码，并与7个原生导出帧比较；不是自评代替实际渲染。

默认final_policy=proxies，RenderQueue明确Use All Proxies，对应作者使用高质量代理的流程；--final-policy originals明确Use No Proxies，保留交互代理但最终从原始图层计算。两者均有实际案例。不要只切界面开关就假定最终队列遵循它。

保留project.aep、final.mp4、assets/proxy.mov、原始AEP输入、原生QA PNG和报告。MOV是工程必需媒体，不是可删中间渲染；本例195–254MB使用Git LFS。克隆后运行git lfs pull取回实体，Git指针文本不能当MOV打开。跨机优先重建，或重链接代理文件及输入。发布工具同时核对实际MOV的SHA/大小与Git索引中的LFS指针。

本机实测注意：OutputModule的Depth在脚本中为只读，setSetting会失败；应重建原生输出模板并核实GUI/实际编码。ShapeLayer和TextLayer在本机不是instanceof AVLayer，编辑测试要显式包含它们。完整课程输入与源层都有所有权/脏工程检查，失败后不要盲目重试覆盖。

代理不会自动追踪后续源合成改动。编辑内容后先禁用旧代理，用新请求目录重新烘焙，再挂入新文件。若以修改后的交付工程为新输入，先在其副本上Set Proxy→None（原生setProxyToNone），另存并更新profile的SHA；只关useProxy仍有旧代理，入口会拒绝。不要因为路径相同就把旧MOV当最新。原生曲线等CUSTOM_VALUE不可完整指纹化，因此本候选没有宣称自动检测所有陈旧代理。

测得的加速仅是选定帧清缓存后的PNG导出，包含压缩、等待和I/O；本轮还同时运行本机转录，不能当严格性能基准。文字案例几乎没有提速，符合课程优先处理昂贵组件的建议。交互播放FPS及其他AE版本未测，整体Skill保持candidate。
