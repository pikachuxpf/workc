# 作业路由、验收依据与授权

本参考负责确定“本次做什么、哪些是通过门”；实际操作顺序见 [WorkC 作业员执行 SOP](execution-sop.md)。修复/交付/无人值守中，主 WorkC 是作业员/协调者，主动查找、确认、修复并验证授权 tests/根 QA 的问题，不以审计意见代替返修，也不等待独立 QC 发现全部问题。作业员自查及报告自查是生产责任，不是独立 QC；CONSULT、READ_ONLY、REPORT_QC、RUN_ONLY 仍遵守各自明示上限。写范围统一按 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围)，质检默认许可、必要合法本地 oracle 验证和开工准入按 [qc-exceptions-and-admission.md](qc-exceptions-and-admission.md)；运行细节见 [runtime-acceptance.md](runtime-acceptance.md)，计数与报告见 [verification-and-reporting.md](verification-and-reporting.md)。WorkC 目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准；题包由作业员修当前题 tests/** 全部内容及同根 QA，用户明示限制优先；tests 外除 QA 只读移交，instruction 按实际位置分流，tests 内无名称/用途冻结或逐文件批准。QC 是未参与返修的独立非写入角色，不生成/应用补丁、不写任务 QA；可核验不等于作业获准运行，CONSULT/READ_ONLY 与默认静态 REPORT_QC 不运行。执行边界统一见 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)。Skill 维护不启动题包作业。目标不明先核事实；未双冻结先完成独立推导/冻结，不请求授权代替。工具拒绝、用户明确更窄限制、无安全入口或未授权外部动作仍阻止相应操作，其他冻结边界不变。

## 修复与外侧发现接口

写范围以 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围) 为准，作业闭环及 QA 结构分别复用 [执行 SOP](execution-sop.md) 与 [报告合同](verification-and-reporting.md#7-报告与qc接口)。在本次获准修复范围内，已确认的 tests 内缺陷由 worker 实际修复、完成适用验证并写同根 QA；runner、judge、helper、config、instruction 和验证入口均属完整 tests 范围，不得仅因文件类型标 OUT_OF_SCOPE，或只给建议、移交、登记就收口。明确局部/只读/RUN_ONLY、写前保全及安全限制仍按实际依赖约束对应操作。

验证入口不可用时先区分 tests 内可修缺陷与真实外侧依赖：前者先由 worker 保全、修复入口并验证其安全/生产接入，再补依赖验证；不能把“当前入口坏了”自动当作无法运行或环境移交。QC 不写任务，只回报问题，由 worker 落实修验；尚无合法安全入口时不试跑，不新增安装、网络、候选、业务实现或外侧写权。

当前 task tests 外相关允许材料的发现直接写同根 QA，列精确规范化路径/版本、观察证据、影响、责任/移交方；只读不改外侧。仅实际影响当前必需依赖的缺口限制对应结论，其余发现记录后继续完成 tests 修验，不等待外侧整改。仅回复或禁写作业仍守明示上限，不为记 QA 扩权。

## 现行无人值守默认与闭环

已有唯一明确当前task，用户仅下达“无人值守”或等价执行指令且无明确更窄/只读/禁写限制时，默认 `execution_mode=UNATTENDED`、`operation=FULL_ACCEPTANCE`，覆盖当前全题tests侧自动修复验收。本请求许可当前题tests/**全部内容与同根qa_report.md写入；worker按主文第2节核规范化实际目标与链接，记录实际范围映射，无须重复或逐文件批准。明确限制优先，早前仅LOCAL_REPAIR、REPORT_QC等作业标签不阻新默认；无唯一目标、Skill维护或纯咨询不据此启动题包。旧作业沿用、仅模式不新增tests/QA写权及默认8轮/2轮停止口径如与此规则冲突，以本现行默认为准；其余质量和安全要求保留。

worker先从允许正式材料独立设计并依次双冻结，自动核准入、备证，自查修tests并真实验证；默认只读检查当前task tests外相关允许正式材料，把已查范围及问题路径/证据/影响/责任/移交写同根QA，未发现也记范围，不扫工作区、不读.pipeline/秘密，GT及oracle答案由独立QC角色核。完成实质报告后派未参与修复的非写入QC实际读QC文档，核当前task、本轮报告质量及外侧记录，分别核适用历史失败 A/B 归因；无 always-failing、零缺陷或未改 tests 仍审事实/状态/运行。worker核实反馈→集中tests/QA修复→按技术依赖补适用验证→独立复检对应结论，不以自检冒充独立QC；任何报告变更核对应内容，技术未失效不空重跑，最后仅追加准确回执不无限自指。复用技术表、issue 和轮次引用，不复制台账。

无显式预算不设默认轮数或无进展计数停止；尚有合法可修/补证路径就持续处理。重复无效动作不算进展，须换查证/归因/修法，只有真实无法继续才停止对应范围。尊重显式预算及退出；`STOPPED_BUDGET`仅显式预算耗尽，真实无法继续为`STOPPED_BLOCKED`，用户退出为`STOPPED_USER`，不因仅计数停。外侧无关/建议不门控tests；真影响必需判据则对应结论BLOCKED/UNVERIFIED/FAIL，tests侧通过与整题外部阻塞分报，移交不算修复、不冒UNATTENDED_COMPLETE。准入、双冻结、真实验证及答案隔离/外发/候选标准均为内部自动处理，不逐项索要用户审批；未获许可的外部动作仍不执行。

## 1. 作业与权限分别记录

| 字段 | 值或内容 |
|---|---|
| operation | CONSULT / READ_ONLY / LOCAL_REPAIR / FULL_ACCEPTANCE / REPORT_QC / RUN_ONLY |
| execution_mode | STANDARD / UNATTENDED；明确执行指令触发；唯一当前task且无明确限制时按现行默认FULL_ACCEPTANCE及tests/QA写许可，显式限制优先 |
| loop_budget | 仅记录用户显式预算及最后完成轮次；无显式预算不设轮数/无进展计数停止，合法可修/补证路径尚存则继续 |
| target_scope | 当前题的反馈行、规则、共享依赖、整题或明确运行模式；不把工作目录当审核范围 |
| mutation | none / report-only / tests-allowlist-plus-report；按主文第2节写 tests 与同根 QA，保留既有字段值仅作实际范围记录，QC 独立核验且绝不写题包 |
| tests_allowlist | 实际写范围映射，默认 tests/** + 同根 qa_report.md；仅用户明示局部/路径/只读等限制裁剪，不额外排除 tests 内 instruction、runner、judge、helper 或配置，不逐文件审批 |
| outside_tests_review | 仅当前task tests外与 tests 相关的允许材料：实际只读范围、精确位置/版本、证据、影响、责任/移交；无人值守默认检查，其他作业按目标必要性，不扩局部门；未发现也记已查范围，GT/oracle答案仅独立QC核 |
| repair_basis | tests 修复从获准正式输入独立推导缺陷、必要性与修法；tests 内 instruction 合同变更按主文第2节备证、独立重推双冻结和重验，外侧需求仅记录精确只读对象/版本、依据、影响与移交责任 |
| qc_role | 实际未参与返修的独立非写入 QC reviewer；尚未派发/不可用如实记录，不填协调者或设计/修复角色。作业员自查及报告自查按实际工作记入既有 issue/轮次，不另设状态机；QC不生成/应用补丁或写任务QA |
| qc_read_scope | 当前题相关精确 GT/oracle 静态对象；范围审计，非整包或递归目录、非逐项批准 |
| qc_permission_basis | WORKC_DEFAULT；目标明确、独立双冻结后相关静态 QC 不需逐题读取授权 |
| applicable_clause | 适用质检条款及采用依据；无外部条款时当前明确 QC 目标可作必要性依据，不空造条款 |
| obligation_freeze_ref | 独立义务冻结引用：范围、正式版本、来源、记录时间 |
| scoring_design_freeze_ref | 独立评分设计冻结引用：同范围/版本的答案空间、判据、部分分、路由及聚合；先义务后设计 |
| actual_reads | reviewer 实际已读的精确对象、版本/位置与读取范围；计划/默认许可不冒充已读 |
| admission_status | ADMITTED / NOT_ADMITTED / N/A；逐依赖范围判定，非声明表自动认证 |
| admission_scope | 本次准入/未准入的实际依赖范围：返修、历史 QC 或独立当前全题/局部范围；旧缺口不自动将当前全题裁成局部 |
| history_object_status | APPLICABLE / CONFIRMED_ABSENT / UNDETERMINED；历史对象/反馈ID、正式来源位置/版本/已查结果、必需旧材料及缺口影响；开工与收口核，报告自 N/A 不自证 |
| historical_requirements / preimage_refs | 必需旧材料及 VERIFIED 或正式替代接受记录；各授权 tests 目标的写前原内容引用，本轮 preimage 不自动替旧原题 |
| admission_evidence_refs / admission_owner / admission_reason | 实际准入依据、责任与理由；缺口和恢复条件可核 |
| future_run_plan | 修前核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT）、合法 evidence 来源、隔离/挂载、版本/依赖/服务、逐项/聚合结果位置、失败处理及责任；不是未来结果 |
| execution | 静态解析 / 隔离探针 / 正式 verifier / candidate / judge / oracle；按实际作业核范围，角色能力不生运行权，CONSULT/READ_ONLY/默认静态REPORT_QC不运行；QC仅按§1.1已有有效隔离入口执行必要已获准核验及本地oracle，不扩新普通候选/网络/外发 |
| delivery | chat-only / authorized-tests-and-root-report / approved-external-package / explicit-submit；题包变更按主文第2节 tests/同根 QA 范围，tests 外需求只读移交，外发另需授权 |
| architecture | legacy / adopted-0917 / other-rewardkit / hybrid / unresolved |

这些字段不能互相产生权限。打包不授权提交，judge 权限不授权候选，运行授权不扩大写权。作业类型从请求选最小充分范围；“直到 pass”不改变禁读、授权和评分合同。

## 2. 本次验收清单

执行前记录一份清单，修改时进入同一根报告；只读时只在回复记录。

| 要求 ID | 目标对象/范围 | 正式来源/版本 | 适用/采用依据 | 必需证据及通过条件 | 当前状态 |
|---|---|---|---|---|---|
| REQ-* | 局部修复/整题/QC/运行/外部阶段 | 精确段落或批准记录 | 已采用/未采用/不适用/采用未确定 | 静态、实跑、逐行终态等 | PASS/FAIL/NOT_RUN/BLOCKED/UNVERIFIED/N/A |

区分三种来源：

1. **业务义务**：正式 instruction、persona、policy、fixtures 和正式需求载体决定候选应做什么。
2. **运行/结构合同**：schema、task、runner、当前批次决定如何加载、隔离、评分、聚合和验收。
3. **辅助材料**：旧报告、历史题、模板、扫描器和环境快照提供线索，不创设义务或通过门。

现有 tests/grader 是待审核的实现，不是独立业务真值。模板不提供 expected value、ID、权重、evidence、模型、canary 或版本权威。先独立推导本次范围义务，再对照实现；QC 可先读待证报告行，不照抄其结论。

历史门以 [§7.2 历史对象、审核状态与交付必需性](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 为统一判定来源；在本清单分别核对象存在性、审核状态、具体条款采用/主张依赖及必需证据。当前 FULL_ACCEPTANCE/裸“无人值守”不自动采用全历史认证，来源名/模板/报告/失败标记不单独创设门。无历史必需门且无无据沿用的旧主张时，当前全题技术、报告及独立 QC 全部实际通过即可当前交付/UNATTENDED_COMPLETE；有明确历史门仍限制原请求全范围认证，不抹当前已证成果。恢复、穷尽记录及旧 QA 纠错也按该中央规则，不另设状态机。

## 3. 外部规范的适用性

| 规范/对象 | 启用依据 | 缺材料的影响 |
|---|---|---|
| WorkC 本轮报告质量 QC | 本轮新写/更新 qa_report.md 即适用；无 always-failing、无 tests 修改或零缺陷也审实质主张、事实、状态、运行和限制 | 关键缺陷/修法/有效性主张缺证 UNVERIFIED，确证错误 FAIL；准确报告技术或历史未证可质量 PASS，但不等于技术/历史 PASS。FULL_ACCEPTANCE/UNATTENDED 有报告写入须独立质量审核；标准局部自查、按影响/风险复核，不新增全题独立门 |
| 历史失败 A/B 归因 QC（qc-qa-report） | 对象发现不等于启用必需门；仅用户明确历史验收、已采用正式批次条款适用于具体对象，或实际交付主张实质依赖旧行为/修改，依 [§7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 核来源与依赖 | 对象状态、审核状态与必需性分判；N/A 仅 CONFIRMED_ABSENT，已审缺证 UNVERIFIED，未请求且无依赖可“本次未请求”。只将实际依赖项 NOT_ADMITTED，继续独立当前全题；明确历史门仍限制原请求全范围认证 |
| rubric_delivery_requirements | 当前请求明确要求该实测交付规范，或批次正式采用 | 适用时每 criterion 至少两次有效 attempt；不足只限制该交付验收 |
| RewardKit 两遍 QC 附录 | 当前请求/批次明确采用，且形态匹配 | 适用质量、等价解、覆盖与两向审查按原规范；不从架构名推导采用 |
| 新版判分对齐 | 当前批次/请求正式采用具体版本 | 适用 LLM≤40%、三类负控和消融；未采用不当全局门 |
| 人工/负责人/算法/平台 | 明确本阶段交付要求及真实回执 | 影响对应阶段，不自动否定局部 tests 工作或独立自动技术结论 |

先核当前允许读取的正式来源。历史摘要不是当前采用证据；采用未知写 UNVERIFIED，不默认全部适用，也不伪装为 N/A。如果用户要求完整外部流程，其规则或必要材料不可得就不能宣称该流程 PASS。

外部规范不自行产生权限。目标明确的 WorkC 作业按统一合同默认许可相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证，不需逐题批准；写范围和 instruction 合同变更统一按主文第2节，外侧 instruction 只读记录移交。双冻结是防污染顺序，精确对象、正式映射及必要性是范围审计，不是用户另批条件。无外部条款时明确 QC 目标可作必要性依据，不空造条款，也不从附录扩大权限。多报告、.pipeline 或其他冻结路径要求仍不放行，记录具体条款、受影响结论和移交责任，不丢弃全部合法审核部分。不要以“单题”豁免已采用门；解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史。

本次清单可以因确证缺陷而修订，但须给来源、影响和版本变化；不能因模板有一列、读到旧文件或 reviewer 猜测而扩大门。

## 4. 请求路由与完成条件

**通用返修收口**：STANDARD 的 FULL_ACCEPTANCE 也必须独立复核；完整验收、明确“直到 pass”或要求完成交付时，沿本次对象执行作业员自查修验→实质 QA 自查→独立审核→核实逐项反馈→授权修复/合法补证→相关验证与 QA 更新→当前版本独立复检，直到请求范围实际通过或真实无法继续、用户退出/显式预算耗尽。不需另说“无人值守”，也不改成局部作业默认全题/QC 新门：LOCAL_REPAIR 的审核要求仍按影响、风险及请求，CONSULT/READ_ONLY/REPORT_QC/RUN_ONLY 的上限不变。尚有已确认、获准且可执行的 tests/报告修复时，不能只记录审计意见就结束；独立审核是证据，不是投票或主角色自我认证。

- 咨询、问题描述、规范对比：CONSULT，给评估并停；不修文件、不运行题包代码。
- 明确只读、不产生文件：READ_ONLY，静态范围内完成；“质检”一词不授权 import/collect、动态运行或根报告写入。
- 用户明确仅修具体反馈/具体规则或指定局部范围：LOCAL_REPAIR，核相关义务、共享依赖及注册/聚合影响，执行正反例与适用回归，更新根报告并自查本轮质量、按影响/风险复核，不新增全题独立门。其余未审范围不宣称 PASS，也不自动当局部完成门。
- 要求整题 tests 交付/完整验收，或唯一当前task下仅下达“无人值守”且无明确更窄/只读/禁写限制：FULL_ACCEPTANCE，附带反馈只是起始线索，不因有反馈改成 LOCAL_REPAIR；未明示局部的“修复 tests”按当前题 tests 全范围检查修复，不另造更窄范围。全题独立设计、全部规则、真实注册聚合、正式 verifier、实际必需 judge 和已采用门闭合；有本轮报告写入时，本轮质量 QC 及未参与修复的非写入 QC reviewer 独立质量审核是该报告/模式交付必需项，历史归因另按对象与原请求门判。完整修复与该无人值守请求均按主文第2节许可tests/**全部内容与同根QA，由worker记录范围映射，不索要重复或逐文件批准。
- 审核 qa_report：REPORT_QC，默认静态、不写题包、不运行；QC角色核验能力不自动产生执行许可，只有本次实际另有有效运行授权且满足§1.1才执行对应范围。用户明示只审历史 A/B、运行声明或某行等窄范围时优先遵守，不自动扩另一层；未指定窄范围时识别并分别审本轮报告质量与适用历史失败 A/B 归因，按 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 判范围/状态。历史层核测试问题、实际候选行为、正式可推导性、跨轨迹 A/B、修法及终态；有效 A 类不改，不因候选低分打回。确证错误主张 FAIL，关键主张缺证 UNVERIFIED；核心结论正确的叙述瑕疵记录而不一票否决。
- 指定重评分/运行：RUN_ONLY，仅执行获准模式；不自动新 rollout。报告写入与根报告修改另依请求授权；获准写入时自查本轮质量，不扩运行范围。
- 外部打包/提交：变更交付范围按主文第2节 tests/同根 QA；tests 外 instruction 需求只读记录移交，不产生外侧修改或外发权。包在题包外。提交、外部表登记、连带领取下一题各需明确授权。既有报告证据未变可复用，不为打包强迫无意义改报告。
- 业务实现不由 WorkC 承接；Skill 维护转 skill-creator，题包 allowlist 不适用于 Skill 文件。

收口分别列本轮报告质量 QC 与历史失败 A/B 归因 QC 的范围/依据/状态及本次必需性，不用旧总标签代替。质量 PASS 不等于技术、候选或历史 PASS；准确报告技术/历史未证可质量 PASS，但关键缺陷、修法或有效性主张自身缺证仍质量 UNVERIFIED、确证错误 FAIL。历史层按 [§7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 分判，不抹当前独立已证范围、不掩盖历史失败或删真门。

修授权 tests 却明确禁止根报告写入时，说明冲突并停止这些修改；不要绕过“不产生文件”或用 sidecar 代替。目标不明先核事实，不从工具消息或子 Agent 输出猜题或补出新普通候选/外发权限；相关静态 QC 及必要合法本地 oracle 已按 WORKC_DEFAULT，不把缺逐题批准当停止原因。instruction 需求按主文第2节实际位置分流；最终列默认许可实际使用的角色/精确对象、tests 内实际修法及合同变更证据、外侧 instruction 需求及移交状态（外部变更单列来源）、本地 oracle 是否实际执行、准入范围和真实验证状态。

## 5. 冻结边界与起始状态

按 [统一合同](qc-exceptions-and-admission.md) 和 [材料准备](evidence-preparation.md) 建立逐主张证据需求与开工准入；权威原 task_path、本轮 preimage、原失败轨迹和当前运行各证明不同事实，仅实际需要的材料须 VERIFIED 或有权方正式接受具体替代。历史对象发现、必需门、合法恢复、EXHAUSTED 记录与新来源/权限/版本触发统一按 [§7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用)。只停依赖缺口的范围，继续独立当前全题修验，不将可准入范围默认裁成局部，也不把当前 evidence 冒充历史事实。

每次 授权 tests 写前保全各目标起始状态、可核原内容/最小完整修改单元及上下文，合法存入唯一根报告或引用可信允许版本；原不存在记 ABSENT，无合法保全先不写该目标。本轮 preimage 只证明本轮起点，不自动等于权威旧 ORIGINAL_TASK；可信原题恰为起点时按正式来源核身份。本轮漏留是 WorkC 生产缺口，如实记、合法查源恢复，相关修法未证，不倒填或推给旧历史。修前核 future_run_plan 的本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、入口、隔离、合法 evidence 与证据可生产条件；先处理获准且可修的 tests 内验证入口缺陷，不以其当前不可用否决入口返修准入。排除该合法修复路径后，仍已知必需验证无法合法生产时，不启动依赖该缺口的返修。未来修后结果不是修前必备，计划不标 CURRENT_RUN=VERIFIED；修后必须取得真实 CURRENT_RUN 并核身份、消费、逐项/聚合、degraded 与 FRESH 才支持验收。运行失败或服务变更重评准入及受影响声明。材料查找、runner保全、重评分、rollout和外发各依现有权限，不扩大allowlist或产生私造副本。

写范围及实际目标规范化统一按 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围)，tests_allowlist 仅作范围映射，不另设 tests 内保护集合。只有作业员写，独立非写入QC对任务所有路径均无写权，含tests、QA、cache、日志、字节码、结果及别名/链接/挂载落点。tests 外除同根 QA 均只读，问题记录精确对象/依据/影响/责任并移交；移交不算修复或 PASS。CONSULT/READ_ONLY/RUN_ONLY 不因范围定义变成写作业，用户明确更窄限制优先。

目标明确、先义务后评分设计独立双冻结可核后，未参与修复的独立非写入 QC reviewer 默认可静态核当前题相关根 ground_truth.json 和 oracle 源码，不需逐题读取授权；记录 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先独立推导/冻结，不请求授权代替。READ_ONLY 可据此静态核查，仍不写不跑；CONSULT 不启动题包核查。协调者及设计/修复角色不读 GT、不接收隐藏答案或可反推答案的摘录/数值/摘要；独立非写入QC仅给缺陷位置、正式来源可独立推导的方向、可推导性、结论及脱敏引用，不生成/应用补丁、不参与修复。实际核验回执复用现有运行/轮次表，记执行者、无秘密命令/模式/版本、输入输出范围及实际隔离、结果/freshness，由协调者写授权根报告，QC不写QA、不新增审批/台账。答案不成为业务义务、运行时评分依赖、候选输入或 judge evidence，也不外发。所有参与者对 `.pipeline/` 仍禁读、禁引用、禁依赖，禁止搜索、hash、挂载及副本/他人结果绕过；秘密不读不转写，默认许可不绕过工具拒绝或明确用户限制。

tests 内正式 instruction 的合法修复及外部有权负责人改变外侧正式合同，均沿主文第2节合同变更接口记录正式来源/版本、preimage（本轮自改）与实际变更及影响，失效受影响义务/评分设计/证据，独立重推双冻结并重验后送检；外部变更单列来源。作业员不改外侧文件，不据 GT 放宽规则，不用新题面追认旧候选违规或历史事实。

执行前记录允许位置的起始摘要/状态和既有异常；无 Git 不宣称已核全历史。最终区分：

- 本轮主动变更：必须符合主文第2节及记录的实际范围映射；本轮越界先停止并核实、合法处理，不擅自删除未知产物。
- 历史/用户/平台变化：标来源已知或未知，按是否影响正式合同、输入或证据限制相关结论，不自动归责当前代理，不恢复用户文件。
- 禁读或无法检查的范围：声明范围限制，不通过未知内容证明“整包零变化”。

无人值守默认只读核当前task tests外相关允许正式材料，不扫描工作区或禁区，GT/oracle答案仅独立QC核；同根QA记录已查范围，未发现也记范围，发现列路径、观察证据、影响、责任和移交，并交独立QC核记录与实际对象。外侧无关问题/建议不阻tests通过；真影响必需判据则对应结论BLOCKED/UNVERIFIED/FAIL。tests侧通过与整题外部阻塞分报，不妨碍独立可核补丁披露限制后交接，但记录移交不等于已修复，不冒UNATTENDED_COMPLETE。

## 6. 运行授权与安全约束

静态解析不执行题包模块；import、collect、注册及 pytest 都属于执行。明确运行模式、入口、隔离、副作用和网络范围。独立非写入QC可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查；实际作业允许执行时才可按§1.1经已有有效隔离入口独立运行必要且已获准parser/回归/verifier-only和本地oracle，角色能力不产生作业权限。任务所有路径含tests、QA、cache、日志、字节码、结果及别名/链接/挂载落点均不可被QC写入；须最小允许只读挂载或已有强制等效sandbox的实际文件系统只读边界，-B/cache开关不替代防写。不 whole-task mount、不复制整题绕过；scratch仅题包外独立已获准位置，不作源码副本、补丁或staging。先核入口/import/collect/子进程及环境探查副作用，禁止凭据/.pipeline/范围外隐藏材料泄漏。无安全入口不动态运行，精确报限制并移交协调者；协调者仍守自身权限及隔离，移交不授权新副本、系统安装、配置修改、重启、新候选、网络或外部judge。

完成请求允许已授权范围内的可逆本地验证，不自动授权外部模型上传或新候选。检查服务与 secret reference 状态而不读值；judge 运行时与候选隔离。无合法 evidence/入口时 BLOCKED，不用自造轨迹认证真实过程。

当本次作业允许执行且相关本地 oracle 验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不产生额外写权，不让协调者/修复方、普通候选或 judge 接触 GT/隐藏答案，静态核查不冒充动态验证。没有满足隔离的合法入口即停止对应运行，不索要逐题批准代替安全条件。

服务端访问候选 URL 时只允许 http/https，逐次重定向核 host 与实际解析地址，拒绝环回、私有和保留地址。正式隔离 mock 仅在可信固定 allowlist 与获准网络内访问，不推广到任意内网。

## 7. 架构路由与来源账本

从正式 schema 与实际 loader 确认架构。0917 结构只在正式采用该 profile 时要求；有效 legacy 不迁移；其他 RewardKit 不强套 process quality 唯一路径。hybrid 追两套真实加载与聚合；unresolved 不猜。详见 [seal-rewardkit.md](seal-rewardkit.md) 和 [legacy-claw-eval.md](legacy-claw-eval.md)。

每条义务至少记 `claim_id / source_path或carrier / scope / version / trigger / resolution / reason`；有正式冲突再记优先级和 recast。runner 证明加载、证据与聚合事实，不定义业务真值；materialization 的正式映射需独立核实。

persona 按真实 actor 绑定；HTML 内容按正式口径核可见语义/结构/可访问文本，不以源码片段替代；建议研究不升级为硬门。未披露/不可用服务、凭据和 harness noise 不归候选失败。

轨迹后环境缺失按正式采用批次要求，在同根 QA 逐精确路径/版本记录 `observed_at / exact_normalized_missing_path / expected_source_or_mount / evidence / responsible_party` 及影响。先排查并修验获准且可修的 tests 内 runner/helper/config/收集入口缺陷；仅核实为 tests 外环境缺口且确无合法 tests 修法时，才记 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF` 并停止该项重复返修。移交不算通过，仅限制实际依赖它的当前结论，不等待无关外侧整改。
