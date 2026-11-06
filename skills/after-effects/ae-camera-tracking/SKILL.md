---
name: ae-camera-tracking
description: 用After Effects原生3D Camera Tracker从刚性场景视频求解摄影机，三点选面后贴入可替换图像并测量全段漂移；已验证三种原创合成场景，真实拍摄素材仍需单独验收。
---

# 原生三维摄像机跟踪

按严格课程标准当前为candidate。0.2.0已在Windows中文AE26.0x67通过三种原创合成场景的原生技术测试，但教程中的参考增强、地面原点、网格、Normalize Track和Alpha元素整条流程尚未完成复刻。既有验证仅覆盖刚性场景的平面图像贴入；真实拍摄、遮挡、模糊、畸变、滚动快门未验证。Agent仍需截图选点。证据见tests/results.json和项目evaluations/course-fidelity-audit-001.md。

1. 阅读 [调用步骤](references/invocation.md)、[技术与限制](references/workflow.md) 和 [课程证据](references/sources.md)。先判断场景是否刚性、视差是否充分、是否存在焦距变化和滚动快门。
2. 以 scripts/start.py 接收单镜头视频、生成独立JSX，使用AfterFX -r执行。不要把添加效果器当成求解完成。
3. 轮询本机效果控件的状态。原生matchName是ADBE 3D Tracker；误差和求解方法是自定义属性，值接口不可读时可读取其动态name显示，不假设存在点云导出API。
4. 通过实际效果面板的“创建摄像机”，或在已观察的跟踪目标上右键创建参考平面和摄影机。GUI坐标每次根据当前截图确定；不可复用其他显示布局的坐标。优先用可观测的菜单与已安装工具。
5. 读取创建的CameraLayer与关键帧，保存原生工程。设置地面和原点，叠加测试网格/新素材，验证全段附着稳定性，然后恢复原始参考画面。
6. 按 tests/protocol.md完成原生渲染、三组输入、变参和误差审查，全部通过后才能升级状态。

漂移检查需同时覆盖锚点和贴图四角。参考光流的特征包络必须覆盖四角，否则标为inconclusive；不能用很小邻域的单应外推误差给大贴图定论。检查区域也必须目视确认为同一个刚性平面。详见references/workflow.md。

不能解决的镜头保留失败报告。归一化坐标不等于提高求解质量；禁止用已知摄影机数据替代原生跟踪结果。
