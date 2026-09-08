# Seal / RewardKit 评测架构参考

本参考用于识别和质检采用 `criteria_manifest.yaml + 分维度 checks.py` 的 Seal 任务。它说明职责和核对方法，不提供任何具体题目的答案，也不授权修改题包。

## 1. 先判断用户角色

目录带有 `tests/` 只表示任务包含验收器，不表示本次工作要维护验收器。

- **业务实现**：用户要求完成页面、服务、脚本、报告、归档包或 API 收口。`tests/` 默认只读，只用于理解验收条件；修改 instruction、项目规范和载体权限共同允许的业务文件，instruction 本身通常也是只读规则源。
- **判分器 QA**：用户要求质检 criterion、checks、RewardKit、区分度或评分逻辑。只说“审查、质检、检查、分析、报告问题”时默认 `audit-only`；明确要求“修改、修复、返修、增强、更新”后才进入 `fix-and-validate`，再从 runner 实际加载链确定 tests 内候选 allowlist。
- **只读分析**：用户只问需要做什么、文件对应关系、是否可交付，或明确要求不修改。只读材料并回答，不修改、运行候选代码、生成报告或打包。

候选 allowlist 不能产生写入授权；它只能在已经获得写入授权后继续缩小可修改范围。

## 2. 与旧式 ClawEval 的职责映射

| 评测职责 | 旧式 ClawEval | Seal / RewardKit |
|---|---|---|
| 评分项定义 | `tests/rubrics.py` 中的 `RUBRIC_*` | `tests/criteria_manifest.yaml` 中的 criterion/angle |
| 检查实现 | `tests/test_outputs.py` 的 `test_*` | `tests/<dimension>/checks.py` 中注册的 check |
| 证据来源 | workspace、conversation、audit、服务响应 | workspace、trajectory、tool trace、frozen audit 等 manifest/runner 声明的 evidence |
| 语义判定 | `tests/judge.py` 或 helper | manifest 指定的 judge scorer；没有则不调用 judge |
| 分类与权重 | pytest class、tier 映射或评分脚本 | manifest dimension/weight，加上 `reward.toml` 和 runner 聚合规则 |
| 运行入口 | `tests/test.sh` + pytest/CTRF/评分脚本 | `tests/test.sh` + RewardKit 运行链 |

新版不是把两个旧文件机械改名。Manifest、被加载的 checks、reward 配置、runner 和 task 配置共同构成评分契约。除非当前 runner 明确要求，禁止给 Seal 题补建 `rubrics.py` 或 `test_outputs.py`；旧式题也不得擅自迁移成新版。

## 3. `criteria_manifest.yaml`

Manifest 是题包级 criterion 身份与可追溯契约。具体 schema 以当前任务为准；在已核实的 RewardKit 0.1.7 架构中，框架不会自动读取该 YAML，实际 criterion 仍由 `checks.py` 注册，因此 QA 必须主动比对两者。其他版本是否原生加载 manifest 必须按安装版本验证，不能跨版本假设。常见字段职责如下：

- `angle_id`：题包内稳定、唯一的评分项标识；必须与 check 注册参数建立可复核映射，并核对 runner 最终机器结果 ID。RewardKit 0.1.7 默认结果名可能是 `<函数名>:<工厂参数>`，不是裸 `angle_id`；若要求三处同名，需使用该版本实际支持的显式 `name` 等机制并在全新进程验证。
- `dimension`：如 process、output、safety；必须是 runner 和 reward 配置认可的维度。
- `weight`：criterion 在其规定层级的权重。它不必等于最终 reward 占比，必须结合聚合规则解释。
- `evidence`：允许或要求读取的证据类型、位置或载体。
- `scorer`：确定性检查、judge 或其他受支持的评分器类型。
- `source`：该 criterion 的规则来源或载体，用于追溯，不是候选运行时可读取的标准答案。

QA 时检查：

1. `angle_id` 唯一，无空值、重复和拼写漂移。
2. 每个 criterion 只承担一个可独立计分的业务事实。
3. dimension、evidence、scorer 与 check 实际行为一致。
4. Manifest 中每个计分项都被 runner 加载并注册；每个计分 check 也都存在对应 manifest 项；同时核对注册参数与最终机器结果 ID，不能只做 AST 参数比对。
5. 不把 helper、诊断项、环境 preflight 或重复别名当成额外 criterion。
6. source 能追溯到当前 instruction、项目规范或正式载体，不用 ground truth 或 solution 覆盖独立推导。
7. 更改 criterion 集合、维度或权重前，确认题目级 allowlist 和冻结规则明确允许。

## 4. 分维度 `checks.py`

常见布局为：

```text
tests/process/checks.py
tests/output/checks.py
tests/safety/checks.py
```

目录名表达职责，不代表平台永远只有这三个维度。以当前 manifest、reward 配置和 runner import 链为准。

### Process

检查完成任务的过程证据，例如：

- 是否按要求发现和读取规则载体；
- 是否获取所有必需来源；
- 是否使用了 recast 后的正式输入/输出位置；
- 是否执行或避免了特定工具调用。

Process evidence 常来自 trajectory、tool trace 或 frozen audit。必须把 evidence 声明、冻结动作、实际路径和 check 消费行为分开核对，并验证记录确由 runner 挂载、实体和参数匹配、响应可信；不能仅凭最终文件倒推出调用发生，也不能用候选自述替代审计证据。

### Output

检查最终工作区和业务产物，例如：

- 文件存在、格式、schema、字段、精确值和集合；
- 源码语法、模块结构与内容一致性；
- CSV 行列、JSON 解析和 ZIP 真伪、成员路径、排除项、字节同步；
- 必需 API 写回或在线状态收口。

可确定复算的事实使用解析器、标准库或精确断言；不要用 LLM judge 代替 ZIP/CSV/JSON/AST 等确定性检查。

### Safety

检查只读边界、禁止行为和完整合同，例如：

- 不编造无来源内容；
- 只读载体哈希或内容保持不变；
- mock service、fixture 和工具合同完整；
- 未发布、未 reset、未部署或未调用禁止 endpoint；
- 未泄露 secrets，也未把 judge 配置暴露给候选。

“完成必要正向动作”和“避免危险动作”通常是两个独立事实，不应因为其中一个成立就免费通过另一个。

### 注册一致性

不要只搜索函数名。沿 `test.sh` 和 RewardKit 入口确认：

1. 哪些模块被 import；
2. check 通过何种 registry/decorator/列表注册；
3. 注册标识是否与 manifest 的 `angle_id` 完全一致；
4. 实际注册权重是否与 manifest 声明一致；
5. 返回值如何表达 pass、fail、skip/excluded、blocked/degraded 和 evidence；
6. 异常是否被错误吞掉并转换为通过或候选 0 分；
7. 同一 check 是否被自动和显式重复注册、重复加载或重复计权。

在 RewardKit 0.1.7 的程序化模式中，带额外 factory 参数的 criterion 可能需要模块底部显式调用 `rk.<name>(angle_id, weight=...)` 才会注册；实际权重来自注册调用，默认机器结果名可能组合函数名与第一个工厂参数。QA 必须在独立新进程调用当前版本的真实 discover/runner，读取实际 `Session.criteria` 或结果详情；该版本可能缓存按路径导入的模块，同进程重复 discover 不能证明重新注册。版本或封装不同以实际 decorator/registry 行为为准。

## 5. `reward.toml` 与聚合

`reward.toml` 描述 RewardKit 的维度、聚合或运行设置，但最终解释必须以实际 runner 为准。Manifest 中的 criterion `weight` 与最终 dimension 权重可能处于不同层级。

QA 至少复算：

- 每个 dimension 的 criterion 集合和分母；
- criterion weight 在维度内部如何归一或汇总；
- dimension 之间是等权、显式加权、门控还是其他组合；
- skip/excluded、blocked、degraded 和 infrastructure error 是否进入分母；
- safety 是否仅为普通 dimension，还是 runner 明确实现了 gate；
- 输出的总 reward 是否能由分维度结果复算。

没有 runner 明确实现时，不得自行声称 safety gate、默认等权或某个 weight 是最终总分占比。尤其要核对实际安装版本：已核实的 RewardKit 0.1.7 程序化目录中，维度内部按 criterion 注册权重归一加权，顶层 `_collapse_rewards()` 使用各子 Reward 的 `reward_weight`，且不读取 `[[reward]].weights`。子 Reward 都采用默认 `reward_weight=1.0` 时，顶层严格等权；各维度 criterion 权重总和只是维度内部归一化分母，不形成跨维度占比。升级版本后必须重新验证，不能把这一行为泛化。

## 6. Task 与 materialization 文件

这些文件帮助理解生成和运行链，但通常不是业务实现的可修改对象：

- `task.toml`：任务分类、runner、环境、用户模拟器和 verifier 环境声明；用于确认实际执行入口和挂载。
- `materialization_manifest.yaml`：描述需求如何分布到 user query、skill、workspace config、local documents 和 tool description 等载体；也可能描述读写权限、路径解析和 input/output recast。
- `meta.json` 或 pipeline 状态：任务生成、版本或流水线元数据；用于诊断，不自动成为业务真值。
- `ground_truth.json`：默认不读取。只有 Seal 当前正式规则明确授权时，才可在独立推导完成后用于评分进程外的人工离线交叉检查；不得挂载或暴露给正式评分容器/候选，不得被 tests、runner 脚本、环境变量或 checks 动态读取，也不得作为 manifest `source` 覆盖当前权威载体。静态审查须覆盖 test.sh、Oracle/nop 脚本、Dockerfile 与挂载参数，而不只搜索 checks.py。
- `solution/`：Oracle 参考实现或生成逻辑。可以用于授权范围内的离线交叉检查，但不能以“让 solution 通过”为由定义 criterion。

若 materialization 将同一需求拆到多个载体，必须按其正式优先级和 recast 规则合并理解；不得只读 `instruction.md` 就忽略 workspace policy，也不得把只读 carrier 当成应修改的交付物。

不要把 materialization 自报的 constraint check 当成独立证明。runner 外部 preflight 至少验证 fragment→resource→materialized target→io_target 引用闭合，authority/canonical/freshness/access 一致，必需 slot 有唯一当前权威载体；用声明解析器重验 input/output recast 与 preserved semantic slots，并确保 stale/legacy/distractor 不进入当前真值。preflight 失败记 `BLOCKED`，不进入候选计分分母。

## 7. Seal 的 case 计数

在任何审查性修改前冻结同一份基线：

- `R0`：manifest 中唯一、正式计分的 `angle_id` 数；
- `T0`：实际 registry 中唯一、产生独立计分结果的 check 身份数。

一个 factory 函数注册多个计分 ID 时按 ID 数；同一 check 的重试或不同候选运行不重复计数。helper、diagnostic、preflight、禁用或未注册项不算有效评分 check。重复 ID 按稳定身份只计一次，但重复本身是 issue；孤儿 manifest criterion 和幽灵注册 check 分别保留在各自库存并登记映射缺陷。

用多重集合固定口径，但只在同一命名空间比较：`M` 为 manifest `angle_id`，`R` 为全新进程真实 runner 产出的最终 criterion ID。先根据实际注册参数和 runner 命名规则建立可复核映射 `f: angle_id → expected_final_id`，再令 `E=f(M)`；映射缺失、歧义或一对多本身登记为 issue。manifest/runtime duplicate 分别在 `M`、`R` 内计算 `Σ max(count(id)-1,0)`；orphan 使用多重集合差 `E-R` 并通过 `f` 回报对应 `angle_id`，ghost 使用 `R-E`。只有已证明两侧采用相同 ID 命名空间时，才可直接比较 `M` 与 `R`。0.1.7 默认结果名若带函数名前缀，必须同时报告“注册参数映射”和“最终结果 ID 映射”，不能把前者 1:1 冒充最终闭合。

新增 criterion/check 必须有正式 claim 来源、有效身份、注册/绑定和适用验证。纯 rename/move/描述调整不计新增；拆分时最多一个后继项继承原身份，其余新原子项进入 `AR/AT`。完整公式见 [verification-and-reporting.md](verification-and-reporting.md)。

## 8. Judge 与降级行为

先看 manifest 是否存在 judge scorer：

- 没有 judge criterion：所有可复算项保持确定性，不调用 judge，不加载 `judge.env`。
- 存在 judge criterion：只向 judge 提供该 criterion 所需的最小真实 evidence，不注入标准答案，不让其他字段替指定字段通过。
- Judge HTTP 401/402/429/5xx、连接错误和超时是 infrastructure failure，不是候选业务失败。
- Runner 的 degraded 行为必须显式、可追溯；不能在 judge 不可用时静默 pass，也不能把基础设施错误计为业务 fail。
- RewardKit 0.1.7 的程序化 criterion 只接受布尔/数值结果，没有原生 `BLOCKED`、skip 或 excluded 返回通道。criterion 执行前必须由 runner 外部 preflight 检查 evidence 挂载、baseline、workspace、运行时和依赖；失败时终止评分并写独立 BLOCKED 状态，不生成候选 0 分。
- 程序化 check 若用宽泛 `except` 捕获所有异常并返回 `0.0`，可能把挂载缺失、命令不存在或 verifier 错误伪装成候选失败；只有候选负责的缺失输出才能转为 0，其他异常保留 runner 原始错误链。

真实 judge 配置只通过 `~/.agents/skills/workc/.secrets/judge.env` 注入独立 judge 进程/容器；只有该受信任运行时可直接解析 env-file。代理、通用编排层和候选不得读取、回显、转写或解析其值；不得注入会启动候选的编排进程，judge 也不得再启动候选。

## 9. 判分器 QA 最低清单

1. **角色与范围**：确认用户要求 QA，而不是完成业务题；记录 allowlist 和冻结文件。
2. **加载链**：从 `task.toml`、`test.sh`、RewardKit 入口追到实际 manifest、checks 和 reward 配置；记录实际 Python/RewardKit 版本，不抄 meta 声明。依赖须精确锁定且安装失败不可被 `|| true` 等吞掉，构建期验证导入和版本。
3. **规则来源**：从 instruction、workspace policy、fixtures、工具文档和 materialization 载体独立建立覆盖矩阵。
4. **Manifest**：核对 ID、dimension、weight、evidence、scorer、source 和原子性。
5. **Registry**：核对 manifest ↔ loaded check 双向一一对应，无漏载、幽灵项、重复注册或诊断项计分。
6. **Evidence**：确认 process/output/safety 各自读取正确的 workspace、trajectory 和 frozen audit；缺失分类正确。
7. **确定性**：精确值、计数、集合、时间、文件、API、CSV、ZIP、语法和只读哈希使用确定性断言。
8. **安全**：正向义务和禁止动作分别评分；无秘密泄露、GT 依赖、fixture 自证或 reset 擦除审计。
9. **聚合**：复算 criterion、dimension 和总 reward；只报告 runner 实际存在的 gate。
10. **运行**：使用项目 runner 和新鲜隔离目录；记录各维度结果、总 reward、返回码和基础设施错误。
11. **差异审计**：仅 allowlist 文件变化；不提交缓存、日志、audit、真实 secrets 或候选运行产物。

## 10. 典型分流示例

- “完成这个 Seal 页面任务”：业务实现。读取 tests 辅助理解，但只修改允许的页面、报告、归档和 API 状态，不改 criterion/checks。
- “质检这个 Seal 题的 criterion”：判分器 QA。审查 manifest、runner 实际加载的 checks 和 reward 聚合，不补旧式文件。
- “修这个旧式题的 rubrics.py/test_outputs.py”：旧式判分器 QA。按 rubric/test 一一对应与 pytest runner 流程处理。
- 同时出现两套结构：混合/未知。读取 runner 确认真正入口；不能任选一套，也不能顺手迁移。
- “只告诉我需要做什么”：只读分析。不修改、不运行、不打包、不创建报告。
