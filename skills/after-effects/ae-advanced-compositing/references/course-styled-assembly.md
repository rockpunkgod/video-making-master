# 第16节原生风格化总装候选

来源：[课程第16节](https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=16)，06:30–19:44。前半节核心沿用已获整体认可的p16-core-001；本总装未获视觉验收。课程第17节继续制作，不能将本候选视为完整片头。

## 已按课程实施

- 第15节11层粗总装作为原生输入，替换为可编辑动态核心和第16节噪波，不使用渲染视频贴到图层上。
- 径向背景外部Hue/Saturation：最终315°、明度−37。15:28原片放大数字明确为315.0，31.5是本轮一度出现的读数错误。08:30蒙版羽化114、扩展−33；手绘轮廓未显示坐标，当前在源1920×1080坐标中估为中心960/540、半径520/300的椭圆，保留推定标记。
- 噪波沿用FN6/7关闭、Scale342/423/100、白键→Colorama→Glow48.2%/122/0.8及约59→95帧淡出，详见course-noise-style.md。
- 圆环内六个噪波层Screen；14:00顺序Fractal Noise→Polar Coordinates→Find Edges，Invert开启。外部改为键黑→Colorama→Glow5%/20/1。主层Z−7000，开始约第80帧。
- 15:20调色盘新增右下白色色标。自制assets/course-p16-colorama-polar-template.aep经原生界面添加并保存重开，保留可编辑的四个色标。白色为#FFFFFF，位置根据画面估为循环约0.36；紫色#5500FF及顶部位置继承先前估算，精确原课数值未显示。
- 16:40核心Opacity表达式保留transform.opacity；点阵及径向背景引用核心Opacity。核心100→0约第34→43帧，按尺标估计。新排序为Camera/title/core/dots/radial/noise/polar/contours/streaks/lines/background。
- 17:34轮廓预合成外部Fill白色，内部红色描边保留；19:24外部Glow60%/10/1。控制器Time offset1；Z spacing0→1300，2600为中间尝试。18:23明确执行Easy Ease In。Z末键约3秒/90帧，Trimpath末键约1.3秒/39帧，均在30fps预合成中估读；原生incoming influence33.333333为重建值，不是源课实读曲线。

## 输入、调用和交付

scripts/build_styled_assembly.py使用examples/course-styled-assembly.json，四个SHA固定输入为自制P15总装、动态核心、噪波样例及Colorama调色模板。examples/style-inputs保留前三个独立原生工程。默认只测试1920×1080、24fps、20秒合成，拒绝未验证的其他尺寸和时长契约。

从实验室根目录执行：

```powershell
python skills/after-effects/ae-advanced-compositing/scripts/build_styled_assembly.py --out samples/runs/新目录
python skills/after-effects/ae-advanced-compositing/scripts/run_ae.py samples/runs/新目录/build.jsx --ae "已核实的AfterFX.exe路径"
python skills/after-effects/ae-advanced-compositing/scripts/render_ae.py samples/runs/新目录 --aerender "已核实的aerender.exe路径" --reuse
```

--polar-glow-intensity0.7为显式变体；默认1。自动复制输入，输出可编辑project.aep、真实final.mp4、请求/计划、原生回执、质量报告及14个原生检查PNG。变体已从隔离Skill副本独立构建和渲染，不依赖Video Making。

## 宿主回读与检查

AE26重开后，Hue/Saturation主色相和明度可能暂时回读0，尽管软件界面及内部设置仍保留值。本机实际测试before[0,0]，将通道控制切到2再回1后after[315,−37]。生成器刷新通道后读取并断言，不能把暂时的0直接当成保存失败，也不能省略原生验证。

圆环Glow Radius20→21实际保存重开，再恢复20重开；每个表达式按480个主合成时间点求值，核心/点阵/径向Opacity全480帧核对，轮廓控制器另覆盖210个源帧。全帧解码后与14个真实AE PNG比较，160×90亮度平均误差限8/255。这是结构、编辑和编码一致性测试；不证明审美、课程精确同步或跨素材泛化。

## 尚未解决与可执行诊断

后段灰色条带和红色线条保留第15节阶段，下一课程继续处理；标题Z−22000在继承相机有效标题帧中仍位于相机背后。不要为通过“完整成片”验收自行翻转相机方向、移动标题或添加课程未展示的调色。

Hue回读0先刷新通道，再对照原生界面；值仍不符才停止。圆环黑盘或线条消失，核对六层Screen、Find Edges Invert以及外部键黑；不可仅提高亮度掩盖混合方式错误。彩虹或缺少白色层次时核对随附Colorama模板SHA和完整复制图层的方法，CUSTOM_VALUE未支持，不猜写色标API。复制图层后按唯一名称定位，不假定新层位于layer(1)。蒙版形状、关键帧位置、相机曲线仍需和课程连续回放对齐。

003基线及强度0.7变体技术检查通过，全部14个原生检查图实际查看。三组新素材、完整序列、课程视觉验收和精确时序仍缺，状态candidate。详见tests/styled-assembly-results.json。
