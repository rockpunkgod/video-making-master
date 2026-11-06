# Numbers联动读取进度（候选）

[来源2第31节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=31)。先复现原课Numbers效果、独立X/Y缩放、透明度循环和单独调节层；不能换成SourceText计数器、TrimPaths、LinearWipe或在条形本身拉伸渐变来冒充原法。实际5例AEP/视频1750帧，71张原生PNG已检查；边界见tests/loading-progress-results.json。

Numbers位于合成大小Solid上，Value原始值100，表达式：

```javascript
if(time<10)
 time*10;
else
 value;
```

value是未套表达式的原始值，不是上一帧。原课先用70导致10秒之后掉回70，之后明确设100。不能把else改成100而失去原始值联动。每次原生测试实际把原始值改70、保存重开，确认完成后的数字与条形均为70，再恢复100。

条形Solid550×50，anchor左侧[0,25]，X受数字控制，Y保持原缩放：

```javascript
x=thisComp.layer("数字").effect("Numbers")("ADBE Numbers2-0003");
y=transform.scale[1];
[x,y]
```

Numbers位置391/355、Size62、Decimal0可见，Random/CurrentTime/CompositeOriginal关闭。效果重命名Numbers，并用实测matchName取Value，适配中文AE而不改变原理。Numbers Options最终为Gulim Regular Horizontal Right：05:02到05:07逐秒核对，曾切Left/Center但最后选Right，不能将过程当终值。

LOADING的Opacity在0/8/16帧为100/50/100，Info明确Linear。最终`loopOut(type = "pingpong", numKeyframes = 0)`，不是最初cycle阶段。Number和bar在10秒保持100，标题继续闪烁；不能因全片仍变化就误判完成后的条形也在动。

原课说明：条形自身加4ColorGradient会压缩全部颜色，不是固定位置逐步显露的目标。将4ColorGradient放到独立调整层并向下移，避免染到标题和数字。当前550×50条形左95/纵448为测量推定，调整层位置364/678有推定，其他边界见结果。源面板Point1[124,446]/red、Point2[345,448]/yellow、Point3[595,451]/green、Point4[392,4798.4]/blue（远移避免影响），Blend100/Jitter0/Opacity100/None。原始显示值直接用于当前宿主；端部色相仍有视觉差异，源工程身份/全部坐标解释尚未恢复。曾实际渲染“减去调整层偏移”假设，效果更差而未采用，不能把未验证的转换说成课程参数。

本机原生字体目录不含AdobeHeitiStd/Gulim。标题ArialNarrow-Bold，57px/Tracking123；为匹配参考字形加入111%/130%字体补偿（单画面量测推定，不是原课TextScale）。Numbers实际原生窗口选择的是Microsoft YaHei UI Regular Right，截图见native-numbers-options.png。曾意图选择Arial但原生结果是上述字体，以实际结果为准。不得将其标为原课字体精确恢复。

Numbers创建会打开原生字体窗口，枚举未提供可脚本写入的字体参数。使用本Skill自制assets/numbers-msyhui-right.aep原生种子，保留Numbers的字体/对齐内部数据，再通过普通原生参数设置数值/字号/位置。没有复制教程或Adobe供应商项目，不声称存在字体setter。运行时打开种子创建新项目并另存；种子没有外部媒体。整个Skill复制到独立目录后已实际制作/渲染，后续调用不需逐次处理弹窗。AE26/Windows字体为已测环境，其他系统/版本必须重新核验字体及Numbers兼容。

```text
python scripts/build_loading_progress.py --out <全新目录>
python scripts/run_ae.py <输出目录>/build.jsx --ae <AfterFX路径>
python scripts/render_ae.py <输出目录> --aerender <aerender路径> --reuse
```

输入：`--title`1..12个大写ASCII/数字/空格；`--complete`默认10，3..12秒；`--duration`默认15，至少complete+2且不超过15秒，25fps整帧；`--pulse-frames`默认8，4..16。独立变体实际测试complete6/duration10/pulse6及RENDERING。仅列出的组合实测，不把允许区间当成覆盖证明。

`--asset`可用自有260×57PNG替换标题并复用相同Opacity循环，三种原创export/render/sync已实做。PNG必须非空，导入后匹配合成PAR。此处为素材适配变体，基线仍保留可编辑TextDocument。支持范围未扩展至任意语言、尺寸或视频素材。过暗/极细图案可能无法通过标题像素检测，需另行适配和测试。

项目保留PAL720×576/1.094017094/25fps；视频按未校正预览的原始720×576像素封装，SAR1是明确交付选择。保留AEP/MP4/assets/请求、计划、原生回执、质量报告及必要PNG。迁移时重新链接PNG或从随附脚本构建。

验证分开记录：原生每帧Number/Scale/Opacity及保存重开；影片每帧条形左右界限≤2px、标题循环误差≤3百分点、已被覆盖的固定点色差≤8；数字ROI对13/9张原生检查点RGB均差≤3。实际开关调整层PNG证明标题/数字字节相同、条形显著改变。冻结末帧电影被条形、闪烁和数字检查拒绝。非全片OCR、非原课像素身份、非审美验收。

先给原课18:16–18:21与右侧真实渲染的时间码采样对照再请求人工反馈。评审视频左右5fps，右侧仅选择已有原生电影帧；不是改写AEP或改变完整15秒成片。原课100%预览裁掉边缘，右侧采用对应的推定可见区域；原片刷新滞后不能称完全逐帧同步。

诊断：10秒后回跳先检查原始Value是否100；条形向两侧长检查anchor；高度随进度变检查独立Y赋值；颜色随条形拉伸检查效果是否错误放在bar上；标题/数字被染色检查调整层覆盖边界。原生FontOptions缺失时保留candidate并报告实际替代字体，不伪造恢复。源幕上的刷新禁用/编辑中报错需区分过程与最终状态。与其他文字或信息图可组合成透明预合成，但跨软件DynamicLink尚未由本单元验证。
