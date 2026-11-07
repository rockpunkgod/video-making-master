# 原创组合演示：共振

输出：samples/composition-demo-001/resonance-002/final.mp4及project.aep，20秒1080p30。以六项已有方法组合新图形、画幅、文字、镜头和声音，实际Adobe制作、保存重开、文字编辑恢复、600帧渲染、像素和音频检查通过。新组合的审美反馈待用户观看；不据此扩大既有Skill的verified范围。

在实验室根目录，以已有NumPy/Pillow环境运行tools/build_resonance_demo.py --out全新目录；按既有run_ae.py调用AfterFX；tools/render_resonance_demo.py调用aerender并封装分轨混音。该渲染器使用本机-help已确认的-mfr OFF/-mem_usage10/50和两线程编码，不降低分辨率。若只是封装失败，用--package-only复用实际600帧，禁止重称未完成的渲染成功。

tools/audit_resonance_demo.py执行保存工程的媒体及时间精度原生检查，--report必须新文件；随后tools/validate_resonance_demo.py --audit同一报告核查对应工程。表明真实同输入valueAtTime时间量化与理想公式的差异，不能用模糊容差掩盖原因。方法、像素检查、声音和失败历史见本目录JSON。

最终保留工程、四份WAV、视频、请求/计划、原生回执及13张PNG。未采用原课视频、原始AI素材、外部插件或现有VideoMaking内部实现。
