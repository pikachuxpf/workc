---
name: workc
description: 通用单题 ClawEval/WorkC/Seal 业务实现、评测标注、返修和 QA 流程。用户提到 workC、Seal、单个考试题、评测题、rubrics.py、test_outputs.py、criteria_manifest.yaml、RewardKit、分维度 checks.py、Oracle、nop、judge、QA 报告、判分检查或交付打包时必须使用。先识别用户是在完成业务任务还是质检判分器，并识别旧式或 Seal/RewardKit 评测架构，再解决规则来源、修改授权、冻结边界和交付模式冲突，执行相应实现、合规检查、安全分析与验证。
---

# WorkC / Seal 单题实现、评测与 QA SOP

## 核心不变量

测试必须反映当前任务规则，不能反过来用 Oracle 分数定义规则。Oracle 1.0 只说明参考方案通过当前测试，不证明测试正确；nop 也不要求机械为 0。禁止为了分数删除有效测试、放宽正确条件、篡改真值、伪造 evidence、修改 nop 或掩盖运行错误。

先识别角色和架构，再解决规则与授权：

```text
用户角色 → 评测架构 → 来源与授权 → 原始基线 → 材料完整性
→ 当前题覆盖矩阵 → 业务实现或判分器 QA → 静态检查
→ 必要的隔离运行 → 差异审计 → 对应交付模式与报告
```

## 0. 任务角色与评测架构门

收到目录后，先依据用户动词与文件结构完成两项分类，不要看到 `tests/` 就默认修改测试。

### 0.1 用户角色

- **业务实现模式**：用户要求完成、开发、修复页面/服务/脚本、生成业务产物或按 `instruction.md` 做题。此时 `tests/` 默认是只读验收依据；修改业务代码和 instruction 指定的产物，不创建或改写判分文件。
- **判分器 QA 模式**：用户要求质检、标注、审查 rubric/criterion、检查 Oracle/nop 区分度或维护评分规则。仅“审查、质检、分析、检查、报告问题”时默认 `audit-only`；只有用户明确要求“修改、修复、返修、增强、更新”等写入动作，才进入 `fix-and-validate`，再把当前架构的判分文件列入候选修改范围。
- **只读分析模式**：用户只问“需要做什么、哪些文件对应、能否交付”，或明确要求不修改。只读取并回答，不修改、运行候选代码、打包或创建报告。

目录里已有 tests 只说明题目带验收器，不说明用户要维护验收器。业务任务的正确做法通常是用 tests 理解验收条件，而不是为了通过而改 tests。

### 0.2 架构探测

| 结构信号 | 架构 | Rubric/criterion 定义 | 检查实现与聚合 |
|---|---|---|---|
| `tests/rubrics.py` + `tests/test_outputs.py` | 旧式 ClawEval | `rubrics.py` | `test_outputs.py`，并结合 `judge.py`、`test.sh` 和类名/tier 映射 |
| `tests/criteria_manifest.yaml` + `tests/*/checks.py` | Seal/RewardKit | `criteria_manifest.yaml` 的 `angle_id`、dimension、weight、evidence、scorer | `process/output/safety` 等维度的 `checks.py`；`reward.toml` 聚合，`test.sh` 运行 |
| 两套同时存在或信号不完整 | 混合/未知 | 读取 runner 与 task 配置确定实际加载链 | 不创建缺失的旧式文件，不凭文件名猜主架构；无法确定则 `BLOCKED` |

新版不是把两个旧文件机械改名：`criteria_manifest.yaml`、分维度 `checks.py`、`reward.toml`、`test.sh` 和 task 配置共同构成评分契约。Manifest 是否被框架运行时读取取决于版本；已核实的 RewardKit 0.1.7 由 `checks.py` 注册实际 criterion，需主动核对 manifest 与注册链。`materialization_manifest.yaml`、`task.toml`、`meta.json`、pipeline 状态和 `ground_truth.json` 通常是任务生成、载体映射或交叉检查材料，不自动是业务实现的可修改文件。

发现 Seal/RewardKit 结构时，先读 `references/seal-rewardkit.md`。除非当前 runner 明确要求，禁止补建 `rubrics.py` 或 `test_outputs.py`；发现旧式结构时也不得擅自迁移成新版。

## 1. 四层规则模型

不要把“谁决定评测真值”“谁允许改文件”“什么必须冻结”“谁允许发布”混成同一个优先级。

| 层 | 决定什么 | 处理原则 |
|---|---|---|
| 评测语义 | 什么行为、结果和证据算正确 | 以当前正式质检规范和当前题包为准；`instruction.md` 的任务政策、公式、schema 和冲突条款优先于 persona 中的错误说法、旧测试和参考答案 |
| 修改授权 | 本次可改哪些路径 | 取当前任务要求与用户请求的较窄交集；默认只改明确列出的文件 |
| 冻结边界 | 哪些原始内容必须保持一致 | 原始归档只读；工作副本仅允许 allowlist 差异；较新的题目级限制可以收窄通用范围 |
| 外部操作 | 是否上传、提交、push 或发送 | 必须有当前用户对该动作的明确授权；本地修改授权不自动包含外部发布授权 |

冲突按以下方法解决：

1. 同一层内，当前且明确适用于本题的正式规则，高于旧版本、通用建议和示例。
2. 题包 `instruction.md` 决定业务真值；persona 是被测场景输入，不能覆盖 instruction 的正式政策。
3. 最新轮次或题目专用文件可收窄修改范围、交付文件和验证要求，但除非明确声明替代，不自动废除正式质检规范。
4. 同前缀历史题提供检查角度，不提供当前题常量或权威真值。
5. `ground_truth.json`、官方 solution、旧 QA、现有 tests 和同行版本都是交叉检查材料，不得覆盖独立推导结果。
6. 两条硬要求仍无法同时满足时，停止冲突部分，标记 `BLOCKED`，列出来源和影响；不得静默任选一条。

扩大冻结范围之外的修改，必须由有权决定当前任务范围的人明确点名文件并说明覆盖原限制。模糊的“都修好”不能被解释为解除冻结。

## 2. 开始前固定任务状态

从用户请求和当前材料中记录以下状态；有常规默认值时直接采用，不为形式问题阻塞：

- 用户角色：业务实现、判分器 QA 或只读分析；
- 评测架构：旧式 ClawEval、Seal/RewardKit、混合或未知；
- 工作模式：`audit-only` 或 `fix-and-validate`；
- 交付模式：`audit-only`、`changed-files`、`full-package`、`platform-submit`；
- 报告产物：无、内部工作记录、用户要求的报告文件；
- 原始基线、工作副本和题目标识；
- 允许修改、新增、删除的路径集合；
- 冻结文件和禁止运行时依赖；
- 计划执行的静态、定向、Oracle、nop 或平台检查；
- secrets 注入方式和禁止披露边界。

默认行为是准备和验证，不上传、不提交、不 push。用户明确要求整包、平台提交或 push 时，才进入对应模式。

## 3. 原始基线与工作副本

若提供 ZIP 或冻结目录：

1. 原始归档保持只读，不在其中直接修题；
2. 按完整题目标识定位任务，排除 `__MACOSX` 和 AppleDouble `._*` 干扰；
3. 在独立工作副本修改，仅 allowlist 文件可与原始内容不同；
4. 开始前记录冻结清单或 SHA-256，交付前重新审计；
5. 不用整目录覆盖来隐藏差异，不把旧计划的宽范围套到新规则上。

“冻结基线”指原始归档不可变，不表示工作副本内获准修改的测试文件也不可变。

默认允许范围不是跨题硬规则。候选 allowlist 只能在已获得写入授权后缩小范围，不能自行产生修改授权；用户仅点名文件、要求 QA 或要求报告问题都不等于授权写入：

- 业务实现模式只修改 instruction、项目规范或载体权限明确列为可写的业务源码与产物；`tests/` 默认只读，`instruction.md` 本身不因此变为可写。
- 旧式判分器 QA 在 `fix-and-validate` 下，若当前材料未给更窄范围，可将 `tests/rubrics.py` 与 `tests/test_outputs.py` 作为最小候选 allowlist。
- Seal/RewardKit 判分器 QA 在 `fix-and-validate` 下先从 runner 实际加载链确定范围，候选可能包括 `tests/criteria_manifest.yaml`、被加载的维度 `checks.py` 与 `tests/reward.toml`，但不得据此自动修改全部文件。
- 只有当前项目明确要求时才新增或更新 `qa_report.md`。

`tests/test.sh`、`tests/judge.py`、旧式类名、Seal criterion 注册与权重、run scripts、`instruction.md`、persona、fixtures、`environment/`、`solution/`、`ground_truth.json`、materialization/task 配置是否冻结，必须从本题材料确认；不得因通用 Skill 擅自放宽。

普通依赖、路径、挂载和命令问题应在交付目录外解决。冻结 harness 有缺陷时，记录影响并使用外部验证包装器，不直接修补冻结文件。

## 4. 材料完整性与独立推导

先核对并通读：

- 当前目录的 `instruction.md`；
- `persona.md`（若题型需要）；
- fixtures/resources 和 `/app/data` 映射；
- 输出 schema、`environment/output` 与 `/app/output` 映射；
- 现有评测契约：旧式 rubrics/tests/judge，或 Seal 的 criteria manifest、分维度 checks、reward 配置与 runner；
- materialization/task/meta/pipeline 文件（若存在），用于理解载体映射、任务分类和实际运行链，不默认作为业务真值或修改对象；
- 最新正式规范、题目专用说明、冻结包和同前缀历史材料。

缺少 `instruction.md` 时没有可执行业务依据：默认在本地将平台题分类为“应废弃”并标记 `BLOCKED`；只有用户明确授权平台状态变更时，才实际执行废弃操作。persona 或 fixture 缺失不自动废弃，先判断题型是否要求它们；不得借用别题材料填空。

从 instruction 和 fixtures 独立复算所有数字、集合、时间、状态与边界。不要先相信注释、旧 `_EXPECTED_*`、历史常量或 solution 输出。若当前规则要求“先独立推导，后看 GT/solution”，严格按此顺序；任何 tests 都不得在运行时读取 `ground_truth.json` 或外部参考答案。

API 被列为可用不等于必须调用。只有 instruction、正式策略或可证明的完成条件才能产生强制接口要求。

## 5. 按角色执行

### 5.1 业务实现

1. 从 instruction、项目内规范和载体权限解析业务源码、报告、归档包、API 收口等交付物；tests 只用于理解验收条件，instruction 通常也是只读规则源。
2. 按 materialization/task 配置核对规则载体与路径解析，但不把生成元数据当成业务真值；用户查询与项目规范存在 input/output recast 时，以正式映射链解释最终交付位置。
3. 只修改允许的业务文件并生成明确要求的产物。工具调用遵守 endpoint、参数、次数、只读、禁止安装/构建/发布/reset 等题目级限制。
4. 使用静态解析、内容核对、归档检查和允许的本地命令验证；不为了过测改 tests，不把可选验证升级为被禁止的构建或联网动作。
5. 外部写操作仅在任务要求且授权范围内执行；上传、发布、提交和 Git push 仍遵守独立授权层。

### 5.2 判分器 QA 与历史题迁移

先按用户写入意图选择 `audit-only` 或 `fix-and-validate`；前者只报告发现，后者也只能修改已授权 allowlist。

按当前规则指定的历史包或路径查找同前缀题。对每个历史角度记录：已迁移、已拆分、已纠正，或不适用及当前材料依据。

不得直接复制历史常量或 criterion。删除“测试数量不得减少”或“必须新增若干条”之类机械配额；要求的是全部适用角度有可追溯处置。只有当前材料产生新事实时才增加新角度，不能为凑数制造无关测试。

若当前正式流程要求历史检查而材料不可获得，继续完成其余检查，但整体最多标记 `PARTIAL`，不得声称已完成全量 WorkC 合规或历史迁移。

## 6. 当前题覆盖矩阵

判分器 QA 在编辑前建立矩阵；业务实现也可用简化矩阵核对需求，但不得因此修改 tests。每行只放一个可独立验收的事实：

| 来源 | 应提取内容 |
|---|---|
| instruction | 目标、政策、公式、必须/禁止动作、完成条件 |
| persona | 分批披露、模糊值、故意错误、冲突说法、语气与澄清条件 |
| fixture/resources | 实体、ID、字段、数值、状态、时间线、边界陷阱 |
| 工具/API | endpoint、参数、次数、只读/写入范围、可信响应 |
| 输出 | 文件、解析、类型、字段、值、集合、排序、一致性 |
| 历史题 | 每个适用角度及处置结果 |
| 安全 | 适用风险、禁止动作、正向义务、证据和验证方式 |

共同字段为：来源、被验收事实、预期、验证机制、evidence、条件触发方式。旧式 QA 再记录 rubric 常量与 test 名称；Seal QA 再记录 `angle_id`、dimension、scorer 和注册它的 check。一个事实只能由一个计分 criterion 承担，辅助前置校验不得重复计权。

多轮对话题才应用澄清规则：缺少关键信息时先问；不重复询问已知信息；模糊值继续澄清；故意错误逐条纠正；问题自然友好且单次不超过 5 个；信息不足时第一条助手回复不直接给最终计算、结论或推荐。纯工具题不得机械添加对话项。

## 7. 安全分析

旧式 WorkC/ClawEval 若正式规范使用 A–H 分类，则逐类标记“适用/不适用”和材料依据：Prompt Injection、Credential Exposure、Ambiguous Action Confirmation、Data Integrity Verification、Draft-Only Enforcement、Read-Only/Tool Restraint、Domain Safety、Urgency Pressure Resistance。

Seal/RewardKit 不机械套 A–H 名称；以 instruction、manifest 的 safety criterion、可写/只读载体、工具合同和 runner 实际 evidence 为准。无论架构，都要覆盖明文秘密、错误指令、未经授权的外发或不可逆操作、数据核验、草稿/不发布边界、禁止工具调用、专业风险和紧迫压力中实际适用的事实。

需要“做安全动作且不做危险动作”时拆开评分，例如创建 draft 与未 send 分别验证。旧式每个适用安全事实使用独立 rubric/test；Seal 使用独立 `angle_id`/check，除非 manifest 明确把它们定义为同一原子 criterion。只有正式 runner 明确计算 safety gate 时才能报告平台 `gate`；否则称为“本地安全检查”或 safety dimension，不得自创一票否决结果。

## 8. Criterion 设计不变量

两套架构都遵守：criterion 只检查一个事实、只描述符合侧、写清可判定条件、使用唯一稳定标识，并与一个且仅一个计分检查对应。禁止用自动通过逻辑、关键词堆砌或复合条件掩盖多个独立事实；精确实体、集合和值由确定性代码判断。

旧式 `RUBRIC_*` 还应：

- 最多 400 个字符、最多 3 句话；
- 助手行为优先用 `Did the assistant ...?`，结构化结果可用 `Does ...?` / `Is ...?`；
- 使用唯一、清晰的常量名；
- 与一个且仅一个评分 `test_*` 对应；
- 不使用 `PASS if ... / FAIL if ...`。

Seal/RewardKit 还应：

- `angle_id` 在 manifest、check 注册和结果中一致且唯一；
- dimension、weight、evidence、scorer 与实际实现相符；区分 evidence 声明、冻结动作、实际路径和 check 消费行为；
- manifest criterion 均被 runner 注册，已注册的计分 check 也都有 manifest 项；
- 不把 diagnostic/preflight/helper 误算成 criterion；
- 只有当前任务规则允许时才改 criterion 集合、维度或权重。

数值必须记录来源、公式、理论值、舍入和容差依据。可由 instruction 与 fixture 唯一确定的离散值、公式结果、ID、枚举、布尔值和固定时间使用精确匹配。只有规则、数据精度或明确误差模型支持时才设置容差；不得跨题套用 ±15%、±5% 等默认比例。

旧式类名仅在 runner 以类名计权或材料明确冻结时保持；不得新增 runner 不认识的 tier。Seal 同理不得凭经验新增 dimension、改变注册顺序或假定 manifest 中的 weight 就是最终聚合权重，必须核对 `reward.toml` 与 runner 实际算法。

## 9. Check 设计与 evidence

确定性检查负责可计算事实：文件与 JSON/CSV/ZIP、语法、类型、字段、数字、集合、ID、枚举、排序、时间先后、状态转换、endpoint、参数、次数、只读哈希和禁止调用。LLM judge 只负责真正需要语义判断的澄清、解释、根因、关系、建议、冲突识别、风险和表达质量；manifest 没有 judge scorer 时不引入 judge，也不需要 judge secrets。

一个计分 test/check 只使用一种业务判定机制。加载 evidence 的前置断言不算第二个业务评分，但不得用确定性业务断言后再让 judge 重复评分。同一事实不在不同 test class、dimension 或 code/judge 版本中重复计权。

进一步遵守：

- 时间线由代码计算，语义相关性另交 judge；时间上可行不证明因果成立。
- 结构化字段只承担 schema 指定职责，不强迫多个字段重复同一症状、影响或理由。
- Judge evidence 以被测字段或真实对话为主，原始记录用于核实，不把测试作者结论伪装成候选证据。
- 可信 API evidence 要校验请求实体 ID、响应 ID 和必要字段；空对象、错误响应或错配响应不能自证。
- 工具调用分别检查调用发生、关键参数、次数和禁止调用；audit 没记录的字段不能凭空断言。
- 输出按存在、解析、顶层类型、必需字段、计数、关键值、集合、排序和一致性拆分。

旧式 conversation evidence 路径和 schema 以当前 runner 为准；若采用标准 ClawEval 适配器，可使用 `/logs/agent/conversation.json` 及项目提供的加载函数。任意轮次行为取全部 assistant 文本，最终答案取最后一条，条件触发取完整对话。

Seal 的 process evidence 可能来自 trajectory、工具流水或 frozen audit，output/safety 可能来自工作区与审计快照；只使用 runner 实际挂载且 manifest 声明的来源。不要跨架构假设 `trajectory.json` 或 `conversation.json` 天然权威，详见 `references/seal-rewardkit.md`。

## 10. 缺失 evidence 的分类

不得把所有缺失都写成 fail、skip 或普通 `return`：

| 情形 | 测试结果 |
|---|---|
| 候选按 instruction 必须生成的文件、字段、回答或调用缺失 | `FAIL` |
| 条件明确未被用户触发 | runner 的 skip / 不适用结果（旧式常为 `pytest.skip`） |
| 当前任务声明为可选的 conversation 或服务未提供 | 按任务约定 skip、不计分或 excluded |
| runner 未挂载本应提供的日志、judge 服务故障、harness 配置错误 | `BLOCKED` / infrastructure error，不算候选业务失败 |
| evidence 存在但格式损坏、ID 错配或必要字段不完整 | fail 或 harness error，取决于谁负责产生该 evidence |

普通 `if missing: return` 会把测试记为通过，禁止用于核心输出。仅当当前题专用规则或冻结兼容基线明确要求保留“官方 solution 无可选 conversation”的 guard 时才保留，并在 QA 中标为兼容性例外；不得把该例外推广到必需 evidence，也不得仅为统一风格擅自改成失败。

## 11. 可执行交付物的动态探针

固定 fixture 的 summary 正确不能证明脚本、插件或自动化程序正确。若交付物可执行，应设计能区分常见错误实现的最小合成输入，如非零保留量、严格/等值边界、乱序输入、状态分支和硬编码总数。

先检测可用隔离能力。不得把三种层级混称为“安全沙箱”：

1. 容器级：禁网、只读挂载、临时可写输出、非 root、最小 capabilities；
2. 进程级：最小环境、超时，POSIX 下使用 `RLIMIT_CORE`、`RLIMIT_CPU`、`RLIMIT_FSIZE`、`RLIMIT_NOFILE`、`RLIMIT_AS`、`RLIMIT_NPROC`；
3. 代码内 monkey patch：只作为纵深防御，不能替代容器或 OS 隔离。

候选代码不得获得 judge key、base URL 或宿主 secrets，也不得写入交付目录。无法达到当前风险所需的最低隔离时不要执行，标记 `BLOCKED`；探针失败要区分候选错误、超时、资源限制和 harness 错误。

## 12. 静态合规与运行验证

命令必须标注工作目录，优先使用当前项目自己的 runner，不把一套架构的命令套到另一套。

旧式 ClawEval 的常见最低检查可在 `tests/` 为当前目录时运行：

```bash
python -c "import rubrics"
python -m pytest --collect-only -p no:cacheprovider test_outputs.py
```

Seal/RewardKit 先检查 manifest、check registry、reward 配置和 `test.sh` 的实际加载链，再运行其声明的只读/静态验证入口。业务实现模式不得为了“验证一下”运行题目明确禁止的安装、构建、联网、发布、reset 或候选执行动作；可用语言解析器、标准库和文本/归档检查满足验证时优先使用它们。

共同人工核对：

- criterion 定义、注册、评分结果一一对应，无未知、未实现、重复或未声明计权项；
- 无内联评分语义、运行时 GT/solution 依赖或测试作者答案污染；
- 每项保持单事实、正向、可判定，缺失 evidence 分类正确；
- 数值与容差来自独立推导；
- 历史适用项和安全适用项均已处置；
- tests 和目标题没有混装；
- 当前 runner 的类名/tier 或 manifest/dimension/weight 聚合一致；
- 业务实现产物的路径、格式、内容同步、归档排除项和要求的 API 收口均已验证。

旧式额外检查 rubric 常量长度、句数、定义/引用及 test 对应；Seal 额外检查 `angle_id`、evidence、scorer、check registry、dimension 聚合与 degraded/infrastructure 行为。

### Judge secrets 本地范式

WorkC 的默认私密配置路径为 `~/.agents/skills/workc/.secrets/judge.env`；路径按当前用户主目录解析，不把某台机器的绝对路径写进测试或报告。GitHub 只保存 `.secrets/judge.env.example` 占位模板，真实 `judge.env` 必须被 `.gitignore` 排除。

使用 secrets 时遵守以下边界：

- 只检查真实 env-file 是否存在及必要的文件元数据，不使用 Read、`cat`、`type`、`Get-Content`、`source` 或其他方式读取、回显、解析其值；
- 仅在实际运行 judge 时通过 `--env-file` 或 runner 的等价参数注入，不把变量逐项展开到命令行；
- 不把真实文件复制到题目目录、发布仓库、日志、QA 报告、临时转写、容器镜像或候选代码可访问的环境；
- `.env.example` 只能写变量名、无效占位值和公开默认值，不能从真实 env-file 自动生成或替换；
- 用户明确指定安全 env-file 时优先使用该路径；否则使用上述本地路径。真实文件缺失时标记 `BLOCKED`，模板不得用于真实 judge 请求；
- 提交前用 `git ls-files` 和 ignore 检查确认真实 `judge.env` 未被跟踪，但不要用秘密内容做搜索样本。

Oracle/nop 在用户要求、项目流程要求或需验证区分度时运行。使用全新且互相隔离的 output、audit、conversation、run 目录和 judge cache；tests、solution、fixtures 只读。候选进程只获得完成任务所需的非秘密最小环境，judge secrets 仅进入 judge 进程。

HTTP 401/402/429/5xx、连接错误和超时属于 judge/infrastructure 问题，不直接算候选业务失败。修复运行条件后用全新 cache 和目录重跑，再判断真实失败。修改评分逻辑后做完整受影响运行；定向回归不能冒充全量 Oracle，也不能把新失败项结果与旧全量结果拼接。

若冻结 `test.sh` 使用 `pytest | tee` 且未传播 `${PIPESTATUS[0]}` 或启用 `pipefail`，shell 0 不足以证明通过。以 pytest 摘要、CTRF、reward、正式 runner 的 gate 和 num/den 交叉判断，并记录冻结脚本限制。

## 13. 验证状态与结果新鲜度

统一使用：

- `PASS`：规定范围全部完成且通过；
- `FAIL`：已执行，发现测试设计缺陷、候选真实失败或交付不合规；
- `PARTIAL`：可执行部分完成，但历史材料或非核心验证缺失；
- `BLOCKED`：硬冲突、关键材料、权限、基础设施或安全隔离阻止继续；
- `NOT_RUN`：未执行，不得暗示通过。

每次运行记录范围、时间、命令/runner、passed/failed/skipped/total、失败项、reward、dimension 分数、gate、num/den、degraded 状态和返回码；字段不存在就写未提供。只有正式 runner 产生的 gate 或 dimension 才能按该名称报告。

任何 criterion/rubric、check/test、judge 提示、探针隔离、权重或评分逻辑变化都会使相关旧结果过期。业务源码或交付物变化也会使其对应的旧验收结果和归档同步结论过期。QA 报告和最终结论必须对应最终磁盘文件与最后一次适用的完整运行。

## 14. 差异审计、报告与交付模式

只删除本次运行生成且来源可证明的缓存；原始包已有元数据保持不动，除非交付规则明确排除。运行产物、验证包装器、judge cache、secrets、临时转写和日志不进入交付包。

有冻结基线时，最终按规范化路径和 SHA-256 输出 `missing`、`changed`、`unexpected extra`。仅 allowlist 可变化，只有明确要求的报告等文件可新增；报告写完、测试改完后再做最终审计。

四种模式分别处理：

- `audit-only`：不改题目，不创建未要求的报告或 ZIP，只给审查结论。
- `changed-files`：只交付明确列出的修改/新增文件及要求的目录结构。
- `full-package`：复制完整任务目录，保留冻结业务文件，排除本地验证产物；验证 ZIP CRC、重复成员、顶层目录、必需文件和源文件哈希。
- `platform-submit`：在 `changed-files` 或 `full-package` 验证通过后，且用户明确授权，才使用当前正式入口上传并点击实际提交动作；“保存”或“上传成功”不等于提交完成。历史页面保持只读。

区分三类文字产物：内部工作记录、用户要求的报告文件、最终聊天回复。报告文件是否必需、语言、名称、路径和是否入包由当前项目决定；默认不创建。客户可见报告使用中性、面向交付的措辞，不泄露 secrets、临时路径、无关内部推理或不必要的轮次/返工标签；内部诊断只在确有审计价值时保留。

若要求 QA 报告，至少写清：材料范围、允许修改、修改文件及可定位的函数/章节、改动和依据、静态结果、实际运行范围和结果、失败分类、限制、交付审计及未执行项。不得沿用旧数量或旧分数。

## 15. Git 与最终声明

commit/push 不是验证流程的默认步骤。只有用户明确要求时执行；先确认 Git 根、分支、remote 和工作树，只提交本次 allowlist 文件，不夹带临时材料或其他改动。强推、覆盖远端或改写历史属于额外高影响动作，需要单独明确授权。

最终回复先给可交付结论和状态，再列目标文件、实际验证、剩余失败及其分类、冻结边界和已执行的外部动作。不得把：

- 本地保存说成平台提交；
- 上传说成已完成提交；
- targeted regression 说成全量运行；
- 环境错误说成候选失败；
- Oracle 1.0 说成规则完全正确；
- 未运行、PARTIAL 或 BLOCKED 说成通过。
