# video-skills-lab

第25节新增随动放大镜候选：5份真实AEP/视频、750帧检查、65张原生时点/效果开关PNG，含独立Skill副本调用、变参及三个新图片输入。原法光学机制通过技术检查；源课是手动拖动，示例位置关键帧为采样重放适配，人工光学反馈待答。ae-advanced-expressions当前0.7.0 candidate。[报告](evaluations/course2-p25-magnifier-001/summary.json)。

第24节新增双翅铰链/平面飞行部分候选：6个真实AEP/视频、1200帧检查、60张原生检查PNG，含变速及三个新原创图形；蒙版/父对象/路径朝向已原生审计。Particular缺失，整节粒子拖尾未制作；运动反馈待答、摄像机与关键帧仍推定。ae-advanced-expressions当前0.6.0 candidate。见[报告](evaluations/course2-p24-butterfly-001/summary.json)。

来源2第23节新增水平弹簧连接候选：保持课程宽度归一化与线性减幅原法，7份真实AE工程/视频、1320帧独立轨迹检查和70张原生检查PNG；含参数变化、三组新图形和外部透明PNG。技术检查通过，整体课程效果待人工反馈，ae-advanced-expressions为0.5.0 candidate。详见[evidence](evaluations/course2-p23-spring-001/summary.json)及[执行说明](skills/after-effects/ae-advanced-expressions/references/spring-connector.md)。课程视频2803.2秒但音轨仅1401.7065秒，无声尾段未声称完整学习。

第10节replay006已收到“这次方向对，可以保留”，并保留该份可编辑工程和成片；绝对源种子/数字身份、跨输入泛化仍未完成。旧002–005失败记录保留，接受不转移到其他文件。当前完整技能库与全部课程学习尚未完成。按最新要求，入库后清理对应中间产物，只保留交付物、必要素材和验证证据。

独立的 AE / Premiere Pro 高级制作技能实验室。所有脚本、来源、测试输入和回执位于本项目；未读取、修改或依赖 Video Making 内部实现。

Git提交包含Skills、来源、验证记录及代表性可编辑工程/成片；数量以交付清单为准，包含未验收或被否决的历史。第10节已保留原片时点驱动的006及两个seed变参；第14节基线002整体效果获用户认可，另有三组新文字原生变体；第11/12节静态设置仍为候选，不冒充最终动画。已入库的临时数据按清理规则删除，来源链接和验证报告保留。分发范围和跨机器重建说明见[Git交付范围](reports/git-delivery.md)，逐文件校验见[交付清单](reports/git-delivery-manifest.json)。

**当前状态：1个verified、4个candidate。** ae-procedural-motion 0.3.0已按课程第5、6节原法制作、完成变参、三组原创素材、原生编辑重开和独立目录调用；用户确认最终效果符合课程。验证仅覆盖记录的课程配置与PNG分支，录屏播放时码的精确逐帧对齐未确认。第8节ae-advanced-expressions新增五组原生制作及逐帧像素验证，待课程整体视觉验收；摄像机跟踪与PR声音仍待完整课程流程复刻。详见 evaluations/course-p06-final-001/summary.json、evaluations/course-p08-suite-001/summary.json和registry.json。全部课程学习和完整AE/PR技能库未完成。

已访问18条课程页面，并读取B站分P目录，共166个章节条目。第一套课程的第1、5—14节已有画面取证，第5—14节复用已有本机语音工具转录；第11/12节已有静态设置候选，第14节已制作文字选择器动画及三组文字变体，曲线部分估算与源种子未读仍标明。第13节已制作三维粗排候选及三素材变体，主合成后段仍空，不能当最终片头；第15—18节已追加学习与原生候选，第19/20节方法课已读；仍有估算及整片缺口，第2—4节未完成学习，不能称首套课程完成。共有13条来源已开始局部分析，尚未完成全部课程学习。详见 [课程清单](reports/source-catalog.md)、[当前执行报告](reports/status.md) 和 [技能登记](registry.json)。

首个技能：[ae-procedural-motion](skills/after-effects/ae-procedural-motion/SKILL.md)，制作带主控动画、时间延迟和三维深度的轮廓隧道；课程已验范围为矩形轮廓及三组PNG透明度/空间分支。旧三角形、六边形及自制曲线是历史变体，不计入0.3.0课程验收。第7节杂色/Tint扩展仍为candidate。视频素材输入和其他宿主版本仍未验证。

## 工具

- Ego Lite 负责访问页面，已实际工作。tools/browser-*.mjs 是本次任务的分轮操作记录，不能从第一轮重新批量执行。浏览器空间ID不构成可移植依赖。
- Watch 使用现有 `D:/Codex/skills/watch/scripts/watch.py`，已实际完成本地下载、抽帧和字幕检查。未复制或重写下载器、播放器或ASR。它的缓存位于 cache/，不参与技能分发。
- 项目隔离环境 `.venv` 安装了 yt-dlp 2026.10.26 及其默认依赖。基础构建脚本只需 Python 标准库。自制测试图和接触表使用已有 Pillow 12.2.0，目的是提供原创测试输入和检查证据。
- FFmpeg 8.1.2 用于局部高密度抽帧、Adobe帧序列封装和解码检查。
- AE 26.0、aerender 26.0x67、PR 26.0.0.72、Mocha AE 文件已找到；存在文件不等于宿主可执行。

## 接续首个闭环

AE已能正常执行脚本。使用空白工程，或本工具保存且没有未保存修改的课程工程。PR已有BridgeTalk制作通道，候选技能按自身说明运行。

在项目目录打开 PowerShell，生成一个全新的测试目录（已有目录不要复用）：

```powershell
python skills/after-effects/ae-procedural-motion/scripts/build_course_stage.py --stage trim-final --out samples/runs/course-new
python skills/after-effects/ae-procedural-motion/scripts/run_ae.py samples/runs/course-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
python skills/after-effects/ae-procedural-motion/scripts/render_ae.py samples/runs/course-new --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe' --reuse
```

也可在 AE 的“文件 → 脚本 → 运行脚本文件”选择生成的 build.jsx。只有收到 receipt.json、真实 project.aep 并成功重开后，才进行渲染。工具读取AE实际提供的输出模板，优先PNG，否则选原生H.264 15Mbps；本机已实测中文H.264模板。不能假定英文模板名存在。宿主脚本读写权限需按当前AE设置处理。

构建脚本拒绝替换已有内容的工程，避免关闭用户工作。新素材路径由 asset 参数指定；原素材和预合成保留。跨机器迁移时须连同样例资产一起复制，并重新生成其绝对路径配置。

render_ae.py 只接受成功的原生构建回执，通过aerender原生输出H.264或帧序列，再保留为final.mp4。quality.json包含解码、帧数、帧率、画幅和运动存在性检测；回执还逐帧核对延迟旋转、Z深度及形状顶点。技术检测不评价美感，工程可编辑性和视觉对照另有原生审计与审查记录。

当前课程配置为1080方形、30fps、7秒；2→5帧延迟是已测变参，PNG输入使用opacity分支。旧triangle/hexagon、自制画幅和曲线属于历史泛化变体，不在0.3.0课程配置验证范围。按技能tests/protocol.md记录技术与视觉证据，registry不会因为生成脚本自动升级。

## Agent 调用约定

已实测的新需求入口接受brief和parameters，自动选择已验证技能、复制输入素材、保存制作方案，并调用AE及渲染。它只覆盖登记中已验证的能力，超出范围会明确拒绝，不会自动降级成简单阵列。

```powershell
python tools/make_video.py skills/after-effects/ae-procedural-motion/examples/course-request.json --out samples/runs/course-request-new --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe' --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe'
```

当前课程入口实测结果在samples/runs/course-request-001，自动选择0.3.0并输出plan.json、project.aep、final.mp4和quality.json。新成片仍单列视觉复核。samples/new-request.json是历史自制画幅示例，当前严格入口会拒绝其超出课程验证范围的参数。

接到新需求时读取 registry.json，选择有相关场景的技能，检查状态和依赖；候选能力必须明确标为试验。按SKILL制定方案、配置参数、调用宿主、渲染、检查并记录每一步。没有匹配技能时进入学习队列，不能假装已具备功能。PR、Mocha Pro、Projection 3D相关技能尚未实现。

摄像机跟踪按skills/after-effects/ae-camera-tracking/references/invocation.md调用：Agent读取截图选择平面点，脚本负责原生求解设置、合成、像素尺寸适配、渲染与独立漂移检查。该技能是可独立携带的目录，已从复制目录和项目外工作目录实际调用。make_video.py仍只覆盖无人值守的程序化阵列，不能把它当作跟踪技能入口。

Skills 本体是可独立搬走的目录；环境路径由调用端提供。无需数据库、服务或前端。当前CLI已跑通登记能力范围内的需求到方案、Adobe制作与检查；复杂自然语言的参数制定由读取Skills的Agent负责。完整多技能自主制作仍未完成。

## 分发与测试

分发 skills/、tools/、sources/videos.json、来源笔记、原创 fixtures 与 registry.json。不要打包 cache/、.venv/、教程视频、页面会话快照或未经许可的配套素材。此阶段不打包失败运行作为成功示例。

```powershell
python skills/after-effects/ae-procedural-motion/tests/test_requests.py
python tools/prepare_tests.py
python tools/environment_probe.py
```

旧输入测试仅检查build.py历史变体。当前课程技能验收以evaluations/course-p06-final-001/summary.json为准；所有课程总体任务仍未完成。
# 第15节径向背景补充

空间条带的14层原生候选与10层独立调用变体也已制作；两版均为7秒/210帧，保留随机空间位置与噪波演化。Position底值和旧Scale表达式的处理未在课程中完整展示，当前明确是部分流程重建，不能视为已验课程原法；详见skills/after-effects/ae-advanced-compositing/references/course-streaks.md。所有第15节资产仍需总装及跨三种素材验证。

同节极坐标圆环已完成六层原生基线与九层参数变体，保留动态Offset Turbulence和可编辑3D图层；另有独立Skill副本的三层真实制作、渲染与冻结视频负例。参见skills/after-effects/ae-advanced-compositing/references/course-polar.md及evaluations/course-p15-polar-001/summary.json。原片对照反馈单独记录；参数变化不等于三组新素材，本节条带和总装仍待制作。

已制作第15节径向轮廓背景原生基线与速度/种子/时长变体，保留原生RGB曲线、可复用自制AEP模板和独立调用脚本。基线p15-radial-002经原版左/复刻右对照后，用户反馈“整体符合，可以保留”；精确曲线和噪波身份仍是推定。参见skills/after-effects/ae-advanced-compositing/references/course-radial.md和evaluations/course-p15-radial-001/summary.json。该分支保持candidate，三组跨素材验证及本节圆环、条带、总装尚未完成。自包含Skill隔离原生制作、72帧渲染与完整解码已通过。


第15节总装最新进展：11层可编辑AEP、20秒/480帧真实视频及独立调用背景Blend150变体已制作并通过技术检查。最终圆环Z=-2830、条带Z=-12735、轮廓Z=-8230，保留课程白色线性颜色键和选择性折叠。标题沿课程可读Z=-22000，在继承摄影机后方，尚未显示，不能当完整片头；课程一致性保持未通过。详见skills/after-effects/ae-advanced-compositing/references/course-assembly.md。此前“总装未制作”的进度由此更新。圆环002用户整体反馈已接受；不转移至总装或变体。

第16节动态核心已按渐变描边/动画Alpha Matte/控制器关键帧/Tritone→CC Vector Blur→CC Lens真实制作，保留100层可编辑基线及80层/speed65独立调用变体，各151帧。基线001用户反馈“整体符合，可以保留”；精确缓动及三素材尚缺，Skill仍candidate。后半节整体调色、圆环混合与转场仍在处理，未替代完整片头验收。详见skills/after-effects/ae-advanced-compositing/references/course-core.md。

第16节噪波调色新增4秒可编辑组件基线与发光变化版：原生Colorama→Glow，96帧解码及7原生PNG、每帧淡出和编辑重开恢复通过。仅组件技术检查，前段空黑、近似相机和未完成总装仍待处理，未通过课程视觉验收，ae-advanced-compositing0.1.6为candidate。详见evaluations/course-p16-noise-style-001/summary.json。

第16节总装新增p16-style-003与圆环发光0.7变体，保留原生Colorama白标、Screen/FindEdges黑键、Hue315/-37、三层淡出联动及白色隧道深度；各480帧、14个原生检查图与编辑重开通过。仍有后段条带/线条、标题和课程视觉/三素材未验，ae-advanced-compositing0.1.7保持candidate，见evaluations/course-p16-styled-assembly-001/summary.json。


第17节线条已接入总装，基线003与参数变化002通过原生工程/全帧/同帧对照检查；精确课程视觉、首组最终参数及完整标题仍待验证。见evaluations/course-p17-line-style-001/summary.json。


第18节新增高质量Alpha代理工作流，三组件与最终原始合成策略变体通过实际制作；必要的ProRes4444代理较大，以Git LFS交付，克隆后运行git lfs pull。第18节结尾相机/漂移/文字是课外改动，现有20秒粗排不能当最终约25秒片头；第19/20节为方法课，不新增未经制作的效果Skill。
