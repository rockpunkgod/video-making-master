# 与Video Making Master制作层衔接

该目录可独立复制，脚本仅用Python标准库及调用方现有FFmpeg/FFprobe；不附带浏览器、播放器、下载器、ASR或新Agent框架。Brief和评审是交换文件，AE/PR执行仍使用现有技能与真实软件接口。

1. 明确目的、约束与选定方向，保存Brief。示例examples/resonance-brief.json为下一版设计提案，不能覆盖现有影片的历史记录。
2. 需要突破惯性时，`python scripts/art_direction.py explore --out 新文件.json`；保存seed，随后人工/Agent真正写出2–3个不同概念。已有方向则跳过。`--seed`复现指定seed。
3. 根据方向选择AE/PR技能。把每个镜头绑定到具体原生操作和已知适用范围；新的画幅/材质/音频/表达式组合先做短段实测，候选能力不能假称已验。制作Brief相符的工程、声音和实际渲染。

   `python scripts/art_direction.py plan --brief brief.json --registry 调用方的registry.json --out 新方案.json`检查镜头时间覆盖与技能名称，并输出方案。registry可省略以便独立携带；省略时不检查调用方技能可用性。此命令不操作Adobe，执行仍须读取所选制作Skill。它也不判断方向是否真正有创意。
4. `python scripts/art_direction.py packet --brief brief.json --video final.mp4 --out 全新目录`。保存全片引用、SHA、规格和盲评提示；实际全解码仅作技术预检。默认不复制影片。提供给评审者的是reviewer-prompt.md、brief.json与原片，别附带源码/历史解释/技术分数。原片移动后重新定位文件，重新渲染后重新建包。
5. 评审者真实正常速度播放与试听，按review-template.json回填。未播放/未听的字段留pending，不为了通过脚本填空白断言。`python scripts/art_direction.py check --packet review-packet.json --review review.json --out review-check.json`核对证据记录。
6. 优先1–3个问题做减法，再重渲染并绑定新SHA复看复听。使用相同观察维度，不把前轮分数告诉独立评审者。按Brief预算停止；交付工程、影片、声音/必要素材和实际评审记录。

记录状态采用两条线：技术预检passed/failed；艺术评审pending/needs_revision/reviewer_approved。自查记录、缺少试听或只有截图时保持pending；检查器只生成证据一致性结果，不写任何Skill的verified状态。未实现的设计方向只属于提案。

在本项目registry中，艺术指导Skill负责意图/方向/评审，ae-procedural-motion、ae-advanced-expressions、ae-advanced-compositing、跟踪及PR技能负责实现。不要为了展示已会的效果强行把它加进镜头，也不要因删除一个特效而宣称另一个技术已掌握。
