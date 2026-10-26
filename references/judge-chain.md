# Judge 逐评分项链路匹配与真实验收

实际存在且本次相关的 judge 验收读取本参考；开放答案不必然需要 LLM，判定器先按可验证性质/行为与正式合同选择。模型第二审与正式评分 judge 不互相代替。咨询/只读不启动调用；LOCAL只重核受影响项和依赖，FULL_ACCEPTANCE覆盖全部实际语义判据及其判定链（不限quality标签或LLM路由），未变且足够的有效链可复用。全题技术核查不依赖外部两遍QC已采用，清单见 [pre-delivery-qa-fusion.md](pre-delivery-qa-fusion.md)；外部实测交付/两遍QC等仍分别核正式采用，不因此扩授权。新外部模型上传需要授权，不能用配置或 secret reference 存在代替。连接成功或总分正常不能证明匹配。

## 0. 受控 QC、精确写权与运行生产准入

按 [质检默认许可与准入合同](qc-exceptions-and-admission.md) 先记录独立正式义务 `obligation_freeze_ref`，再冻结评分设计、答案空间、判据、部分分、路由与聚合为 `scoring_design_freeze_ref`；两份均绑定范围、正式版本、来源、时间，同版有效独立记录可重核复用。WorkC 目标明确、独立双冻结可核后，未参与修复的独立 QC reviewer 默认可静态读取当前题相关根 ground_truth.json/核相关 oracle 源码，不需逐题读取授权，记录 `qc_role / qc_read_scope / qc_permission_basis=WORKC_DEFAULT / applicable_clause / obligation_freeze_ref / scoring_design_freeze_ref / actual_reads`，scope 逐精确对象用于审计。无外部条款时当前明确 QC 目标可作必要性依据，不空造条款；未冻结先完成独立推导/冻结，不请求授权代替。QC 的非写入角色不等于永不执行；实际操作仍受 §1.1 和本次权限约束，READ_ONLY 仍不写不跑，CONSULT 不启动题包核查，REPORT_QC 默认静态、不自动取得运行权；默认许可不绕过明确用户限制或工具拒绝。

GT/oracle 只作离线对账，不定义正式义务，不进入运行时评分、候选输入或正式 judge evidence；协调者/修复方不读取 GT，不接收答案原文、摘录、数值或可反推摘要，仅接收正式来源支持的缺陷位置、可推导性、结论和脱敏证据引用。答案一致不证明设计正确，不据 GT 改期望。当本次作业允许执行且相关本地 oracle 验证确有必要时按 WORKC_DEFAULT 默认许可，不需另批；独立非写入 QC 可依 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，在双冻结及答案输出隔离后直接执行；协调者也可在其自身权限及隔离约束内编排已获准运行，但不读隐藏答案，仅收脱敏状态/结果引用。先核必要性、已有效入口、版本、入口/import/collect/子进程副作用、实际文件系统只读边界、最小挂载及题包外已获准 scratch，不因 QC 角色能力新增执行授权；CONSULT/READ_ONLY、明示禁运行、需要未授权外部调用/秘密或无安全入口时不执行。默认 oracle 许可不扩新普通候选 rollout/外发、不改 tests 外冻结入口；tests 内入口可按授权正式依据修复并复验，不凭 oracle 结果改义务，不让协调者/修复方、普通候选或 judge 接触隐藏答案，静态核查不冒充动态验证。`.pipeline/`对所有角色绝对禁读、禁引用/依赖，不搜索/hash/挂载或借副本/他人结果绕过；秘密不读不转写，QC 默认许可不授权答案外发或新模型上传。

题包写集合为当前 task 的全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、legacy judge.py、runner、helper、shim、instruction、config 均可按正式依据修复，不按文件类别冻结。tests 外除同根 QA 均只读/移交，包括外侧 runner、业务实现、persona、environment、solution、Dockerfile、依赖、根 manifest、shim/helper、instruction；移交不算已修复或 PASS，不据 tests 写权编写业务实现。QC 独立核验且整个 task 绝无写权，CONSULT/READ_ONLY/RUN_ONLY 不变成写作业，用户显式局部、只读或路径限制优先。目录/glob/别名/链接不扩权，写前核真实规范化目标；指向 tests 外的链接/别名目标不可写，无根报告写权不改 tests，不建 sidecar/整题副本。独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，实际作业允许执行时才经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle。整个任务含tests/QA/cache/日志/字节码/结果及别名、链接、挂载落点须实际文件系统只读边界，-B/cache开关不替代防写；仅题包外独立已获准scratch，不作源码副本/补丁/staging。先核入口/import/collect/子进程副作用及隔离，无安全入口不动态运行并移交协调者，后者仍守自身权限/隔离；不新增安装/配置修改/重启/候选/网络/外部judge权。CONSULT/READ_ONLY及默认静态REPORT_QC不运行；Skill 维护不启动题包作业。目标不明先核事实，工具拒绝、明确用户限制、无安全入口或未授权外部动作仍阻止相应操作。

修改前按合同记录 `admission_status / admission_scope / historical_requirements / preimage_refs / future_run_plan / admission_evidence_refs / admission_owner / admission_reason`。历史必需性依 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 按明确历史验收请求、适用正式采用条款或当前主张依赖确定；按具体主张所需核旧ORIGINAL_TASK、失败身份映射/反馈及HISTORICAL_TRAJECTORY，须实际VERIFIED或有具体对象/版本/条款的正式替代接受记录，不一律捆绑。权威原task_path用于旧修改对照，旧轨迹用于旧行为；当前快照、preimage、handoff指标与新run不能替代相应旧证据。每个授权tests写目标先合法保全完整ROUND_PREIMAGE/起始状态/最小完整修改上下文于唯一根报告，原不存在记ABSENT，hash不足。修前 future_run_plan 核必需入口/模式、本次运行范围（必要合法本地 oracle 记 WORKC_DEFAULT，不扩新普通候选/外发）、合法 evidence/来源、隔离挂载、版本依赖服务预检、逐项聚合取证位置及失败责任；先处理获准且可修的 tests 内验证入口缺陷，保全并安全修验该入口不被其当前失效否决；排除此路径后仍已知不可合法生产必需验证，才不启动依赖该缺口的返修，修前不要求已有修后结果。计划/预检/ADMITTED不填CURRENT_RUN=VERIFIED、不认证PASS；修后实际正式run核身份、消费、逐项聚合、degraded与FRESH。材料先有限合法恢复，权限不足列阻止，确穷尽记EXHAUSTED/历史验收NOT_ADMITTED，仅新来源、权限或版本变化时重试已穷尽来源；独立不依赖该历史的当前范围（包括FULL_ACCEPTANCE）可另列准入，确属本次必需历史QC门仍保留，缺证不能称包含该门的原请求全通过或自行换验收口径。

tests 内正式 instruction 可按获授权正式来源合法修订，不另设路径批准门；写前在同根 QA 保全完整 ROUND_PREIMAGE、起始状态、正式来源/映射及版本，记录实际 diff、版本前后与合同影响。tests 外 instruction 只读/移交，外部修订另记可核有权来源。两类正式合同变更都将受影响旧义务/评分设计及依赖运行证据标 STALE；未接触隐藏答案的设计角色从获授权新正式来源重新独立推导义务，再冻结评分设计，双冻结受影响范围，重核 tests、注册聚合、候选可见载体及适用真实验证。不得从隐藏答案、候选输出或低分反推合同救分；已接触答案的 reviewer 不承担独立设计，仅按新冻结复检；不追认旧候选违规。以下历史合成实测记录不改写为本轮真实题验证。

**本页修复/移交接口**：范围以 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围) 为准，闭环及 QA 复用 [执行 SOP](execution-sop.md) 和 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 范围含 judge/parser/runner/helper/shim/config/instruction；获准范围内确认缺陷须由 worker 实际修复、验证正式接入与适用链路并写同根 QA，不能只记风险、给建议/移交或因文件类型标 OUT_OF_SCOPE。验证入口的内部可修缺陷先保全修验，再补依赖验证，不自动按外部环境阻塞收口。QC 只核验、不写任务；没有安全入口时不试跑，明确局部/只读/RUN_ONLY、真实目标、preimage、答案隔离和运行授权不变。

相关允许的 tests 外发现直接写同根 QA，列精确规范化路径/版本、证据、影响及责任/移交方，不改外侧。外侧 SDK/配置缺陷不自动阻塞所有 judge/tests 结论；核是否有保持正式语义的合法 tests 修法，仅实际当前必需依赖缺口限制对应结论，其余记录后继续，不等待外侧整改；不新增安装、系统配置、网络、模型调用或业务实现权限。

## 1. 一项一链，保留批量请求的多对一关系

根报告“judge 逐项链路匹配”中，逐identity记录 `input_refs / expected / actual / run_id / version / coverage_status / unverified_reason` 及以下节点证据。expected来自正式义务及独立双冻结尺度，actual来自实际判定链，分别保留引用；version绑定正式合同、输入/evidence、判定实现/config与运行版本。覆盖记对象、适用分支及合法/违规/等价变化，未证明项明确UNVERIFIED，实际阻止记BLOCKED，不因缺结果从库存消失；只读审现有材料、缺动态证据记未验，不为补字段启动调用。批量评分允许多个 criterion 共享一次请求，但要记录请求内成员及各响应字段，不能要求无意义的一项一 HTTP 请求。单项模式的无 ID 平坦响应，只能绑定到该次请求唯一的 criterion；禁止按全局列表位置猜归属。

| 节点 | 核验内容 |
|---|---|
| 正式义务 | 正式来源、独立语义义务、适用条件、答案空间、满分/不通过条件；必需义务须进入正式评分/通过关系，缺失记设计问题，不自创硬门、cutoff或替换聚合。 |
| 身份与投影 | 源 rubric/criterion ID、manifest/legacy 映射、运行时 ID/name、dimension/weight、actual loaded path/digest；ID 与 name 可以不同，但映射必须明确且无歧义。不允许漏载、幽灵、重复注册或重复计权。 |
| prompt 渲染 | 正式模板路径/digest、实际 criterion 描述和评分尺度、变量绑定来源、渲染后消息摘要；查空变量/残留占位符、错条目、旧模板/系统提示覆盖。文件正确不代表实际消息正确。 |
| evidence | 逐义务的source/producer/owner/backing state、候选可写性与mutation path，冻结时间、精确路径/digest、目标对象/actor/时间段、允许字段、实际文件读取/工具观察与最后发送块摘要；authority及肯定完成/权威空集的区分按 [seal-rewardkit.md](seal-rewardkit.md) §5，GET名称/候选自述不自证。检查编码、文档/图片转换、token/字符/图片限制、截断或大文件跳过。关键信息没有送入模型时不得认证该项。 |
| 运行路由 | scorer/judge 类型（LLM/React/其他）、runner/SDK/plugin/LiteLLM 版本、配置来源/优先级、请求的 provider/model 和端点非秘密标识、实际响应模型（若服务提供）、能力参数和工具 schema。别名或响应模型不同须有正式允许映射，不凭字符串相等/不等直接裁决。 |
| 请求与响应 | task/attempt/run_id、调用/批次 ID、请求成员/消息/schema 摘要、响应/提交工具调用 ID、各字段归属、重试序号；本地生成关联 ID 可以使用，但不能冒充 provider 回执。不得把 A 项分数归 B 项。 |
| 解析与尺度 | JSON/工具提交 schema、成员集合 exact-once、字段类型、必填 reason、原始 raw 合法域/有限值、normalized value、negate/optional、真实转换及舍入；bool 不冒充整数，NaN/Infinity、缺项、重项、额外项、错类型、越界原分须明确拒绝或按正式合同处理。 |
| 聚合与门控 | criterion→group→dimension→reward 的实际分母、权重、skip/error/degraded/fallback 和最终通过判据；复算 raw→value→分项/总分，验证 mandatory semantics 不仅是装饰分。 |
| freshness | prompt/evidence/模型/非秘密调用参数、parser/尺度、权重/门控、runner/plugin/shim 摘要、cache/retry来源及结果摘要；输入改变使依赖结果 STALE。可引用前轮未变证据，不跨版本拼接。 |

证据摘要不是缺失内容的替代品；关键节点无法证明记 UNVERIFIED，确有权限/环境阻止则 BLOCKED，仅限制受影响的验收对象。按真实协议提供字段和摘要，不为内部 SDK 无法观察的非必需实现细节无限加门；正式必需关键关联仍须证实。报告不保存密钥、完整鉴权头、私人端点参数或非必要业务文本；敏感消息只留获准隔离日志，原话先脱敏。禁止将整题或禁读答案发给模型。

## 2. 配置、模型与真实调用预检

- 使用本批正式 runner 批准的同一配置来源/secret reference，不另造一套模型或端点救绿灯。WorkC 的既有 secret reference 为 `~/.agents/skills/workc/.secrets/judge.env`，只有不会启动候选的受信任 judge 运行时能解析其值；Agent 和通用编排只能检查存在性、传路径、读取脱敏状态。正式批次采用其他来源时需明确可信映射及隔离批准，不能自行读取内联秘密。
- 核有效配置的来源优先级：quality、runner override、子进程 export、env-file、SDK 默认值；不允许模型缺失后静默用默认模型。测试仅记录配置键名/来源、非秘密摘要和模型身份；endpoint 报类别或脱敏标识。
- **先查既有引用，再判断缺配置**：本机上述引用对应 `C:/Users/DELL/.agents/skills/workc/.secrets/judge.env`。实际有 judge、相关运行已获准时，先核本批正式来源/映射，再对既有精确路径做存在性检查（PowerShell 可用 `Test-Path -LiteralPath <路径> -PathType Leaf`）；已有可信脱敏状态可复用。不用 `Get-Content`、`type`、env dump 或通用编排脚本读取/export 其值。正式来源另有批准位置时遵从正式优先级，本地文件不是通用覆盖。
- 文件存在但未生效时，核实际入口是否接收该 secret reference、可信运行时的加载状态与脱敏缺键/鉴权错误，沿既有获准集成恢复；不要求用户重发密钥、不另造端点/模型、不改评分救绿灯。仍缺配置或权限时记录已核来源/存在性/脱敏错误、受影响门及恢复责任，继续其他可执行工作。配置存在只证明引用可定位，不证明配置有效、服务可用或外发获准；无 judge 不访问。真实配置只留本机，GitHub 仅可同步不含真实值的显式示例，不能上传 `.secrets/judge.env`。
- profile 使用 RewardKit→LiteLLM 或 shim 时，核实际 model prefix、provider 解析、模型 metadata/context window、工具/structured-output 支持及参数过滤。QC 中的旧模型白名单是对应 driver 的行为，不是全局允许模型表。不同 React/LLM backend 实际发出的参数不同，不能机械要求都删 `response_format`。需要改 tests 外冻结 driver/shim 时直接写同根 QA 的路径/版本、证据、影响及责任并移交，仅实际当前必需依赖受阻的结论 BLOCKED；tests 内 driver/shim/runner/config 的确认缺陷由 worker 按正式依据实际修复、沿真实正式链复验并更新 QA，不按类别冻结。独立测试 adapter 只能证明自身集成，不能冒充原题正式 runner。
- 预检不仅测连通性：用无题包内容、无秘密的微型正/反样例，走实际获准 backend 的渲染、调用、响应解析及结果关联。成功需合法响应、正确身份及尺度；失败保留脱敏错误类别。这样的 smoke 证明环境能力，不证明真实 criterion 语义正确。
- FULL_ACCEPTANCE对全部实际语义判据按独立冻结的正式尺度做双向对拍：合法履约应获对应分数/通过，违反义务应按相应程度失分/不通过；同时核措辞、结构、顺序或实现的合法等价变化不被误拒（仅在合同允许等价时）。LOCAL覆盖受影响项及依赖；不要求开放语义全二元化、所有负例归零或固定样本数。expected须独立于judge输出，核原分、转换及实际通过关系，按正式输入可独立推导的尺度核判定，不让judge自评正确。对拍不能只测关键词命中：适用时用关键词堆砌但未履约、术语/语气齐全却事实或关系错误等浅代理反例，并配无固定关键词但合法履约的等价例；不把正式义务缩成参考原文匹配。
- 对拍经实际获准判定链取证，合成smoke不补真实题消费；只读不跑，未获执行/外发授权则记对应动态项UNVERIFIED或BLOCKED。自然波动全部记录，不挑最好一次；服务失败/超时是infrastructure，不充作语义负例。逐identity保留输入refs、expected/actual、run/version和覆盖未证记录，不用平均总分掩盖某项反向或漏判。

## 3. React 工具链与 evidence 消费

React 类 judge 要检查：注册的 backend、tool registry/plugin 版本、cwd/工具访问范围、工具 schema/调用名/arguments/result 与最终 `submit_score` schema；仅挂载需要的合法 evidence，不暴露整题或候选可篡改 scoring 文件。工具输出成功（包括空集合）不得被其他候选文本替代；调用失败、文件跳过/截断、工具次数/超时耗尽不能被当成正常评分。

有工具时记录读取了哪个 evidence 对象、消费了哪些字段、结果摘要及截断标记；没有工具的 LLM 模式则记录实际消息内容块。秘密只由受信任配置层持有，候选/不可信工具子进程不能继承秘密；涉及 shell、MCP、网络和读取任意路径的 judge 工具必须由正式运行合同限制。若没有合法隔离，不启动。测试 smoke 可以显式限制工具，仅说明该受限 profile 的调用链已验证，不冒充完整探索能力。

## 4. 请求响应、异常与缓存负控

使用当前真实 parser/loader 做确定性边界探针，按实际支持的协议选择：缺项/多项、交换两项身份、重名/重复 JSON 键、坏 JSON、缺 reason、评分类型错误、NaN/Infinity、raw 边界外值、平坦响应错绑及 optional/negate。必要时在获准 tests 中补正式入口会执行的校验；外部 Skill 辅助校验只能定位和回归，未接入正式评分链不能宣称已修生产缺陷。

先验证原始响应，再归一化。只看 0–1 value 会漏掉上游将 9 分裁成 1 的问题。框架 schema 即使写 strict，仍要核真实 parser 的行为和原响应；不能相信服务一定遵守 schema。发现默认填分、静默丢额外字段、重复键覆盖、越界 clipping 时明确记判分风险，按正式允许位置修复并重新运行；tests 外冻结 SDK 或基础设施发现直接写同根 QA 的路径/版本、证据、影响及责任；无合法 tests 修法且实际阻止当前必需判据时，才限制对应结论为 BLOCKED，不等待其他外侧整改。tests 内 helper/shim/runner/config 等确认缺陷须 worker 按正式依据实际修复、重新验证真实生产接入并更新 QA，不把它们冻结或以独立 adapter 冒充已修，不在报告中将缺陷合理化。

本机 `harbor-rewardkit==0.2.0` 的独立合成实测（2026-10-13）已复现：默认 parser 接受额外成员、重复 JSON 键、越界/布尔/字符串/小数/非有限 Likert 原分及缺 reason；`all_pass` / `required_pass` 使用 `value > 0`，不能直接等同于本批 `value == 1` 的逐项通过标准。这些是已发现而非已修复的框架行为。当前项目是否受影响须沿实际入口复验；按义务验证部分分的 mandatory 项不能从最终 gate 偷过，不擅自改冻结 SDK 或替换正式 aggregation。辅助脚本 `scripts/check_judge_response.py` 仅验证显式声明的响应合同，不证明正式 parser 已接入保护。

上述 2026-10-13 SDK 行为与“未修改”是历史实测事实，不改写为本轮已修。现行修复边界按第0节落点判定：tests 外 SDK/driver/aggregation 冻结、只能移交；tests 内正式 parser、runner、helper、shim/config 可按正式依据保全并修复，须证明实际生产接入、身份/原分/转换/聚合及适用复验，不能因历史冻结措辞封锁 tests 内等价文件，也不能擅改正式通过语义。

实际 runner 有 retry/fallback/cache 才检查这些分支，不制造无关配额：

- retry 记录可重试错误、次数/backoff、deadline、每次成员和最终选取响应；SDK/框架两层重试不能产生重复有效结果，不能把最大分当最终结果。部分批次失败不要用另一批响应补错项。
- fallback/degraded 记录实际模型/权重/分母变化；必需语义未有效评分不能正常通过。采用 rubric_delivery_requirements 时 reward_degraded 非空使该轮全部 judge 类 criterion 结果不可用并须补跑，不能只丢异常项；独立有效确定性证据可保留。其他合同按明示范围。还查逐项 error、warnings、timeout、空raw、调用失败/工具耗尽；框架把超时变0仍是基础设施失败，不是候选失败。
- cache key 应包含实际影响判定的 criterion/渲染消息/evidence/model及参数/尺度/parser；检查磁盘/进程缓存和断点续跑。单变量变更须 cache miss 或正确失效；无缓存记实际依据，不能仅靠新 run_id 推断无缓存。保留所有真实 attempt，不凭最高分交付。包裹 `litellm.acompletion` 只能证明 SDK 调用和返回，不足以证明绕过 SDK/外部/provider 缓存；未取证的缓存层明确记 UNVERIFIED。
- 当前 0.2.0 loader 会缓存 Python 模块；同一进程重复 `discover/run` 可能不重新注册程序项。本机合成测试已复现重复发现后 `facts` 丢失并报 unknown weights。正式重跑使用新进程，不能用同进程重复发现当成两次 attempt。逐项列表先校验数量、ID 唯一性和成员 exact-once，再转换成字典；否则重复 ID 会被覆盖。
- 输出结构沿实际版本读取。`reward-details.json` 可直接是 dimension 的 detail，也可含 `components[].detail`；先核实际 shape，再绑定 criterion，不能把解析脚本报错当候选不通过，也不能静默跳过整维度。

辅助响应校验的合同与运行示例（只用于采用该 `score/reasoning` 协议的入口；不要套到其他 backend schema）：

```json
[{"id":"quality.example","name":"example","kind":"likert","min":1,"max":5}]
```

```bash
python -B <workc>/scripts/test_judge_response.py
python -B <workc>/scripts/check_judge_response.py --contract contract.json --response response.json
```

批量响应须以声明的 `name` 为键；单项 flat 响应显式加 `--flat`。numeric 支持显式 min/max，binary 只接受该合同声明的 `yes/no` 字符串，negate 为 bool。极端尺度导致非有限运算时拒绝，而不是输出 NaN。运行结果列表可用 `validate_runtime_scores` 检查 exact-once ID、归一化值与逐项基础设施错误，但它不代替 raw 响应校验或语义对拍。CLI 不打印响应原文；合同外协议按正式入口另核。以上命令只是已有Skill检查用法，不产生本次运行权；独立非写入QC执行时仍按§1.1先核副作用及实际只读边界，-B不替代sandbox，输入仅允许非秘密对象，文件输出仅题包外独立已获准scratch，不建源码副本/补丁/staging；CONSULT/READ_ONLY及默认静态REPORT_QC不因示例启动运行。

## 5. 通过条件及验证范围

本次相关 judge 链的关键节点均匹配且证据有效新鲜，才标该项 VERIFIED；错绑、缺失必需证据、服务错误或未知聚合不能以其他项/低权重弥补。用事实正确而语义违规的负例核必需语义实际失分及正式判据；不能自创统一 gate。去全部 judge 的端到端消融仅在正式已采用规范/本次请求要求时执行；其他作业可以做相关判分职责探针但不冒称完整消融。实测交付规范正式采用时逐项绑定至少两次有效 attempt，定义及 degraded 范围见 runtime-acceptance.md。辅助响应校验能发现结构/身份键错，不能发现合法结构下语义分数被互换，也不证明正式 parser 已接入。

范围区分：配置存在→依赖可用→微型真实调用 smoke→实际 backend 集成→正式任务 verifier→整题实测交付/QC。前层成功不自动证明后层成功。报告接口依 [报告合同 §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 分本轮报告质量与历史失败 A/B 归因两层；REPORT_QC 明示窄范围优先，未指定时识别并核两层。本轮新写/更新 QA 均审实质链路主张、实际运行/消费、归因、限制、状态与 freshness；无 always-failing、零缺陷或只运行不使质量 N/A。关键缺陷/修法/有效性主张缺证质量 UNVERIFIED、确证错误 FAIL；准确报告 judge/技术或历史未证可质量 PASS，但不等于技术、候选或历史 PASS。

开工及收口沿请求、正式映射/manifest 与 rubric/test 失败标记、允许反馈/既有 artifact、已有 QA 历史发现对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED、对象/反馈ID、来源版本/已查结果及缺口影响；不扫工作区/禁区。只有确认无对象才历史 N/A，报告自 N/A、无 A/B 表或未找到清单不自证；已审未知或对象存在但旧材料缺失保留历史 UNVERIFIED，未审且未请求明确记本次未请求；相应依赖历史 NOT_ADMITTED，有限合法查源。按 §7.2 对象存在/未知或历史未证不增门，FULL_ACCEPTANCE/无人值守/模板本身也不增普遍历史门；不阻独立当前范围（包括全题）修验/报告审核，确属本次必需历史门仍保留。ROUND_PREIMAGE 非旧 ORIGINAL_TASK 的自动替代；本轮漏留是 WorkC 生产缺口，如实记、合法查源，不倒填。

复用 judge 链、技术表、issue/轮次证据，不复制第二套台账。本轮 issue 留正式依据/断言、反例/独立预期、观察/归因、写前完整上下文、实际 diff/终态、适用验证/run/版本/freshness及未证责任；静态发现不虚构历史行为，未执行标推演/NOT_RUN，未验证不标 FIXED+FRESH。协调者对所有本轮报告写入自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部按影响/风险复核，不新增全题独立门。先完成实质报告再审，反馈复检对应结论；任何报告变更核对应内容，judge/技术证据仅按实际依赖变化失效，不空重跑，最后仅追加准确回执不无限自指。最终分报本轮质量与历史归因范围/依据/状态；按 §7.2，无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题 PASS/UNATTENDED_COMPLETE，历史仍准确 UNVERIFIED/本次未请求，不冒称历史 PASS。确有必需历史门缺证仍阻包含该门的原请求全通过。透明纠正无依据旧结论，保留旧行、来源、纠正原因及未证范围，不删行逃避实际错误修法或分类。

维护 Skill 的题包外独立合成测试夹具/报告仍需本轮相应范围许可，不能冒称真实 task/attempt 或据维护启动题包作业；真实题包写集合为当前 task 全部 `tests/**` 内容与同一根 `qa_report.md`，由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守默认 `tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 instruction、runner、helper、shim、config 等按正式依据可修；tests 外除同根 QA 均只读/移交，移交不是已修复或 PASS，用户显式局部/只读/路径限制及真实规范化目标边界优先。目标明确后的相关静态 QC 及必要合法本地 oracle 不需逐题批准，不扩新普通候选/外发。真实题包有明确用户限制、工具拒绝、无安全入口、其他禁读/冻结冲突或必需材料缺口时，不能用合成样例补足外部验收；解除操作权限不改变材料证据或正式替代接受口径、不授权自造历史。最终分别报默认许可实际使用的角色/精确对象、准入/未准入对象、tests 内 instruction 实际修订/版本/双冻结及复验状态、tests 外 instruction 只读需求与移交状态（外部变更单列来源）、本地 oracle 是否实际执行、真实运行及对应验收状态。
