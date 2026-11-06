---
name: ae-advanced-compositing
description: 制作课程原法的三维预合成粗布局、径向轮廓背景和极坐标噪波圆环；保留可编辑原生工程与参数控制。当前candidate，非完整风格化片头。
---

0.1.2候选。第13节组合五个可编辑组件，第15节提供径向轮廓背景与极坐标噪波圆环；均不代表完成整套片头。先按需求选择references/course-composite.md、references/course-radial.md或references/course-polar.md，只加载相关分支。第13节20秒例子后段尚空，不能用于要求完整成片的交付或自动降级替代其他高级效果。

径向背景：scripts/build_radial.py --out全新目录；随后run_ae.py与render_ae.py。默认examples/course-radial.json引用本Skill自制可编辑AEP模板，保留课程Fractal Noise/CC Radial Fast Blur/Unsharp Mask/Find Edges/Curves链。--speed、--seed、--duration为显式变体；基线002整体已获用户认可，精确曲线及跨三种素材仍未验证，详见tests/radial-results.json。不要把此分支当任意素材处理或完整第15节总装。

极坐标圆环：scripts/build_noise_asset.py --out全新目录，随后run_ae.py与render_ae.py。默认examples/course-polar.json复用自制噪波AEP，保留六层3D/Multiply及value+[0,time*100]。偏移速度、Height、数量和种子变体明确记录；每层全帧检查并实际修改、重开、恢复表达式，渲染检查不能替代原片对照。详见references/course-polar.md与tests/polar-results.json；跨三种素材尚未验证。

scripts/build_composite.py --profile examples/course-composite.json --out全新目录，复制五个自制原生AEP和必要素材，保存请求/计划；随后scripts/run_ae.py --ae本机AfterFX路径，再scripts/render_ae.py --aerender本机路径 --reuse。脚本拒绝关闭未保存或不属于本实验的工程。示例和底层工具均在本Skill内，不读取其他视频仓库或教程缓存。

输入为core/noise/contours/lines/dots五角色AEP及SHA、内部合成名、显式素材映射；来源不同先建立新Profile，不静默猜层名。--camera-time-scale、--dot-seed、--noise-width为明确变体。三个core-*.json展示原创PNG替换；不能称任意字体/图片可读性均通过。输出project.aep、final.mp4、请求、原生回执和质量报告，图层/表达式/关键帧保持可编辑。

原生检查480帧摄像机、12个独立点阵延迟、实际关键帧编辑/重开/恢复、媒体缺失和表达式错误。渲染器全解码并自动检查场景阶段和空段。timeRemap负值由本机宿主读回0，不给课程表达式擅加clamp；摄像机原生键时刻量化为1/1024帧，按实际键值另核请求偏差。细节和失败证据见tests/results.json。课程摄像机时间/最终复制数量仍有估算，整体效果未获用户复核，保持candidate。

排错：导入只递归新FolderItem，不假定工程项目按末尾追加；线性颜色键本机实际为ADBE Linear Color Key2；折叠变换按角色启用，Mirror线条维持普通预合成；素材按Profile明确重链接，缺失即失败。验证失败保留报告，另建目录修复。完成入库后按实验室清理规则删除对应临时渲染、抽帧、失败工程和隔离副本，保留交付物、必要素材及验证证据。
