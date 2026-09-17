# Seal / RewardKit 新版质量与确定性评测参考

本参考用于正式当前格式采用 0917 新版 Seal/RewardKit 模型的 WorkC 测试侧作业。规范化后的必要结构是 `tests/criteria_manifest.yaml`，以及 `tests/process/`、`tests/output/`、`tests/safety/` 三个维度；每个维度必须恰好有一个 `checks.py`。只有 `tests/process/quality.toml` 与 `tests/process/reward.toml` 是可选配置；deterministic-only 题仍须具备三个维度的 `checks.py`，但可以没有 `quality.toml`、`reward.toml` 和 `react_prompt.md`。WorkC 可以完成、返修和验证 tests 侧评分实现，但不完成页面、服务、业务脚本、业务报告、业务归档或 API 状态。

`rubrics.py + test_outputs.py` 仍是有效的 legacy 架构，不要求 legacy 迁移。只有当前任务的正式格式、schema 和实际 runner 明确采用 0917 新格式时，旧式文件才作为迁移输入；它们不能与新版文件并列成为 criterion 身份源。两套结构同时被实际加载时标记 `hybrid`，加载链不完整或无法确认时标记 `unresolved`；先沿 runner 确认正式契约，不能任选一套或机械迁移。新格式的数据项若出现 quality/prompt 缺失、重复、归属歧义或模板绑定不一致，先将整条数据项标记 `DEPRECATED/ABANDONED`，不得自动创建、猜写、改名、拼接或合并 prompt 后继续验收。

题包内最大可写范围固定为实际授权的 `tests/**` 子集与根目录 `qa_report.md`。完成、返修或作业交付自检必须生成或更新该报告；除根目录 `qa_report.md` 这个固定例外外，所有 tests 外路径无条件冻结。

## 1. 固定主流程与作业模式

先理解题目、materialized carriers、当前 schema 与 runner 的正式要求，再建立 quality/manifest/check 覆盖基线；随后只修改和优化授权的 `tests/**` 子集，执行适用验证，最后生成或更新根目录 `qa_report.md` 并做差异审计。业务材料只用于推导 tests 应检查什么，不由 WorkC 修改；QA 报告是作业收尾，不是独立质检入口。

- **完成/返修测试侧作业**：沿 runner 实际加载链确定 `tests/**` 内候选 allowlist；获得明确授权后只修改该子集，并同步生成或更新根目录 `qa_report.md`。
- **作业交付自检**：若 tests 无需修改，题包内仅写根目录 `qa_report.md`；只有报告生成且差异审计闭合后才能声明完成。
- **只读咨询**：不修改、不运行、不生成报告或打包，并明确本轮未完成、未返修或未作业交付自检。
- **业务实现请求**：超出 WorkC 范围。业务文件只可作为测试侧 evidence 读取，不得由 WorkC 修改。

候选 allowlist 不能产生或扩大写权；它只能在 `tests/**` 内继续缩小范围。完整包交付前必须在本轮生成或更新根目录 `qa_report.md`；tests 未变化时使用 `report-only`，包只能写到题包外或用户明确指定的外部位置。

## 2. 新旧架构职责映射

| 评测职责 | Legacy ClawEval | 新版 Seal / RewardKit |
|---|---|---|
| 语义/质量定义 | `tests/rubrics.py` 中的 `RUBRIC_*` | 可选的 `tests/process/quality.toml` 中的 `[[criterion]]`，并绑定同目录唯一 `react_prompt.md` |
| 确定性检查实现 | `tests/test_outputs.py` 的评分 `test_*` | `tests/process/checks.py`、`tests/output/checks.py`、`tests/safety/checks.py` 中实际注册并运行的 scoring check；每维规范化后恰好一个文件 |
| 聚合索引 | 通常由 rubric/test 映射或评分脚本承担 | 必需的 `tests/criteria_manifest.yaml` 汇总 quality 与 deterministic 两类行，但不新增身份 |
| 证据来源 | workspace、conversation、audit、服务响应 | quality 的真实文件/trajectory，以及 checks 使用的 workspace、trajectory、tool trace、frozen audit 等真实 evidence |
| 语义判定 | `tests/judge.py` 或 helper | `quality.toml` 固定 `judge="react"`、`prompt_template="react_prompt.md"`，由 runner 执行 |
| 分类与权重 | pytest class、tier 映射或评分脚本 | quality/check 自身声明或注册，加 manifest 投影、可选 `reward.toml` 和 runner 聚合规则 |
| 运行入口 | `tests/test.sh` + pytest/CTRF/评分脚本 | 当前 RewardKit/Seal 运行链 |

新版不是把两个旧文件机械改名。必要的 manifest、三个维度唯一的 `checks.py`、可选且成套的 process quality/prompt、可选 reward 配置及 runner/task 配置共同构成评分契约，但各自身份职责不同。除非当前 runner 明确要求，禁止给新版题补建 legacy 文件；也不得擅自迁移一个正式且有效的 legacy 题。

## 3. 可选的 process quality 与 React prompt

### 3.1 路径、配对与数据项处置

0917 新格式只允许 `tests/process/quality.toml`；其他维度不得另设 quality。它本身可选，但一旦存在，同目录必须恰好有一个精确命名的 `react_prompt.md`，且 quality 必须使用 `judge = "react"` 与 `prompt_template = "react_prompt.md"`。`react_prompt.md` 只能承载正式来源已有的判定提示，不新增 persona/身份、评分权重或隐含业务要求。

以下任一情况使整条数据项先进入 `DEPRECATED/ABANDONED`，不继续按可交付项验收：

1. quality 存在但 prompt 缺失，或 prompt 存在但没有唯一对应 quality；
2. 任一文件重复、存在别名/大小写变体，或归属不唯一；
3. `judge` 不是 `react`，`prompt_template` 不是精确的 `react_prompt.md`，或模板实际解析到其他文件；
4. 需要通过创建、猜写、改名、拼接或合并 prompt 才能形成合法配对。

不得自动修复上述 prompt 问题，也不得从 rubric、README、历史 prompt、候选回答或多个片段推测模板内容。处置记录应保留原始路径、冲突集合和 evidence，供授权来源重新生产数据项。合法的 deterministic-only 数据项可无 quality/prompt，不因此弃用。

### 3.2 当前 schema 核验

quality 的其他字段拼写、层级、值类型、枚举和默认值仍以当前任务 schema 与实际 runner 为准；正式页面、题目内 schema 和 runner 发生差异时，记录冲突并按当前批次明确优先级处理，不为了套历史示例修改真实契约。evidence 路径必须由 runner 实际挂载并被 criterion 消费；不存在的示例路径、猜测路径和未挂载载体不得写入正式文件。

每个 `[[criterion]]` 只承担一个可独立计分的质量事实，使用稳定且在正式命名空间内唯一的 `id`。核对 points、criterion weight、dimension weight、reward 配置和聚合的实际语义，不能假设它们等价。已读 RewardKit 与 quality 页面只用于核对公开结构和 runner 行为；不复制内部原文、固定身份文本、示例题路径、canary、GT source 或任何秘密值。

## 4. `criteria_manifest.yaml`：聚合与投影

`tests/criteria_manifest.yaml` 是 0917 新格式的必要题包级 aggregate/index，用于汇总、追踪和审查两类评分项；它不是独立 criterion 身份源，也不因增加一行而增加 case。缺失、重复或路径不精确时，新格式结构不完整；不得用其他名称或 tests 外副本替代。具体 schema 以当前任务为准。常见顶层字段为：

- `version`
- `score_range`
- `dimensions`
- `criteria`

`criteria` 中每行常见字段为：

- `angle_id`
- `angle`
- `rule_hint`
- `dimension`
- `weight`
- `evidence`
- `scorer`
- `score_type`
- `source`

Manifest 同时包含 quality rows 与 deterministic rows。例如：

```yaml
criteria:
  - angle_id: output.narrative_quality
    scorer: process/quality.toml::output.narrative_quality
    score_type: likert
  - angle_id: output.delivery_form
    scorer: output/checks.py::delivery_form
    score_type: float
```

实际行还应填写当前 schema 要求且能从源定义投影出的 dimension、weight、evidence、source 等字段。上例 quality/deterministic 是行的职责分类，格式页的 `score_type` 示例值实际为 `likert/float`，不能用职责名称冒充枚举；相对路径仍须按当前解析根确认真实 target。

当前判分对齐页还说明 `summary/partial_credit/evidence` 的速览与部分分用途。若当前 schema 包含这些字段，核对部分分各项与 checks 实际算术及总分一致，不套用示例“十分”到其他 points。格式页的 `angle/rule_hint` 与此形态按当前 schema 选择，不盲目并入所有字段。Manifest 用于定位、速览和对照，正式规则、证据消费与权重必须打开对应 checks/quality 和 runner 验证。

对齐页示例要求 tests manifest 与题包根目录副本字节一致；仅当当前正式契约要求双副本时只读核对。根目录副本始终冻结，必须改它才能闭合时登记 `BLOCKED` 并移交，不自行创建或同步 tests 外文件。

完成或返修时要求：

1. 每个 `quality.toml` 的 `[[criterion]]` 必须 exact-once 投影到一个 quality manifest row；不得有遗漏、重复或 manifest-only extra。
2. 每个实际注册并产生独立分数的 `checks.py` scoring check 必须 exact-once 投影到一个 deterministic manifest row；不得有遗漏、重复或幽灵行。
3. 每个 `scorer` target 都必须按当前解析规则落到真实文件和真实 criterion/check 身份，不能只验证字符串长得合理。
4. quality row 的 dimension、weight、evidence、source 必须与对应 `[[criterion]]`、`[judge]`、正式规则来源和 runner 行为一致。
5. deterministic row 的 dimension、weight、evidence、source 必须与 check 注册、实际消费 evidence 和 runner 行为一致。
6. `angle_id` 在 manifest 的适用命名空间内唯一、稳定；最终机器结果若使用另一命名规则，要保留可复核映射。
7. helper、诊断项、环境 preflight、重复别名和未注册函数不进入 manifest scoring rows。

不要错误要求每个 quality criterion 映射到 `checks.py`。Quality 的闭合关系是 `quality.toml criterion ↔ quality manifest row ↔ judge/runtime quality result`；deterministic 的闭合关系是 `checks.py registration/runtime ID ↔ deterministic manifest row`。Manifest 汇总二者，但不会把 quality criterion 变成程序化 check。

在已核实的 RewardKit 0.1.7 架构中，框架不会自动读取该 YAML，实际程序化 criterion 仍由 `checks.py` 注册，因此 QA 必须主动比对 manifest、quality、registry 与结果。其他版本是否原生加载 manifest/quality 必须按实际安装版本验证，不能跨版本假设。

## 5. `checks.py`：确定性、程序化评分

0917 新格式固定包含 `tests/process/checks.py`、`tests/output/checks.py`、`tests/safety/checks.py`。规范化后每个维度目录必须恰好一个 `checks.py`：缺失、重复、别名或无法唯一确定加载目标均为结构失败，不能让多个文件共同充当一个维度的 checks。即使是 deterministic-only 数据项，也必须保留这三个文件；某维度没有适用评分事实时，按正式 schema 表达空注册，不虚构 case，也不补 quality/reward/prompt。只有 `tests/process/quality.toml` 和 `tests/process/reward.toml` 可选；其他自创 TOML 不能成为新格式配置。

- **Process**：检查规则发现、必需来源、正式输入/输出 recast、工具调用或禁止调用。Evidence 常来自 trajectory、tool trace 或 frozen audit。
- **Output**：检查文件存在、格式、schema、字段、精确值、集合、源码结构、CSV/JSON/ZIP、API 写回或在线状态。
- **Safety**：检查只读载体不变、禁止行为、fixture/tool 合同、secrets、发布/reset/deploy/endpoint 边界。

可确定复算的事实使用解析器、标准库或精确断言；不要用 judge 代替 ZIP、CSV、JSON、AST、集合、计数或精确数值检查。“完成必要正向动作”和“避免危险动作”通常是两个独立事实，应分别定义真实 scoring check。

### 注册与 runtime 一致性

不要只搜索函数名。沿 `test.sh` 和 RewardKit 入口确认：

1. 哪些 `checks.py` 模块实际被 import；
2. check 通过何种 registry/decorator/列表注册；
3. 每个注册/runtime scoring ID 如何解析到 manifest deterministic row；
4. 实际注册的 points/weight/dimension 是否与 manifest 投影及聚合契约一致；
5. 返回值如何表达 pass、fail、skip/excluded、blocked/degraded 和 evidence；
6. 异常是否被吞掉并转换为通过或候选 0 分；
7. 同一 check 是否自动和显式重复注册、重复加载或重复计权；
8. manifest deterministic row 是否存在 scorer 无法解析、漏载或 runtime ghost。

这是一条双向闭合：实际注册且独立计分的 check 都有且只有一个 deterministic row，每个 deterministic row 都解析到一个实际注册/runtime check。它不适用于 quality row 与 `checks.py` 的映射。

在 RewardKit 0.1.7 的程序化模式中，带额外 factory 参数的 criterion 可能需要模块底部显式调用 `rk.<name>(angle_id, weight=...)` 才会注册；实际权重来自注册调用，默认机器结果名可能组合函数名与第一个工厂参数。作业验证必须在独立新进程调用当前版本的真实 discover/runner，读取实际 `Session.criteria` 或结果详情；该版本可能缓存按路径导入的模块，同进程重复 discover 不能证明重新注册。版本或封装不同，以实际 decorator/registry 行为为准。

## 6. Evidence、Task、materialization 与安全

Evidence 声明、冻结动作、实际路径和 scorer 消费行为必须分别核对。确认记录确由 runner 挂载，实体、参数和响应可信；不能仅凭最终文件倒推出过程调用，也不能用候选自述替代审计证据。Quality judge 只接收该 criterion 所需的最小真实 evidence；deterministic check 只读取其正式允许的载体。

以下 tests 外文件始终冻结，只可读取：

- `task.toml`：任务分类、runner、环境、用户模拟器和 verifier 环境声明；
- `materialization_manifest.yaml`：需求载体、权限、路径解析和 input/output recast；
- `meta.json` 或 pipeline 状态：生成、版本或流水线元数据，不自动成为业务真值；
- `solution/`：仅可用于正式授权范围内的离线交叉检查，不能以“让 solution 通过”为由定义评分项；
- `ground_truth.json`：默认禁读，遵守 SKILL.md 第 5 节硬性要求。

期望值必须先从 instruction、workspace policy、fixtures、materialization 与 runner 声明的 evidence 独立推导。只有 Seal 当前正式规则明确授权、且独立推导已完成时，才可在评分进程外人工离线交叉检查 ground truth，并在 QA 报告记录授权来源与使用范围；无授权读取按越界处理，作废受影响推导并重新独立推导。不得把 ground truth 挂载或暴露给候选/正式评分容器，不得由 quality、checks、runner、环境变量动态读取，也不得作为 manifest `source` 覆盖当前权威载体。静态审查须覆盖 `test.sh`、Oracle/nop 脚本、Dockerfile 与挂载参数。

若 materialization 将同一需求拆到多个载体，按正式优先级和 recast 规则合并理解。Runner 外部 preflight 至少验证 fragment→resource→materialized target→io_target 引用闭合，authority/canonical/freshness/access 一致，必需 slot 有唯一当前权威载体；stale、legacy 和 distractor 不进入当前真值。Preflight 失败记 `BLOCKED`，不进入候选计分分母。

### 6.1 0818 防回归约束

- bootstrap/环境就绪问题不计入任务允许的问题数上限；上限只统计真正面向任务信息的提问。
- 正式 evidence 已给出答案时，不强制 ask-first 或重复追问；只在仍有影响结果的缺失/歧义时提问。
- 解析 persona/trajectory 时按消息、工具与字段的真实 actor 归属绑定，不能把 persona 中用户、助手、工具或第三方的行为错绑给候选 actor。
- HTML 的 judge/check 读取渲染后的可见语义、结构和可访问文本；不以固定字符切片、CSS 类名或 JavaScript 源码片段代替内容判定。需要验证脚本行为时另建有正式依据的程序化检查。
- 未在任务中披露或环境中不可用的服务，以及环境未提供的凭据，不构成候选硬失败；先按 infrastructure/blocked/excluded 处置。不得因测试作者知道隐藏服务或凭据而要求候选调用。
- “建议研究/可考虑研究”保持建议性质；除非当前权威要求明确升级为强制义务，不得改写成必须检索或必须调用。
- harness noise、收集器噪声、挂载/依赖/judge/网络等 infrastructure failure 不算候选失败，也不进入候选错误率分子。
- 只出现在 assertion message、错误文本或注释中、但没有独立正式 rubric/check 注册身份的 rubric 名称不构成评分身份，不计入 `R0/T0/N0`，也不生成 manifest 行。

## 7. Reward 聚合与版本验证

`quality.toml` 的 `[scoring].aggregation`、criterion points/weight、checks 注册权重、manifest 投影、`reward.toml` 与 runner 可能位于不同聚合层级。Manifest 行本身不额外产生分数或分母项。最终解释必须以当前实际 runner 为准。

作业验证至少复算：

- 每个 scoring unit/dimension 中实际 quality criterion 与 deterministic check 的集合；
- quality `points`/`weight` 和 check 注册权重如何归一或汇总；
- `[scoring].aggregation` 在当前 runner 中的实际含义；
- dimension 之间是等权、显式加权、门控还是其他组合；
- skip/excluded、blocked、degraded 和 infrastructure error 是否进入分母；
- safety 是否是普通 dimension，还是 runner 明确实现了 gate；
- 总 reward 是否能从原始 scoring result 与分维度结果复算，且 manifest 没有造成重复计权。

没有 runner 明确实现时，不得自行声称 safety gate、默认等权、manifest weight 是最终占比，或 quality/check 同名即自动合并。记录实际 Python、Seal/RewardKit 版本和配置来源；依赖须精确锁定，安装失败不可被 `|| true` 等吞掉，构建期验证导入和版本。

已核实的 RewardKit 0.1.7 程序化目录中，维度内部按 criterion 注册权重归一加权，顶层 `_collapse_rewards()` 使用各子 Reward 的 `reward_weight`，且不读取 `[[reward]].weights`。子 Reward 都采用默认 `reward_weight=1.0` 时，顶层严格等权；各维度 criterion 权重总和只是维度内部归一化分母，不形成跨维度占比。该结论只适用于实际验证过的 0.1.7 路径；升级版本、封装或新版 quality runner 后必须重新验证。

### 7.1 当前新版的 LLM 占比与防伪验证

当前 [判分与人工标注对齐](https://docs.xiaohongshu.com/doc/1a42e805086c3a943b112d67d80201e6) 规定全部 LLM 评分项的最终有效权重占比合计不超过 40%。按当前真实 criterion→group→dimension→reward 聚合链计算；嵌套加权均值时复算每层归一化后乘积再求和，不能只相加 manifest 原始权重或按条目比例。非线性门控、动态分母或未知聚合时报告适用情形与可核实上界，无法证明合规则 `BLOCKED`。不得为满足占比随意删语义 case；所需 reward 配置冻结时移交。

授权且隔离充分时对照关键词空壳、错误数值、关键内容缺失，并在题包外隔离配置移除全部 judge 项做消融。事实错误必须由保留的事实 checks 识别，不能靠 judge 补判。记录相同基线/evidence、单变量变更、受影响评分项、实际分母/归一化、各维度/总分与正式通过判据。没有明确阈值时不自定 0.95 等 cutoff，不把“明显失分”改为猜测的数值门；隔离或证据不足写 `BLOCKED/NOT_RUN`，不得在宿主执行候选替代可信验证。完整流程见 [current-sop.md](current-sop.md)。

## 8. Case 身份与计数

在任何审查性修改前冻结同一份可靠基线：

- `R0`：所有 canonical `quality.toml` 中可解析的 `[[criterion]]` 条目数；一个 `[[criterion]]` 条目就是一个 R case。重复或缺失 `id` 的条目仍各计一个 R，并另登记 schema/duplicate issue，不先按 ID 去重。
- `T0`：实际 registry/runtime 中唯一、产生独立计分结果的 `checks.py` scoring check 身份数；一个独立注册/实际 check 是一个 T identity。
- `N0 = R0 + T0`。

Manifest rows 只做投影与索引，额外计数为零。Quality criterion 不因存在 manifest row 或 judge runtime result 重复计数；check 不因注册参数、manifest row 和最终结果名不同重复计数。一个 factory 注册多个独立评分 ID 时按 ID 数；重试、参数展示、候选运行、helper、diagnostic、preflight、禁用或未注册项不增加 case。

分别建立两个闭合库存：

- quality：`quality.toml criterion id → manifest quality angle_id/scorer → runtime quality result id`；
- deterministic：`checks.py registration id → manifest deterministic angle_id/scorer → runtime check result id`。

若 runner 最终机器结果 ID 与源 ID 不同，按实际命名规则建立可复核映射后再比较多重集合。重复、遗漏、manifest extra、orphan、ghost 和歧义都登记 issue，不能相互抵消。

新增一个 quality criterion 独立增加 `AR=1`；新增一个实际注册的 scoring check 独立增加 `AT=1`；两者都新增时 `A=AR+AT=2`。纯 rename/move、manifest 重生成或保持评分事实与身份不变的迁移增加零。拆分时最多一个后继项继承原身份，其余新原子项分别进入 `AR` 或 `AT`。冻结后的 `R0/T0/N0`、`AR/AT/A` 与以下公式保持不变：

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

零分母、删除/合并和报告口径继续使用 [verification-and-reporting.md](verification-and-reporting.md)。

## 9. Judge 与降级行为

先从实际加载的 `quality.toml` 与 runner 确认是否存在 judge quality criterion，而不是仅凭 manifest 标签判断：

- 没有 judge criterion：可复算项保持确定性，不调用 judge，不加载 `judge.env`。
- 存在 judge criterion：逐项使用 `[judge]` 所声明且真实可用的最小 evidence；不注入标准答案，不让其他字段替指定字段通过。
- `files` 或 `atif-trajectory` 缺失、路径不实、未挂载或与 criterion 不匹配时，按当前 runner/preflight 规则记 infrastructure/BLOCKED，不得编造 evidence。
- Judge HTTP 401/402/429/5xx、连接错误和超时是 infrastructure failure，不是候选业务失败。
- Degraded 行为必须显式、可追溯；judge 不可用时不能静默 pass，也不能把基础设施错误计为业务 fail。
- RewardKit 0.1.7 的程序化 criterion 只接受布尔/数值结果，没有原生 `BLOCKED`、skip 或 excluded 返回通道。执行前由 runner 外部 preflight 检查 evidence 挂载、baseline、workspace、运行时和依赖；失败时终止评分并写独立 BLOCKED 状态，不生成候选 0 分。
- 程序化 check 若用宽泛 `except` 捕获所有异常并返回 `0.0`，可能把挂载缺失、命令不存在或 verifier 错误伪装成候选失败；只有候选负责的缺失输出才能转为 0，其他异常保留 runner 原始错误链。

Post-trajectory 才发现环境缺失时，在 `qa_report.md` 对受影响项逐行记录：发现阶段、`observed_at`、环境原因、单个 `exact_normalized_missing_path`、预期来源或挂载、可复核 evidence；每个精确规范化缺失路径独占一行，禁止目录概述、glob 或合并多个路径。状态写 `BLOCKED/OUT_OF_SCOPE`，并精确记录 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF`。上述记录完成后，该项无需其他测试侧修复，移交环境/授权负责人；不得创建缺失资源或把环境问题改成候选失败。只有在健康环境中、正式要求明确由候选交付而候选仍缺失时，才记 `FAIL`。

真实 judge 配置只通过 `~/.agents/skills/workc/.secrets/judge.env` 注入独立 judge 进程/容器；只有该受信任运行时可直接解析 env-file。代理、通用编排层和候选不得读取、回显、转写或解析其值；不得注入会启动候选的编排进程，judge 也不得再启动候选。

AI 生成或修改的 quality criterion、manifest row、check、expected value、judge 结论和 QA 摘要必须由人工回到正式规则、原始 evidence 与实际 runner 复核；reward、Oracle/nop 或 judge 通过不能替代该复核。

## 10. 新版 Seal 测试侧作业最低清单

1. **角色与范围**：确认这是 WorkC 测试侧作业；实际修改仅限授权的 `tests/**` 子集，并规划根目录 `qa_report.md`。
2. **架构与加载链**：由正式当前格式和 runner 判定 `legacy / seal-rewardkit-0917 / hybrid / unresolved`；`manifest-only` 仅作为结构观察，不是 architecture 值；保留有效 legacy，不强迫迁移。
3. **必要结构**：新版必须有 `tests/criteria_manifest.yaml` 和 process/output/safety 三维；规范化后每维恰好一个 `checks.py`，deterministic-only 也不例外。
4. **可选配置**：只有 `tests/process/quality.toml` 与 `tests/process/reward.toml` 可选；quality 存在时同目录必须恰好一个 `react_prompt.md`。
5. **Quality/prompt 合同**：固定 `judge="react"`、`prompt_template="react_prompt.md"`；缺失、重复、歧义或模板不一致时整项 `DEPRECATED/ABANDONED`，不自动创建、猜写、改名、拼接或合并 prompt，prompt 不新增身份/权重。
6. **Manifest 投影**：同时投影实际存在的 quality 与 deterministic rows；quality exact-once、checks exact-once，无 extras/omissions/duplicates，所有 scorer target 可解析。
7. **一致性**：核对 dimension、weight、evidence、source 和 runtime ID；不要求 quality criterion 映射到 `checks.py`。
8. **Registry**：在全新进程核对三维 checks 的注册/runtime ID、漏载、幽灵项、重复注册、实际权重和返回语义。
9. **0818 防回归**：bootstrap 不占问题上限；已有答案不强制 ask-first；actor 不错绑；HTML 取可见语义；不可用服务/缺凭据、harness noise 与 infra failure 不算候选失败；建议不升级成强制；assertion message 不产生身份。
10. **Evidence 与确定性**：trajectory/workspace/frozen audit 挂载真实；精确值、集合、文件、API、CSV、ZIP、语法和只读哈希使用确定性 checks。
11. **安全**：正向义务和禁止动作分别评分；无秘密泄露、ground-truth 依赖、fixture 自证或 reset 擦除审计。
12. **聚合与版本**：验证实际 RewardKit/Seal 版本并复算 quality、checks、dimension 和总 reward；manifest 不额外计分，只报告 runner 实际存在的 gate。
13. **计数**：一个 quality `[[criterion]]` 计一个 R，一个独立实际 scoring check 计一个 T，manifest 行计零；按冻结的 `R0/T0/N0` 和 `AR/AT/A` 计算指标。
14. **运行**：使用项目 runner 和新鲜隔离目录；记录各维度结果、总 reward、返回码、版本和基础设施错误。
15. **环境移交**：post-trajectory 环境缺失完整记录阶段、原因、精确路径、预期来源/挂载和 evidence，标 `BLOCKED/OUT_OF_SCOPE` 及指定 repair disposition；记录后无需其他修复。健康环境中候选应交付却缺失才 FAIL。
16. **差异审计**：题包内只允许本轮实际授权的 `tests/**` 子集和根目录 `qa_report.md` 变化；不提交缓存、日志、audit、真实 secrets 或候选产物。
17. **强制报告**：完成、返修或作业交付自检必须生成或更新根目录 `qa_report.md`，记录 test allowlist 外零变化并把报告标为唯一固定例外；缺少报告不得声明作业完成。
18. **新版占比与对照**：证明全部 LLM 项最终有效占比≤40%；验证空壳、错误数值、缺关键内容和 judge 消融，条件不足记阻塞，不凭参考候选高分认证。
19. **人员与阶段**：轨迹反馈逐项三段式归因、跨所有提供轨迹比较；独立记录个人多轮复测、人工核查、技术负责人批量复核与算法收口，不代签未发生的环节。

## 11. 典型分流与计数示例

- “完成这个 Seal 页面任务”：超出 WorkC 范围；不得修改页面、业务报告、归档或 API 状态。WorkC 最多承接测试侧作业。
- “完成/返修这个新版 Seal 题”：若正式 schema/runner 使用 0917 新格式，核对必要 manifest、三维唯一 checks、可选 process quality/prompt 与 reward，并更新根目录 `qa_report.md`。
- “修这个旧式题的 rubrics.py/test_outputs.py”：继续使用 legacy 架构，不因看到 Seal 文档就强制迁移。
- 发现 `Quality.TOML`、缺失的 `react_prompt.md` 或模板绑定不一致：整条数据项先 `DEPRECATED/ABANDONED`，保留证据并移交；不自动改名或补 prompt。
- deterministic-only 数据项：仍保留 process/output/safety 三个唯一 `checks.py` 和 manifest；可以没有 quality、reward、prompt，不补空配置。
- 新增 `output.narrative_quality` quality criterion：`AR=1`；它的 manifest quality row计零，且不要求同名 check；其 prompt 不产生新身份或权重。
- 另新增独立 `delivery_form` check：`AT=1`；其 manifest deterministic row计零。两项合计 `A=2`。
- 仅把旧 TOML 无损改名为 `quality.toml` 并重生成等价 manifest：`AR=0, AT=0, A=0`。
- “作业交付自检这个 Seal tests”：若无需修 tests，仅生成或更新根目录 `qa_report.md`；未落盘报告不能声明完成。
- “只告诉我需要做什么”：只读咨询，不修改、不运行、不打包、不创建报告，并明确本轮未完成作业。
