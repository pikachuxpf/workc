# Seal / RewardKit 架构与判分技术参考

本参考不决定作业范围或外部规范采用。先读 [主Skill](../SKILL.md) 和 [路由](routing-and-authority.md)。仅正式采用0917 profile时要求其专用结构；RewardKit名称或文件名不等于采用该profile、实测交付或新版判分对齐。有效legacy不强迁移，其他RewardKit沿自己的schema/runner，hybrid追全部真实加载链，unresolved不猜。

按 [质检默认许可与准入合同](qc-exceptions-and-admission.md)：WorkC 目标明确后相关 GT/oracle 静态 QC 及必要合法本地 oracle 验证不需逐题单独批准。题包写集合为当前 task 的全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、legacy judge.py、runner、helper、shim、instruction、config 均可按正式依据修复，不按文件类别冻结。tests 外除同根 QA 均只读/移交，包括外侧 runner、业务实现、persona、environment、solution、Dockerfile、依赖、根 manifest、shim/helper、instruction；移交不算已修复或 PASS，不据 tests 写权编写业务实现。QC 独立核验且整个 task 绝无写权，CONSULT/READ_ONLY/RUN_ONLY 不变成写作业，用户显式局部、只读或路径限制优先。目录/glob、同名/别名/链接不扩权，写前核真实规范化目标；指向 tests 外的链接/别名目标不可写，无根报告写权不改 tests，不建 sidecar/整题副本。独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，实际作业允许执行时才经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果及别名、链接、挂载落点须实际文件系统只读边界，-B/cache开关不替代防写；仅题包外独立已获准scratch，不作源码副本/补丁/staging。先核入口/import/collect/子进程副作用及隔离，无安全入口不动态运行并移交协调者，后者仍守自身权限/隔离；不新增安装/配置修改/重启/候选/网络/外部judge权。CONSULT/READ_ONLY及默认静态REPORT_QC不运行，judge 凭据与候选隔离。Skill 维护不启动题包作业或授权新普通候选/外发。目标不明先核事实，工具拒绝、明确用户限制或无安全入口仍阻止相应操作。

**本页修复/移交接口**：写范围按 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围)，闭环及 QA 按 [执行 SOP](execution-sop.md) 与 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 含 judge/runner/helper/shim/config/instruction；获准范围内确认缺陷须 worker 实际修复、适用验证并写同根 QA，不能仅给建议、登记、移交或因类型标 OUT_OF_SCOPE。结构/入口/注册/聚合的内部可修缺陷先保全修验，再补依赖验证，不以当前入口失效自动否决入口返修准入或移交环境；不以空文件/自创合同救绿灯。QC 只核验、不写任务。

相关允许的 tests 外发现直接入同根 QA，列精确规范化路径/版本、证据、影响及责任/移交方，不改外侧。外侧 SDK/依赖/manifest 等缺口仅在实际影响当前必需依赖时限制对应结论；其余记录后继续 tests 修验，不等待外侧整改。明示局部/只读/RUN_ONLY、真实目标、preimage、安全与答案隔离不变，不新增安装、执行、网络或业务实现权限。

## 1. 架构身份与正式0917结构

| 职责 | Legacy | 正式采用0917 profile |
|---|---|---|
| 质量/语义源 | runner消费的rubrics.py等 | 可选tests/process/quality.toml criterion与react_prompt.md |
| deterministic源 | 实际评分test_outputs.py等 | process/output/safety各canonical checks.py的注册项 |
| 索引 | runner映射 | tests/criteria_manifest.yaml，投影不新增身份 |
| 入口/聚合 | 实际test.sh/grader | 实际RewardKit/Seal runner及reward配置 |

0917 canonical结构：

```text
tests/
  criteria_manifest.yaml
  process/
    checks.py
    quality.toml       # 可选；存在则绑定唯一react_prompt.md
    react_prompt.md
    reward.toml        # profile允许的可选配置
  output/
    checks.py
  safety/
    checks.py
```

三维各恰好一个直接canonical checks.py和唯一manifest是该profile要求，deterministic-only可无quality/prompt/reward，无适用评分事实按schema表达空注册不凑case。其他RewardKit允许的TOML以实际schema为准，不用0917示例否定其reward布局。

记录expected/discovered/canonical/status/digest；核缺件、alias、大小写碰撞、重复、实际loaded path与scorer target。结构缺件不补空文件救绿灯；正式来源足以独立推导修法且在获准 tests 范围内时，由 worker 保全后实际修复、验证真实加载/注册及受影响判据并写同根 QA，不因缺件类型仅移交或标 OUT_OF_SCOPE。若配置合同冲突只阻塞相关认证，不凭诊断自动废弃整题。

## 2. Quality/prompt的profile条件

正式0917只允许process quality，存在时同目录唯一react_prompt.md，judge="react"、prompt_template="react_prompt.md"；路径、变量、实际加载digest与schema核实。prompt不提供新增业务义务、身份或权重。

配对缺失、重复、alias/大小写、归属歧义、绑定错误是确认结构风险。**在正式采用规定弃用及禁止自动补prompt的批次时**按其DEPRECATED/ABANDONED与移交；其他profile记录具体FAIL/BLOCKED，不从历史规范自动弃用整题。不得猜写、拼接、从候选/Oracle/旧题推断prompt救绿灯。只有当前正式合同认可该处理、存在完整权威模板且实际runner支持时，才能按合同处理；tests 内写入使用当前授权（FULL/无人值守默认 `tests_allowlist=tests/**`），不另设文件子集批准门，用户显式更窄限制仍优先。正式合同依据不是额外路径许可，WorkC不自行发明judging架构。

Quality其余字段、Likert/binary/float、默认值与枚举沿实际版本schema，不合并不同示例。需要audit metadata/registry仅schema明许才进manifest；否则获准不被scoring-discovery的tests位置，缺合法落位移交。不要因技能偏好新增正式入口必跑的validator或两mutation门；若正式合同要求validator，再核实际接入及漂移负控。

## 3. Manifest投影与身份

常见字段version/score_range/dimensions/criteria及angle_id/angle/rule_hint/dimension/weight/evidence/scorer/score_type/source只作结构线索，实际schema优先。summary/partial_credit等仅明许时核，不加未知字段。模板是NON_AUTHORITATIVE scaffold，不提供固定ID、路径、权重、canary、GT引用或模型。

采用manifest合同的任务核双向投影：

1. 每个实际source criterion/check exact-once到合适行，行target解析到真实身份。
2. source→manifest→runtime→result命名映射明确，ID与name可不同但不歧义。
3. 在source、manifest、runtime、result各层先核实际成员列表、唯一身份及exact-once，再按明确映射核层间覆盖；不能先转字典掩盖重复，数量相同不证明成员一致。逐层追dimension、权重、evidence、skip和实际消费/聚合，无漏项、ghost、额外/重复计权；正式分组/批量映射可多对一，但不得丢身份或重复贡献。
4. quality行映射quality runtime，不要求对应checks；deterministic行映射实际注册check。
5. helper/diagnostic/preflight/未注册函数不冒充评分行。
6. source/evidence路径规范化并核producer/owner/backing state、actor、候选可写性、mutation path与freeze；字符串路径不证明authority。

Manifest本身不增加case，prompt/reward/目录也不增加。根manifest双副本只在正式合同要求时只读核，需改根副本则冻结移交，不为所有题创建副本。

历史RewardKit 0.1.7未原生消费YAML的观察不能推广到其他版本；实际loader优先。

## 4. Rules、答案空间与证据

先独立推导本次范围正式义务并记 `obligation_freeze_ref`，再冻结评分设计、答案空间、判据、部分分、路由与聚合为 `scoring_design_freeze_ref`，之后核实现及受控答案对账。两份均绑定范围、正式版本、来源、时间，同版有效独立记录可重核复用；完整全题，局部修改及共享依赖。事实解析目标对象后复算，有限多解接受完整合法集/性质谓词，开放实现可行为测试；必要语义用正式允许judge而非个人关键词/参考原文。开放不必然LLM，缺架构/授权不外发救分。

WorkC 目标明确、独立双冻结可核后，未参与修复的独立 QC reviewer 默认可静态读当前题相关根 ground_truth.json/核相关 oracle 源码，不需逐题读取授权，记录 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先完成独立推导/冻结，不请求授权代替。QC 的非写入角色不等于永不执行；实际操作仍受 §1.1 和本次权限约束，READ_ONLY 仍不写不跑，CONSULT 不启动题包核查，REPORT_QC 默认静态、不自动取得运行权；默认许可不绕过明确用户限制或工具拒绝。协调者/修复方不读 GT、不接收答案原文、摘录、数值或可反推摘要；只收正式来源支持的缺陷位置、可推导性、结论及脱敏引用，不据 GT 改期望到一致，答案一致不证明评分正确。

Process核正式发现/工具调用/参数/禁止行为；Output核存在、真实格式、schema、成员/值、源码/行为和最终状态；Safety核只读、危险行为、合同/秘密/发布边界。某义务不在实际可观测证据中则说明限制，不从最终文件倒推真实过程，不以候选自述认证动作。

每条本次相关deterministic rule核helper/parser/baseline/排除分支，合法PASS和违规FAIL实测或明确推演。完整动态验收须实际证据；有限例不冒称穷尽。按实际义务选反例，不设无关配额：过程空集合导致all真空通过、遗漏/颠倒必要调用顺序；对象数量不变但换成员或读错字段；锚点仅在result提到路径、叙述“将调用”而无真实call，或真实call的对象/参数/响应不符；before-after错用不同主体、对象、字段、版本/时间段（须同一主体及可比状态，并有正式允许的变更关联）；否定/嵌套/Unicode、候选可写伪造及服务失败/坏payload被误作空集。合法等价变化不应误拒，缺失真实过程不由最终产物补证。

注册行为按实际SDK：追decorator/factory/显式rk调用、discover、Session criteria与最终结果。不要全局规定装饰器和调用必须成对注释/删除；不同版本可能自动注册或需要显式factory。停用/新增时核真实exact-once及权重，不能只grep文本。独立新进程避免模块cache；同进程discover重跑不是两个attempt。

## 5. Evidence与materialization

区分允许live source、candidate输出、frozen evidence、实际消费。逐义务绑定evidence producer（谁生产）、owner（谁控制）、backing state（实际读取的状态及版本）、候选可写性与mutation path（候选能否经文件、API、工具或共享状态改写它），再核来源权限、actor/对象/参数/响应、字段、时间、freeze摘要及实际消费。GET名称或只读调用不证明authority：其backing state仍可能候选可改；冻结候选产物也不能使其自证独立真值。候选产物可证明正式允许的提交内容，独立事实仍须正式认可的独立参照或状态证据。

区分肯定完成证据与负向安全事实：声称“已完成”须对应真实动作/结果，不能用空过程或候选自述补证；合法权威查询在正确主体、对象、范围与时间内成功返回空集，可证明该范围内无禁止事件，但不证明完成了应做动作，也不推广到未覆盖范围。核响应状态、schema、分页/截断及查询覆盖后才认空集；失败、坏payload、缺字段或未读到数据不是空集。live成功包括[]不得回退候选文件；失败同样不以候选文件补权威证据，服务失败是infrastructure不候选错。

task/materialization/policy 给正式载体与 recast；期望从允许输入独立推导。根 meta 不是自动真值，solution 不是义务来源。GT/oracle 只由前述独立 reviewer 受控离线对账，不成为运行时评分答案依赖、候选输入或正式 judge evidence，不外发答案、不由默认许可授权新模型上传。当本次作业允许执行且相关本地 oracle 验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不改 tests 外冻结入口；tests 内入口可按授权正式依据修复并复验，不凭 oracle 结果改义务，不让协调者/修复方、普通候选或 judge 接触隐藏答案，静态核查不冒充动态验证。`.pipeline/`对所有角色始终不读、搜索、hash、引用、依赖或挂载，不借副本/他人结果绕过；秘密不读不转写。构建上下文/whole-task mount 会暴露禁区则停止。

核fragment/resource/materialized target/io_target的实际合同与唯一权威载体；stale/distractor不当当前真值。只有正式必需映射才门控，不为未采用profile增加统一preflight配额。

persona按actor；HTML按正式可见内容口径不CSS/JS捷径；bootstrap不占正式业务提问上限、已有答案不ask-first；建议研究不升级强制；未披露服务/凭据/噪声不归候选。

## 6. 聚合、版本与freshness

按真实criterion→group→dimension→reward/gate逐层复算points/weight/归一/skip/error/degraded/fallback，并与source→manifest→runtime→result的exact-once身份链对齐；manifest行不重复计权。对本次范围全部可复算项，以正式输入及双冻结设计独立推导参照值，与实际实现/config、报告中的逐项/分维度/总分三方比对；不能仅由实现生成expected，或仅核报告自洽。非线性/动态分母按适用分支核，缺实际消费证据不认证复算已验证。无runner证据不声称默认等权或safety硬gate。必需义务须进入正式评分/通过关系，缺失是设计问题，不能代理自创threshold/veto。

部分分条件、前提、尺度、分母先冻结；核合法满分路径是否可达、互斥条件是否被错误要求同时满足/重复计分、skip/optional/error是否不当改变分母及有效权重。核心前提不满足不靠质量分补，不用clip隐藏超额。候选低分不等于grader错，Oracle高低分不反推尺度。

精确SDK版本由当前正式合同采用依据确定。已采用批次要求harbor-rewardkit==0.2.0则核精确pin与实际容器同版，不用0.2.1或前缀匹配；tests 外 Dockerfile/依赖冻结、只能移交；tests 内同类配置可按正式依据修复并复验，但不擅换正式版本要求。不是全局常驻版本门；纯文本/AST解析无需装SDK，依赖版本相关执行须实际同版。历史0.1.7/0.2.0行为仅风险线索，当前受影响沿入口复验。

FRESH需当前相关grader/prompt/evidence/config/runner/版本依赖一致且范围足够；修改只失效受影响结果。定向PASS不冒称全量，兼容有效历史证据可引用，不拼不兼容版本。日志无字段不造。

tests 内正式 instruction 可按获授权正式来源合法修订，不另设路径批准门；写前在同根 QA 保全完整 ROUND_PREIMAGE、起始状态、正式来源/映射及版本，记录实际 diff、版本前后与合同影响。tests 外 instruction 只读/移交，外部修订另记可核有权来源。两类正式合同变更都将受影响旧义务/评分设计与依赖运行证据标 STALE；未接触隐藏答案的设计角色从获授权新正式来源重新独立推导义务，再冻结评分设计，双冻结受影响范围，重核 tests、注册聚合、候选可见载体及适用真实验证。不得从隐藏答案、候选输出或低分反推合同救分；已接触答案的 QC reviewer 不承担独立设计，仅按新冻结核终态。不通过新合同追认历史候选违规。

开工按依赖记 `admission_status=ADMITTED/NOT_ADMITTED/N/A` 及 `admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`。历史必需性依 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 按明确历史验收请求、适用正式采用条款或当前主张依赖确定；按具体主张所需核旧ORIGINAL_TASK、反馈/失败身份映射及HISTORICAL_TRAJECTORY，在依赖返修/历史QC前实际VERIFIED或有具体对象/版本/条款的正式替代接受记录，不一律捆绑。快照、ROUND_PREIMAGE、handoff指标、新run不替代相应旧证据。每个授权tests写目标先在唯一根报告合法保全完整ROUND_PREIMAGE、起始状态、最小完整修改单元/上下文，原不存在记ABSENT，hash不足。有限合法查源，可恢复先恢复，权限不足记阻止，确穷尽记EXHAUSTED/历史验收NOT_ADMITTED，仅新来源、权限或版本变化时重试已穷尽来源，不启动依赖循环；独立不依赖该历史的当前范围（包括FULL_ACCEPTANCE）可另列准入，确属本次必需历史QC门仍保留，缺证不能称包含该门的原请求全通过或自行换验收口径。

修前 future_run_plan 核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、合法 evidence/来源、隔离挂载、版本依赖服务预检、逐项聚合取证位置及失败责任；先处理获准且可修的 tests 内验证入口缺陷，保全并安全修验该入口不被其当前失效否决；排除此路径后仍已知不能合法生产必需验证，才不启动依赖该缺口的返修，修前不要求已有修后结果。计划/预检/ADMITTED不填CURRENT_RUN=VERIFIED、不认证PASS；修后实际正式CURRENT_RUN核身份、真实消费、逐项/聚合、degraded、FRESH，服务/运行失败重新评估准入并停止受影响完成声明。声明表/辅助工具不认证准入，只读仅审材料、不写不跑。

## 7. 已采用新版对齐与外部QC

FULL_ACCEPTANCE的全题技术核查不以外部两遍QC采用为前提；使用 [pre-delivery-qa-fusion.md](pre-delivery-qa-fusion.md) 的全题技术清单核全部实际判据、证据与聚合。LOCAL仅核受影响项及依赖，只读不跑；上述技术清单不扩读写/执行授权，不替代真实消费证据或外部回执。

只有当前正式采用《RewardKit判分与人工标注对齐》才执行其LLM最终有效占比≤40%、适用关键词空壳/数值替换/内容缺失三负控及规定两向消融。线性嵌套复算每层权重；非线性/动态分母核适用情形与上界，不按条目数量估计，不随意删语义case。

同一合法真实基线/evidence、单变量、实际评分链取逐项/分维度/总分；去judge后事实错误仍按正式判据拒绝，必需语义对应负例非装饰分。无正式“明显失分”数值阈值不自创cutoff；缺合法覆写接口/隔离/授权阻塞该认证，不能改 tests 外冻结配置或污染正式基线；tests 内配置修复另按正式依据保全、记录依赖并复验，不借消融调门救分，不自造轨迹证明动作。

rubric 实测交付、两遍 QC 及其两 attempt/三等价样本/覆盖门分别核采用，形态匹配不等于全部启用；已采用不借单题豁免。相关 GT/oracle 静态对账按现行独立双冻结后的 WORKC_DEFAULT，不需逐题批准；必要合法本地 oracle 同按统一合同，不扩新普通候选/外发；tests 内正式 instruction 可按获授权正式来源合法修订并保全 preimage/版本、重新独立双冻结与复验，不另设路径批准门；tests 外 instruction 只读/移交。仍冲突的 .pipeline/禁读、明确用户限制、工具拒绝、无安全入口、未授权执行/外发或唯一报告要求单列并限制相应外部 PASS，不以默认许可删门，继续合法质量检查。解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史。详见 [runtime-acceptance.md](runtime-acceptance.md)。

## 8. Judge与失败归因

沿实际quality或其他runner配置确认活跃judge，无judge不访问judge.env。实际相关验收读 [judge-chain.md](judge-chain.md)，逐项prompt/证据消费、请求响应关联、raw合法域、转换、聚合及cache/freshness。

401/402/429/5xx、超时、缺挂载、degraded是infrastructure，不静默PASS或候选0。采用rubric_delivery_requirements时非空reward_degraded使该轮全部judge结果无效并须补跑，独立有效确定性证据仍可保留；其他合同按明示范围。框架无原生blocked通道时用正式认可预检/错误状态，不伪造候选分。辅助响应校验不是生产接入或语义正确证明。

秘密只由不会启动候选的受信任judge解析已有引用，不由代理/调度/候选读值。模型审查不代签人；必需judge缺真实证据时对应语义验收未完成，独立确定性证据可保留范围。

## 9. 指标、报告与本次范围收口

计数权威集中在 [verification-and-reporting.md](verification-and-reporting.md)：正式profile基线R0/T0/N0固定，F与AR/AT/A跨轮更新；manifest/prompt/回归函数不新增评分身份。0917可解析quality条目与实际runtime库存分开，不从当前身份反推失踪原基线。N/A不是质量门。

授权 tests 修改更新同一根报告，核心结构+适用 judge/外部门，不机械全填；只读不写。本轮报告质量 QC 与历史失败 A/B 归因 QC 依 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 分别判定，不沿用单层总标签。REPORT_QC 明示窄范围优先，未指定时识别并核两层。所有本轮新写/更新 QA 都审范围/来源、实质缺陷/归因/修法、实际变更、运行/验证/freshness、指标、阻塞与状态；无 always-failing、零缺陷或未改 tests 不使质量 N/A。关键缺陷/修法/有效性主张缺证质量 UNVERIFIED、确证错误 FAIL；准确报告技术/历史未证可质量 PASS，但不等于技术、候选或历史 PASS。

开工及收口从请求、正式映射/manifest 与 rubric/test 失败标记、允许反馈/既有 artifact、已有 QA 历史发现对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED、对象/反馈ID、来源版本/已查结果和缺口影响；不扫工作区/禁区。确认无对象才历史 N/A，报告自 N/A、无 A/B 表、未找到清单不自证。已审未知或对象存在但旧材料缺失保留历史 UNVERIFIED，未审且未请求明确记本次未请求；相应依赖历史 NOT_ADMITTED，有限合法查源。按 §7.2 对象存在/未知或历史未证不增门，FULL_ACCEPTANCE/无人值守/模板本身也不增普遍历史门；不阻独立当前范围（包括全题）修验/质量审核，确属本次必需历史门仍保留。历史层按具体主张依赖核原反馈、权威原task_path（旧修改对照）、断言/可推导性、全部提供的相关轨迹（旧行为）、A/B、旧修法及终态。

复用技术、issue 与轮次引用，不复制台账；本轮缺陷/实质修法留正式依据/断言、反例与独立预期、观察/归因、写前完整上下文、实际 diff/终态、适用验证/run/版本/freshness及未证责任。主动静态发现不虚构旧 Agent 失败，未执行标推演/NOT_RUN，未验证不标 FIXED+FRESH。ROUND_PREIMAGE 只证明本轮起点，不自动替旧 ORIGINAL_TASK；本轮漏留为 WorkC 生产缺口，如实记、合法查源，不倒填。协调者对所有本轮报告写入自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部按影响/风险复核，不新增全题独立门。先完成实质报告再审，反馈复检对应结论；任何报告变更核对应内容，技术按依赖失效补验，不空重跑，最后仅追加准确回执不无限自指。

保留历史与原反馈映射、证据新鲜度，历史维护记录不改写为本轮实际验证。本轮 allowlist 外写须停止处理，既有历史/用户/平台变化按真实影响记录，不擅删。最终分报本轮质量与历史归因的状态/范围/依据；按 §7.2，无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题 PASS/UNATTENDED_COMPLETE，历史仍准确 UNVERIFIED/本次未请求，不冒称历史 PASS。确有必需历史门缺证仍阻包含该门的原请求全通过，不抹掉已证当前范围。透明纠正无依据旧结论，保留旧行、来源、纠正原因及未证范围，不删行逃避实际错误修法或分类。

最终先本次对象，并分别报默认许可实际使用的角色/精确对象、准入与未准入对象、tests 内 instruction 实际修订/版本/双冻结及复验状态、tests 外 instruction 只读需求与移交状态（外部变更单列来源）、本地 oracle 是否实际执行及真实运行状态：局部必需项闭合可称局部完成，整题未审不泛称PASS；补验交接不是动态验收通过；完整验收全题门闭合才PASS。外部人工/算法/平台未请求不门控tests，未获回执不代签/提交。
