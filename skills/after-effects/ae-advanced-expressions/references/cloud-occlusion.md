# 第32节：云层 Alpha 采样与耀斑亮度联动（显式变体）

来源：https://www.bilibili.com/video/BV1c7GTzMEh5/?p=32 。本单元保持 candidate。课程示范使用 Optical Flares / Golden Sun，本机实际效果目录与既有插件目录未发现该插件，原版未完成。05:37语音允许选择其他镜头光晕插件，因此另提供明确声明的 ADBE Lens Flare 变体；不能拿它代替原版视觉验收。

## 课程方法与证据

01:10：PAL720×576、25fps、10秒。04:40与07:45：红色固态层 Fractal Noise，白色固态层以其亮度作遮罩，形成有变化 Alpha 的白云预合成。不是直接采样不透明杂色层的 Alpha。最终 Contrast177、Brightness−44、Width237、Height100、Complexity6、SubInfluence70、SubScale56；关闭等比缩放。最终 Offset X 为 time*60、Y保留原值。Seed0未从课程明确读出，作为推定。

05:52：Optical Flares选Golden Sun；最后使用透明渲染，太阳层Screen，白云最终Screen位于太阳上方（24:30/24:59图层栏核验）。24:50–24:59最终表达式：

```javascript
mubiao=thisComp.layer("白云");
alpha=mubiao.sampleImage(effect("Optical Flares")("Position XY"),[2,2])[3];
linear(alpha,0,1,100,50)
```

[3]是Alpha，[2,2]是采样半径。课程早期120/40、100/20及不完整表达式属于制作过程，不采用为最终值。原片多次手动拖动太阳，不推断已有运动关键帧。最后位置236/164可见。暗蓝背景精确颜色未读出。后半光学对象编辑参数未完整读出。

## 执行

在全新目录调用 scripts/build_cloud_occlusion.py --implementation native-lens-flare --out <新目录>，再以同目录 run_ae.py --ae <AfterFX.exe> 执行生成的 build.jsx，最后 render_ae.py <新目录> --aerender <aerender.exe> 打包实际Adobe输出并校验。

输入：--speed 默认60，绝对值10..100；--floor默认50，0..80；--duration默认10，4..10秒且完整25fps帧。固定720×576/PAL像素宽高比。--asset只接受720×576PNG，并必须搭配--sweep，用于独立素材空间采样测试。输入自动复制到assets；不要删除工程依赖。

PNG扫光是泛化变体；课程无此关键帧。内置Lens Flare枚举1、深蓝背景近似值、随机种子0均有明确边界，不声称Golden Sun光学身份。非正方像素只在目标软件工程中保留，检查视频播放器是否正确呈现像素比例。

## 宿主故障与修复

AE26中直接同步脚本循环读取跨层 sampleImage 实际曾返回0或未稳定值；仅设置明确时间/短暂等待不能可靠修复。失败回执和原生探针留在evaluations/course2-p32-cloud-001。采用原生scheduleTask逐帧分阶段：预取表达式→渲染云层Alpha PNG→渲染主合成PNG→读取已稳定的采样/亮度。每阶段回到宿主事件循环。只允许一个这样的原生任务运行，任务期间不得打开别的工程或启动其他AE脚本。工程路径变化会中止，保留外来工作。

每帧原生PNG是真正Adobe渲染，FFmpeg只编码视频；native-render-method.json明确aerender_invoked:false。旧技能仍走aerender分支。完成后原生回执才是终态，不能把进度文件当成完成证据。超时先检查宿主和回执，不重复启动。

验证同时检查整段视频解码/变化、逐帧原生公式、若干原生Alpha像素检查点、反馈开关真实图像差、保存重开位置编辑和媒体。原生自导出与视频对照只证明编码质量，不证明课程视觉一致。客观结果与人工审美反馈分别记录；原版插件缺失状态不会因变体技术通过解除。
