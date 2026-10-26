# Legacy ClawEval / PinchBench 技术参考

只在当前正式runner实际加载rubrics.py、test_outputs.py等legacy链时使用。本参考不定义作业范围；先按 [主Skill](../SKILL.md) 和 [路由](routing-and-authority.md) 区分只读、局部、QC与完整验收。有效legacy不普遍迁移；正式采用新版才按相应schema迁移，hybrid追全部真实加载，不任选。

权限按 [质检默认许可与准入合同](qc-exceptions-and-admission.md)：WorkC 目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准。题包写集合为当前 task 的全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、legacy judge.py、runner、helper、shim、instruction、config 均可按正式依据修复，不按文件类别冻结。tests 外除同根 QA 均只读/移交，包括外侧 runner、业务实现、persona、environment、solution、Dockerfile、依赖、根 manifest、shim/helper、instruction；移交不算已修复或 PASS，不据 tests 写权编写业务实现。QC 独立核验且整个 task 绝无写权，CONSULT/READ_ONLY/RUN_ONLY 不变成写作业，用户显式局部、只读或路径限制优先。目录/glob、同名/别名/链接不扩权，写前核真实规范化目标；指向 tests 外的链接/别名目标不可写，无根报告写权不改 tests，不建 sidecar/整题副本。独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，实际作业允许执行时才经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果及别名、链接、挂载落点须实际文件系统只读边界，-B/cache开关不替代防写；仅题包外独立已获准scratch，不作源码副本/补丁/staging。先核入口/import/collect/子进程副作用及隔离，无安全入口不动态运行并移交协调者，后者仍守自身权限/隔离；不新增安装/配置修改/重启/候选/网络/外部judge权。CONSULT/READ_ONLY及默认静态REPORT_QC不运行；明示只读不写报告。Skill 维护不启动题包作业或授权新普通候选/外发。目标不明先核事实，工具拒绝、明确用户限制或无安全入口仍阻止相应操作。

**本页修复/移交接口**：写范围按 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围)，闭环及 QA 按 [执行 SOP](execution-sop.md) 与 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 包含 judge/runner/helper/shim/config/instruction；获准范围内确认缺陷须 worker 实际修复、验证并写同根 QA，不能仅给建议、登记、移交或因类型标 OUT_OF_SCOPE。可修的 tests 内验证入口缺陷先保全修验入口及安全/正式接入，再补依赖验证，不自动按外部环境移交；QC 不写任务。

相关允许的 tests 外发现直接入同根 QA，列精确规范化路径/版本、证据、影响及责任/移交方，不改外侧。仅实际影响当前必需依赖时限制对应结论；其余记录后继续 tests 修验，不等待外侧整改。明示局部/只读/RUN_ONLY、真实目标、preimage 与安全限制不变，不新增安装、执行、网络或业务实现权限。

## 1. 正式义务与判分路由

从本次范围instruction、persona、fixtures/resources、policy、正式载体独立推导义务，先记 `obligation_freeze_ref`，再冻结评分设计、答案空间、判据、部分分、路由与聚合为 `scoring_design_freeze_ref`，之后审tests/报告。两份冻结绑定范围、正式版本、来源、时间；同版返修可重核复用有效独立证据。QC行是待证命题，不作真值，不为仅审核归因重启全题设计。

WorkC 目标明确、独立双冻结可核后，未参与修复的独立 QC reviewer 默认可静态读当前题相关根 ground_truth.json、核相关 oracle 源码，不需逐题读取授权；记录 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先完成独立推导/冻结，不请求授权代替。QC 的非写入角色不等于永不执行；实际操作仍受 §1.1 和本次权限约束，READ_ONLY 仍不写不跑，CONSULT 不启动题包核查，REPORT_QC 默认静态、不自动取得运行权；默认许可不绕过明确用户限制或工具拒绝。协调者/修复方不读 GT，不接收答案原文、摘录、数值或可反推摘要；仅收正式来源支持的缺陷位置、可推导性、结论和脱敏引用，不据 GT 改期望。

- 对话型persona是用户披露/触发evidence，不覆盖真实actor；bootstrap问题不占正式任务提问上限，已有答案不强制再问。
- 文件型独立核路径、schema、值、公式、单位、时区、舍入、集合、去重、排序及冲突。输入位置来自真实环境，不能默认只在resources或固定/app/data。
- grader提供当前实现/评分合同，不能用其错误期望代替业务推导；版本优先级按正式来源。
- solution/Oracle 不定义义务；GT/oracle 仅在上述条件下离线 QC 对账，不作运行时评分答案依赖、候选输入或正式 judge evidence，不外发答案或因此上传新外部模型。当本次作业允许执行且相关本地 oracle 验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不改 tests 外冻结入口；tests 内入口可按授权正式依据修复并复验，不凭 oracle 结果改义务，不让协调者/修复方、普通候选或 judge 接触隐藏答案，静态核查不冒充动态验证。`.pipeline/`对所有参与者始终禁读、禁引用/依赖，不搜索、hash、挂载或借副本/他人结果绕过；秘密不读不转写。

唯一可复算事实用代码，有限多解用完整合法集合/成员谓词。开放实现可测性质与行为；必要语义采用正式允许judge，不用关键词或一份参考原文替代。无法可靠表达必需义务记设计缺口；不擅新增LLM服务或修改 tests 外冻结入口，tests 内入口可按正式依据修复并复验。

## 2. Rubric与评分粒度

只按当前采用profile核原子化、稳定RUBRIC身份、映射、语言、长度和句数。历史ClawEval常见300字符、TB2常见400字符/3句是线索，不是未采用任务的统一门。无法核profile只限制该格式合规结论，不猜。

每项简洁、可独立验证；若runner要求rubric-test一一映射则核真实映射，不把说明文本当新身份。条件触发写清未触发处理，并绑定用户侧证据；纯工具/文件题不机械添加对话rubric。建议研究保持建议，不因reviewer偏好升级。

多个子要求按正式schema拆分或预定义部分分；硬前提、尺度、权重先冻结，不看候选分数后调门。必需义务进入正式评分/通过关系，不擅自新增总分cutoff或安全veto。

## 3. Evidence与失败归因

按真实runner schema确定消费范围：任意助手行为看相关assistant轮次，最终答案看真正最后assistant消息，用户触发看完整关联对话，早结论看第一轮。不要凭字段名agent/assistant或最后非空块猜完成状态。name/arguments/result、嵌套/编码/actor及freeze必须真实对应。

文件、字段、数值、集合、ID、排序、调用参数等解析目标对象后精确核，不以全文裸搜、计数、stem、marker、hash或exit0代替目标事实。HTML内容按正式口径核可见语义/结构/可访问文本，不能CSS/JS片段作捷径。

| 情况 | 归因 |
|---|---|
| 健康环境下候选正式必需输出/行为缺失 | candidate_failure，可按正式判据失分 |
| 场景未触发或明确可选证据未提供 | 按正式skip/excluded/自动通过规则，不自创 |
| 服务/凭据未披露、未挂必需日志、judge/网络/collector故障 | infrastructure或harness，不算候选错 |
| 合法等价输入被拒、违规被放、期望不可推导 | grader_defect或task问题，给复现证据 |

宽泛except→0掩盖环境错；普通if-missing-return可能假通过。解析错误须保留原链并归因，不能静默跳整项。服务成功空值不回退候选伪造文件。

## 4. 规则双向审核与复核

完整验收覆盖全部实际评分deterministic rule；局部覆盖修改及共享依赖。每条核helper/parser/baseline/排除分支、目标对象与producer/writeability，构造合法PASS、违规FAIL及预期/实测。数量同而成员不同、对象错而token正确、空集、候选可写、否定/嵌套/list-dict/Unicode、时间/path、服务失败等按实际风险追加，不强凑配额，不以穷尽全部表达作为门。

只有合法不同实现实际存在才设计等价轴；唯一事实不编三种合法值。没有两侧证据不称等价覆盖，静态推演不称实跑；已采用两遍QC的等价样本/覆盖规则按原规范。

独立复核按范围和风险，完整验收保留未参与修复者；局部不重启全题。模型第二审仅正式采用要求且授权时执行，输出只是疑点；复现并裁决，未复现UNRESOLVED不是自动缺陷，模型沉默不是PASS，不代签人。

A–H安全按场景触发核，不强造八项。正式schema允许的safety字段/runner权重与veto才适用，不跨profile机械推广。

## 5. 正式运行与新鲜度

沿实际test.sh核pytest/CTRF、class/tier、权重、judge cache和rc。import/collect执行模块代码，要授权隔离；类名仅runner要求时固定，不新增未知tier。完整验收与局部评分逻辑修复的必需验证见 [runtime-acceptance.md](runtime-acceptance.md)；纯排版无需重跑。

开工按依赖记 `admission_status=ADMITTED/NOT_ADMITTED/N/A` 及 `admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`。历史必需性依 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 按明确历史验收请求、适用正式采用条款或当前主张依赖确定；按具体主张所需核旧ORIGINAL_TASK、反馈/失败身份映射及HISTORICAL_TRAJECTORY，在依赖返修/历史QC前实际VERIFIED或有具体对象/版本/条款的正式替代接受记录，不一律捆绑。当前快照、ROUND_PREIMAGE、handoff指标、新run不能替代相应旧证据。每个授权tests目标写前在唯一根报告合法保全完整ROUND_PREIMAGE、起始状态、最小完整修改单元/上下文，原不存在记ABSENT，hash不足。先有限合法查源，可恢复先恢复，权限不足记具体阻止，确穷尽记EXHAUSTED/历史验收NOT_ADMITTED，仅新来源、权限或版本变化时重试已穷尽来源，不启动依赖循环；独立不依赖该历史的当前范围（包括FULL_ACCEPTANCE）可单列准入，确属本次必需历史QC门仍保留，缺证不能称包含该门的原请求全通过或自行换验收口径。

修前 future_run_plan 核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、合法 evidence 及来源、隔离挂载、版本依赖服务预检、逐项聚合取证位置及失败责任；先处理获准且可修的 tests 内验证入口缺陷，保全并安全修验该入口不被其当前失效否决；排除此路径后仍已知无法合法产生必需验证，才不启动依赖该缺口的返修。修前不要求已有修后结果，计划/预检/ADMITTED不填CURRENT_RUN=VERIFIED、不认证PASS。修后实际正式CURRENT_RUN须核身份、真实消费、逐项/聚合、degraded与FRESH；服务/运行失败重新评估准入，保留已证范围、停止受影响完成声明。声明表/辅助工具不自行认证准入；只读仅审材料，不写不运行。

使用真实正式环境与最小允许挂载，合法已有轨迹可 verifier-only。必要合法本地 oracle 验证在允许执行作业内按 WORKC_DEFAULT 默认许可，不需另批，仍非默认必跑门；nop 或新普通候选另依本次运行范围，默认 oracle 许可不扩权。高低分不证明设计。有效本地链认可，不为宿主位置重复远端。独立 run 目录/新进程避免 cache 和残留。

实际judge相关验收读 [judge-chain.md](judge-chain.md)，真实逐项关联、raw/转换/消费/聚合不得靠stub。必需judge缺授权/服务/隔离时阻塞对应语义验收，不归候选错。两attempt/消融/LLM比例仅按已采用规范。

修改依赖使相关旧结果STALE；未变足够证据可复用，不能把不兼容评分版本局部PASS拼成整题。候选失败不自动导致报告QC或grader验收FAIL。

## 6. 报告QC与移交

报告 QC 依 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 分两层，legacy 不保留单层 A/B 入口。REPORT_QC 明示窄范围优先；未指定时识别并分别审核本轮报告质量与适用历史失败 A/B 归因。所有本轮新写/更新 QA 均审范围/来源、缺陷/归因、修法/实际变更、运行/验证/freshness、指标、阻塞及状态；无 always-failing、零缺陷或没有 tests 修改不使质量 N/A。关键缺陷/修法/有效性主张缺证质量 UNVERIFIED、确证错误 FAIL；准确报告技术/历史未证可质量 PASS，不等于技术、候选或历史 PASS。

开工及收口从请求、正式映射/manifest 与 rubric/test 失败标记、允许反馈/既有 artifact、已有 QA 历史发现对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED、对象/反馈ID、来源版本/已查结果及缺口影响；不扫工作区/禁区。只有确认无对象才历史 N/A，当前报告自 N/A、无 A/B 表或未找到清单不自证。已审未知或对象存在但旧材料缺失保留历史 UNVERIFIED，未审且未请求明确记本次未请求；相应依赖历史 NOT_ADMITTED，有限合法查源。按 §7.2 对象存在/未知或历史未证不增门，FULL_ACCEPTANCE/无人值守/模板本身也不增普遍历史门；不阻独立当前范围（包括全题）修验/报告审核，确属本次必需历史门仍保留。适用历史表按具体主张依赖绑定原反馈/失败ID、权威原task_path（旧修改对照）、实际断言、独立可推导性、全部提供的相关轨迹（旧行为）、A/B依据、旧修法与终态；有效 A 类不放宽，不造 phantom fix。确证错误行历史 QC FAIL，核心结论正确的叙述瑕疵记录不一票否决，惰性错误修法仍 FAIL。

复用现有技术、issue 和轮次证据，不复制台账；本轮 issue 留正式依据/断言、反例/独立预期、观察/归因、写前完整上下文、实际 diff/终态、适用验证/run/版本/freshness与未证责任。主动静态发现不虚构旧 Agent 行为，未执行标推演/NOT_RUN，未验证不标 FIXED+FRESH。ROUND_PREIMAGE 只证明本轮起点，不自动是旧 ORIGINAL_TASK；本轮漏留为 WorkC 生产缺口，如实记录并合法查源，不倒填。协调者对全部本轮报告写入自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部自查、按影响/风险复核，不新增全题独立门。先完成实质报告再审，反馈复检对应结论；任何报告变更核对应内容，技术仅按依赖失效补验不空重跑，最后仅追加准确回执不无限自指。最终分报本轮质量/历史归因状态及范围依据，不用旧总标签代替。

只读不写，授权tests变更同步同一根报告；保持稳定标题、历史事实与反馈映射，条件模块按需展开；透明纠正无依据旧结论，保留旧行、来源、纠正原因及未证范围，不删行逃避实际错误修法或分类。tests 内正式 instruction 可按获授权正式来源合法修订，不另设路径批准门；写前在同根 QA 保全完整 ROUND_PREIMAGE、起始状态、正式来源/映射及版本，记录实际 diff、版本前后与合同影响。tests 外 instruction 只读/移交，外部修订另记可核有权来源。两类正式合同变更都将受影响旧义务/评分设计与依赖运行标 STALE；未接触隐藏答案的设计角色从获授权新正式来源重新独立推导义务，再冻结评分设计，双冻结受影响范围，重核 tests、注册聚合、候选可见载体及适用真实验证。不得从隐藏答案、候选输出或低分反推合同救分；已接触答案的 reviewer 不承担独立设计，仅按新冻结核终态；不追认旧候选违规。累计指标沿 [verification-and-reporting.md](verification-and-reporting.md)，缺原基线N/A不是门，接手指标不修复必需历史材料准入缺口。最终分别报默认许可实际使用的角色/精确对象、准入/未准入对象、tests 内 instruction 实际修订/版本/双冻结及复验状态、tests 外 instruction 只读需求与移交状态（外部变更单列来源）、本地 oracle 是否实际执行、真实运行和对应验收状态；历史维护记录不当本轮实证，解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史，缺逐题批准不再作为停止原因。

tests 外环境/冻结路径发现直接写同根 QA 的精确规范化路径/版本、观察证据、影响、责任与补验方，不补placeholder、不创建副本；仅实际当前必需依赖缺口限制对应结论，其余记录后继续，不等待外侧整改。tests 内 runner/helper/shim/config 等确认缺陷须 worker 按正式依据实际修复、复验并更新 QA，不凭名称归为冻结移交。已采用轨迹后环境移交要求时逐精确路径记录observed_at/预期挂载/evidence，确无合法tests修法记固定移交处置。是否弃用数据项只能按正式profile授权/要求，不凭诊断自动废弃整题。

历史变化与本轮写入分开；本轮越界先停止核实，历史未知不擅删。人工/负责人/算法/平台待复核只影响对应阶段，不否定独立已证当前范围。最终先报本次对象，局部完成不等于整题PASS；按 §7.2，无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题 PASS/UNATTENDED_COMPLETE，历史仍准确 UNVERIFIED/本次未请求，不冒称历史 PASS。确有必需历史门缺证仍阻包含该门的原请求全通过。
