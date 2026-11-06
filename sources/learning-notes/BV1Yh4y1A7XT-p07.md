# 第7节：Effects and Layers

全394.1秒已通过Watch下载，18张场景帧全部审阅，复用已有faster-whisper small完成全片转录。随后补看13张指定帧：cache/watch/watch-_t0xs182和watch-_8modxt3；补齐03:50—06:10的关键界面，未覆盖每次鼠标操作。

00:24与03:17的画面保留第6节最终stepRep_2，合成暂停在02:02。它为上一节提供独立静态参考：实际新制作的第62帧轮廓对照通过，见course-p06-final-001/summary.json。该图不代表第7节新数字块效果已复刻。

本节可见新Fractal Noise预合成与黑白方块；字幕解释Blocks噪声、约2000对比度、复杂度1、反相，Evolution使用time*5，Random Seed用seedRandom(...,true)与random(1000)避免逐帧跳种子。语音识别把专业词误作factor/C value等，具体枚举与表达式要读界面，不能直接执行转录文本。

后半字幕讲把原形状的Position/Rotation/Scale/Opacity表达式复制到噪声Solid，Solid没有Trim Paths；禁用Opacity表达式，Rotation Z spacing重置为0，Scale interval也可归零。用Multiply混合移除白色背景，重复得到数字块隧道；再给某一层加Tint改变黑色，或替换为插画、其他纹理。尚未逐项读取这些末段数值与GUI设置，未制作或验证该效果。

指定帧确认：01:20 Fractal Type=Strings、Noise Type=Block、Invert开启、Contrast=2000、Complexity=1；02:30明确seedRandom(5,true); random(1000)，03:58复制到主合成后的种子已改为1。04:28 Rotation Z spacing与Scale interval均为0，Opacity表达式保留但禁用；04:50主合成20个FN层均Multiply，摄影机沿用上一节。05:40给FN15加Tint时颜色框为00FFDD；06:00又给FN18改成蓝色，最终蓝色精确RGB未读出。黑白隧道阶段与后续Tint实验分开，不能将暂时青色当成最终蓝色。

原生能力实际探测见evaluations/course-p07-probe-001：ADBE Fractal Noise存在，Random Seed的matchName为ADBE Fractal Noise-0027。对枚举的首次推测16实测显示“地形”，不是Strings；保留enum-values-ui.png。改19后本机原生界面实际显示“字符串”，Noise Type=1显示“块”，见strings-ui.png。部分分组头为NO_VALUE，未当数值使用。

已按黑白阶段制作samples/course-reproduction-003/p07-blocks-002：原生22层（摄影机、controls、20个FN Solid），16位、1080方形30fps7秒；复制第6节已验表达式，禁用Opacity和主控旋转表达式而不删除，空间控制归零。20层种子值不同且210帧内恒定；Evolution=time*5、Z间距1000、Scale100%逐帧原生核验误差0。实际种子编辑813→923，保存重开，再还原813重开通过。原生视频210帧全解码，14张接触帧已审阅，观察到白底黑块向前穿越且中心保持深度密集。种子结果依赖AE层身份，未声明和教程逐像素相同。

首次p07-blocks-001因缺少PNG输出模板停止，失败回执和failed-project.aep保留；002改用已实测原生H.264模板成功。此扩展仍为candidate：没有三组跨素材验证、独立目录执行、教程参考定量对照或用户视觉验收；不随第6节0.3.0通过自动升级，不宣称已完成最终Tint变体。

续作补证：额外05:41—05:49的9张指定帧全部审阅（watch-46dmgj2c）；05:43—05:46颜色框读出0057FF，解决上述蓝色参数缺口。FN15改蓝后Tint复制给FN18。对应--course-tint已实际制作samples/course-reproduction-003/p07-tint-001，22层、20个固定不同种子、原生Tint颜色保存重开检查通过；210帧视频全解码，14张抽帧显示黑/灰/蓝层次及向前推进。已请求用户整体效果反馈，未自动认可。上述“未制作最终Tint”是前一阶段记录，现由真实工程补齐；仍缺三组泛化等条件，保持candidate。
