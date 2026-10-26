# 本次范围的真实验证与验收

先按 [路由与依据](routing-and-authority.md) 固定作业与适用门，再按 [质检默认许可与准入合同](qc-exceptions-and-admission.md) 核实际范围。WorkC 目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准；题包写集合为当前 task 的全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、judge.py、runner、helper、shim、instruction、config 均可按正式依据修复，不按文件类别冻结；tests 外除同根 QA 均只读/移交，显式局部、只读或路径限制优先。别名/链接按真实规范化目标判权，落到 tests 外不因入口位于 tests 内而可写；业务实现与答案隔离等边界不变。CONSULT/READ_ONLY 不运行题包代码；REPORT_QC 默认静态审核、不写题包、不自动启动运行，独立非写入 QC 的核验能力与本次作业权限分开，统一按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)：不参与返修、不生成/应用补丁、不写任务QA；可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，仅实际作业允许执行时经已有有效隔离入口运行必要且已获准的parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果、别名/链接/挂载落点均不可写；须最小允许只读挂载或已有强制等效sandbox，-B/cache开关不足以防写。scratch仅题包外独立已获准位置，不作源码副本、补丁或staging；先核入口/import/collect/子进程副作用，屏蔽凭据/.pipeline及范围外隐藏材料。无安全入口不动态运行，报对应限制并交协调者，后者仍守自身权限/隔离；不新增系统安装、配置修改、重启、候选、网络或外部judge权。Skill 维护不启动题包作业或授权新普通候选/外发。目标不明先核事实；未双冻结先完成独立推导/冻结，不请求授权代替。工具拒绝、用户明确更窄限制、无安全入口或未授权外部动作仍阻止相应操作，其他冻结边界不变。

## 1. 哪些运行是本次必需项

| 作业/规范 | 必需验证 |
|---|---|
| LOCAL_REPAIR 评分逻辑修改 | 受影响规则与共享依赖双向例、注册/聚合影响、默认正式 verifier 回归；可复用足够且新鲜的有效证据或正式认可替代证据 |
| LOCAL_REPAIR 仅报告/非评分排版 | 任何报告变更均核对应内容与本轮质量；核实评分语义/配置/证据依赖未变，不空跑 verifier；标准局部自查、按影响/风险复核，不新增全题独立门 |
| FULL_ACCEPTANCE | [全题逐项技术清单](pre-delivery-qa-fusion.md)：全题义务、全部确定性与语义判据双向/等价审核、独立复算、真实输入解析对拍、真实注册聚合、正式 verifier、实际必需 judge、已采用外部门及独立复核；有本轮报告写入须本轮质量 QC 与独立质量审核闭合，历史归因另判 |
| REPORT_QC | 默认静态、不写题包、不运行，角色能力不生运行权；明示窄范围优先；未指定窄范围识别并分别核本轮报告质量与适用历史失败 A/B 归因。本轮审实质主张/事实/状态/运行/限制，历史审反馈、实际断言、正式可推导性、跨轨迹行为及旧修法终态；关键主张缺证 UNVERIFIED、确证错误 FAIL，不自动启动运行 |
| RUN_ONLY | 获准指定模式健康完成、真实逐项/聚合结果可核；不增加新 rollout，仅获准报告写入时自查本轮质量 |
| 已采用实测交付 | 每条 rubric/criterion 至少两次有效 attempt，逐次绑定证据与判别力 |
| 已采用两遍 QC | 依原规范落实结构/契约、设计/数值/对抗、适用等价解与覆盖门 |
| 已采用新版判分对齐 | 实际 LLM 有效占比、适用三类负控、事实与语义判分职责及规定消融 |

显式 `execution_mode=UNATTENDED` 按 [现行路由](routing-and-authority.md)：唯一当前task且无明确更窄/只读/禁写限制时，默认FULL_ACCEPTANCE全题tests侧自动修复验收，本请求许可全部 `tests/**` 内容与同根QA写入，worker记录 `tests_allowlist=tests/**` 与同根QA映射并核真实目标，不另设内部冻结子清单或更窄批准门，无须重复批准，早前仅作业标签不阻新默认。先正式材料独立双冻结、准入备证、自查修tests真实验证；默认只读核当前task tests外相关允许正式材料，QA记范围及问题路径/证据/影响/责任/移交，未发现也记范围，不扫工作区、不读.pipeline/秘密，GT及oracle答案仅独立QC核。实质报告完成后派未参与修复的独立非写入QC实际读QC文档，核当前task、本轮报告质量及外侧记录，分别核适用历史失败 A/B 归因；无 always-failing、零缺陷或只运行也不跳过本轮报告质量。worker核实反馈→集中tests/QA修复→按技术依赖补适用验证→独立复检对应结论；最后仅追加准确审核回执不无限自指。本次成功需全部必需门、独立复检及本轮质量 QC/独立质量审核闭合，历史门仅按 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 的明确请求、适用正式采用条款或当前主张依赖确定；历史未知/未证本身不阻独立当前全题 PASS/UNATTENDED_COMPLETE，确属本次必需门则缺证仍阻包含该门的原请求全通过，不删门，不降真实验证、准入、双冻结、答案隔离/外发/候选标准，内部核查不逐项索要审批。

无显式预算不设默认8轮或2轮无进展停止，尚有合法可修/补证路径则继续；重复无效动作不算进展，须换查证/归因/修法，只有真实无法继续才STOPPED_BLOCKED对应范围。STOPPED_BUDGET仅显式预算耗尽，尊重用户退出，不因仅计数停。现行规则见 [路由与依据](routing-and-authority.md) 与 [无人值守细则](unattended-mode.md)，旧维护记录仅作历史；停止或流程结束不算PASS。

只读上限优先。缺运行证据只限制相应动态声明，不否定静态审查工作完成。未采用附录不强加；采用未知先核来源，仍未知为 UNVERIFIED，不按架构默认启用。已采用项不能借“局部/单题”冒称整个该规范通过。

由作业员/协调者集中写当前 task 全部 `tests/**` 内容与同一根 `qa_report.md`；FULL_ACCEPTANCE/无人值守默认 `tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、judge.py、runner、helper、shim、instruction、config 不因名称或类别冻结，合法修复仍须正式依据、写前保全、影响记录及适用复验；不据 tests 写权编写业务实现。tests 外除同根 QA 均只读/移交，包括外侧 runner、persona、environment、solution、Dockerfile、依赖、根 manifest、shim/helper、instruction；移交不算已修复或 PASS。CONSULT/READ_ONLY/RUN_ONLY 不变成写作业，用户显式局部、只读或路径限制优先。目录/glob/别名/链接不扩权，写前核真实规范化目标，指向 tests 外的目标不可写；无根报告写权不改 tests，不建 sidecar/整题副本。QC 对整个 task 仍绝无写权，不参与返修、不生成/应用补丁、不写任务 QA。

## 2. 模式和证据效力

WorkC 目标明确、正式义务 `obligation_freeze_ref` 与评分设计 `scoring_design_freeze_ref` 依次独立冻结可核后，未参与修复的独立 QC reviewer 默认可静态读当前题相关根 ground_truth.json/核相关 oracle 源码，不需逐题读取授权；记 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计，不写递归目录。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先完成独立推导/冻结，不请求授权代替。QC 的非写入角色不等于永不执行；实际操作仍受 §1.1 和本次权限约束，READ_ONLY 仍不写不跑，CONSULT 不启动题包核查，REPORT_QC 默认静态、不自动取得运行权；默认许可不绕过明确用户限制或工具拒绝。GT/oracle 只离线 QC 对账，不定义义务、不进入运行时评分、候选输入或正式 judge evidence；协调者/修复方不读 GT、不接收答案原文、摘录、数值或可反推摘要，只收正式来源支持的缺陷位置、可推导性、结论和脱敏引用，不据 GT 改期望到一致。QC 默认许可不授权答案外发/新模型上传。

当本次作业允许执行且相关本地 oracle 验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不改 tests 外冻结入口；tests 内入口可按授权正式依据修复并复验，不凭 oracle 结果改义务，不让协调者/修复方、普通候选或 judge 接触 GT/隐藏答案，静态核查不冒充动态验证。`.pipeline/`所有参与者绝对禁读、禁引用/依赖，不搜索/hash/挂载或借副本/他人结果绕过；秘密不读不转写。

| 模式 | 证明范围 | 不证明 |
|---|---|---|
| 静态解析/独立复算 | 来源、语法/schema、源码与可推导事实 | 运行健康、注册成功或正式评分 |
| 隔离定向探针 | 真实 scorer/依赖对给定正反例的结果 | 候选真实 rollout 或完整正式链 |
| verifier-only | 正式允许已有产物/轨迹在当前 grader 的评分链 | 新候选现场执行、两次 rollout |
| candidate/rollout | 获准 runner 产生 workspace/轨迹/冻结证据并评分 | 低分就说明 grader 错误 |
| 真实 judge | 实际获准 backend 对指定 evidence 的评分链 | smoke 等于真实题全部语义正确 |
| 负控/消融 | 同一合法基线/evidence 单变量对实际链影响 | 自造轨迹等于真实调用、纸面总分等于实测 |
| 必要合法本地 oracle | 允许执行作业内 WORKC_DEFAULT 的隔离 QC 对照；独立非写入QC可按§1.1直接执行，协调者可在自身权限/隔离内编排且仅收脱敏状态/引用 | 默认必跑、新普通候选/网络/外发许可、分数是业务真值 |
| nop | 另获运行范围支持的正式候选对照 | 默认 oracle 许可自动授权、默认必跑 |

正式 verifier-only 须由 runner 提供或正式认可；不能手写近似评分器冒充。缺新鲜合法证据时需获准 rollout，未授权则阻塞该运行，不静默调用新候选。

### 两次有效 attempt 的统一口径

只在正式采用实测交付规范时启用。有效 attempt 是按该规范认可的、同题真实候选执行及合法产物/轨迹，其 task、候选身份、runner、来源和阶段可追溯；两次 verifier 重跑、两个 fixture、Oracle+nop 不自动凑两次 rollout。

历史 attempt 允许复用时重核正式来源、产物/轨迹、身份、grader/runner/config 和完整性。新 grader 可对原真实 attempt 正式重评分，记录原 attempt 与新 run_id；不把新 run_id 算成新 attempt。是否满足该规范由其历史复用条款决定，不自行放宽。

正式采用 rubric_delivery_requirements 时，reward_degraded 非空使该轮所有 judge 类 criterion 结果不可用并须补跑，包括正常返回的其他 judge 项；不能将它们计入两次有效实测。该规定不自动抹去独立有效的确定性结果。其他正式合同按其明示失效范围处理；规定整轮无效时严格执行。不得用缺失/失败项拼出完整有效 attempt。

### 本地效力与新鲜度

健康本地真实链可满足对应正式运行项，不因宿主位置或路径映射重复远端；需证明输入、评分语义、隔离和版本等价。精确版本来自当前正式合同，不永久固定某一 SDK。题包跑通、候选通过、报告 QC、技术验收和人工/平台分别记录。

FRESH 需当前依赖摘要一致且覆盖足够；STALE 是依赖输入实质变化；UNVERIFIED 是无法核实。任何报告变更均核对应内容/结论，纯排版或仅归因变化不自动失效评分、不空重跑 verifier；规则、prompt、evidence、权重或 runner 变化只失效依赖结果。可组合兼容且依赖未变的分项证据并给依赖矩阵，但不能伪称一次全量 run 或拼接不同评分版本的 PASS。

tests 内正式 instruction 可由作业员按获授权正式来源合法修订，不另设 instruction 路径批准门；写前在同根 QA 保全完整 ROUND_PREIMAGE、起始状态、正式来源/映射与版本，记录实际 diff、版本前后、合同影响及责任。tests 外 instruction 仍只读/移交；外部有权负责人修订时记录可核外部来源，不冒称作业员已修。两类正式合同变更都使受影响旧义务/评分设计及依赖运行证据 STALE；由未接触隐藏答案的设计角色从获授权新正式来源重新独立推导义务、再冻结评分设计，双冻结受影响范围，重核 tests、注册聚合、候选可见载体与适用真实验证。不得从隐藏答案、候选输出或低分反推合同救分；已接触答案的 QC reviewer 不承担独立设计，仅按新冻结独立核终态。不用新合同追认旧候选违规或当旧合同事实；源不合法、变更依据不可核或无法生产必需验证时限制对应修改/结论。

## 3. 尽早预检，而不是修完才发现不能运行

**先修内部入口，不自动移交环境**：写范围和例外按 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围)，闭环按 [执行 SOP](execution-sop.md)，证据按 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 包括 runner/judge/helper/shim/config/instruction；获准范围内确认的缺陷须由 worker 实际修复、适用验证并写同根 QA，不因类型标 OUT_OF_SCOPE，不以建议、登记或移交替代。入口失效若源于可修的 tests 内缺陷，先保全并修验入口、安全隔离及实际生产接入，再补依赖验证；预检失败本身不是否决该入口修复准入的理由。QC 不写任务，只回报发现供 worker 落实；无安全入口时不先试跑，不新增安装、系统/外侧配置修改、候选、网络或业务实现权限。

相关允许的 tests 外发现直接写同根 QA：精确规范化路径/版本、观察证据、影响、责任/移交方；不改外侧。只有当前必需依赖确受影响才限制对应结论，其他发现记录后继续 tests 修验，不等待外侧整改。明示局部/只读/RUN_ONLY、真实目标、preimage 与安全限制不因此放宽。

按 [材料准备与补证](evidence-preparation.md) 和现行准入合同，在修改前固定逐项依赖，记录 `admission_status=ADMITTED/NOT_ADMITTED/N/A` 及 `admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`；声明表或辅助checker不认证准入。历史分流不豁免当前写前保全/漏留责任、必需CURRENT_RUN或真实输入parser兼容性；这些是本次证据门，不是旧历史灭失。

- **历史对象发现**：开工及收口从请求、正式映射/manifest 与 rubric/test 失败标记、允许反馈/既有 artifact、已有 QA 历史核对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED、对象/反馈ID、来源位置/版本/已查结果及缺口影响；不扫工作区/禁区。仅确认无对象才历史 N/A，报告自 N/A、缺清单或无 A/B 表不自证；已审未知或对象存在但旧材料缺失为历史 UNVERIFIED，未审且未请求明确记本次未请求。按 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 分开对象、证据与门：对象存在/未知或 UNVERIFIED 不自动增门，FULL_ACCEPTANCE/无人值守/模板也不增普遍历史门；只限制实际依赖历史的主张/准入，不阻独立当前范围（包括全题）修验/报告审核，确属本次必需历史门仍保留。
- **旧材料实际准入**：本次必需历史证据按 §7.2 的门依据和具体主张依赖核，不一律捆绑：权威原task_path/ORIGINAL_TASK用于旧修改对照，HISTORICAL_TRAJECTORY用于旧候选行为，反馈/失败身份映射绑定相应对象；依赖返修/历史QC前所需材料实际VERIFIED，或有负责方对具体对象、版本、条款的可核正式替代接受记录。当前快照、ROUND_PREIMAGE、handoff指标和新run不替代相应旧材料，新rollout不证明旧行为；正式重评分绑定原attempt与新run。先有限合法查源，可恢复先恢复，权限不足列具体阻止，确穷尽记EXHAUSTED/历史验收NOT_ADMITTED，仅新来源、权限或版本变化时重试已穷尽来源，不启动依赖修改循环。独立不依赖该历史的当前范围（包括FULL_ACCEPTANCE全题）可另列范围准入与交付；确属本次必需历史QC门仍保留，缺证不能称包含该门的原请求全通过或自行换验收口径。
- **所有写目标准入**：每个授权tests修改目标写前有完整可核ROUND_PREIMAGE、起始状态与最小完整修改单元/上下文，在唯一根报告合法保存/引用；原不存在记ABSENT。无法合法保全先不写该目标，hash不是完整修法证据。本轮 preimage 非权威旧原题的自动替代；本轮漏留为 WorkC 生产缺口，如实记、合法查源，相关修法未证，不倒填或推给旧材料灭失。
- **修后运行可生产准入**：修改前 future_run_plan 核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、合法 evidence 及来源、隔离/挂载、版本/依赖/服务预检、逐项/聚合结果获取位置、失败处理与责任。先处理获准且可修的 tests 内验证入口缺陷；按写前保全/安全要求修验该入口不被其当前失效否决。排除此路径后仍已知无法合法生产必需验证，才不启动依赖该缺口的返修。修前不要求已有修后结果；现有CURRENT_RUN单独核来源/对象/版本，计划、预检成功或ADMITTED不能填CURRENT_RUN=VERIFIED、不保证后续服务健康。
- **修后实际验收**：获准正式入口实际取得CURRENT_RUN后核身份、真实消费、逐项/聚合、degraded与FRESH；每次保留可复核逐项/阶段/结果证据，不只抄终端PASS。运行失败或服务变化时重评准入，保留已证范围、停止受影响完成声明；仅计划不认证PASS。只读可完成材料审计并报NOT_ADMITTED，不写不运行。

先独立冻结正式义务 `obligation_freeze_ref`，再冻结评分设计、答案空间、判据、部分分、路由与聚合为 `scoring_design_freeze_ref`；两份绑定范围、正式版本、来源、时间，同版有效独立记录可重核复用。在双冻结后、修改前核以下事实；静态作业只检查获准可读部分：

1. **入口/副作用**：task、Dockerfile、tests/test.sh 及实际调用链；cwd、build context、依赖、候选/外部调用、freeze、挂载、输出和 rc。禁止递归读取禁区或未确认工具副作用。
2. **运行能力**：按架构核 Docker client+daemon、Harbor 版本/help、WSL/Linux 或其他正式环境。只用安装存在的能力，不为探测安装/重启系统。获准运行时已安装 Docker 未启动，主代理按 [环境自主恢复](continuous-execution.md#2-已安装环境未就绪作业员自主恢复) 核组件、普通启动、有界检查 daemon 就绪并续跑；普通启动不是修改题包外冻结文件，不直接移交用户。QC 不自行管理宿主服务；不扩为重启工作中服务、安装、重置或改系统配置。
3. **版本**：当前合同精确要求时核实际 verifier 内版本。镜像标签不代替 digest/实装版本；纯宿主文本解析不要求安装评分 SDK。tests 外冻结依赖/环境缺陷移交，不改外侧环境救绿灯；tests 内依赖声明、runner/config 等可按正式依据修复并复验，不替换正式版本要求。
4. **权限/隔离**：普通候选/verifier/judge 仅挂载最小允许文件/子树，不暴露 ground_truth.json、隐藏答案、.pipeline/、秘密或整题；candidate 可写区与 frozen evidence 分离，tests 对候选只读/不可见。必要合法本地 oracle 仅按统一合同隔离执行及最小 QC 挂载，输出只由 QC 角色核查，不向协调者/修复方、普通候选或 judge 暴露答案；静态读取默认许可不扩为普通运行时答案权限。
5. **服务/网络/外发**：获准 mock、judge endpoint、模型路由及 secret reference 状态。不得读值；secret 存在不是调用授权。缺连通或隔离按观察证据归 infrastructure。
6. **evidence**：合法位置的真实 conversation/trajectory/audit/产物，根类型、字段、actor、编码、freeze 与 producer；仅禁区内有证据则请求授权方提供独立合法来源，不搬出绕过。
7. **起始差异**：允许位置基线、既有用户/平台/历史异常和来源限制，不要求凭未知历史证明零变化。

健康命令示例 `docker version`、`docker info`、`harbor --version`、`harbor --help`；安装版 help 有子命令才查其参数。执行 `.sh` 前先确认实际 shell；当前 Windows 工作站显式使用 Git Bash，并明确处理 MSYS 路径转换，不猜容器根或照搬另一版本参数。

## 4. 按真实入口运行并保留阶段结果

记录 `能力预检 / build-start / 服务健康 / evidence freeze / 契约 / scorer / gate / 结果读取` 的实际适用阶段。CLI rc=0 不足；核 trial exception、阶段执行、verifier 状态及结果一致性。gate 正常拒绝并 reward=0 不一定是 runner 错误；候选低分不要求修 grader。

- Harbor：从当前批准配置与安装 help 取精确命令，沿其 build/staging/collect/shared-verifier 规则；直接 Docker 不冒充 Harbor rollout。
- Docker verifier：正式允许时运行当前正式入口（tests 内合法修订须记录版本与 diff 并复验，tests 外冻结入口不改），确认 build context、cwd、entrypoint 和挂载；标签/build 成功不等于运行。
- 其他架构：沿正式 runner，不强加 Docker/Harbor。

执行前形成 `host→target / producer / consumer / ro-rw / authority` 挂载表。运行产物/cache 放获准隔离位置，不生成 sidecar；不得 privileged、挂 Docker socket/个人目录/整盘。构建会暴露禁区时停止；正式 runner 可以按合同在题包外 materialize 允许输入，这不授权复制可编辑整题。

核 source、freeze、collected artifact 与实际消费字节/时间；verifier 后写文件不冒充已收集 evidence。没有合法 snapshot/收集接口时阻塞相关证据，不改 tests 外冻结 hook；tests 内 hook/runner/helper 缺陷可按正式依据保全、修复并重核真实收集/消费。

真实 judge 仅由受信任、不会启动候选的进程消费既有 secret reference，不把 env-file 加给会启动候选的调度进程。网络范围按正式合同，未经授权不发题包内容。score SDK/validator/版本断言由实际环境执行，运行后核旧结果清理、重复/漏注册、空证据和 rc；每次独立 run 目录/新进程。

### 4.1 运行时同步留证，缺证先合法补产

证据生产是正式运行的一部分，不在运行结束后凭当前环境补写“当时使用”。复用已获准题包外 run artifacts 和同根 QA 的运行表，运行文件仅留非秘密审计数据；不新建题包 sidecar、不复制整题，也不无过滤导出环境变量、完整容器 inspect 或秘密。

- **启动前**：固化 run_id、实际工作目录、脱敏外层命令/参数数组、外层 wrapper 及其调用的实际入口/hash、grader/config/合法 evidence 的精确允许清单及摘要、来源/attempt/freeze、挂载表、预期输出位置及镜像身份。输入枚举只核明确允许项，不遍历秘密/.pipeline/隐藏答案。`__validation` 等参与真实执行的 wrapper 即使不计评分身份也要单独登记，不能随通用 `__*` 排除规则漏掉；QA 自身仅作报告版本，避免自指 hash。
- **实际执行时**：把 tag 解析到实际 image ID/digest，固定或核验启动对象，标签不代 digest；从实际执行容器/环境取得正式要求的实装版本。记录真实 cwd、entrypoint、最小挂载及 ro/rw、实际命令、阶段时间/退出状态，避免只记录内层 `test.sh` 而丢外层调度。支持时在启动后核实际生效的最小运行元数据，不读取容器 env 中的秘密。
- **执行后**：绑定实际结果路径/hash、逐身份/权重/聚合、错误/degraded、输入消费与前后允许输入完整性；核证据确属本 run 和当前版本。进程 rc=0、文件名、终端截图或事后当前版本查询不能单独证明以上事实。

缺证时先核同一 run 的可信现存元数据，可找回就标实际恢复来源/时间，不伪称事前已捕获。已无法证明旧 run 的关键身份，但当前合法 verifier-only 可重跑且在本次运行/外发范围内时，作业员补齐取证机制后自主生产新 run，核当前门；旧 run 仍保留 UNVERIFIED 及具体缺口。新 run 不认证旧行为、不新增 attempt，不为补证启新候选/未授权 judge。不能因“只改报告不空跑”的规则拒绝这种为实际缺证而必要的重跑；证据本已充分且 FRESH 时才无需重复运行。只有合法补产确被权限、证据或安全条件阻止，才按停止闸门限制相应结论。

## 5. 逐项结果、正反例与复核

每个 run 在现有运行/轮次/证据表中绑定实际执行者（独立非写入QC或协调者等）、task/attempt（适用时）、run_id、无秘密命令/模式、cwd、实际版本、镜像 digest（适用时）、grader/config/evidence 摘要、输入输出范围及实际隔离（任务只读边界/最小挂载/题包外已获准scratch/答案输出可见角色）、时间、实际阶段结果、结果 artifact/digest、范围及 freshness；不另造审批或台账。QC实际运行回执由协调者核脱敏内容后写授权根报告，QC不写任务QA。字段不存在时解释，不伪造 rc、raw/reason 或 provider 回执。

沿实际 schema 读取逐项、维度、聚合与 degraded/error；不要机械套 logs 路径或 JSON 嵌套。manifest/source→runtime→结果 exact-once，身份、权重/分母/gate 可复算。候选失败、grader 缺陷、harness 噪声和 infrastructure 分开归因。

按 [逐项技术清单](pre-delivery-qa-fusion.md) 对本次范围逐 identity 留源码/helper/parser、适用轴、输入引用、独立预期、实际结果、run/版本及未证原因。完整验收覆盖全部实际确定性与语义判据，含未改项；记录已实测/适用总数，静态另列，不以只测改动/风险代替全题。确定性给合法PASS/违规FAIL，部分分/语义按正式尺度，不强制所有违规归零。全部可复算项独立推导比较参照值—实现/配置声称值—报告值，不调用被审函数抄结果；逐层核权重、分母与满分可达性。合法多解按真实轴验证性质/集合，不宣称一个正例等于完整证明。两遍 QC 已采用时按其三类等价样本和覆盖门，真实唯一事实不造三种值；同时严格审提取器name/arguments/result三字段族及真实rollout兼容性，现有实现未消费不构成自动豁免。额外探针按风险，不无穷扩展解析器。

凡消费 conversation/trajectory/tool result/文档转换产物，完整验收用合法正式导出的真实输入样本对拍解析器，支持模式沿实际runner合同；核根类型/actor/name/arguments/result关联、真实文件名及目标提取，适用嵌套group/list/dict/Unicode/规范化路径。区分未调用、缺字段、合法空集、失败payload和解析失败，正向应有目标须提取出来，负向合法空集不强行非空。fixture不证明真实兼容；缺样本先合法查取/获准补证，仍缺UNVERIFIED，不擅启新候选或搬出.pipeline。

实际 judge 相关验收读 [judge-chain.md](judge-chain.md)。真实语义正反例、响应边界/身份/聚合按适用合同核；无 judge 不访问秘密或调用服务。新版负控/两向消融仅在已采用门或本次明确要求时运行；使用同一可信基线，合法单变量隔离接口，不改 tests 外冻结配置、不污染正式基线；tests 内配置修复另按正式依据保全、记录依赖并复验，不借负控调门救分，不自造轨迹来认证过程。

复核目标是裁决确认缺陷和关键未决风险，不是不断重启全题。现行报告接口按 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口)；协调者对所有本轮报告写入做质量自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入时，由未参与修复的非写入 QC reviewer 独立核本轮质量，局部按影响/风险，不新增全题独立门。REPORT_QC 明示窄范围优先，未指定时分本轮质量/历史归因两层；无失败清单或零缺陷仍审事实、状态及运行。工具不可用如实记未独立复核，不能代签。复用技术、issue 和轮次证据，返修只更新受影响证据与结论；先完成实质报告再审，最后仅追加准确 reviewer 回执不无限自指。

## 6. 收口与移交

按本次验收清单判状态：必需项确认 FAIL 则该范围打回；未执行 NOT_RUN、无法证明 UNVERIFIED、具体权限/环境阻止 BLOCKED。建议和未请求外部阶段不门控。

- 局部修复必需项闭合：局部修复完成；整题未验收，不泛称全部通过。
- 补丁/报告/本轮差异闭合但必需运行缺失：可交接补验，动态验收未完成，写精确影响与责任。
- 完整技术范围全部适用门有效：完整技术验收 PASS；外部规范未验证不能称其 PASS。分别列本轮报告质量 QC 与历史失败 A/B 归因 QC 的范围/依据/状态，质量 PASS 不等于技术、候选或历史 PASS；准确报告技术/历史未证可质量 PASS，但本轮关键缺陷/修法/有效性主张缺证仍质量 UNVERIFIED、确证错误 FAIL。FULL_ACCEPTANCE/UNATTENDED 报告写入的交付还须独立质量审核闭合；无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题 PASS/UNATTENDED_COMPLETE，同时保留历史 UNVERIFIED/本次未请求，不冒称历史 PASS。确有必需历史门缺证仍阻包含该门的原请求全通过，不抹掉已证当前范围。保留旧行及来源，透明纠正无依据旧结论并说明原因/未证范围，不删行逃避实际错误修法或分类。
- 显式无人值守，或本次验收清单确需外侧证据时，按获准相关范围只读核当前task tests外正式材料；标准局部作业不新增全题外侧巡检或额外独立QC门，CONSULT/READ_ONLY仅回复、不写QA。适用检查的已查范围及问题路径、证据、影响、责任、移交写同根QA，未发现也记范围，独立QC核记录及对象；不扫工作区、不读.pipeline/秘密，GT/oracle答案仅独立QC核。外侧无关/建议不阻tests通过，真影响必需判据则对应结论BLOCKED/UNVERIFIED/FAIL；tests侧通过与整题外部阻塞分报。环境/冻结路径问题核合法恢复路径后，真实无法继续才停止对应范围并移交；说明和移交不等于修复或通过，未闭合必需门不冒UNATTENDED_COMPLETE。

历史异常不自动归责本轮；若影响 grader 或 evidence 可信性，只限制相关认证。本轮新增越界写必须先核实合法处理；不要删除未确认归属文件。人工、负责人、算法、平台不代签，不用其尚未发生否定独立成立的技术结论。最终分别报默认许可实际使用的角色/精确对象、准入/未准入对象、tests 内 instruction 实际修订/版本/双冻结及复验状态、tests 外 instruction 只读需求与移交状态（外部变更单列来源）、本地 oracle 是否实际执行、真实运行与对应验收状态；历史维护记录不改写为本轮实际验证。解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史；缺逐题批准不再作为停止原因。

“可交接补验”不许可提前停工：仅用户要求阶段性交接或 [连续执行停止闸门](continuous-execution.md#4-最终回复前的停止闸门) 已确认真无合法路径时采用。否则继续自主恢复、修入口、补生产运行证据及独立复核；静态报告 PASS 不代运行有效性或完整技术 PASS。
