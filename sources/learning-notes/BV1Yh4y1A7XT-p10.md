# 第10节：Generating Number Sequences with For-Loop

后续修订（0.3.1）：用户看过002原版对照后回复“排版仍需调整”。该回复绑定002，不撤回也不当作003通过。实测同一可见视口行带：002上块偏高、下块偏低且整体偏右，最大行中心误差7.5显示像素。将此前推定位置[60,120]/[60,600]改为[56,138]/[56,592]，重新实际制作003/variation-002/single-digit-002，原生重开编辑、全150帧解码及内容行带均通过；后两组在isolated-skill-008目录外调用。每组10帧已审阅。同一对照阈值下003最大行中心误差0.5像素、横边界差0；仅证明可见行带几何，不证明源AEP属性、数字身份或原版播放速度。新对照cache/reviews/p10-original-vs-003-001已提供，003用户复核待答。以下保留原始学习和旧版测试历史。

全693.7秒，Watch缓存watch-czbuz5j5；12张全局帧、watch-94owtyd3和watch-zvet78ic共10张指定帧均实际审阅。复用本机已有small模型完整转录并阅读，没有新装或下载ASR模型。ASR把for-loop、seed、Math等识错，代码以09:32和10:50的完整画面为准。

初始尝试对巨大随机数Math.round，在02:30可见科学计数法9.119...e+22；课程改为每次生成一位，转成字符串相接而非加整数。s=""；n/seed/col取本层三滑块；for(i=1;i<=n;i++){seedRandom(seed+i); randValue=Math.round(random(9)); s+=randValue; if(i%col==0)s+='\n';} s。第二层只把random(9)改为random()得到01。源代码没有timeless=true，不能套用第8/9节静态随机模板。Math.round的十进制端点概率较小，这是原法，不暗改成floor。

画面明确：seed201、num262、columns30；DM Sans Bold35；1080方形、30fps、5秒、16bpc。文本段落两端对齐，末行也撑满。文本框[980,420]和位置[60,120]/[60,600]及灰色224来自画面推定，不是读取到了原始AEP属性。10:50—10:55原版停在合成第0帧，只能比较排版，不能当作源播放速度依据；实际AE对同一表达式生成150种文本，验证其时间依赖。

本机AE及系统字体查询原先DMSans-Bold匹配0，未静默换字体。取用作者googlefonts/dm-fonts固定版本4412393b...的Sans/Exports/DMSans-Bold.ttf，73452字节，保留OFL与LICENSE。只用Windows当前会话AddFontResourceEx注册、广播字体变化，不改注册表；AE原生再查匹配1，所有构建实际字体家族DM Sans、Bold、35像素一致。本机app.fonts.addFontsFromPath实测undefined，未假定其存在。

真实输出samples/course-reproduction-006：002基线（201/262/30）、variation001（55/180/20）、single-digit001（77/1/1），各有可编辑AEP和5秒150帧视频。原生逐帧字符集、位数、列数/换行、字体和画面边界全部通过。真实num修改保存重开、还原再重开：262→261→262、180→179→180、1→2→1。最小二进制输入仅2种字符串，不能错误要求它产生100种独特画面；都能时间变化。后两组由isolated-skill-007副本、实验室外cwd执行。三组各10张画面帧已审阅。

第一版001直接用Position定位，忽略addBoxText实际boxTextPos[-490,-210]，导致越界。002读取原生boxTextPos补偿。保留001并实际渲染，普通全帧解码虽过，但独立画面检查每帧只有16行而非18行，且边距内出现异常内容，全部150帧判失败。002及180位变体均18行、单字版2行，逐帧画面检查通过。这是已有失败案例的真实检测证据，不是空白图片自测代替生产验证。

用户要求先原版对照，已展示cache/reviews/p10-original-vs-002-001：左课程10:50—10:55、右复刻；原版视口被AE面板裁掉顶部，因此右侧只在评审视频匹配裁剪[0,220,1080,860]，原始成片完全无裁剪。未宣称精确帧同步；已请求整体排版反馈，当前待答。

融合到ae-advanced-expressions0.3.0的第三单元，不单按视频新增Skill。三次是参数配置，不能冒充三组外部图片素材或任意字符集泛化，仍为candidate。详见references/number-sequences.md与tests/number-sequence-results.json。
