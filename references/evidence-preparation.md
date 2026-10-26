# 修改前备证、合法补证与指标建账

本参考解决“本来可取的材料没取、修改后原状态丢失、运行没有留证、跨轮指标未建账”这些流程缺陷。不能创造已丢失的历史事实。它适用于标准与无人值守模式；CONSULT/READ_ONLY仍不写、不运行题包。默认许可与准入以 [qc-exceptions-and-admission.md](qc-exceptions-and-admission.md) 为统一合同：WorkC 目标明确后，相关 GT/oracle 静态 QC 及必要合法隔离本地 oracle 验证默认许可，不请求逐题批准；tests内instruction属于授权测试侧修复，tests外instruction仅只读、记录移交；Skill 维护不启动实际题包。证据仅从本次合法范围取得，独立非写入 QC reviewer 先从正式输入独立核义务和评分设计，再核先义务后设计的双冻结，随后静态核精确相关 GT/oracle，记录 qc_permission_basis=WORKC_DEFAULT。协调者及设计/修复角色不读 GT、不接收隐藏答案或可反推答案的摘录/数值/摘要；reviewer 只给正式来源支持的结论与脱敏引用。GT/oracle 不成为义务来源、运行时答案依赖、候选输入或普通 judge evidence，不外发答案。.pipeline 对所有参与者继续禁读、禁引用、禁依赖，禁止搜索/hash/挂载及副本/他人结果绕过；凭据值不读不转写。独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，仅实际作业允许执行时经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果及别名/链接/挂载落点须实际文件系统只读边界，-B/cache开关不替代防写；题包外仅独立已获准scratch，不作源码副本/补丁/staging。先核入口/import/collect/子进程副作用，无安全入口不动态运行并交协调者，后者仍守自身权限/隔离；不新增安装/配置修改/重启/候选/网络/外部judge权，默认静态REPORT_QC不运行。作业员单点写整个tests/**与同一根qa_report.md，写集合硬锁；tests/test.sh、tests/judge.py及tests内runner/shim/helper/instruction/config均可按正式依据修复，不另设冻结子集或allowlist审批。tests_allowlist映射本次实际操作范围，默认tests/**+根QA，用户明示局部/只读/禁改/更窄路径限制优先；tests外除根QA均只读移交，包括外侧instruction/runner，规范化真实目标在tests外的别名/链接不能写；根QA仅授权真实同根qa_report.md，不借其别名/链接扩至其他外侧目标。移交不算修复或PASS；整个tests写权不授权秘密/GT读取或答案暴露。用户明示只读/禁改/禁运行、更窄范围及工具权限拒绝优先，默认许可不扩普通新 candidate 或外部 judge，也不绕过安全边界。

## 1. 不以一句证据不足结束：先建立取证计划

内外问题处置统一按 [SKILL §2](../SKILL.md#2-先选本次作业固定验收范围)，详细登记按 [报告合同 §2](verification-and-reporting.md#2-状态归因与证据范围)。修复/交付范围内已确认的 tests 内缺陷（含 runner/config/helper/instruction）必须实际修复、完成适用合法验证并在同根 QA 写实际修改/结果，备证、记录或移交不替代返修；明示只读、局部、指定运行及真实证据/安全限制仍优先。

先从允许正式输入独立推导义务并记录 obligation_freeze_ref，再独立冻结评分设计、答案空间、判据、部分分、路由和聚合为 scoring_design_freeze_ref；两份记录绑定范围、正式版本、来源及时间，同版有效记录可重核复用。双冻结后、首次授权 tests 写入前，为每个本次实质结论列证据需求，按具体结论/作业依赖确定 required，不把所有历史材料无条件加给所有作业。开工及收口按 [历史对象与门控统一规则 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 核允许来源，分别记录对象存在性、审核状态和本次必需性；复用既有矩阵，不新增状态机。仅缺历史证据的声明不能靠新运行替代；缺当前运行可以按授权补跑，但修后未来结果不列修前必备。

记录 qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads，scope 列本次相关精确读取对象，实际已读与计划分开；实际动态核验在现有运行/证据/轮次表记执行者、无秘密命令/模式/版本、输入输出范围及实际只读/答案隔离、结果/freshness，由协调者写授权根报告，QC不写任务QA、不新增审批/台账；精确对象与适用依据用于范围审计，不是用户逐项批准。没有某条外部条款时，当前明确 QC 目标可作必要性依据，不空造条款；未双冻结先独立推导/冻结，不请求授权替代。tests内instruction需求核正式载体、版本、作用及正式可推导缺陷后，可在本次授权内修复，先留preimage再记实际diff/终态与验证；tests外instruction仅只读记录精确对象、依据、影响、责任与恢复条件并移交外部有权负责人，不修改，移交不是已修复或PASS。授权tests写前核规范化真实目标，目录/glob、同名、链接或别名不能让tests外真实目标获得写权，根QA仅按单独授权；tests_allowlist仅映射实际操作范围、默认tests/**+根QA，不另审批或设冻结子集，定位失败是事实缺口。仅审核、READ_ONLY/CONSULT/RUN_ONLY 不因此变成写作业，用户明确更窄范围或禁改优先。

| 证据类型 | 必需内容 | 不能替代它的材料 |
|---|---|---|
| ORIGINAL_TASK | 证明相对权威原题的历史修改时所需 QC manifest/mapping 指向的原 task_path、task身份/版本、具体对象及可核原文件；不是每个当前主张的前提 | 当前快照、ROUND_PREIMAGE、.bak、未绑定该映射的Git版本、只有hash/mtime、handoff指标 |
| ROUND_PREIMAGE | 核本轮实际修法所需各授权 tests 目标存在状态、版本/hash、可访问原内容或最小完整修改单元及上下文；原不存在记ABSENT；配合正式依据、diff/终态及真实验证 | 修改后回忆、只报hash却无法比对修法；它不证明旧历史 |
| HISTORICAL_TRAJECTORY | 证明旧候选行为/失败原因时所需原 attempt 与反馈/失败映射、正式producer、允许位置真实轨迹/产物、失败断言及相关行为；不捆绑给无旧因果依赖的当前主张 | 合成fixture、新rollout、只重评分而没有原行为记录、handoff指标 |
| CURRENT_RUN | 当前grader/config/evidence下已有真实结果或修后实际取得的正式运行逐项/聚合、阶段结果、run_id、来源与freshness；当前同一 attempt scorer 核该 attempt 真实 evidence 与当前评分/消费/聚合，不强要无关两类旧材料；与future_run_plan分开 | 未来计划/预检、stub、纸面分数、rc=0、旧不兼容版本 |
| SCORING_BASELINE | 原评分身份逐项库存、正式profile/来源/版本与计数口径、F根因/新增继承关系 | 当前函数数、回归数、运行数、修改次数 |

每个需求记录 `evidence_id / claim或反馈ID / kind / scope / required / source_authority / source_ref / expected_content / actual_ref / status / acquisition_actions / remaining_gap / owner`。来源清单只含任务相关、已授权位置，不递归整个工作区/用户目录，不扫描禁区或秘密。

证据收集状态：`AVAILABLE_UNCHECKED`（发现待核）、`VERIFIED`（当前对象实际核实）、`MISSING_RECOVERABLE`（有合法补取路径）、`NEEDS_AUTHORIZATION`（确需本次范围外的普通新候选、外部调用或其他未获许可动作，不用于缺逐题 GT/oracle 批准；tests内instruction属授权修验，tests外instruction只读移交，不以此要求allowlist审批）、`EXHAUSTED`（具体合法来源与补证动作已核、仍无材料）、`N/A`（有正式不适用依据）。实际核为 VERIFIED 的证据才支持对应必需门；旧材料的正式替代按下述有权负责方可核接受记录，只在接受范围内使用，不将仍缺的原件标 VERIFIED。N/A不当PASS。同步验收状态：未执行NOT_RUN，真实性/内容未证UNVERIFIED，具体权限/禁读/环境阻止BLOCKED；EXHAUSTED不是假通过。

### 开工准入与未来运行计划

记录 `admission_status=ADMITTED / NOT_ADMITTED / N/A`、`admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`。准入是作业员按本次依赖范围逐项实际核验，不是用户批准，不要求逐项批准；不能由声明表、指标或 checker 自动认证。解除操作授权条件不取消材料准入或正式 QC 证据接受要求。

- **旧材料**：仅对应历史主张必需的 ORIGINAL_TASK 或 HISTORICAL_TRAJECTORY/反馈映射须 VERIFIED，或由有权方对具体对象/版本/条款正式接受可核替代；材料选择按 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论)，不为每个当前结论/同一 attempt scorer 要两类旧材料。缺项先按第3节合法恢复；穷尽或真实限制仅使依赖项 NOT_ADMITTED，不循环等待、不由作业员自签替代。材料审计可先做，不能冒称依赖历史 QC 已准入。
- **写前保全**：每个 授权 tests 目标须有可核 ROUND_PREIMAGE、起始状态、完整修改单元/上下文或 ABSENT，合法保存/引用在唯一根报告；无保全或无根报告写权不写该目标，hash 不替完整修法证据。
- **未来结果生产**：修前核 future_run_plan 的必需入口/模式、本次作业运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，普通新候选/外部 judge 另依实际权限）、合法 evidence 与来源、最小挂载及输出/凭据隔离、版本/依赖/服务预检、逐项/聚合结果获取位置、失败处理和责任。实际作业允许执行、验证必要且合法隔离可行时，独立非写入QC可按§1.1在双冻结及答案输出隔离后经已有有效入口直接执行本地oracle，协调者也可在自身权限/隔离内编排已获准运行而不读隐藏答案，仅收脱敏状态/结果引用，不请求逐题oracle另批。先区分内部可修入口缺陷与真正外部/安全限制：可在本次范围合法修复的 tests 内 runner/config/helper/instruction 必须先留 preimage 修复并验证，不以当前入口有错判外部环境阻塞或拒绝依赖返修；确因写/运行权限、证据或安全条件无法合法生产必需验证时，才停止受影响范围。修前无需已有修后结果，计划不得标 CURRENT_RUN=VERIFIED，也不保证未来服务不会失败。
- **最终验收**：修后取得真实 CURRENT_RUN，核身份、真实消费、逐项/聚合、degraded 与 FRESH；仅 ADMITTED、计划或预检成功不认证 PASS。运行失败或服务变化重评准入，保留已证范围，停止受影响完成声明。

历史材料缺口、旧 QA 主张纠错和全题继续验收统一按 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论)。合法可恢复先恢复；不可恢复/EXHAUSTED 复用证据需求与 issue/轮次，记录精确主张、对象/版本、attempt/材料、权限依据、实际路径/动作/结果、影响、责任与新触发。无新来源/权限/版本不重查同一穷尽项；只停实际依赖项，继续独立 CURRENT FULL scope，不降为局部 workaround，不自签历史替代接受。

## 2. 三种基线分别保全，不能合并冒充

### 权威历史原版

先核用户提供或正式批次manifest/mapping的原task_path；若有多个来源，逐一核task、版本、反馈对象。当前目录、.bak或平台文件名相似不能自动当权威。既有Git/发布归档仅在正式来源映射指向其版本时可用，不能随手挑一个commit认证历史。源不存在先沿同一正式记录中给出的合法artifact/恢复映射取证，不无界猜目录。

历史认证实际采用的QC唯一原task_path要求仍有效，仅限制该历史依赖范围，不自动成为当前tests交付门；WorkC不能单方宣布根报告中的preimage或可信runner产物取代它。正式证据替代仍须现行QC规范指定的负责方，或当前批次明确有权决定证据接受的负责人接受，具有可核记录（接受者职责/时间/具体条款及对象/版本/接受范围）；协调者、reviewer和工具结果不代替该接受，未指定接受权限时不能自封。恢复或替代证据须有明确接受依据和原task_path/版本映射；这只解决被接受的具体核查，不能改变历史事实。此为正式 QC 证据接受要求，不是已解除的逐题操作批准，不能取消或自造历史。

### 本轮起始版

在每次写授权 tests 目标前，作业员先记录该文件允许范围的起始状态、SHA-256（字节口径）、原评分身份或正式合同版本及计划修改的完整单元/相关上下文，核对应实际 tests_allowlist、规范化实际目标及写范围硬锁；tests内instruction/runner/config均可为写目标，不另设冻结子集或allowlist审批；tests外instruction及其他外侧目标除根QA均只读移交，用户明示更窄限制优先。记录在同一根报告，或引用已存在、来源可信的不可变允许版本；不得创建题包.bak、复制整题、sidecar/staging目录或在题包外私造副本绕过边界。根报告不存整题业务原文、秘密、GT/隐藏答案或禁读内容。

若修改单元含敏感内容，不能转写；记录摘要/合法载体引用。若仅局部片段无法支持后续修法审核，应先取得可访问的权威原内容，或正式认可的最小文件保全接口。正式runner保全须已获准且只涉及最小允许对象，来源绑定原版本，不扩大读写权。没有合法保全方式则暂不写该目标；其他独立可保全对象可继续。

文件本来不存在时记ABSENT与身份来源；新建不编造preimage。删除/大范围重构需要足以证明被删内容/相关行为的原内容，不能用几行摘要冒充全diff。授权 tests 写入前已有根报告记录可核起点，写后同步实际 diff 与终态；tests内instruction需求按授权留证、修复、验证并登记；tests外instruction需求仅列只读对象、正式可推导缺陷、影响与移交责任，不修改。中断后先核最后保全版本，不从改后文件回填。

若开工前已有人修改且最初原版缺失：本轮起始记录只证明本轮，不证明旧修法。ROUND_PREIMAGE 不自动成为权威 ORIGINAL_TASK；可信原题恰为未返修起点时按正式来源/身份核实，不强造另一条路径。保留历史缺口并建立后续本轮可核链，不阻独立本轮修法/报告审核。

若 WorkC 本轮已经修改却漏留原内容，这是本轮生产缺口，不是外部历史缺失免责。记录受影响 issue/目标/轮次与缺口，核合法可信恢复来源及结果；相关修法主张未证，不从改后文件、回忆、hash或自造副本倒填 preimage。恢复来源须绑定实际写前版本，无法恢复保留 UNVERIFIED；不把所有未来可独立备证的轮次永久写证据不足。

交付及接续还须按 [回顾登记](verification-and-reporting.md#731-回顾登记先对账不能把漏写当灭失) 核 QA 与实际发现/变更/验证的漏项。证据仍在只漏登记时主动核来源补齐，标事后登记/找回，不把未写报告当 EXHAUSTED；只有回忆则查可信来源、缺证不补造，事后恢复不伪称已写前保全，也不抹本轮生产缺口。局部只核相关范围，只读仅回复；登记与证据真实性/修法正确性分开审核。

### 评分身份与指标基线

按verification-and-reporting的正式profile记录R0/T0逐项库存，不仅一个N0总数。每行有内部唯一`key`、`kind=criterion/check`、实际源ID/位置、计数依据和版本；重复/缺ID条目用可追溯内部key区分，不修饰成合法runtime身份。注册/消费异常另记，不用库存正常冒充运行正常。

只有来源证明当前评分集就是该正式合同最初未经返修的版本时，才建立`origin=original`原题基线；“新作业员自己还没改过”不足以证明原题未修改。同版返修引用可信原基线，不重算N0。版本已被历史修改或历史状态无法证明且原基线找不回时，原题累计指标仍不可伪造，但可以**另立接手阶段基线**，明确`origin=handoff`、起算时间、scope和遗漏历史；只算之后的修复/新增，标“接手阶段指标”，不称原题累计。无需改历史数据，属于当前授权作业的描述性统计。

F逐issue记录是否基线根因、修复路径、fresh验证证据；F与原评分身份不是一对一，可能超过N0。新增/继承/删除逐评分身份对账。无新增且已核完整库存则A=0，不因没有新增而N/A；部分库存/身份不可证时相应数值待核，不能假设0。

## 3. 自动补证顺序与授权

对MISSING_RECOVERABLE项按以下顺序执行，不先宣告不可恢复：

1. **本请求材料**：核明确提供的manifest、反馈清单、原task_path、轨迹路径及运行索引；只读文件内容，先核对象/版本再采用。正式映射中的明确父目录可以有限列名找记录，不递归整个任务或工作区，不读禁区。
2. **现有正式来源**：沿明确映射的原版、获准Git对象/批次artifact、已产生正式run结果，核producer、身份、完整性和时间。远程下载/认证访问按现有授权，不上传题包换材料，也不读凭据值。
3. **旧attempt重评分**：真实已有轨迹/产物完整且当前门允许时，由作业员依实际权限运行正式verifier-only，或由独立非写入QC按§1.1经已有有效隔离入口独立运行本次必要已获准verifier-only取得当前评分；绑定原attempt→新run，不恢复不存在的旧行为，不新计attempt。
4. **新证据生产**：缺当前正式运行时执行本次合法入口；实际作业允许执行、必要且合法隔离可行的本地oracle按WORKC_DEFAULT，由独立非写入QC按§1.1在双冻结及答案输出隔离后经已有有效入口直接执行；协调者也可在自身权限/隔离内编排已获准运行而不读隐藏答案，仅收脱敏状态/引用。普通新rollout/外部judge 仍须对应明确权限、隔离和真实输入；缺该权限记 NEEDS_AUTHORIZATION，不由默认 oracle 许可、“必须解决”或无人值守推导外发/候选授权。新attempt若合同认可可满足当前交付门，不能替代旧报告历史归因。
5. **结果收集与验真**：同一run记录stage、freeze、真实消费evidence、逐项/聚合及degraded、结果artifact摘要；发现存在只是AVAILABLE_UNCHECKED，经核才VERIFIED。正式工具应在获准隔离位置保留产物，不能只把终端一句PASS抄到报告。
6. **移交**：合法动作确已穷尽或确不可恢复，或用户明示限制、工具拒绝、范围外动作缺权限、无安全入口/服务阻止时，按 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论) 在既有记录绑定精确主张、对象/版本、attempt/材料、来源/权限依据、实际路径/动作/结果、影响、责任及重开触发。不能写“缺材料”一句就结束；无新来源/权限/版本不重复同一穷尽源或无效请求，只停依赖项，继续独立当前全题验收。

上述顺序不允许在旧材料 NOT_ADMITTED 时启动依赖返修；合法补证与新证据生产仅满足它能证明的具体门，不能恢复不存在的旧事实。静态核查本身不等于动态验证；本次作业允许执行、oracle 验证必要且合法隔离可行时，独立非写入QC可依WORKC_DEFAULT及 [§1.1](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 在双冻结及答案输出隔离后经已有有效入口直接执行，不再索要逐题运行批准。先核入口/import/collect/子进程副作用、版本、实际文件系统只读边界、最小挂载、题包外已获准scratch及输出/凭据隔离；协调者可在自身权限/隔离内编排已获准运行而不读隐藏答案，只收脱敏状态/结果引用；不让协调者/修复角色、普通候选或 judge 接触 GT/隐藏答案，不修改tests外或用户明示禁改的入口，不扩普通新候选/外部 judge；tests内入口修复仍须授权正式依据、preimage/diff及真实验证，不能在oracle核验中绕过答案隔离。CONSULT/READ_ONLY、用户明示禁运行、工具权限拒绝、需要未授权外部调用/秘密或确无安全隔离入口时停止对应运行，列真实原因，不伪造证据。

只读仅执行1–2中的合法静态查源，可回复材料审计与 NOT_ADMITTED，不import/运行/创建报告或称动态验收成功。题包不提供安全正式入口时不能手写替代评分器冒充正式链，也不能修改tests外或用户明示禁改入口；修复/交付范围内确认缺陷位于 tests 内正式 runner/shim/helper/config/instruction 时，必须按正式依据留证修复并重验，不以入口有错冒称外部环境阻塞；合法隔离条件成立前仍不执行依赖运行。结构与运行证据缺失分开，不把candidate正常失分当缺证。

## 4. 修改检查点、无人值守和收口

将备证插入 D0 起始定位、D1–D3 独立义务/评分设计双冻结后的 D4 准入及写前检查、D5 真实运行收集。仅所审主张需要的原版或旧轨迹/反馈映射须在依赖作业前 VERIFIED 或正式接受具体替代；每个授权 tests 目标先保全 preimage。修前核 future_run_plan 的本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT）、入口、隔离及证据可生产条件，修后实际取 CURRENT_RUN，不要求修改前已有修后结果。历史缺口不改变独立当前全题工作范围；依 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论) 逐项准入，不替真实历史门。

合法变更tests内正式instruction（作业员在本次授权内修复）或外部有权负责人变更tests外instruction、导致正式合同变化后，记录授权正式来源、版本前后、写前preimage/实际diff及影响；旧相关义务/评分设计及运行证据标STALE，由未接触隐藏答案的设计角色从授权正式来源重新独立推导并双冻结受影响范围，再核tests、注册聚合、候选可见载体及真实验证和独立复核。tests外instruction仍只读移交；已接答案reviewer不充当独立设计角色，不以GT污染修法，不用变更后的instruction追认旧candidate失败或放宽仍有效义务。

无人值守按 [现行路由](routing-and-authority.md)：唯一明确当前task、用户仅下达“无人值守”且无明确更窄/只读/禁写限制时，默认FULL_ACCEPTANCE当前全题tests侧自动修复验收，本请求许可整个tests/**与同根QA写入；worker将tests_allowlist映射为实际操作范围（默认tests/**+根QA），不另设冻结子集或allowlist审批，明确限制优先，早前仅作业标签不阻新默认。worker从正式材料独立双冻结，先查源/合法补证与实际准入、保全preimage，自查修tests真实验证；完成实质报告后派未参与修复的独立非写入QC实际读QC文档，核当前task、本轮报告质量和外侧记录，分别核适用历史失败 A/B；无 always-failing、零缺陷或未改 tests 不跳质量审。worker核实反馈→集中tests/QA修复→按技术依赖补适用验证→独立复检对应结论。独立非写入QC可先审准入及三个基线关联，并按§1.1独立核必要已获准运行，不冒充worker的修验、不造材料、不参与返修；最后仅追加准确回执不无限自指。准入、双冻结、真实验证、答案隔离/外发/候选标准不降，内部自动核查不逐项要求审批。

默认只读检查当前task tests外相关允许正式材料；来源清单和同根 QA 记录实际范围、版本，相关允许发现直接写问题位置、证据、影响、责任与移交，不改外侧、不等待外部先修，不把全部外侧缺陷变成交付门，只限制实际依赖的必需项对应结论。未发现也记范围，不递归工作区、不读.pipeline/秘密，GT及oracle答案仅独立QC角色核。独立QC核外侧记录及相关实际对象。外侧无关/建议不阻tests通过；真影响必需判据则对应BLOCKED/UNVERIFIED/FAIL，tests侧通过与整题外部阻塞分报，移交不算修复、不冒UNATTENDED_COMPLETE。

无显式预算不默认8轮或2轮无进展停止；每轮缺口记acquisition_actions，尚有合法可修/补证路径就持续处理。重复无效动作/仅新增查源记录不算进展，须换查证、归因或修法，不能仅因计数停；只有真实无法继续才STOPPED_BLOCKED对应范围。STOPPED_BUDGET只用于显式预算耗尽，尊重用户退出；冲突的旧作业沿用及默认停止口径不再适用，其他细则保留。历史不可恢复的记录、实际依赖项停止及新来源/权限/版本触发按 [§7.2.1](verification-and-reporting.md#721-历史未证只限制实际依赖的结论)；无新触发不重复同一穷尽来源，继续独立当前全题验收。完成声明按同节分当前通过与原请求含历史门的全范围认证，不冒全历史通过。

结束时分别报：qc_permission_basis=WORKC_DEFAULT 的实际角色/精确读取范围、准入/未准入对象与依据、已取得材料及它证明什么、本轮授权 tests 修改前后链、tests内instruction修验/正式版本变化、tests外instruction只读需求/移交状态与外部变更来源、本地 oracle 是否实际执行及真实运行/freshness、仍缺材料及已尽合法动作、原题/阶段指标。不再以缺逐题 GT/oracle 批准停止；tests内instruction属授权tests修验，不另设冻结子集或路径审批，tests外instruction仅只读移交，用户明示更窄限制优先；未闭合需求按实际影响限制结论；分别列目标/正式映射事实缺口、材料灭失、用户明示限制、工具拒绝、无安全入口或未授权外部动作的实际影响。指标可计算不依赖整题PASS或外部人工签署；缺原累计不拖累可信阶段数值，handoff指标不替历史准入。现行报告接口按 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口)，分别列本轮报告质量 QC 与历史失败 A/B 归因 QC 的范围/依据/状态，不用旧总标签代替；本轮缺陷/实质修法复用技术、issue 与轮次引用，留正式依据/断言、反例/独立预期、观察/归因、写前完整上下文、实际 diff/终态、适用验证/run/版本/freshness与未证责任，不复制台账。主动静态发现不虚构 Agent 历史行为，未执行标推演/NOT_RUN，未验证不标 FIXED+FRESH。所有本轮报告新写/更新均质量自查，无缺陷也核事实、状态、运行与限制；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部自查、按影响/风险复核，不新增全题独立门。REPORT_QC 明示窄范围优先，未指定时识别并核两层。任何报告变更核对应内容，技术证据按依赖变化失效、不空重跑；先完成实质报告再审，最后仅追加准确回执不无限自指。关键缺陷/修法/有效性主张缺证为质量 UNVERIFIED、确证错误 FAIL；准确报告技术/历史未证可质量 PASS，不等于技术、候选或历史 PASS。历史审核状态、必需性及当前全题/无人值守完成声明统一按 [§7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用)，不把已证独立修复或已知整数抹成 N/A。

## 5. 辅助台账检查

`scripts/check_qa_ledger.py`从标准输入接收**仅非秘密的结构化台账声明**，不读取题包/路径/秘密，不自动取证、不写文件。它核需求状态完整性、身份继承/新增/删除与根因去重，并算未约分比例；返回missing_required及checklist_ready，只表示声明的完整性，不能证明来源权威、真实运行或验收PASS。

输入使用schema_version=1、baseline、current、fixes、requirements，完整格式及边界见脚本回归。作业员先以证据人工核实声明，再把本次结构化字段置同一根报告（可代码块或表格），通过stdin调用检查器，不另存台账JSON。完整库存已证时才填空列表为0；未知baseline/current/fixes填null以保留相应未知，不将缺数据默认为0。

最小示例（虚构声明，不是实测）：

```json
{
  "schema_version": 1,
  "baseline": {
    "id": "B0", "origin": "original", "scope": "whole-task",
    "source_ref": "正式来源及版本引用", "captured_at": "修改前实际时间", "verified": true,
    "identities": [{"key": "T0-1", "kind": "check", "source_ref": "计数依据", "verified": true}]
  },
  "current": [{"key": "T1-1", "kind": "check", "source_ref": "当前消费身份依据", "verified": true, "inherits": "T0-1"}],
  "fixes": [],
  "requirements": [{"id": "E1", "kind": "ROUND_PREIMAGE", "scope": "变更目标", "required": true,
    "state": "VERIFIED", "actual_ref": "根报告原内容引用", "source_authority": "本轮写前核实"}]
}
```

当前身份`inherits=null`表示经核新增；指向原key表示继承，多个后继不能同时继承同一原身份。fixes每个独立根因一行：`root_id / baseline_root / fixed / verified / freshness / evidence_ref`；已修已验须有证据引用。unknown用null而非空数组。每次检查单一明确基线；原累计与阶段指标分别检查，不合并。

CLI从stdin接收上述JSON：rc=0表示声明结构有效且没有声明的必需缺口；rc=2表示结构有效但有未闭合必需材料；rc=1表示结构不合法。任何rc均不认证真实来源。脚本只输出非秘密统计和缺口ID，不回显完整证据内容，输入必须先剔除秘密。

辅助工具不决定formal QC是否接受某证据，也不认证 admission_status；不能用checklist_ready=true、合法JSON、rc=0或能算百分比代替实际旧材料准入、reviewer、正式run和权威原task_path。future_run_plan 与准入/QC字段按统一合同在根报告另记，不以扩展声明冒充 schema_version=1 已支持它们，未来结果不列修前必需 VERIFIED。
