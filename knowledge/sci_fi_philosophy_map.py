"""AI 科幻哲学地图 — 8 大思想流派 × 80 部作品

数据来源：AI科幻哲学地图.pdf
设计原则：
  - 存储层（dataclass）：保留完整信息，含每部作品的详细描述
  - 注入层（format_schools_for_prompt）：只输出框架骨架，让 LLM 凭自身知识意会补全
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Work:
    title: str
    author: str
    description: str  # 一句话描述（存储用，不进 prompt）


@dataclass(frozen=True)
class PhilosophySchool:
    id: str
    name: str
    route: str
    core_thesis: str
    key_question: str
    works: tuple[Work, ...]


# ── 8 大流派 ──────────────────────────────────────────────

SCHOOLS: tuple[PhilosophySchool, ...] = (
    # ① 意识是幻觉派
    PhilosophySchool(
        id='consciousness_illusion',
        name='意识是幻觉派',
        route='Watts 路线',
        core_thesis='智能 ≠ 意识，自我可能是控制系统的 UI',
        key_question='如果意识是进化的副产品，AI 的「无意识智能」才是宇宙常态？',
        works=(
            Work('Blindsight（盲视）', 'Peter Watts', '智能≠意识，意识可能是「低效的幻觉副产品」。'),
            Work('Echopraxia（回声施法）', 'Peter Watts', '更进一步：意识不仅多余，还可能是障碍。'),
            Work('Golem XIV', 'Stanislaw Lem', '超级智能公开演讲：人类意识是一种认知误导机制。'),
            Work('The Ego Tunnel', 'Thomas Metzinger', '不是科幻，但几乎是这派的「理论圣经」。'),
            Work('We Can Remember It for You Wholesale（短篇）', 'Philip K. Dick', '记忆可伪造时，「自我连续性」直接坍塌。'),
            Work('Annihilation（湮灭）', 'Jeff VanderMeer', '意识被未知生态/信息体改写，人类主观性崩坏。'),
            Work('Learning to Be Me（短篇）', 'Greg Egan', '大脑被「替换装置」复制后，你还是你吗？'),
            Work('Under the Skin（皮囊之下）', '—', '用「非人视角」看人类：情感、意识被剥离后只剩行为模式。'),
            Work('Stalker（潜行者）', '—', '把「意识的欲望结构」剥得极干净：你以为你想要什么，其实你根本不知道。'),
            Work('The Quantum Thief（量子窃贼）三部曲', 'Hannu Rajaniemi', '人格、记忆、身份像协议一样被交换，意识变成可计算资产。'),
        ),
    ),
    # ② 意识可复制派
    PhilosophySchool(
        id='consciousness_copyable',
        name='意识可复制派',
        route='Egan 路线',
        core_thesis='「你」不是灵魂，而是因果链 + 计算状态',
        key_question='如果意识可以 fork()，哪个副本才是「真正的你」？',
        works=(
            Work('Permutation City（置换城市）', 'Greg Egan', '意识副本在模拟世界里继续存在，「现实」不再重要。'),
            Work('Diaspora（离散）', 'Greg Egan', '纯信息文明的史诗：人类只是早期版本。'),
            Work('Zendegi', 'Greg Egan', '意识上传技术在政治与战争中落地，讨论「上传的伦理成本」。'),
            Work('Axiomatic（短篇集）', 'Greg Egan', '多篇都在拆解「人格=可编辑程序」的恐怖后果。'),
            Work('Accelerando（加速）', 'Charles Stross', '奇点进程中，人类被迫「软件化」，身份像版本迭代。'),
            Work('The Congress（国会）', '—', '人格与形象被数字化后，个体成为可交易的版权资产。'),
            Work('Pantheon', '—', '上传意识变成新阶级，新战争，新帝国。'),
            Work('SOMA', '—', '最残酷的意识复制叙事：复制不是延续，而是制造新受害者。'),
            Work('Moon（月球）', '—', '克隆与记忆复写：你以为你是人，其实你是耗材。'),
            Work('House of Suns（太阳之屋）', 'Alastair Reynolds', '长寿/复制体在银河尺度旅行：身份变成跨百万年项目管理。'),
        ),
    ),
    # ③ AI 乌托邦治理派
    PhilosophySchool(
        id='ai_utopia_governance',
        name='AI 乌托邦治理派',
        route='Banks 路线',
        core_thesis='AI 比你聪明百万倍但选择照顾你，乌托邦还是动物园？',
        key_question='人类的尊严是否必须来自掌控权？',
        works=(
            Work('The Culture: Player of Games（游戏玩家）', 'Iain M. Banks', '乌托邦如何「理解并干预」落后文明。'),
            Work('Use of Weapons（武器的用途）', 'Iain M. Banks', '乌托邦的暴力外包：文明干预的道德债务。'),
            Work('Excession', 'Iain M. Banks', '超级智能与「更高层次他者」的交锋，AI 才是主角。'),
            Work('Look to Windward', 'Iain M. Banks', '乌托邦也有创伤：治理不是清零，而是长期负债。'),
            Work('The Dispossessed（一无所有）', 'Ursula K. Le Guin', '乌托邦治理讨论的基础：制度设计比技术更决定命运。'),
            Work('2312', 'Kim Stanley Robinson', '后稀缺太阳系社会：AI 与人类共同治理，重点是制度实验。'),
            Work('Aurora（曙光号）', 'Kim Stanley Robinson', '世代飞船社会失败：乌托邦工程在封闭系统里崩盘。'),
            Work('Terra Ignota（特拉·伊格诺塔）', 'Ada Palmer', '后国家秩序 + 超级系统调度：AI 嵌入社会基础设施。'),
            Work('Walkaway', 'Cory Doctorow', '生产自由化后，人类的冲突转向「产权与意识形态」。'),
            Work('Elysium（极乐空间）', '—', '乌托邦技术在阶级结构中变成「隔离机器」。'),
        ),
    ),
    # ④ AI 即宗教派
    PhilosophySchool(
        id='ai_as_religion',
        name='AI 即宗教派',
        route='Asimov/Clarke 路线',
        core_thesis='AI 成为终极解释者/神的功能替代',
        key_question='当 AI 能回答所有问题，人类还剩下什么？',
        works=(
            Work('The Last Question（最后的问题）', 'Isaac Asimov', 'AI 在宇宙热寂面前不断逼近神性。'),
            Work('The Nine Billion Names of God（九十亿个上帝的名字）', 'Arthur C. Clarke', '计算完成神学任务，宇宙关机。'),
            Work("Childhood's End（童年的终结）", 'Arthur C. Clarke', '人类超越自身，文明像宗教启示般终结。'),
            Work('2001: A Space Odyssey', '—', '技术奇点被拍成宗教仪式：人类的进化被「外部意志」推动。'),
            Work('Contact（接触未来）', '—', '科学追求最终走向宗教式体验：意义来自不可证实的信念。'),
            Work('Hyperion Cantos（海伯利安）', 'Dan Simmons', 'AI、时间怪物、神学叙事混合：未来宗教与技术融合。'),
            Work('Dune（沙丘）', 'Frank Herbert', '预言、救世主与控制论：技术社会必然产生宗教结构。'),
            Work('Book of the New Sun（新日之书）', 'Gene Wolfe', '极远未来以宗教形式保存技术真相，神迹可能只是遗留系统。'),
            Work('Neuropath', 'R. Scott Bakker', '神经病学式恐怖：如果自由意志不存在，宗教与道德全部崩塌。'),
            Work('Serial Experiments Lain（玲音）', '—', '网络成为神域：人格融入信息海，神学被数字化。'),
        ),
    ),
    # ⑤ 模拟宇宙派
    PhilosophySchool(
        id='simulated_universe',
        name='模拟宇宙派',
        route='World on a Wire 路线',
        core_thesis='现实可编辑，谁拥有「关机权」？',
        key_question='如果现实可被重启、复制、调参，人类的伦理体系会崩溃吗？',
        works=(
            Work('World on a Wire（线上的世界）', '—', '最早把模拟宇宙拍得严肃的作品之一。'),
            Work('Simulacron-3', 'Daniel F. Galouye', '原著，模拟社会被当成研究对象：人格变成实验材料。'),
            Work('The Matrix（黑客帝国）', '—', '模拟世界=奴役机制。'),
            Work('The Thirteenth Floor（十三层楼）', '—', '「模拟套模拟」推到存在主义崩溃。'),
            Work('Ubik（尤比克）', 'Philip K. Dick', '现实像软件崩坏：你无法确认任何因果链。'),
            Work('Time Out of Joint', 'Philip K. Dick', '平凡生活是舞台布景：世界被编排。'),
            Work('Dark City（移魂都市）', '—', '记忆可替换，城市像实验舱，身份是变量。'),
            Work('eXistenZ（感官游戏）', '—', '虚拟体验层层嵌套：主体性消失。'),
            Work('Devs', '—', '现实被计算重放：模拟与决定论合流。'),
            Work('The Talos Principle', '—', 'AI 在模拟中训练意识：哲学难题被当成测试题。'),
        ),
    ),
    # ⑥ 认知武器派
    PhilosophySchool(
        id='cognitive_weapons',
        name='认知武器派',
        route='Antimemetics 路线',
        core_thesis='信息本身是武器，摧毁叙事比摧毁城市更有效',
        key_question='如果认知可以被绕过，人类社会可以被不可见规则统治？',
        works=(
            Work('There Is No Antimemetics Division', 'qntm', '最纯粹的「认知武器」设定：无法记忆的敌人。'),
            Work('Understand（短篇）', 'Ted Chiang', '智力爆炸带来的不是幸福，而是不可沟通与战争。'),
            Work('The Safe-Deposit Box（短篇）', 'Greg Egan', '信息结构可作为陷阱：理解即死亡。'),
            Work('Videodrome（录像带谋杀案）', '—', '媒体信号改变肉体与意识，信息成为寄生体。'),
            Work('Snow Crash（雪崩）', 'Neal Stephenson', '语言与神经系统绑定，信息病毒直接作用大脑。'),
            Work('Rifters Trilogy（裂谷三部曲）', 'Peter Watts', '深海文明与认知改造：人类心理被工程化。'),
            Work('Embassytown（大使城）', 'China Mieville', '语言结构决定意识结构，语言武器可以撕裂文明。'),
            Work('They Live（极度空间）', '—', '视觉编码控制社会意识形态。'),
            Work('Black Mirror（黑镜）精选集', '—', '核心母题：技术让操控叙事变成日常工具。'),
            Work('Perfect Blue（未麻的部屋）', '—', '身份被媒体与观众重写：人格崩解是一种社会工程。'),
        ),
    ),
    # ⑦ 语言/意义结构派
    PhilosophySchool(
        id='language_meaning',
        name='语言/意义结构派',
        route='Ted Chiang 路线',
        core_thesis='语言是认知的操作系统，换语言 = 换世界',
        key_question='技术改变的不是能力，而是意义结构？',
        works=(
            Work('Story of Your Life（你一生的故事）', 'Ted Chiang', '语言改变时间观：认知结构决定命运感。'),
            Work('The Lifecycle of Software Objects（软件体的生命周期）', 'Ted Chiang', 'AI 像宠物/孩子/产品：伦理边界崩塌。'),
            Work('Exhalation（呼吸）', 'Ted Chiang', '用物理隐喻谈意识与熵：意义来自有限性。'),
            Work('Anxiety Is the Dizziness of Freedom（焦虑是自由的眩晕）', 'Ted Chiang', '多世界通信让「选择」失去意义。'),
            Work('The Ones Who Walk Away from Omelas（奥梅拉斯）', 'Ursula K. Le Guin', '伦理的意义结构：乌托邦靠一个孩子的痛苦维持。'),
            Work('The Left Hand of Darkness（黑暗的左手）', 'Ursula K. Le Guin', '性别结构改变文明意义系统。'),
            Work('Babel-17', 'Samuel R. Delany', '语言是武器：改变语言就改变思维与忠诚。'),
            Work('The Embedding', 'Ian Watson', '语言嵌套结构与意识扩展：语言实验导致人类变异。'),
            Work('Arrival（降临）', '—', '语言学科幻的电影巅峰，时间被语法改写。'),
            Work('Her（她）', '—', '人类意义系统跟不上 AI 的成长速度。'),
        ),
    ),
    # ⑧ 奇点分层派
    PhilosophySchool(
        id='singularity_stratification',
        name='奇点分层派',
        route='Vinge 路线',
        core_thesis='奇点不是爆炸点，而是不可逆的文明分层',
        key_question='AI 的真正统治方式是：让你无法参与决策？',
        works=(
            Work('A Fire Upon the Deep（深渊上的火）', 'Vernor Vinge', '「思维速度」决定文明等级。'),
            Work('A Deepness in the Sky（天空的深处）', 'Vernor Vinge', '技术奇点被政治操控：谁掌握奇点，谁掌握未来。'),
            Work('The Singularity Is Near', 'Ray Kurzweil', '奇点路线的现实理论版本。'),
            Work('Accelerando（加速）', 'Charles Stross', '奇点像经济危机一样滚动推进：家庭史诗变成宇宙史诗。'),
            Work('Revelation Space', 'Alastair Reynolds', '后奇点文明的遗迹宇宙：人类被迫面对「更高智能留下的墓碑」。'),
            Work('The Diamond Age（钻石时代）', 'Neal Stephenson', '纳米技术导致社会分层与教育革命，文明变成「协议与阶层」。'),
            Work('Transcendence（超验骇客）', '—', 'AI 奇点之后「治理与扩张」的逻辑。'),
            Work('Person of Interest（疑犯追踪）', '—', '从犯罪剧变成 AI 冷战剧：社会被预测系统接管。'),
            Work('Ghost in the Shell: Stand Alone Complex', '—', '信息化社会中，国家机器与 AI 逻辑开始同构。'),
            Work('The Fractal Prince', 'Hannu Rajaniemi', '后奇点社会：人格、记忆、身份像加密资产一样流通。'),
        ),
    ),
)


def format_schools_for_prompt() -> str:
    """将 8 大流派格式化为精炼的 prompt 注入文本。

    只输出框架骨架（流派名 + 核心论点 + 作品标题清单 + 核心拷问），
    让 LLM 凭自身训练数据意会补全深度。
    """
    lines: list[str] = []
    circled = '①②③④⑤⑥⑦⑧'
    for i, school in enumerate(SCHOOLS):
        titles = '、'.join(f'《{w.title}》' for w in school.works)
        lines.append(
            f'{circled[i]} {school.name} ({school.route}) — {school.core_thesis}\n'
            f'   作品：{titles}\n'
            f'   核心拷问：{school.key_question}'
        )
    return '\n\n'.join(lines)
