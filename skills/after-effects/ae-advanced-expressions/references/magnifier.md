# 第25节：随动清晰区与凸起放大镜

[课程来源](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=25)。基线按调节层/减法蒙版/Fast Blur/Bulge原法，不能替换成缩放一块照片的算法。课程在合成第0帧手动拖镜片，未展示制作好的位置动画；示例视频是把观察到的拖动采样为关键帧的交付适配，不能称原课时间轴复现。

## 已观察与推定

- 01:23–02:06：原图片用Mask抠镜框，锚点放到镜片圆心。
- 02:23–04:30：直接在文字上模糊再加Mask会裁掉内容，改为放在文字之上、镜框之下的调节层；Fast Blur8，Repeat Edge Pixels开启，圆形Mask设Subtract。
- 05:00–07:15：直接链接Position造成蒙版错位与调节层边界漏焦。07:30–09:50：将调节层扩到2000，中心画圆、减法蒙版，再把Position链接镜框Position。
- 10:38–11:12：Mask Feather与负Expansion改善边缘；13:50画面可读Feather101/101、Expansion-29。
- 11:40–13:18：文字加Bulge，复位中心再匹配镜片；13:00可读横半径191、纵半径139、高度1、Taper0。Bulge Center直接链接镜框Position。
- 13:30–13:49：仍在合成第0帧，讲师手动移动镜框以演示联动。13:34–13:38每秒圆心检测经逐图核对，换算坐标与中间插值仍为推定，不承诺精确同步。

画布1024×846根据复位中心512/423推定，没有明确尺寸界面。字体KaiTi、自制镜框、原创文字、字号34/行距46为视觉适配；旧变参案例字号28/行距38独立保留。源镜框像素身份未恢复。基线圆形蒙版半径180为自制镜框适配，Bulge的191/139沿用明确参数。

## 调用

实验室根目录、现有Python/AE/aerender/FFmpeg，输出必须全新：

```powershell
python skills/after-effects/ae-advanced-expressions/scripts/build_magnifier.py --out samples/runs/magnifier-new
python skills/after-effects/ae-advanced-expressions/scripts/run_ae.py samples/runs/magnifier-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
python skills/after-effects/ae-advanced-expressions/scripts/render_ae.py samples/runs/magnifier-new --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe' --reuse
```

参数：`--text`替换非空文字，`--blur 1..16`，`--bulge-height 0.2..2`，`--asset PATH`接受调用者PNG/JPG，`--profile`读取配置。文字分支核对实际KaiTi字体，缺失则停止，不静默换字体；字体文件不打包。图片分支复制素材到assets并在全画幅预合成中按比例适配，使中心表达式仍使用相同坐标系。不同画幅或文字排版应先另测，不能假设所有允许范围已验证。

输出project.aep、final.mp4、必要assets、请求/方案/原生回执/视频及光学验证JSON、10张原生时点PNG与3张效果开关对照PNG。AEP保留可编辑文字、镜框矢量源、真实PNG镜框、外轮廓/镜孔蒙版、调节层和效果表达式。修改ART_LENS_SOURCE后重新导出PNG并重载，镜片中心锚点仍为250/250。图片分支素材可替换；不要只改source尺寸而保留不适用的坐标假设。

## 验证与修复

原生逐帧检查镜框、调节层和Bulge中心一致、2000调节层覆盖全画幅；位置实际编辑后保存重开、检查两处联动并恢复。aerender输出真实TIFF，再封装MP4。

每例另外实际渲染同一帧的正常、关闭Blur、关闭Bulge三种原生PNG，然后恢复效果并保存。独立像素检查中心60px内：模糊开关差<1，凸起开关差>0.5；距中心260px外：模糊开关差>1，凸起开关差<0.5（RGB平均绝对差）。这是效果位置/开关检测，不是审美评分或与教程的像素误差。全150帧解码并检查真实运动，冻结视频应拒绝。

清晰区偏移先查镜片圆心锚点、调节层中心蒙版和直接链接；边缘漏焦查调节层尺寸/位置覆盖；整张图被裁掉查是否把Mask错加到内容层；镜框被模糊查调节层顺序；只有清晰而不凸起查Bulge是否开启、中心是否随动。无可用原生Fast Blur/Bulge时记录宿主缺失，不静默换算法。

5例750帧、65张原生检查/对照PNG已技术检查；包含独立Skill副本/不同cwd调用、参数变化和三个新图形输入。课程光学效果人工反馈待答。镜柄在末段可能越过画布，与演示取景相关；任意镜框、缩放/旋转联动、动态视频输入均未验证。保持candidate。
