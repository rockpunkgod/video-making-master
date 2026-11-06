---
name: ae-advanced-compositing
description: 按课程制作程序化三维合成、空间条带、动态球形核心与分层线条动画候选，输出可编辑AE工程和真实渲染。部分参数仍为推定，非完整风格化片头。
---

0.1.10候选。第13节组合五个可编辑组件，第15节提供径向轮廓背景、极坐标圆环与空间条带候选；均不代表完成整套片头。按需求选择references/course-composite.md、references/course-radial.md、references/course-polar.md或references/course-streaks.md，只加载相关分支。第13节20秒例子后段尚空，不能用于要求完整成片的交付或自动降级替代其他高级效果。

径向背景：scripts/build_radial.py --out全新目录；随后run_ae.py与render_ae.py。默认examples/course-radial.json引用本Skill自制可编辑AEP模板，保留课程Fractal Noise/CC Radial Fast Blur/Unsharp Mask/Find Edges/Curves链。--speed、--seed、--duration为显式变体；基线002整体已获用户认可，精确曲线及跨三种素材仍未验证，详见tests/radial-results.json。不要把此分支当任意素材处理或完整第15节总装。

极坐标圆环：scripts/build_noise_asset.py --out全新目录，随后run_ae.py与render_ae.py。默认examples/course-polar.json复用自制噪波AEP，保留六层3D/Multiply及value+[0,time*100]。偏移速度、Height、数量和种子变体明确记录；每层全帧检查并实际修改、重开、恢复表达式，渲染检查不能替代原片对照。详见references/course-polar.md与tests/polar-results.json；跨三种素材尚未验证。

空间条带：scripts/build_streaks.py --out全新目录，随后run_ae.py与render_ae.py。默认examples/course-streaks.json；14个3D噪波层、零漂移、Width24.6/Height2270、Scale503、Z0..2000。Position底值及旧Scale表达式的处理未被课程明确展示，本实现是部分流程重建；不得作为已证实课程原法。先读references/course-streaks.md，实际证据见tests/streaks-results.json。

scripts/build_composite.py --profile examples/course-composite.json --out全新目录，复制五个自制原生AEP和必要素材，保存请求/计划；随后scripts/run_ae.py --ae本机AfterFX路径，再scripts/render_ae.py --aerender本机路径 --reuse。脚本拒绝关闭未保存或不属于本实验的工程。示例和底层工具均在本Skill内，不读取其他视频仓库或教程缓存。

输入为core/noise/contours/lines/dots五角色AEP及SHA、内部合成名、显式素材映射；来源不同先建立新Profile，不静默猜层名。--camera-time-scale、--dot-seed、--noise-width为明确变体。三个core-*.json展示原创PNG替换；不能称任意字体/图片可读性均通过。输出project.aep、final.mp4、请求、原生回执和质量报告，图层/表达式/关键帧保持可编辑。

原生检查480帧摄像机、12个独立点阵延迟、实际关键帧编辑/重开/恢复、媒体缺失和表达式错误。渲染器全解码并自动检查场景阶段和空段。timeRemap负值由本机宿主读回0，不给课程表达式擅加clamp；摄像机原生键时刻量化为1/1024帧，按实际键值另核请求偏差。细节和失败证据见tests/results.json。课程摄像机时间/最终复制数量仍有估算，整体效果未获用户复核，保持candidate。

第15节总装：先读references/course-assembly.md，再运行scripts/build_assembly.py --out全新目录，随后run_ae.py与render_ae.py。自包含六个原生输入，保留11层、四色渐变/原生曲线、径向淡出和后期深度调整。标题仍位于摄影机背后，不能作为完整片头交付；tests/assembly-results.json区分技术通过与课程视觉未通过。--background-blend为显式变体。

第16节动态核心：先读references/course-core.md，再运行scripts/build_core.py --out全新目录，随后run_ae.py与render_ae.py。默认100层、动态Alpha Matte、Phase=time*50及Tritone→CC Vector Blur→CC Lens；--count/--speed为显式变体。六个原生检查帧、每层151帧公式检查与控制器编辑重开恢复均实际执行，基线001整体获用户认可。精确缓动和三组素材仍缺，保持candidate，见tests/core-results.json。

排错：导入只递归新FolderItem，不假定工程项目按末尾追加；线性颜色键本机实际为ADBE Linear Color Key2；折叠变换按角色启用，Mirror线条维持普通预合成；素材按Profile明确重链接，缺失即失败。验证失败保留报告，另建目录修复。完成入库后按实验室清理规则删除对应临时渲染、抽帧、失败工程和隔离副本，保留交付物、必要素材及验证证据。

第16节噪波调色：先读references/course-noise-style.md，运行scripts/build_noise_style.py --out全新目录及通用原生执行/渲染。保留原生Colorama色标；--glow-intensity为显式变体。默认4秒96帧仅展示组件，前段可能为空黑；不作为总装或课程视觉一致的验收。见tests/noise-style-results.json。

第16节总装：先读references/course-styled-assembly.md，运行scripts/build_styled_assembly.py --out新目录及通用原生执行/渲染。组合动态核心、噪波与原生圆环调色，链接三层淡出并制作白色轮廓深度；--polar-glow-intensity为变体。色相回读前刷新通道控制，详见分支诊断。20秒候选后段和标题未完成，不作为完整片头交付，见tests/styled-assembly-results.json。

第17节隧道延续：先读references/course-tunnel-style.md，再运行scripts/build_tunnel_style.py --out新目录与通用原生执行/渲染。关闭首个静止轮廓，静态移动Null、扩展Spacing，叠加time*20+value旋转及淡出；--rotation-speed为显式变体。精确曲线和摄影机未确认，后段条带/线条与标题未完成，保持candidate。

第17节条带延续：先读references/course-streak-style.md，运行scripts/build_streak_style.py --out新目录及通用原生执行/渲染。按课程先处理单层再复制为7层，内层键白，外层原生RGB曲线与两层Glow，X缩放收拢；--glow-intensity为变体。曲线/键时为画面估读，后段线条与标题未完成，仍candidate。


第17节线条延续：先读references/course-line-style.md，运行scripts/build_line_style.py --out新目录及通用原生执行/渲染。两组19路径保留原表达式，TrimEnd从1%展开、错开7源帧，原生Tritone/FindEdges/Curves/Hue及双Glow；--glow-intensity为变体。默认原生TIFF序列经FFmpeg编码以避免本机直接H264饱和色损失。路径总数、曲线/时序和首组最终参数仍有推断，未获课程整体验收，candidate。
