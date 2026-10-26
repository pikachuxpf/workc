# 历史外部 SOP 摘要与供应商交付流程

现行 WorkC 操作顺序以 [WorkC 作业员执行 SOP](execution-sop.md) 为准，修复/交付主角色是作业员/协调者而非独立 QC；该执行 SOP 不构成外部规范采用或已验收证明。本参考仅是历史外部流程摘要，不是内部 SOP 原文镜像，也不证明当前批次采用。外部页面历史核对日期：2026-09-17；本轮 Skill 维护未重新访问外部页面。使用前按 routing-and-authority.md 核当前采用依据与版本，只将已采用条款纳入对应对象的验收清单。现行权限按 [质检默认许可与准入合同](qc-exceptions-and-admission.md)：WorkC 目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准。题包写集合为当前 task 的全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、legacy judge.py、runner、helper、shim、instruction、config 均可按正式依据修复，不按文件类别冻结。tests 外除同根 QA 均只读/移交，包括外侧 runner、业务实现、persona、environment、solution、Dockerfile、依赖、根 manifest、shim/helper、instruction；移交不算已修复或 PASS，不据 tests 写权编写业务实现。QC 独立核验且整个 task 绝无写权，CONSULT/READ_ONLY/RUN_ONLY 不变成写作业，用户显式局部、只读或路径限制优先。目录/glob、同名/链接/别名不扩权，写前核真实规范化目标；指向 tests 外的链接/别名目标不可写，无根报告写权不改 tests，不建 sidecar/整题副本。独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，实际作业允许执行时才经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果及别名、链接、挂载落点须实际文件系统只读边界，-B/cache开关不替代防写；仅题包外独立已获准scratch，不作源码副本/补丁/staging。先核入口/import/collect/子进程副作用及隔离，无安全入口不动态运行并移交协调者，后者仍守自身权限/隔离；不新增安装/配置修改/重启/候选/网络/外部judge权。CONSULT/READ_ONLY及默认静态REPORT_QC不运行。Skill 维护不启动题包作业或授权新普通候选/外发/提交。目标不明先核事实，工具拒绝、明确用户限制或无安全入口仍阻止相应操作。

下列来源表的“本轮已核对/已读”、既有“本次新增/强化”及本地实测表述均保留为对应历史维护记录，不是本轮 Skill 维护的新验证。GT/oracle 静态 QC 及必要合法本地 oracle 默认许可的说明见第8节；第6、7节保留当时维护事实，第8节同步现行边界而非新验证；现行写范围按第8节替代说明：当前 task 全部 `tests/**` 内容与同一根 `qa_report.md` 可由作业员修复，FULL/无人值守默认 `tests_allowlist=tests/**` 并映射同根 QA，显式更窄限制优先；tests 内 instruction 不再普遍只读，tests 外仍只读/移交。历史采用、运行和 QC 门不因本轮文本同步获得 PASS。

## 1. 来源与适用范围

| 文字来源 | 页面显示更新时间 | 用途 |
|---|---|---|
| [0818批次-0917验收](https://docs.xiaohongshu.com/doc/408980eb53309f87bd4c4b1e01777fa7) | 本轮已核对 | 0917 新格式必要结构、0818 防回归、post-trajectory 环境移交 |
| [Work项目-作业SOP](https://docs.xiaohongshu.com/doc/e9c39a5c3309db4149d4cd46e5ca6f30) | 9月14日 16:44 | 当前主流程、人员收口、平台提交、指标登记 |
| [RewardKit 判分与人工标注对齐](https://docs.xiaohongshu.com/doc/1a42e805086c3a943b112d67d80201e6) | 9月10日 14:44；已读 | 新版交付结构、事实/judge 分工、40%上限、防空壳验证 |
| [quality.toml内容格式](https://docs.xiaohongshu.com/doc/d0a8d61b948587efc66d25521e3392a2) | 9月10日 13:47；已读 | quality、prompt 与 manifest 结构核对 |
| [Openclaw 题目 Refine SOP](https://docs.xiaohongshu.com/doc/1b8a26c2e1115ae58c4e74be8fa23464) | 7月7日 14:57 | 失败清单、跨轨迹归因、返修描述 |
| [ClawEval质检标准](https://docs.xiaohongshu.com/doc/87e590f1ae4512468d08bba78e9f9c73) | 5月20日 19:46 | legacy 原子性、覆盖与 evidence 分工 |

以上更新时间按页面显示记录，页面未显示年份的字段不自行补成年份。视频属于历史说明，本轮未观看；附件 skill、示例题包与视频均未作为已验证的实现。后续批次若更新，重新核对受影响 claim，不把本次摘要当永久最新规则。

按 claim、架构、批次与阶段处理来源：新版允许 Likert 的示例不能推广到要求 yes/no 的 legacy rubric；旧 Refine 中修改 instruction/environment 的建议本身不产生写权；现行 tests 内 instruction/config 等按当前授权正式依据处理，不按类别冻结；tests 外 instruction、environment 等只读/移交，移交不算已修复或 PASS。tests 内正式 instruction 合法修订的写前保全、版本、独立双冻结及复验按第8节执行。示例中的 GT source 字符串、canary、固定模型和题目路径不是正式义务或当前精确对象的依据，不复制到新生成的正式标准；相关 GT/oracle 静态 QC 按双冻结后的 WORKC_DEFAULT，不要求逐题读取批准。

## 2. 历史外部主流程与角色收口

1. 按本次作业范围从正式材料独立推导义务，先记 `obligation_freeze_ref`，再冻结评分设计、答案空间、判据、部分分、路由和聚合为 `scoring_design_freeze_ref`，之后审实现及修授权目标；两份均绑定范围、正式版本、来源、时间，同版有效独立记录可重核复用。完整验收覆盖全题全部规则，局部修复核目标及共享依赖，不将只读/QC变成完整返修。授权写作业更新同一根报告。AI可辅助发现；自动技术结论须有真实证据，人工正式签收另凭授权复核者回执，不由代理代签。
2. 技术负责人汇总交付并批量复核；这是独立收口环节，不能把单题代理自检写成负责人已验收。记录包摘要、复核人、结果和未处理问题；无证据时写待复核。
3. 首轮轨迹评估由项目收口方交给算法侧运行，不是标注人员必做的启动步骤。这是上游算法阶段的权限分工，不豁免 WorkC 完成类的正式 verifier 回归，也不豁免当前批次已采用的评分集实测证据要求；按 [运行验收](runtime-acceptance.md) 分开本地验证、合法 attempt 证据与上游阶段。主 SOP 的“问题数≤5%”只约束这一阶段；页面未明确其完整分子、分母和样本范围，不能替换 `F/N0`、漏召率、reward 或单题通过阈值。正式口径缺失时保留阶段条件并记录未核实。
4. 被轨迹打回后，对反馈逐项判断是否真实存在；修复后个人多轮复测，再由技术负责人批量复核，通过后移交项目收口方。当前主 SOP 指出该返修收口不再由项目收口方重跑轨迹，而直接交算法验收；这不等于本地评测已认证或算法已验收。
5. 当前项目指定的辅助 skill 与 WorkC 不是同一个安装身份。若批次要求使用指定 skill，记录其版本/摘要和实际复核证据；未运行不能声称已通过它，也不在不可信或缺隔离环境执行下载附件。

没有人工复核回执只写human_review_status=NOT_RUN，不代签。只有明确要求该人工/负责人阶段完成时才影响对应阶段交付；未发生人工、算法或平台阶段不自动否定独立成立的局部修复、自动技术验收或QC结论。批量复核、首轮轨迹与算法分别记录，不造额外ready门。

## 3. 轨迹返修的三段式判断

先读反馈清单（如正式提供的 `refine.json`），校验 task identity/path、`always_failing_tests`、`num_runs_with_ctrf`、`num_always_failing` 与 `traj_path`。这些是反馈线索，不是测试期望值或新计分身份。新版失败 ID 沿实际 registry、manifest scorer 和结果命名映射定位，不机械创建 legacy 文件。

对每个反馈项记录：

- **测试在检查什么**：实际通过条件、评分身份、evidence 和权重。
- **Agent 实际做了什么**：逐条引用提供的所有相关轨迹、输出或工具调用；写清计算参数、正确公式/值、实际公式/值或字段映射。缺失轨迹明确列出，不把只读一条写成已分析全部。
- **正式规则是否支持该要求**：对照题面、persona、正式输入与环境；区分候选真错、测试过严/过松、隐藏约束、隐藏白名单、规则歧义、环境故障和标准/实现不一致。

多个失败项按根因归组，不机械按失败 test 数计 `F`。合理多解有正式依据时调整 tests 接受等价结果，同时验证明确错误仍会失败；自然语言不可穷尽时不不断扩充个人白名单。tests 内 instruction、fixtures、runner/helper/shim/config 的可推导缺陷由作业员按当前授权集中修复，不另设内部精确路径批准门；正式 instruction 修订按第8节保全来源/版本并独立双冻结、复验。tests 外 instruction、fixtures、环境或 harness 只读核对象，记录精确路径、依据、影响、责任与恢复条件并移交，移交不算已修复或 PASS。当前 task 写集合为全部 `tests/**` 内容与同根 QA，用户显式更窄限制及真实规范化目标边界优先，不从正式映射或建议扩到 tests 外。

报告中的修改情况使用“refine 行为 + 具体操作”：`不修改 test：规则明确且轨迹违反要求`、`修改 test：将原条件改为有依据的等价判定`、`待讨论`、`建议剔除`、`修改 tests 内 instruction：记录正式来源、完整 preimage、版本与 diff，受影响范围重新双冻结并复验`、`tests 外 instruction 需求移交：只读记录精确对象、正式依据、影响与责任，本轮未修改`、`tests 外 environment/其他冻结对象移交（本轮未修改）`；tests 内可修对象不强制移交，外侧移交不算已修复或 PASS。候选真错时只解释不修改测试的依据，不编写候选修复方案。删除或替换无触发/不稳定项须确认正式适用性并记录身份与覆盖变更，不能为了减少问题数删有效 case。

## 4. 历史 0917 与判分对齐要求（分别核采用）

以下结构条款仅正式采用0917 profile时启用；LLM占比、负控和消融仅正式采用判分对齐规范时启用。不能仅因RewardKit架构或本文件存在就全部设为本次门。

- 必要结构是 `tests/criteria_manifest.yaml` 及 `tests/process/`、`tests/output/`、`tests/safety/` 三个维度；规范化后每维必须恰好一个 `checks.py`。deterministic-only 仍须三个 checks 文件，但可无 quality、reward、prompt。有效 legacy 保留原契约，不强迫迁移。
- 只有 `tests/process/quality.toml` 与 `tests/process/reward.toml` 可选。quality 存在时，同目录必须恰好一个精确命名的 `react_prompt.md`，quality 使用 `judge="react"` 与 `prompt_template="react_prompt.md"`。
- 该已采用批次若规定quality/prompt异常弃用，按其DEPRECATED/ABANDONED及禁止自动补prompt要求处置；不得将历史弃用条款推广到未采用profile。缺权威模板不猜写、拼接或从候选推断；完整权威来源及正式批准处理才按合同执行。prompt不新增业务义务、身份或权重。
- 全部 LLM judge 项合计最终 reward 权重占比不得超过 **40%**。沿当前实际 runner 从 criterion 到组、维度和总 reward 复算，不能按文件数、criterion 数或 manifest 原始 weight 相加估算。无法确认聚合时 `BLOCKED`；调整所需配置位于 tests 外冻结路径时移交；tests 内配置可按正式依据修复并复验，不按配置类别冻结。该上限适用于当前新版对齐规范，不无条件推广到 legacy 或其他正式批次。
- 对正式采用本页判分规范的新版题，关键词空壳、正确数值被替换、关键内容缺失三类适用负控都要验证明显失分；可在题包外用当前题真实产物构造单变量变体，对照同一候选基线、环境和 evidence。某类确实不适用时写明题面依据，不因普通单题或本轮无相关改动就默认跳过。记录受影响 checks、分维度和总分，而不只证明参考候选高分。原文未给“明显失分”的数值阈值，不擅造统一 cutoff；事实错误对应检查项须正确失分，最终仍按正式通过判据判断。授权、隔离或可信 evidence 不足时记 `BLOCKED/NOT_RUN`，不能写该规范已通过。
- 对正式采用本页判分规范的新版题，在题包外隔离配置移除全部 judge 项，保留事实 checks，验证事实错误的交付物仍无法按正式判据通过。记录消融后的实际分母、是否重新归一、事实项结果及总分判定；不虚构总分门，不在宿主运行候选补验证。未获授权、缺隔离或健康 runner 时记 `BLOCKED/NOT_RUN`，不以静态推演或 stub 代替实测。
- 所有对照使用一致的适用 evidence、候选基线与环境；只改变预定变量。不能污染 trajectory 后将分数下降归因于输出判据修复。隔离或可信 evidence 不足时记 `BLOCKED/NOT_RUN`，不在宿主运行候选来补分数。
- Manifest 的 `summary` 与 `partial_credit` 若为当前 schema 字段，逐项核对与真实检查及部分分算法一致；manifest 仅用于定位、速览、对照，真正规则与权重必须读取对应 checks/quality 和 runner。格式参考中的 `angle/rule_hint` 形态与对齐页中的 `summary/partial_credit` 形态是不同示例，按当前 schema 判定，不盲目合并字段。
- 若当前正式契约要求 tests manifest 与根目录 manifest 字节一致，先只读比对。根目录副本始终冻结；需要同步根目录才能闭合时标记 `BLOCKED` 并移交，不能扩大写权，也不为所有题新建根目录副本。

### 4.1 0818 防回归清单

- bootstrap/环境准备问题不占任务问题上限；已有权威答案不强制 ask-first 或重复追问。
- persona 与 trajectory 按消息、工具和字段的真实 actor 绑定，不能将用户、工具或第三方行为错绑给候选。
- HTML judge/check 取渲染后的可见语义、结构和可访问文本，不采用固定字符切片、CSS 类名或 JavaScript 源码作为内容捷径。
- 未披露或不可用服务、缺失凭据、harness noise 与 infrastructure failure 不算候选失败；“建议研究”不升级成强制研究。
- 只写在 assertion message、异常文本或注释里的 rubric 名称不产生评分身份，不进入 `R0/T0/N0`、manifest 或任务问题数。

### 4.2 Post-trajectory 环境移交

若轨迹后才发现环境缺失，对受影响项在 `qa_report.md` 逐行记录发现阶段、`observed_at`、环境原因、单个 `exact_normalized_missing_path`、预期来源/挂载和 evidence；每个精确规范化缺失路径独占一行，禁止目录概述、glob 或合并多个路径。状态为 `BLOCKED/OUT_OF_SCOPE`，并写 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF`。记录完整后该项无需其他测试侧修复，交环境/授权负责人处理。该环境移交规则只用于已核实的 tests 外环境缺口，tests 内可合法修复的 runner/helper/shim/config 等不因类别被移交冻结；现行范围见第8节。不得自动创建缺失资源、猜凭据或把环境问题折算为候选失败；仅在健康环境中、候选按正式要求应交付却仍缺失时记 `FAIL`。

## 5. 平台与表格登记

当前主 SOP 使用[星标平台](https://star.annoti.com/)下载、上传题包。平台只用于收发题，不替代评测或人工复核。

- 指派题：按当前实际 UI 从“我的任务→领取新题”定位对应题包；上传后还需点击“领取并提交下一题”。上传动作和提交动作分开观察。
- 自动领取的题允许在上述入口或历史任务上传。显示“进行中”意味着尚未完成提交；不能写 `SUBMITTED_CONFIRMED`。
- 提交后验证正确 task ID、包摘要、回执/提交 ID 和最终状态。若点击可能顺带领取下一题，外部动作授权还须覆盖该副作用；不足则停在 `UPLOADED_NOT_SUBMITTED/NOT_AUTHORIZED`。
- 批次标注表实时登记完成状态和两项指标，采用 `50%（1/2）` 格式。未授权表格写回时仅在 QA 报告提供待登记值，记录 `NOT_REQUESTED/NOT_AUTHORIZED`，不自动回写。
- 主 SOP 公式与现有 Skill 一致：错误率 `F/N0`，漏召率 `A/(N0+A)`。5%轨迹阶段条件是独立流程规则，不是这两项指标的默认门。

## 6. 2026-10-13 本地 QC 运行验收补充

> 现行范围替代说明：本节保留当时规范和维护事实，不表示本轮复验。当前写范围为全部 tests/** 与同根 QA，tests 外只读，QC 全 task 不写；旧内部冻结/全部 instruction 只读口径不作现行权限。现行证据、采用门、双冻结和答案隔离按第8节及主文执行。

本节依据本地 `E:/work-C/doc/质检SKILL/qc-qa-report/` 已读取材料补齐 WorkC 执行，不表示重新访问或确认上表外部页面。主 QC 仍只判报告逐行结论；采用 `rubric_delivery_requirements.md` 时逐 criterion 至少两次有效 attempt，reward_degraded 非空使该轮全部 judge 类 criterion 结果不可用并须补跑，独立有效确定性证据可保留，静态不能替代。采用 RewardKit 两遍流程时落实已适用的反例、等价解、实跑/质量和两向消融门；与禁读/唯一报告边界冲突的要求单列，没有正式替代口径不能宣称完整流程通过。

完整验收与评分逻辑局部修复按本次清单执行对应正式verifier回归；只读不执行，纯报告排版不重跑。Oracle/nop非默认门；已有合法新鲜证据按依赖范围复用。本次必需证据不足限制对应完成声明，可准确交接补验；局部必需项闭合可称局部完成但不称整题PASS。运行细则见runtime-acceptance.md。人工、算法、平台不代签、不默认门控tests交接。

## 7. 历史维护的差异结论

> 现行范围替代说明：下面为当时差异结论，原文事实保留。当前作业员可修全部 tests/** 与同根 QA，tests 内同类载体不因名称冻结，tests 外只读，QC 不写 task；第8节与主文的真实目标边界、正式依据和合同变更规则替代旧权限口径，不追认历史或新增验收回执。

已一致：tests-only 与强制 QA 交付、人工核查原则、事实与语义分工、manifest 不重复计数、两项公式与展示格式。0917 新格式下 quality 是仅限 process 的可选配置；其 prompt 配对不允许自动创建或修补。

本次新增/强化：0917 必要 manifest 与三维唯一 checks、可选 process quality/react prompt/reward 合同、整项 `DEPRECATED/ABANDONED` 处置、0818 防回归、post-trajectory 环境移交、来源版本记录、角色和阶段分离、反馈项三段式归因、多轨迹对照、多轮复测稳定性台账、40%有效占比、伪造产物与 judge 消融、summary/partial_credit 和根 manifest 同步规则、平台确实提交与批次表格登记证据。

保留的安全差异：只按正式 claim/runner 识别架构；保留有效 legacy，不强制迁移；不自动创建、猜写、改名、拼接或合并 prompt；不复制内部原文、固定身份文本、权重、模型/路径/canary/GT 引用或秘密值；instruction、environment、scripts 与其他冻结路径问题仅报告移交。当前 SOP 中更宽的题包建议不解除 WorkC 固定边界，既有错误率和漏召率公式不变。

## 8. 现行默认许可与开工准入（替代说明，不改写历史验证）

**现行修复/移交解释**：写范围以 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围) 为准，作业闭环和 QA 接口分别按 [执行 SOP](execution-sop.md) 与 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 包括 runner/judge/helper/shim/config/instruction；本次获准范围内确认缺陷须 worker 实际修复、适用验证并写同根 QA，不得仅给建议、登记、移交或因文件类型标 OUT_OF_SCOPE。第3节“待讨论/建议剔除”和第4.2节环境处置不替代该责任；先处理内部可修的验证入口/挂载/收集配置缺陷并核安全与正式接入，再补依赖验证，不以入口当前失效自动否决入口返修准入。

第4.2节固定环境移交处置仅用于已核实的 tests 外环境缺口且无合法 tests 修法；OUT_OF_SCOPE 只说明真实写边界，不自动决定技术状态。相关允许的外侧发现直接写同根 QA，列精确规范化路径/版本、证据、影响及责任/移交方，外侧不改；仅实际影响当前必需依赖时限制对应结论，其余记录后继续，不等待外侧整改。明示局部/只读/RUN_ONLY、真实目标、preimage、安全及双冻结/答案隔离不变；QC 不写任务，不新增安装、执行、网络、业务实现或外侧写权。以上只解释现行操作，不改写下述历史事实或声称复验。

本节为现行版本解释；第6节“主 QC 仍只判报告逐行结论”、第7节“本次新增/强化”保留为当时实际维护事实，不代表本轮复验或当前额外门。当前报告按 [§7.1 两个审核对象与生产责任](verification-and-reporting.md#71-两个审核对象与生产责任)，历史对象发现及其门控按 [§7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 和 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论)，当前完成声明按 [§7.4](verification-and-reporting.md#74-完成声明)；这些现行交叉引用不改写第6、7节历史运行、采用或QC事实。第7节“instruction、environment、scripts 与其他冻结路径问题仅报告移交”仅是当时边界记录；当前按真实规范化落点区分，tests 内同类文件可按正式依据修复，tests 外除同根 QA 仍只读/移交，不将历史类别清单重新施加到 tests 内。

第6、7节保留历史维护原记录；GT 禁读冲突及当时的逐题读取/本地 oracle 授权条件，现行由 qc-exceptions-and-admission.md 的默认许可替代：目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准。2026-10-14 现行范围替代旧“tests 子集/全部 instruction 只读”口径：作业员可修当前 task 全部 `tests/**` 内容与同根 QA，FULL_ACCEPTANCE/无人值守默认 `tests_allowlist=tests/**` 并映射同根 QA，不另设内部冻结子清单或路径批准门。tests 内 test.sh、judge.py、runner、helper、shim、instruction、config 均可按正式依据修复；tests 外除同根 QA 均只读/移交，显式局部/只读/路径限制及真实规范化目标边界优先，不据 tests 写权编写业务实现。QC 是独立非写入角色，不参与返修、不生成/应用补丁、不写任务QA；角色核验能力不生作业权限，CONSULT/READ_ONLY及默认静态REPORT_QC不运行，其他核验执行按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)。未冻结先完成独立推导/冻结，不请求授权代替；目标不明先核事实，工具拒绝、用户明确更窄限制、无安全入口及未授权外部动作仍阻止。此替代不表示本轮复验外部页面、本地 QC 文档、SDK 或任何题包，也不改写历史事实/采用依据；解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史。tests 外 environment/scripts/runner/其他冻结对象及 .pipeline/ 绝对边界不变，tests 内同类文件不因类别冻结，原规范采用、degraded、两遍、两 attempt、QC、覆盖及指标细节不降门。

- **独立非写入 QC 的静态核查**：目标明确、第2节独立双冻结可核后，未参与修复的QC reviewer默认可静态读当前题相关根 ground_truth.json/核相关 oracle 源码，不需逐题读取授权；记录 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先完成独立推导/冻结。QC 的非写入角色不等于永不执行；实际操作仍受 §1.1 和本次权限约束，READ_ONLY 仍不写不跑，CONSULT 不启动题包核查，REPORT_QC 默认静态、不自动取得运行权。GT/oracle 只作离线对账，不定义义务、不成为运行时评分答案依赖、候选输入或正式 judge evidence；协调者/修复方不读 GT，不接收答案原文、摘录、数值或可反推摘要，仅收正式来源支持的缺陷位置、可推导性、结论和脱敏引用，不据 GT 改期望到一致。QC 默认许可不授权答案外发或新模型上传。`.pipeline/`所有角色始终禁读/引用/依赖，不搜索/hash/挂载或借副本/他人结果绕过；秘密不读不转写。
- **必要合法本地 oracle**：当本次作业允许执行且相关验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不改 tests 外冻结入口；tests 内入口可按授权正式依据修复并复验，不凭 oracle 结果改义务，不让协调者/修复方、普通候选或 judge 接触隐藏答案，静态核查不冒充动态验证。
- **依赖材料准入**：记录 `admission_status=ADMITTED/NOT_ADMITTED/N/A` 及 `admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`。按上述 §7.2/§7.2.1 分判历史对象状态、历史审核状态和当前必需性；复用验收矩阵required、authority（权威来源/版本/采用依据）、dependency（实际依赖主张/缺口影响），不新增门控状态。对象存在/未知/灭失、缺manifest/旧轨迹、FULL_ACCEPTANCE/无人值守、模板栏或旧候选失败本身不产生历史门。明确历史验收请求、正式采用且适用的历史条款或当前交付主张真实依赖旧失败/旧修改时，保留对应门的来源/版本/对象及受影响主张；必需旧证据在依赖范围前实际VERIFIED或有正式具体替代接受记录。旧修改对比需权威原task_path，旧行为归因需对应旧轨迹，当前修法需正式输入、本轮真实preimage/diff/终态和当前必需验证，不捆绑全部遗失历史，也不以当前快照/指标/新run替旧事实。合法查源可恢复先恢复，确已穷尽才记EXHAUSTED：精确来源/版本、实际动作/结果、缺失对象、受限主张、门控依据/影响、责任及恢复条件；仅依赖范围NOT_ADMITTED。无新来源、权限或相关版本/依赖变化，不每轮重复查已穷尽旧材料，继续当前完整修验及独立QC。非必需历史保持UNVERIFIED，当前FULL tests+当前报告+真实独立QC自身必需门闭合可PASS/UNATTENDED_COMPLETE，不静默降为LOCAL；明确历史门未闭合不称原请求全要求完成，不冒全历史通过。当前引用错误/未证旧行须补证或有据纠正/撤回依赖，保留原行、来源/原因，不擦除或换标签逃避当前错误修法/分类；本轮漏留preimage、漏登记或缺必需run仍是WorkC生产缺陷，合法恢复不倒填免责。
- **现行报告两层接口**：第6节“主 QC 仍只判报告逐行结论”等表述仅保留历史事实；当前按 [verification-and-reporting.md §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 分本轮报告质量 QC 与历史失败 A/B 归因 QC，不改单独外部 QC 规范。所有本轮新写/更新 QA 均审实质主张、事实、状态、运行与限制；无 always-failing、零缺陷或未改 tests 不使质量 N/A。REPORT_QC 明示窄范围优先，未指定时识别并核两层。关键缺陷/修法/有效性主张缺证质量 UNVERIFIED、确证错误 FAIL；准确报告技术/历史未证可质量 PASS，但不等于技术、候选或历史 PASS。协调者全部报告写入自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部按影响/风险复核，不新增全题独立门。
- **历史对象发现**：开工及收口从请求、正式映射/manifest 与 rubric/test 失败标记、允许反馈/既有 artifact、已有 QA 历史核对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED、对象/反馈ID、来源版本/已查结果及缺口影响，不扫工作区/禁区。确认无对象才历史 N/A，报告自 N/A、无 A/B 表或未找到清单不自证；未知或对象存在但旧材料缺失为历史 UNVERIFIED，仅实际依赖历史范围 NOT_ADMITTED；必需性按 §7.2.1 核，不自动阻当前完整验收，不删真实原门、不阻独立本轮修法/质量审核。
- **报告证据与复检**：复用技术、issue 与轮次证据，不复制台账；本轮缺陷/实质修法留正式依据/断言、反例/独立预期、观察/归因、写前完整上下文、实际 diff/终态、适用验证/run/版本/freshness及未证责任。静态发现不虚构历史失败，未执行标推演/NOT_RUN，未验证不标 FIXED+FRESH。先完成实质报告再独立审，反馈复检对应结论；任何报告变更核对应内容，技术仅按依赖变化失效，不空重跑，最后仅追加准确回执不无限自指。最终分报两层范围/依据/状态；历史未知/缺证按 §7.2.1 已核当前必需性及实际依赖限制相应历史认证/主张，不自动阻当前完整范围/模式完成，不删真门或冒全历史通过，不抹掉已证技术范围。
- **所有写目标与未来生产**：每个授权tests目标先在唯一根报告合法保全完整ROUND_PREIMAGE、起始状态、最小完整修改单元/上下文，原不存在记ABSENT，hash不足。本轮 preimage 只证明起点，不自动等于旧 ORIGINAL_TASK；本轮漏留preimage或漏登记是WorkC生产缺口，如实记、合法查源恢复/事后补登记，相关未证修法限制结论，不倒填或伪称当时已登记，不推给旧材料灭失。修前 future_run_plan 核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、合法 evidence/来源、隔离挂载、版本依赖服务预检、逐项聚合取证位置及失败责任；先处理获准且可修的 tests 内验证入口缺陷，保全并安全修验该入口不被其当前失效否决；排除此路径后仍已知不可合法生产必需验证，才不启动依赖该缺口的返修。修前不要求已有修后结果；计划/预检/ADMITTED不填CURRENT_RUN=VERIFIED、不认证PASS，声明表/辅助工具不认证准入。修后实际正式CURRENT_RUN核身份、真实消费、逐项聚合、degraded及FRESH；服务/运行失败重评准入并停止受影响完成声明。只读可审材料报NOT_ADMITTED，不写不跑。
- **tests 内正式 instruction 修订与外部合同变更**：tests 内正式 instruction 可按获授权正式来源合法修订，不另设路径批准门；写前在同根 QA 保全完整 ROUND_PREIMAGE、起始状态、正式来源/映射及版本，记录实际 diff、版本前后、合同影响及责任。tests 外 instruction 只读核精确对象/正式依据/影响/责任并移交，外部有权负责人修订另记可核外部来源；移交不是已修复或 PASS。两类正式合同变更都使受影响旧义务/评分设计与依赖运行证据 STALE；未接触隐藏答案的设计角色从获授权新正式来源重新独立推导义务，再冻结评分设计，双冻结受影响范围，重核 tests、注册聚合、候选可见载体及适用真实验证。不得从隐藏答案、候选输出或低分反推合同救分；接触过答案的 QC reviewer 不承担独立设计，仅按新冻结核终态，不追认旧候选违规。正式来源不可核、未合法保全、用户明确限制、工具拒绝或无法生产必需验证时，停止对应修改并限制受影响结论；tests 外环境等不随之开放。

最终分别报默认许可实际使用的角色/精确对象、准入/未准入对象、tests 内 instruction 实际修订/版本/双冻结及复验状态、tests 外 instruction 只读需求与移交状态（外部变更单列来源）、本地 oracle 是否实际执行、真实运行与对应验收状态。缺逐题 GT/oracle 读取批准或本地 oracle 另批不再作为停止原因；tests 内 instruction 按正式依据与保全/独立双冻结/复验要求可修，不另设路径批准门，tests 外 instruction 仍只读/移交，未闭合需求按实际影响限制结论；默认许可不恢复灭失历史、不改变正式替代接受口径、不保证任何题无条件 PASS。
