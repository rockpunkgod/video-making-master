# 第30节验证范围

7组真实AEP与视频1356帧：baseline201、固定椭圆201、动画控制器201、三图片各201、独立复制变体150。60张必要原生PNG已查看。程序全解码，原生每帧核对brush表达式，保存重开编辑恢复；影片历史点和增长检查。三图片原生27采样图用现有Python313的Pillow/NumPy执行evaluations/course2-p30-spiral-001/validate_material_pixels.py，alpha完全相同，预乘RGB最大量化差<=.501。

先提供课程09:00–09:05左原版/右复刻视频，再请求人工整体反馈。精确时间同步未确认，原片为时间线拖动。人工反馈只绑定baseline-001的SHA722f31bf1962237ee7330fad9ad7cbe1a4ebadf07c4d846b9ae327bb076957dc；其他变体不自动继承。当前待答，整个Skill保持candidate。

负例：冻结末帧影片不通过增长；未校正PAR的原生影片不通过历史点。初版误报与失败原生构建记录存evaluations，不用修改视觉掩盖检查错误。

不声称教程像素身份、全部输入组合、精确椭圆缓动、Particular三维或全课程完成。原生项目媒体依赖实际审计完成后才可清理中间渲染；保留AEP/MP4/assets/JSON/必要PNG/Skill代码。
