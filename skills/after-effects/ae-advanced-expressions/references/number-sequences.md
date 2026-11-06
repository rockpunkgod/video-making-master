# 第10节：可编辑十进制/二进制数字序列（candidate）

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=10 。09:32完整十进制表达式，10:50二进制改法；seed201、num262、columns30、DM Sans Bold35均可从画面读出。文本框尺寸[980,420]、左上位置[60,120]/[60,600]和灰底224/255是视口推定，不能称读到了源属性。课程该处停在第0帧，没有播放参考动画。

原法是s=""，n/seed/col引用各文本层自身的Slider；for(i=1;i<=n;i++)内seedRandom(seed+i)，十进制Math.round(random(9))，二进制Math.round(random())；s+=randValue；if(i%col==0) s+='\n'；最后返回s。先拼接字符串以保留前导0且避免超长数字被科学计数法替换。此处没有timeless=true；不要套用第8/9节的固定随机模板，否则会冻住动画。Math.round(random(9))的端点概率与中间数字不同，基线保留原式，不改floor(random(10))冒称同一算法。

scripts/build_number_sequences.py --out全新目录，允许--seed/--num/--columns，默认课程参数。固定1080方形、30fps、5秒、16位，两个原生段落文本层均可编辑；范围限制为1–40列、最多9行，超出先报错而不是静默裁掉数字。更长列表需另做明确排版变体，不假定这些测试覆盖任意长度。

本机原来未找到DMSans-Bold，已从[作者仓库](https://github.com/googlefonts/dm-fonts/blob/main/Sans/Exports/DMSans-Bold.ttf)固定版本取用73452字节静态字体，assets/fonts附OFL/LICENSE及SHA来源。scripts/load_course_font.py只在Windows当前会话注册该文件、广播字体变化，不改注册表；AE native font probe从0匹配变1，每个构建仍检查实际字体与样式，不允许替换字体。已经可用时不重复加载；重登录后需再次检查/加载。其他平台依其原生字体系统，尚未实测。不要假设本机app.fonts支持addFontsFromPath，实际为undefined。

addBoxText默认boxTextPos为[-490,-210]，直接把Position设[60,120]会导致内容越界。001失败布局工程保留；002使用原生读取到的boxTextPos补偿，Anchor置0，对所有帧实际ink边界检查，未修改循环算法。每帧验证字符集/长度/行列、实际字体及内容边界；num真实修改保存重开再还原重开。另用FFmpeg解码全视频统计黑色文字行带，避免仅凭表达式正确就误认为画面未裁剪，这不是OCR或新播放器。

实际测试：p10-decimal-binary-002（201/262/30），p10-variation-001（55/180/20），p10-single-digit-001（77/1/1）。三者均真实工程、150帧视频、原生编辑保存重开与逐帧行带检查通过，后两者从isolated-skill-007副本在实验室外cwd执行。每组10张抽帧已审阅。单字符二进制只有2种字符串，不能要求它产生100种独特画面；num=1的编辑使用1→2→1，不能以1→1冒充编辑测试。

这些是三个参数配置，不冒充三组不同图片素材。独立字符集/不同外部素材适配尚未验证。原版与002的对照位于cache/reviews/p10-original-vs-002-001：左原版暂停、右原法实时求值。课程视口顶部被面板裁掉，因此右侧相应裁剪[0,220,1080,860]仅供局部比较；完整成片无裁剪。未声称精确帧同步或原版播放节奏一致。总体排版已请求用户反馈，在收到并补齐泛化边界前维持candidate。

负例回查：001也被实际原生渲染并完整解码，随后validate_number_rows.py检查出全部150帧为16行而非18行，且边距异常，判定失败；证据在该目录number-pixel-quality.json。因此“视频存在且可解码”不足以证明文字没有裁剪。失败原工程与视频留在本机，未加入正式示例。
