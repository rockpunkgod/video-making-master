# Write-on 螺旋累积（候选）

来源：[来源2第30节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=30)。本分支覆盖原生Write-on，后半Particular未安装，不制作替代粒子效果。证据与逐项边界见tests/spiral-writeon-results.json及evaluations/course2-p30-spiral-001/summary.json。

先按课程基础复刻：720×576、25fps是明确口述；201帧时长为Info推定，方形像素是声明的适配。单个Solid加ADBE Write-on，BrushPosition：

```javascript
banjing=time*50;
jiaodu=time*30;
x=banjing*Math.cos(jiaodu);
y=banjing*Math.sin(jiaodu);
[x,y]+[thisComp.width/2,thisComp.height/2]
```

30是弧度/秒，不能擅自换成30度/秒。保留原生绘画历史，而非每帧只显示一个圆点或预制矢量线。原课初始半径60圆形是过程阶段，不作为最终增长半径。外圈点状是有限画笔间距的结果，原课明确解释，不能以“修平滑”名义换算法。

效果参数：大小2；硬度79%在原生API为.79；不透明度1；描边长度0（无限保留）；间距UI.001，本机实际最低.00100708007812；PaintTimeProperties=3/Color，BrushTimeProperty=1/None，PaintStyle=2/OnTransparent。这些matchName及枚举经过本机效果创建、参数读取和实际图像核对，不假设其他插件版本相同。

固定椭圆按原课将x替换为`(banjing+time*50)*Math.cos(jiaodu)`。动画椭圆把extra50链接Slider；第50帧0、第125帧80来自口述及可见操作。实现增加第0帧冗余0键以明确前段保持，采用原生线性插值，原课曲线手柄尚未读取，不能声称精确缓动同源。

执行时先构建全新目录，再运行同目录run_ae.py和render_ae.py，分别指定本机AfterFX和aerender。程序拒绝脏工程或非本实验工程；原生完成真实画笔大小修改、保存重开和恢复，随后逐帧表达式核对、TIFF渲染、FFmpeg封装和全帧检查。AEP、MP4、receipt/request/plan/quality、必要PNG及assets为交付。

```text
python scripts/build_spiral_writeon.py --out <全新输出目录>
python scripts/run_ae.py <输出目录>/build.jsx --ae <AfterFX路径>
python scripts/render_ae.py <输出目录> --aerender <aerender路径> --reuse
```

参数：growth默认50、10..80；angular默认30、绝对值5..40且可负；duration默认8.04、2..8.04秒，需25fps整帧。`--ellipse none|fixed|animated`；animated至少5.04秒。只实测列出的7组组合，不将输入边界当成全面覆盖证明。

新素材适配用`--asset <自有PNG/JPG>`，改为PaintStyle3/RevealOriginalImage，这是明确的扩展，并非课程透明白色基线。当前只支持720×576、完全不透明、最低亮度64的图片；三种PNG已实测，JPG尚无独立样例。AE会把此尺寸图片自动解释为PAL像素1.094017094；导入后必须原生设pixelAspect=1并保存重开检查，否则螺旋横向拉宽。保留的三素材图像可替换，AEP媒体路径为原生绝对路径，迁移后重连assets或用独立脚本重建。

基本视频检查不等于课程验收。专门检测每帧16个历史轨迹点，沿一个原生画笔间距内的时间偏移搜索5×5窗口；白色亮度阈值42，新素材按输入最低亮度成比例调整。末帧亮区须比第25帧扩大2倍。原生表达式另按每帧严格坐标核对。冻结末帧和错误像素比例的真实电影均被拒绝。颜色另用既有Pillow/NumPy对27张原生PNG核对：本机saveFrameToPng为黑底预乘RGB，正确模型是sourceRGB×alpha，不能直接与未预乘原图比较；并非完整视频逐像素比对。

故障处理：历史消失先核对StrokeLength=0；Solid露出先核对PaintStyle=2；椭圆异常先核对extra50/控制器及素材PAR；表达式报错检查国际化matchName/原生向量加法；保存重开后重新寻找Comp/Footage，旧对象不可复用。验证器中的初版嵌套条件和旧引用错误已保留失败记录，不做未经证实的宿主普遍性结论。输入过暗/透明/不同尺寸会明确拒绝，适配后须新增真实测试。

与第29节融合的是cos/sin/time及中心偏移；区别是半径随时间增长、Write-on保留历史。可作为后续合成的透明预合成，尚无自动跨软件Dynamic Link验证。三维粒子部分仍缺Particular；原课XY、速度清零、亚帧平滑、寿命、Z表达式/关键帧与相机流程仅记录已观察内容，不标记完成。
