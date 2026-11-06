# 课程23：水平弹簧连接器

来源：[高级表达式第23节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=23)。这是同高端点之间的宽度联动，不能用惯性/overshoot模板替换课程基线。证据及覆盖限制见 sources/learning-notes/BV1c7GTzMEh5-p23.md 与 evaluations/course2-p23-spring-001/summary.json（均相对实验室根目录）。

## 原法与证据

- 03:00画面显示B锚点靠左且在图形内部；精确数值未显示。
- 09:35前段常幅阶段使用角速度3、振幅60。
- 17:50、20:45：弹簧Position绑定A；Scale X为 `(B.x-A.x)/弹簧.width*100`，Y恒100。17:10–17:47解释漏乘100导致缩放过小。
- 21:55：A位置25/50可读。
- 22:25最终B Position：`start=[A.x+弹簧.width,A.y]`，`pinlv=6`，`fudu=linear(time,0,2,100,0)`，`start+[Math.sin(time*pinlv)*fudu,0]`。6是弧度/秒，不是6Hz；不能额外乘2π。两秒后线性映射钳制为零，保持静止是预期。
- 弹簧左锚点固定、X缩放连接至B锚点。B锚点不是黑色圆心；不能把圆心位移当连接端点位置。

自制透明图形替代不可得的教师素材。基线128×32素材、300×100设计画布、B锚点10/20为画面推定/自制适配；外层4倍合成为交付清晰度适配。它们不是教程明确数值。早期常幅及变参样例B锚点0/20，其他五例10/20，均有实际原生回执。

## 执行

在实验室根目录使用现有Python及AE，输出必须为全新目录：

```powershell
python skills/after-effects/ae-advanced-expressions/scripts/build_spring_connector.py --out samples/runs/spring-new
python skills/after-effects/ae-advanced-expressions/scripts/run_ae.py samples/runs/spring-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
python skills/after-effects/ae-advanced-expressions/scripts/render_ae.py samples/runs/spring-new --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe' --reuse
```

模板在examples/course-spring-connector.json。可选参数：`--mode constant|linear_decay`、`--angular-rate`、`--amplitude`、`--decay-end`、`--duration`、`--b-anchor-x`、`--graphic coil|zigzag|ribbon|chain`、`--asset-width`、`--design-width`。参数范围由构建器检查；范围可接受不等于所有组合已实测。

外部素材：`--asset skills/after-effects/ae-advanced-expressions/examples/assets/zigzag-black.png --design-width 340 --amplitude 50 --angular-rate 4 --decay-end 2.5`。真实PNG宽64–256、高固定32，必须有透明背景；左右连接点位于y16。宽度读取PNG本身，不与--graphic/--asset-width并用。CLI相对路径相对当前目录；profile中的external_png相对profile文件。输入复制到输出assets，原生工程依赖该副本。其他尺寸/任意二维路径不在已验能力内。

输出project.aep、final.mp4、assets/connector.png、request/plan/receipt/quality/spring-quality.json和10张原生检查PNG。自制图形的ART_CONNECTOR保留矢量编辑，修改后须重新导出PNG并重载；表达式实际读取PNG内禀宽度。外部PNG仅保留可替换素材，不宣称恢复其矢量源。主动画可作为预合成与其他Skill组合，内部只负责同高水平连接。

## 验证与修复

原生逐帧检查端点等式、Scale Y、正缩放、表达式错误；实际移动A后保存重开、恢复再重开。真实TIFF序列由aerender渲染，再用现有FFmpeg编码。当前AE未提供可用PNG输出模块模板，不能假设模板存在；saveFrameToPng仅用于素材和检查帧。

独立视频检查测量32px连接图形之外的黑色端点圆帽，容差1.5设计像素，检测全部帧；不使用表达式回执代替画面测量。移动异常先查角速度单位和线性振幅；弹簧脱节查锚点、内禀宽度和乘100；宽度变化后重建素材/工程；不透明黑框查PNG alpha。保存前发现非本实验或未保存工程时停止，不关闭用户工程。

7例1320帧及70张原生检查PNG已完成技术/画面检查；源片与基线的整体人工评审待回复，未逐帧同步。像素指标不评价审美，也不证明推定布局或原素材身份正确。保持candidate。
