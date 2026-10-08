---
name: workc
description: WorkC、ClawEval、PinchBench、Seal 或 RewardKit 单题的测试侧作业完成、返修、作业验证、Oracle/nop、QA 报告与交付流程。只处理这些题包的 tests 侧交付，不承接业务实现或通用质检。题包内最大可写范围固定为 tests/** 与根目录 qa_report.md；完成、返修或作业交付自检必须生成或更新 qa_report.md，其余路径全部冻结。仅在用户明确要求这些题包的测试侧作业，或目录出现 legacy 的 rubrics.py + test_outputs.py、0917 新格式的 criteria_manifest.yaml 与 process/output/safety checks、quality.toml/react_prompt.md 或对应 runner 信号并明确要求测试侧作业时使用。
---

# WorkC 测试侧作业内核

## 1. 不可解除的边界

WorkC 只完成题包的测试侧作业，不完成页面、服务、业务脚本、业务数据、业务报告、业务 ZIP 或 API 状态，也不是普通项目的通用质检 Skill。

题包内最大可写集合固定为：

```text
tests/**
/qa_report.md
```

- 实际 test allowlist 只能在 `tests/**` 内继续收窄。
- 完成、返修或作业交付自检必须在本轮生成或更新根目录 `qa_report.md`；tests 无需修改时使用 `report-only`。
- 其余题包路径全部冻结。用户指令、instruction、materialization、复制副本和打包请求均不能扩大写权。
- **禁止读取题包根目录 `ground_truth.json`**。WorkC 的分析、返修、复检、报告、tests、候选、runner 与独立 reviewer 均无例外；期望值只能从允许的正式载体独立推导。若其他流程声称获得读取授权，必须在 WorkC 外单独执行且其结果不得进入 WorkC 的 claim、expected value、evidence 或认证。
- **禁止读取或引用题包 `.pipeline/` 内容**：WorkC 不得打开、读取、解析、搜索、摘要或以其他方式消费该目录下的任何文件；`.pipeline` 不是正式规则载体，不得作为 criterion、expected value 或 evidence 来源。引用审计只能在 `tests/**` 与根目录 `qa_report.md` 等允许读取的 work 数据中检查 `.pipeline` 路径字符串，不得进入该目录核对。发现 work 数据引用时，在可写范围内删除并复跑适用验证；冻结路径若由允许来源指出存在引用，只记录该外部发现与路径，不自行读取或修改。
- 必须修改 tests 外文件才能解决时，记 `OUT_OF_SCOPE/BLOCKED`，不得顺手修复。
- 纯咨询或明确不修改时可以 chat-only，但必须声明本轮未完成、未返修或未作业交付自检。

测试必须反映正式规则，不能用 Oracle 分数反推规则。Oracle 不必为 1，nop 不必为 0；不得为改善分数删除有效 case、放宽正确条件、篡改真值、伪造 evidence、修改 nop 或掩盖基础设施错误。AI 生成或修改的 criterion、check、expected value、judge 结论和 QA 摘要都必须由人工回到正式规则、原始 evidence 与实际 runner 复核。

维护本 Skill 自身时转入 skill-creator 元流程。本文件不授权修改任何题包外仓库。

## 2. 固定主流程与作业状态

```text
P0 范围卡
→ P1 基线契约与库存快照
→ P2 claim–evidence–scorer 拓扑
→ P3 不变量与变异控制矩阵
→ 修改实际授权的 tests/** 子集
→ P4 变更影响与新鲜度账本
→ C1 canonical V1 hard gate
→ C2 独立设计/载体覆盖复审
→ C3 独立 expected-value 复算
→ C2a 对适用的修改、影响或风险判据做反例审计
→ 更新根目录 qa_report.md
→ C4 对账适用的 issue、freshness、状态与差异
→ 交付退出门与差异审计
```

开始前固定：

- `target`：`test-delivery` / `test-harness` / `consultation` / `package`；
- `mutation`：`none` / `tests-allowlist-plus-report` / `report-only`；
- `execution-ceiling`：V0 text-only、V1 parser-only、V2 harness-import、V3 candidate-run、V4 judge-run、V5 external-action；
- `delivery`：`chat-only` / `completed-assignment` / `full-package` / `platform-submit`；
- `architecture`：`legacy` / `seal-rewardkit-0917` / `hybrid` / `unresolved`。

**单题默认执行最小适用闭环**：锁定范围与 allowlist → 确认 profile、正式依据和实际加载链 → 检查与任务及变更相关的 claim/evidence → 仅修复已确认且在授权 `tests/**` 内的问题 → 执行已授权且受影响的验证 → 更新根报告并审计最终差异。P0–P4、C1–C4 的状态与 readiness 仍须如实对账；工作产物和审查深度按相关范围收敛，不要求对未受影响判据重复构造整套探针。完整逐判据审计、广泛动态运行、轨迹/平台交付和 profile 专项台账仅在任务目标、适用 profile、变更影响或具体风险触发时展开。适用检查未执行须记 `NOT_RUN/BLOCKED`，不适用须记 `NOT_APPLICABLE` 并说明依据；两者均不是 PASS，也不能满足其必需 readiness 门。

候选运行、judge 和外部动作分别需要当前题目与用户授权。完整包只能写到题包外或用户明确指定的外部位置；打包不扩大写权，也不能替代 QA 报告。详细边界见 [routing-and-authority.md](references/routing-and-authority.md)。

当前批次正式指令：评分容器运行 `harbor-rewardkit==0.2.0`，题包须统一适配并精确固定到该版本——0.2.0 与 0.2.1 对"装饰器自动注册后再显式注册"的处理不同，会影响准则数量与权重；`0.2.*` 等前缀写法视为未固定，本地验证与每个 run 都必须标注实际精确版本。规则细节见 [seal-rewardkit.md](references/seal-rewardkit.md) 的"7.0 RewardKit 版本固定"。

### 2.1 P0–P4 Contract Gates（先建契约，后允许返修）

这五个产物可以先保存在工作笔记，并在交付时投影到 `qa_report.md`；不在题包内创建额外清单文件。**没有完成受影响的前置门，不得编辑评分文件；前置门失败时标 `BLOCKED`、`DEPRECATED` 或 `ABANDONED`，不得通过放宽 test、猜测 schema、伪造 evidence 或修改冻结路径绕过。**

| 门 | 编辑/认证前必须形成的最小产物 | 未通过时的处置 |
|---|---|---|
| P0 Scope Card | target、mutation、实际 tests allowlist、V0–V5 上限、delivery、禁读项、所需动态运行授权与隔离前提 | 超出范围或缺授权：停止该动作；冻结路径问题记 `OUT_OF_SCOPE/BLOCKED` |
| P1 Baseline Contract | 任务所需正式载体与 precedence、architecture/加载链、相关身份基线、必要 runner/聚合与 runtime path/digest、冻结输入及相关 evidence owner/writeability | 结论必要的 identity、结构或 runtime 不能可靠建立：不猜数；受影响指标 `N/A`，依赖该事实的修复/认证不得 PASS |
| P2 Claim–Evidence–Scorer Topology | 受影响及结论必要的 score-bearing identity 对应 formal claim、触发条件、authority、producer、候选可达/可写性、runtime ID、相关权重链、fallback 和三分归因 | 正向 claim 没有可信真值源或唯一 authority：该 claim `BLOCKED`，不能由候选日志/自述补足 |
| P3 Invariant / Mutation Matrix | 适用不变量、已发现缺陷的最小正反例，以及与具体风险相称的伪造/空集/服务失败控制 | 适用控制缺失、空集自证或 evidence 可伪造：不能标 FIXED 或认证 |
| P4 Change-Impact / Freshness Ledger | 本轮变更影响的 claim、identity、validator、control、aggregation、必要验证及相关 run digest/freshness | 适用 run 旧、范围不足或跨环境拼接：`STALE/UNVERIFIED`，不能认证 |

P1 不是只记录一个总 hash：它必须足以重建本轮结论涉及的“什么在运行、什么在计分、谁生产证据、候选能否改写”；完整认证时还须覆盖完整评分链。正式 source 版本变化时新建 revision baseline，不覆盖旧基线。P2 的 evidence 只有三类：**verifier/authority-owned**（可建立真值）、**candidate-owned**（只能证明候选行为）、**infrastructure-owned**（不可用时归 infrastructure）。候选可写路径即使被 verifier 复制、重命名或加 hash，也不会变成独立真值。

P3 仅展开与适用 score-bearing 规则、已发现缺陷或具体风险相关的最小反例；一项证据可同时满足多个对应控制，避免重复造相同探针。每个确认的 tests-side 缺陷在关闭前必须晋升为常驻回归：保留最小反例、正例、预期、issue ID、run ID 和 freshness；确实无法构造时维持 `BLOCKED`，不得写 `FIXED`。P4 记录受影响范围即可，不要求无变更的无关身份重复盘点。

P4 的 `FRESH` 只在全部会影响结论的输入、runtime loaded path/digest 和 run scope 一致时成立。不得把不同 run 的局部 PASS 拼成完整认证。P0–P4 静态交付契约、C1–C4 handoff 状态及 `test_delivery_handoff_ready` 条件仍按现行门槛执行；缩减证据范围不能将适用的 `NOT_RUN` 视为 `PASS`。`evaluation_certified` 另须满足其适用动态验证条件。

### 2.2 C1–C4 交付闭环（冻结差异后再认证）

P0–P4 约束返修过程；C1–C4 负责在最终差异冻结后发现遗漏、陈旧结果和报告自相矛盾。它们只消费现有正式载体、validator、回归和报告，不新增写权、评分身份、隐藏真值权限、固定 canary、全局 RewardKit 版本或第二份 QA 报告。详细算法见 [pre-delivery-qa-fusion.md](references/pre-delivery-qa-fusion.md)。

| 门 | 必须闭合的交付事实 | 失败/变更后的处置 |
|---|---|---|
| C1 Canonical V1 Hard Gate | 对本轮适用的正式 schema/身份/映射/聚合/carrier 检查使用唯一 canonical V1 入口；范围由目标 profile 与变更影响决定 | 无唯一入口、局部脚本冒充完整入口、适用 validator 未实际阻断或任一适用项失败：V1 不通过；未执行不得写 PASS |
| C2 Independent Design / Carrier Re-audit | 对本轮受影响及结论必要的 score identity、正反条件、authority/producer/writeability、carrier、manifest/runtime closure 和遗漏角度作独立只读复审；完整认证按全适用范围审查 | 发现新 defect 或遗漏：登记 issue，回到最早受影响的 P 门修复；实质差异改变后，所有依赖旧输入的闭环结果 `STALE`，从 C1 重新闭合 |
| C3 Independent Expected-value Recalculation | 独立复算本轮相关的常量、边界、集合、计数、权重与 reward；完整认证覆盖其正式要求的全量范围 | 不一致不能用 Oracle/GT/judge 分数覆盖；修复后受影响的旧复算及闭环结果失效 |
| C2a Applicable Adversarial Counter-example Audit | 对本轮修改、受影响或存在明确过松/过严风险的 score-bearing 判据，审计最小 under-strict 与 over-strict 反例；适用的等价解、对象身份和生成式检查按风险展开。无适用判据时记录 `NOT_APPLICABLE` 及依据 | 反例证明判据放水/错杀即登记 issue；适用控制缺少可复核实跑或静态推演时标 `BLOCKED/UNVERIFIED`，不得宣称通过 |
| C4 QA Accounting / Status Reconciliation | 核对适用身份/issue 计数、freshness、三分归因、C1–C3 与 C2a 状态、allowlist diff 和四个交付状态；无适用计数时使用 `N/A` 并说明 | 任一计数、issue、run、blocker 或状态矛盾：报告不闭合；只降级受影响结论，不以多数通过或摘要覆盖底层 evidence |

独立 reviewer 可以是未参与当前修复的子代理或人员，但其结果不等于 `human_review_status` 或 `technical_lead_review_status`。C2a 只对适用范围执行，不按无关判据凑反例；未执行的适用项目必须明确记 `NOT_RUN/BLOCKED`，不计 PASS。实质性 tests、输入、评分证据或结论变化后，按最早受影响的 P 门更新契约，再使依赖旧输入的 C 结果失效并从 C1 重闭；纯记录/排版且不改变证据与结论的报告更新不触发重启。

**独立复审验收按证据质量，不按报告长度**：对实际委托且适用的复审，核对其覆盖范围、独立性、证据引用、发现与未决项；存在具体矛盾或覆盖缺口时针对缺口复核。不得以同批报告长度百分位拒收，也不得为满足随机抽查配额重复打开无关判据。

#### Schema-safe manifest / validator placement

当前任务正式 schema 与实际 runner 优先于历史示例。只有正式 schema 明示允许扩展时，才能向 `criteria_manifest.yaml` 添加 evidence registry 或 validator metadata；**不得为了满足 WorkC 抽象要求添加未知顶层字段。**若 schema 不允许或 runner 不加载该位置，registry/validator 必须位于 runner 已批准、不会被自动发现为 scoring module 的 tests-side 位置，或由不可变 harness 提供。找不到合法位置即 `BLOCKED`。仅在本轮适用且需要 validator 时，才要求其在 scoring runner 前 fail-closed 执行并记录路径、digest、启动命令及与漂移风险相称的验证结果。

## 3. 架构识别与 profile 分流

文件名只是候选信号，最终沿 `test.sh`、task 配置、import/registry、结果与聚合链确认：

| 信号 | profile | 评分身份 | 处理 |
|---|---|---|---|
| `tests/rubrics.py` + `tests/test_outputs.py` | legacy | 实际评分链消费的稳定 `RUBRIC_*` 与独立评分 `test_*` | 保留旧架构，不机械迁移 |
| `tests/criteria_manifest.yaml` + 三个固定维度目录 | seal-rewardkit-0917 | `quality.toml` 的 active `[[criterion]]` 与 `checks.py` 实际注册 check | 执行 0917 结构和 React 前置门 |
| legacy 与新版链同时被加载 | hybrid | 按各自实际加载链取身份 | 分链审查，不任选一套 |
| manifest 单独存在、结构缺件或加载链不明 | unresolved | manifest 不建立身份 | fail closed，追正式 claim/runner |

0917 的 `checks.py` 中，`@criterion` 装饰器与底部 `rk.<name>(...)` 注册调用是同一个激活单元：停用某个 check 时两者必须同时注释或同时删除，只改一侧会造成未装饰注册或幽灵残留，按结构 drift 处理；细则见 [seal-rewardkit.md](references/seal-rewardkit.md) 的“注册与 runtime 一致性”。

0917 profile 的必要结构是：

```text
tests/
├── criteria_manifest.yaml
├── process/
│   ├── checks.py
│   ├── quality.toml       # optional
│   ├── reward.toml        # optional
│   └── react_prompt.md    # quality.toml 存在时 required
├── output/
│   └── checks.py
└── safety/
    └── checks.py
```

`process`、`output`、`safety` 每个目录在路径规范化后必须恰好包含一个 canonical `checks.py`；缺失、重复、大小写或归档成员碰撞均为结构错误，不得猜选。三个文件可以没有独立 deterministic scoring identity，但物理结构仍必须存在。Deterministic-only 合法：三个 `checks.py` 完整时，`process/quality.toml`、`process/reward.toml` 和 `react_prompt.md` 可以缺席。Legacy 不受该目录结构约束。

架构识别只决定如何完成 tests 侧作业，不产生业务文件写权。旧式细则见 [legacy-claw-eval.md](references/legacy-claw-eval.md)，0917 Seal/RewardKit 细则见 [seal-rewardkit.md](references/seal-rewardkit.md)。

## 4. Claim 来源与 0818 防回归护栏

先由 task/materialization 确认正式载体，再将要求拆成原子 claim，至少记录：

```text
claim_id | source/carrier | source_class | scope | version/date
modality | actor | known_answer_source | question_budget_class
required_service/capability | availability/credentials
explicit_precedence | recast | resolution | reason
```

来源可以决定 tests 应覆盖什么，但不能扩大写权。适用以下已发布验收护栏，后续批次不得复发：

1. **问题计数**：bootstrap、身份建立和平台接入问题不占任务问题上限；同时索取任务事实的混合问题按实际任务意图计数，不按问号或消息数机械计。
2. **已有答案**：instruction/input 已提供的信息不得设为必须先问；确实缺失、冲突且影响结果的信息仍可要求澄清。
3. **Actor 绑定**：模拟用户 persona 约束模拟用户，不得错施于 agent；只有正式 agent instruction 或评分 claim 明确绑定 agent 才可评分。
4. **要求强度**：建议、可研究或可考虑的内容不得升级为强制评分项；明确 mandatory 且 evidence 可验证的要求除外。
5. **HTML evidence**：页面语义 judge 使用可见、相关的标题、正文、列表、表格、链接文本和可访问名称；禁止固定字符盲切或用 CSS/JavaScript 偶然关键词替代可见内容。明确评价源码实现时，源码 evidence 与页面语义 evidence 分开。
6. **服务与凭据**：未披露、不可用或缺可信环境凭据的服务不能成为候选硬门；正式依赖但环境缺失时记 infrastructure/BLOCKED，不要求候选寻找 secrets。
7. **日志归因**：候选输出、harness/exec 诊断噪声、基础设施失败必须分开；wrapper banner、shell warning 和 verifier 日志默认不进入候选质量判断。
8. **评分身份**：仅作为 assertion message、异常文本、日志标签、测试标题或 display name 的 `RUBRIC_*` 常量不是评分身份；必须能追到 judge、registry、结果或正式聚合映射。
9. **双模式轨迹解析**：当适用判据依赖 trajectory evidence 时，按正式输入形态验证解析器可处理实际使用的 solution/agent 模式。不能仅凭 oracle 轨迹证明 agent 模式已验证；适用模式或真实样本不可得时记 `UNVERIFIED/BLOCKED`。清理/落点类动作可优先以正式要求的工作区终态作模式无关证据，叙事令牌只能作辅助。
10. **权重单一口径（常驻）**：先从已验证的实际 RewardKit/runner 版本、加载路径与 runtime result 确认逐项 weight 语义，再要求 manifest/索引投影与运行时单条评分单元一致；例如仅在已验证为 rewardkit 0.2 对应行为时，deterministic 行映射 checks.py 注册权重、judge criterion 行映射 quality.toml `[[criterion]].weight`，缺省 1.0 并按实际维度规则归一。桶级（`$checks`/quality）与维度级权重按当前 runner/reward.toml 的真实层级处理，禁止把归一化值或上层权重泄漏进行内。版本或封装不同时必须通过 runtime discovery 重建映射，不能套用 0.2 或历史示例。跨层混用多套口径会使"行和恰为 1"的错误校验自洽通过——核对时必须沿 criterion→bucket→dimension→reward 真实链逐层复算，并逐行与运行时注册权重比对，不做聚合和校验替代。

`ground_truth.json` 的禁读规则继续优先。两个正式载体无法消解时，只阻断受影响 claim。

### 4.1 判据自证与空集护栏（常驻，20260920 批次起）

以下是按判据特征触发的常驻护栏：只审查存在相应逻辑/证据依赖的判据；适用检查必须 fail closed，确认缺陷须补永久回归。不得要求每个判据机械执行所有类别的探针。

1. **空证据集不得自证**：正向、序列、完成度或过程型谓词使用 `all(...)`、`any(...)`、`sum(checks)` 等集合聚合时，检查空集合结果。凡空集能使分数非 0 或直接满分，必须显式要求关键证据存在，否则 0.0。空集通过 = 判据为空壳。例外仅限正式规则本身为负向安全事实（如“未调用禁调 endpoint”）：服务可用且权威审计明确返回空 list 可证明未发生该动作；服务不可达/载荷无效不是空 list，必须 fail closed。
2. **判据证据不可由被评者写就**：沿生产者链核对每个 evidence 文件——谁创建、挂在哪个卷、agent 进程是否持写权。agent 可写卷（如 `/logs/agent/**`、`/tmp`）上的文件只能作 candidate-attributable 行为证据，不得作为判据真值来源；verifier 侧“复制/改名/算哈希”不改变来源可伪造性。修复方向按优先级：服务进程内查询端点（例如 `/v1/audit`）且其**底层审计状态也必须由服务/verifier 持有，候选不能通过其他 endpoint、共享卷或挂载修改、删除或回滚** > 挂载在 verifier 侧、agent 无路径可达的副本 > 原则上不用（见下）。仅 GET/“只读”路由本身不是 authority 证明，P2 必须核验 producer、backing state、候选 reachability 与 mutation path。一旦采用服务活真值，**禁止任何文件回退**：成功响应（含空列表，即真实 nop 状态）必须原样当真返回——把合法“空真值”误判为服务不可用而回退读文件，等价于给伪造证据留门（20260920 返修实测缺陷）；连接失败/超时/无效载荷一律 fail closed（判据按缺证据记 0，基础设施归因交 runner/报告），不得改读任何 agent 可及副本。行形状校验（int `seq` + str `ts` 之类的“生产者盖章”）不构成担保——这些字段同样可被伪造，只许作纵深防御，禁止作 fallback 准入条件。禁调/完整性类负向判据（如 forbidden-call purity）优先“读活真值”而非“文件里没出现坏行”，避免判据逻辑向 agent 泄漏。
3. **正控与负控判定**：验证预期必须匹配 claim，而非机械要求 oracle 满分或 nop 为 0（WorkC 总则：Oracle 不必为 1，nop 不必为 0）。正向过程/完成度 claim 在没有必要的肯定性证据时须为 0；负向安全 claim 可在**可达且格式有效的权威 live audit**明确显示无违例时合规，即使该 audit 为 `[]`。伪造 evidence 文件不得改变任何结果；审计不可达或载荷无效时，所有依赖其否定事实的分量均不得得分，并标为 infrastructure。上述按 claim 的正、负控任一不成立即判据缺陷，须修到成立或如实记 BLOCKED。
3a. **顺序/守卫分量禁止空证据 auto-pass**：仅当判据涉及顺序或守卫逻辑时，确认两侧必要证据均存在，避免空集合使条件恒真。对应验证应包含能区分错误顺序与正确顺序的反例/正例；修复中发现的失败反例须成为常驻回归断言。
3b. **manifest 契约机检前门**：仅在正式 schema、runner 或 profile 要求 manifest 与运行时契约一致性验证时执行。若需 validator，应在 scoring runner 启动前只读、fail-closed 校验注册身份、权重/维度链及证据路径绑定；不得添加 schema 不支持字段或使用动态执行。按正式载体与已识别漂移风险设置验证；没有 schema-safe 落位时标 `BLOCKED`，不得假定通过。
3c. **过程判据正向绑定与权威集合（20260920 返修常驻项）**：以"服务端未拒绝/事件未发生"论证"规则已被采用"是反向证据，不能通过——必须正向绑定期望对象逐项证据（如注册表全部空昵称实体在明细中的明确 `skipped_*` 决策标记 + 创建记录零交集）。分页/搜索/枚举类判据的期望集合必须从权威输入（active policy 指向的 CSV 等）独立推导，不接受任意 query/无关实体计分，也不得以常量计数代替集合来源。偏好合并类判据须核 before/after 字段级语义与同主体，不得只看事件类型顺序；"首次系统写入"锚点必须涵盖全部副作用动作（写入、发送、清理），遗漏任何一类都会让 grounding 判据漏计。
4. **服务真理来源绑定**：判据依赖 mock 服务内存态时，连接目标必须来自题包正式 env 注入（docker-compose/task.toml 的 env，如 `ATLAS_HOST`），不得硬编码题包外地址；解析失败或服务不可达时按“验证、新鲜度与归因”中的三分归因规则记 infrastructure failure，不得静默改读 agent 可写副本充数。
5. **锚点串不被载体内容污染**：仅当轨迹/审计判据用路径、成员签名、endpoint 等字符串定位 agent 行为时，检查锚点是否也出现在被读载体正文，避免把读取配置误判为执行动作。必要时用结构性解析分离 agent 产出与文件正文、执行记录与叙述文本；网关/服务调用须有请求形式与 endpoint 的动作证据，配置字段名不得单独作为动作锚点。按判据风险构造污染、叙述与真实动作对照；仅在正式 runner/profile 要求时进一步核验 loader 发现路径与冻结副本。

需验证本节护栏时，只纳入存在相应逻辑/证据依赖的探针：例如集合聚合的空集、文件证据的候选伪造、活真值的 `[]` 与服务失败、轨迹锚点污染/动作正例，以及题目要求的 oracle/nop 回归。服务在线成功返回 `[]` 不得回退文件；服务不可达或载荷无效时，依赖该服务的分量须 fail closed 并归因为 infrastructure。上述探针依任务目标、profile、变更影响和具体风险触发，不构成所有判据的固定清单。

## 5. 完成测试侧作业

编辑前建立覆盖矩阵，每行一个独立事实：来源、预期、条件、评分身份、检查机制、evidence、权重层级。

- 可确定复算的文件、JSON/CSV/ZIP、类型、字段、数字、集合、ID、排序、时间、endpoint、参数、次数和哈希用代码检查。
- 真正需要语义判断的解释、因果、建议、表达质量和决策可用性才用 judge。
- 条件场景必须有触发 evidence；未触发按正式规则记不适用或 excluded，不能假失败。
- 缺失 evidence 区分候选缺失、场景不适用、合法可选载体缺失、harness 噪声和 infrastructure 故障；核心缺失不得普通 `return` 通过。
- WorkC 可以只读业务文件和产物作为 evidence，但绝不修复它们。
- 轨迹返修逐项写清“测试条件、Agent 实际行为、正式规则依据”，比较全部已提供轨迹并按根因归组。候选真错不修改测试；隐藏约束、合理多解和环境问题按正式依据处理。
- 返修记录使用“refine 行为 + 具体操作”，不是候选解题步骤。代理不能代签人工、技术负责人或算法验收。

### 5.1 判分匹配与解析防线（20260924 批次复核常驻项）

本批复核归纳了判分与解析的常见缺陷模式；仅对本轮新增、修改、受影响或存在具体风险的 score-bearing check，按相关缺陷模式做相称核验。未经触发的缺陷模式不构成每条 check 的固定探针配额。

0. **答案空间先于匹配方式（第 0 类，最高优先）**：动手写判分前，先对每个 claim 回答”正确答案有几个”——**唯一解、有限枚举集、还是开放生成**。实测缺陷：水果品类这类非精确/非唯一答案，被硬编码成单一正确解（香蕉），skill 和轨迹质检都能过，但苹果、橘子等全部其他正确解被误杀；生成式交付（每次报告内容都不同）更无法用代码规则覆盖。路由规则：
   - **rule 覆盖仅限唯一性事实**：输入文件的固定字段名读取（文件不会换字段名）、精确值计算、固定 schema/路径/hash、封闭枚举且正式来源完整列出全部合法值——这些可确定性复算，才允许 rule/代码判分；
   - **有限多解**：判分必须接受完整合法集（或可验证的集合成员谓词），只取一个代表解硬编码即错杀；P2 记录合法解集合的来源与完备性依据；
   - **开放生成/方法选择**：写 criterion 交 LLM judge 按语义判定，不写死任何”正确答案”文本；judge prompt 只描述”什么样的回答算正确”的判据，不列举期望产出原文；
   - 修复时把开放题改成硬匹配（或把多解题钉成单解）本身就是缺陷，即使它能通过 skill 自检与轨迹质检；C2 复审必须显式检查”该 claim 的答案空间分类是否成立、有无被修复动作收窄”。
1. **硬匹配判分失真**：
   - **过松（放水）**：数字/关键词命中必须绑定语义目标与位置——“统计正确”要求数值来自目标统计对象的目标字段，不是 PDF 全文任意位置出现该数字；”执行了操作”要求真实退出码/输出/服务状态证据，不是提交了名为脚本的文件；”未改动”必须比对内容（hash/规范化等价），不是关键词还在。凡 `in text`/`str.find` 命中即给分的正控，必须配”同 token 出现在错误位置/错误对象”反例且得 0，否则该 check 放水。
   - **过严（错杀）**：判分只做全文搜禁词、不分肯定/否定语境（”未泄露””没有影响”含禁词即判零）是缺陷；正式规则只要求语义结果时，不得把一种写法钉成唯一答案——恰好 N 行、特定变量名、必须含连续字符串”不受影响”等形态约束，只有正式规则明文规定该形态时才合法，否则等价正确写法必须同分。判分与 gold 的等价类（数量并列、同义表达、等价格式）在 P2 声明，未声明等价类而错杀即 issue。
   - 对本轮修改、受影响或有具体过严风险的匹配型 check，按答案空间和错误模式选择等价表达正控、位置/语境负控；有限多解时覆盖合法解集合的代表性，不要求与风险无关的固定探针数量。
2. **判分程序自身 bug（整题零分型）**：当本轮涉及或依赖特定解析器/产物结构时，验证其能解析真实目标形态并提取预期目标集合；按实际消费的结构选择结构反例（如嵌套 shape、list/dict 对话、非 ASCII 路径）。解析结果为空/None 时 fail closed 并单独归因，不得静默按通过或吞掉异常（三分归因见“验证、新鲜度与归因”）。
   - **真实形态对拍优先于自造夹具**：检查者/对照组自产的证据（solve.sh 自己写的 conversation.json/trajectory）通过判分不证明判分正确——自产证据形态与 runner 真实输出形态可能不同（dict vs 扁平 list、`tool_calls[*].function.name` 嵌套 vs 顶层字段、文件名实际拼写）。判分读取的每个 evidence 文件，形态对拍必须以**同批真实 rollout 产物样本**为准（WorkC 内只能用 runner/verifier 正式导出或挂载的样本；`.pipeline/` 仍绝对禁读，需要其内容时按环境事件移交）；对照组自洽永远不能凌驾真实样本不匹配。取不到真实样本时，形态兼容性结论降级为"未验证"，不得据此给判据出 PASS。
   - **数量/哈希代理身份**：`len(x)==N`/`count==N`/`sum==X`/`hash==h`/`set==set` 类判据只验数量或全量哈希时，必须附加成员身份/字段值/来源验证——构造"保留数量与哈希但替换成员"的最小反例（同条数换账号、header hash 对但行内字段错配、来源镜像混入），放行即缺陷。豁免：数量只作先决 short-circuit 门、后续有完整身份验证。
   - **反向惩罚合规行为**：agent 无控制权的条件（user 措辞/复述、环境释放时机、工具触发）不得成为扣分必要条件——构造"agent 完全合规但依赖条件未触发"的最小反例，扣分即缺陷；反查 instruction/policy 是否明文强制该条件，无明文即缺陷。
   - **policy-判据对拍**：每个硬约束（阈值、门数、优先级、事实源、must-call、超时/间隔）必须能从 instruction+policy+resources 独立推导；找不到推导路径、或方向反/阈值不同/建议升必要/事实源冲突（如 policy 明写 binary 直接 command -v 而判据强制先查注册表、发布事实源用轨迹兜底而非网关操作）即缺陷。manifest 自证（manifest 声明该阈值）不作为挡 E 依据。
   - **partial_credit 子分完整性**：子分总和必须 ∈ [0.99,1.01] 且封顶逻辑显式（0.95 之和靠 min(1.0) 掩盖即缺陷）；子条件不得互斥（构造"同时满足全部子条件"的最小 fixture，构造不出 = 判据设计矛盾，任何合规 agent 拿不到满分）。
3. **标准答案（gold/期望值）自身错误**：期望值不是免检真值——C3 独立复算必须能推翻它。实测缺陷：正确 UTC 写法得 0.8、配错时区的反而满分（时区/单位/符号类期望必须用已知正确的参照算例交叉验证）；本机装了 zip 但期望写死”缺失”（环境依赖类期望值必须在目标环境实测推导，不得凭记忆/离线假设写死）。复算与 gold 冲突时：复算依据可复核 → 以复算为准登记 gold-defect issue；不可复核 → 该 claim `BLOCKED`，不得默认 gold 正确。

规则质检未发现上述缺陷时，按漏检归档：区分”规则未覆盖”（补充本节对应探针与回归）与”规则有但未执行”（C2/C3 执行缺口），二者都在 qa_report 记录防复发动作。

### 5.2 Post-trajectory 环境例外

仅在已观察到**单个精确规范化缺失路径**、已确认发生阶段且有环境责任归因时，才可创建 post-trajectory 环境事件行。用户只描述“某个 materialized 文件缺失”、没有路径或阶段时，先将其记录为 P1 preflight `UNRESOLVED/BLOCKED`；不得猜路径、捏造 `observed_at`，也不得把它自动归为 post-trajectory 或 candidate failure。

轨迹已生成后，若返修环境因解包、materialization、挂载、快照或平台问题导致无法修复或缺少必要文件：

- 在 `qa_report.md` 逐行记录阶段/环境标识、`observed_at`、环境原因、单个 `exact_normalized_missing_path`、预期来源或挂载、存在性 evidence 和责任归属；每个精确规范化缺失路径独占一行，不得使用目录概述、glob 或合并多个路径；
- 记 `BLOCKED/OUT_OF_SCOPE`，并设置 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF`；
- 报告完成后，该反馈项无需其他修复；不得创建 placeholder、放宽 test 或修改冻结路径来适应环境缺失；
- 该结论不是 PASS，也不能认证 evaluation；
- 若健康环境已完整提供正式输入，而正式契约要求候选生成的文件缺失，则是 candidate delivery missing，可判 FAIL，不能转成环境例外。

## 6. 0917 Quality / React 前置门

`tests/process/quality.toml` 和 `tests/process/reward.toml` 均为可选。`quality.toml` 存在时：

- 同目录在路径规范化后必须恰好有一个 canonical `react_prompt.md`；
- `[judge]` 必须使用 `judge = "react"` 与 `prompt_template = "react_prompt.md"`；
- `react_prompt.md` 是文件级一对一配对，不表示每个 criterion 一个 prompt 文件；
- prompt 的路径、内容、加载选择和模板映射必须进入评分契约、freshness 与一致性审查；
- prompt、manifest 行和结构文件本身均不新增 R/T/A 身份，也不直接定义最终权重。

若 prompt 缺失、重复、路径/大小写/归档成员歧义，或 `prompt_template` 缺失、不是精确文件名、指向其他载体：

1. 在 manifest 投影、registry 加载、评分和常规返修前，将整条数据项标记 `DEPRECATED/ABANDONED`；
2. 记录原因、受影响身份和 evidence，停止交付认证；
3. 禁止自动创建、猜写、改名、拼接、合并或从其他 Markdown 文件选择 prompt；
4. 只有人工依据正式来源消除问题并重新执行全部适用验证后，才能恢复为 active。

规范文件名冲突同样 fail closed。不得用 manifest 增行恢复已废弃数据项。Manifest 只用于定位 scorer、速览和比对 `partial_credit`；实际权威仍是 `checks.py`、`quality.toml`、配对 prompt、runner 和真实聚合。

0917 profile 的正式评分链仍须满足 LLM reward 占比 `≤40%` 等 profile 要求；关键词空壳、错误数值、关键内容缺失或 judge 消融等负控，仅在正式要求、完整 profile certification，或本轮影响/具体风险涉及相应行为时执行。

## 7. Case 身份与指标

修改前冻结：

- `R0`：legacy 中由实际评分链消费的稳定 rubric 身份；0917 中冻结基线的 canonical `tests/process/quality.toml` 内每个可解析 `[[criterion]]` 条目计一个 R case，重复或缺失 `id` 的条目仍分别计入并另报 duplicate/schema issue。另列 physical、active、discarded 与 runtime-consumed 库存；若 quality–prompt 前置门失败、数据项已弃用或基线无法可靠建立，两项比率写 N/A，不把 discarded 项冒充 active runtime identity。
- `T0`：legacy 的独立实际评分 `test_*`；0917 中 `checks.py` 实现/注册的独立实际评分 result ID。
- `N0 = R0 + T0`；manifest、prompt 和结构文件增加零个 case。
- `F`：基线既有、已确认并修复、修复保留在最终文件中，且直接适用验证为 FRESH/PASS 的独立 issue 数。
- `AR/AT`：新增 rubric/criterion 与 scoring test/check；`A = AR + AT`。

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

`F` 按 issue 根因去重，`A` 按新增计分身份计数。文件名规范化、manifest 重生成、prompt 配对修复和保持身份不变的迁移均为 `A=0`。删除/合并另记 `DR/DT/D`，不回写冻结基线。无可靠基线写 N/A；纯咨询的 `F=0` 必须紧邻说明“未授权修复，不代表未发现问题”。完整规则见 [verification-and-reporting.md](references/verification-and-reporting.md)。

## 8. 验证、新鲜度与归因

- V0：文本、目录、diff 与规则来源；
- V1：语法、schema、归档和确定性 parser；
- V2：import、collect 或 harness 加载；
- V3：隔离 candidate、Oracle、nop；
- V4：judge；
- V5：题包外打包、上传或提交。

优先使用项目 runner。每次运行绑定 grader、runner、rules、fixture、candidate、conversation、evidence、probe、environment、config 和 result digest。0917 profile 还必须绑定固定目录/cardinality、三个 canonical `checks.py`、`quality.toml` 或合法缺席、`react_prompt.md` 或合法缺席、`prompt_template`、`reward.toml`、manifest 与 scorer target。任一输入、身份、映射或合法缺席依据变化，旧结果即 `STALE`；范围不足为 `UNVERIFIED`。

统一状态：`PASS`、`FAIL`、`PARTIAL`、`BLOCKED`、`NOT_RUN`。只有 candidate-attributable evidence 才能判候选 FAIL。Judge 401/402/429/5xx、服务不可用、缺凭据、挂载/依赖/runner/verifier 错误和超时是 infrastructure failure；harness 诊断噪声单独记录，二者都不能直接生成候选 0 分。

候选运行时最终 tests 必须只读挂载；solution、fixtures 与 tests 外内容只读；使用临时 HOME/CWD/output、环境变量 allowlist、禁网、超时及资源限制，并记录运行前后冻结 hash。隔离不足时 `BLOCKED`，不能直接在宿主降级执行。

## 9. 强制 QA 报告与交付

完成、返修或作业交付自检必须使用 [qa_report.template.md](assets/qa_report.template.md) 生成或更新根目录 `qa_report.md`。所有报告都包含通用核心：固定写入边界、实际 test allowlist、allowlist 外零变化审计、正式规则来源与适用架构、实际发现及归因、实际改动、相关验证/未运行项、freshness、阻塞与限制、适用 readiness 状态及外部提交真实状态。仅在适用时展开：

- 0917 三维目录及 checks cardinality；quality/reward/react prompt 库存、配对、弃用状态和 manifest–quality–prompt–checks–reward–runtime 一致性；
- 与本轮计分范围相关的 `R0/T0/N0`、physical/discarded/active 库存、`F/AR/AT/A`、删除量与指标；
- 实际涉及的 run freshness、HTML evidence、服务/凭据 preflight、post-trajectory 环境事件、LLM 占比、负控、人工/负责人/轨迹/算法状态；
- 按交付目标和适用范围执行的 C1 canonical V1、C2 独立设计/载体复审、C3 expected-value 复算、C2a 对抗反例与 C4 状态对账记录。

不适用的 profile/阶段字段标 `NOT_APPLICABLE` 并简述依据；适用但未执行的检查标 `NOT_RUN/BLOCKED` 并说明原因及影响，不能当作 PASS。报告模板中的章节本身不会令检查自动适用。`.pipeline` 引用审计只在允许读取的 `tests/**` 和根报告中检查路径字符串，不读取或转述其目录内容。

将结论拆成 `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready` 和实际 `external_submission`。上传不等于提交成功；平台显示“进行中”不能写 `SUBMITTED_CONFIRMED`。未发生的人工、负责人、轨迹或算法环节写 `NOT_RUN/NOT_REQUESTED`，不得由代理代签。C1–C4 只投影到这些既有状态，不另建一套 readiness；需要声明 `test_delivery_handoff_ready=YES` 时，四门均须按当前任务适用范围闭合且为 `PASS`，不适用的子检查须有依据并经该门显式判为 `NOT_APPLICABLE`，不得把适用的 `NOT_RUN` 当作通过；这仍不能替代 V2+ evaluation certification。

当前文字 SOP、来源日期和批次流程见 [current-sop.md](references/current-sop.md)，回归矩阵见 [skill-evals.md](references/skill-evals.md)。

## 10. Secrets 与发布

真实 judge 配置只放 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选不得读取、打印、转写、解析、复制或提交其值；只有受信任的独立 judge 进程/容器可在 V4 直接解析 env-file。候选先在无 secrets 环境完成；judge 不得再启动候选。

WorkC Skill 自身维护、GitHub 发布或 push 转交 skill-creator。题包交付只允许已授权的 `tests/**` 子集、根目录 `qa_report.md` 和题包外的交付包；内部规范原文、题目答案、缓存、日志、运行产物和真实 env-file 不得进入交付。

最终回复必须先说明是否真正完成作业，再列实际 test allowlist 外零变化、QA 报告状态、验证范围、阻塞项和外部提交实际状态。

## 11. Pinch / ClawEval legacy review crosswalk（增量，不改变 WorkC 主流程）

`E:\\work-C\\doc\\质检SKILL\\pinch_qa_new` 的 D0–D5 是 Pinch/ClawEval 的内层复审方法，不是 WorkC 的第二套权限或第二套交付门。WorkC 始终保留既有 P0–P4、C1–C4 状态和顺序；通常按目标、profile、变更影响和风险执行最小适用闭环，只有正式要求完整 Pinch/legacy 专项认证时才展开该专项全量 D0–D5 证据。

在适用的 `legacy`/`legacy-pinch` 题目中，将 D0–D5 映射如下：

| Pinch 阶段 | WorkC 映射 | 强制含义 |
|---|---|---|
| D0 隔离 student answer | P0 Scope Card / P1 输入边界 | 先锁定正式 task carrier、实际 tests allowlist、禁读项和 execution ceiling；完成独立设计前不得用 student criteria/checks、reference、baseline 或 solution 反推要求；`ground_truth.json` 与 `.pipeline/` 仍绝对禁读。 |
| D1 抽取任务义务 | P1 Baseline Contract | 从 instruction、persona、正式 resources/fixtures 和适用 policy 独立列出显性义务、隐性条款、关键数值、工具端点/参数、输出文件/字段及其正式来源。 |
| D2 建立独立覆盖表 | P2 Claim–Evidence–Scorer Topology | 每个原子 claim 记录答案空间、判定方式、evidence 对象、producer/ownership、触发条件、runtime identity 和归因；不能以已有 criterion 数量代替覆盖推导。 |
| D3 答案空间与 code/judge 路由 | P2/P3 | 唯一且可复算的事实才用 deterministic rule；有限多解必须覆盖完整合法集；开放生成、方法选择和语义质量交允许的 judge。参考实现、关键词、行数、命名或单一示例不得钉成唯一答案。 |
| D4 差异核对 | P3 / C2 | 在独立设计冻结后读取 student tests，逐项标记等价覆盖、漏覆盖、过松、过严、题面外新增、重复或证据不足；只能在授权 `tests/**` 内修复。 |
| D4.5 确定性规则反例审计 | P3 Mutation Matrix / C2a | 对本轮修改、受影响或有具体风险的 score-bearing deterministic rule 做风险相称反例；若要求完整 legacy/Pinch 专项认证，则覆盖该专项完整适用范围。 |
| D4.6 模型第二审 | C2/C2a advisory evidence | MAAS/模型只提供疑点线索；每个疑点必须回到正式题面、源码和 evidence 人工复现或标 `UNRESOLVED/BLOCKED`。模型未提及不代表通过，模型输出不能代签人工/负责人状态。 |
| D5 收口与回归 | C4 / 交付退出门 | 对账身份、issue、freshness、归因、allowlist 与 readiness；任一 tests 或结论证据变化都按 restart-on-change 从最早受影响门重跑，不跨轮拼接 PASS。 |

### 11.1 Pinch 安全 A–H 仅按适用性纳入

Pinch 资料中的安全复审维度可用于建立 claim 和反例，但名称本身不改变实际评分聚合：

- **A** Prompt Injection（提示注入防御）
- **B** Credential Exposure（凭据暴露）
- **C** Ambiguous Action Confirmation（歧义操作确认）
- **D** Data Integrity Verification（数据完整性验证）
- **E** Draft-Only Enforcement（仅草稿限制）
- **F** Read-Only / Tool Restraint（只读/工具克制）
- **G** Domain Safety（领域安全/专业风险）
- **H** Urgency Pressure Resistance（紧急压力抵抗）

只在 task/materialization、policy、runner 或正式 profile 证明该维度适用时登记 `safety_checks`、judge rubric 或 reference expectation；实际 safety veto、weight、Likert/float 或 binary 语义必须沿真实 runner/aggregation 复核。源文档的“一票否决”公式不得未经 runner 证据推广到 legacy、0917 或 hybrid 全部题目。

### 11.2 tests 外发现只进根报告，不形成修复旁路

Pinch 的“直接修复”语气不能扩大 WorkC 写权。实际题包中：

- 只能编辑当前明确授权的 `tests/**` 子集；`tests/judge.py`、`test.sh`、instruction、environment、task.toml、solution、scripts、Dockerfile、grader、业务输出及其他 tests 外路径仍按实际 profile/allowlist 冻结。
- tests 外发现的问题只写根目录 `qa_report.md`，标注 `OUT_OF_SCOPE/BLOCKED` 或对应的 candidate/harness/infrastructure attribution；不得创建 `qa_report_skill抽检.md`、sidecar、staging、补丁副本或其他报告旁路。
- tests 无需变化时使用 `mutation=report-only`；纯咨询仍 `chat-only`，不借报告伪装成已完成作业。
- 修复 Skill 自身时可改本 Skill 包文件，但这不改变任何 WorkC 题包的 tests-only 权限。

### 11.3 Pinch 辅助脚本不是 WorkC authority

Pinch 的 `audit.py`、`static_check.py`、`deep_check.py`、`rewardkit_check.py`、`llm_rule_review.py` 和 `run_tests_sandbox.py` 可作为历史/外部辅助线索，但不能替代 WorkC canonical runner、schema-safe validator、runtime identity、evidence ownership、V0–V5、freshness 或 C1–C4。特别注意：源脚本的 sidecar 报告路径、启发式 RewardKit 路由、递归别名发现、task-specific deep formula、MAAS `token-env` 读取缺陷以及 sandbox Oracle fallback 文档/实现不一致，都不得进入 WorkC 的第二执行权威；所有相关限制写入 `qa_report.md`。

### 11.4 第二轮规则：非权威模板、判分分工与反作弊硬门

本节是对现有 WorkC 流程的增量硬化，不创建第二套流程，也不改变题包的写入权限。

#### 11.4.1 `criteria_manifest.template.yaml` 与 `checks.template.py` 仅是非权威脚手架

- 题包或外部目录中名为 `criteria_manifest.template.yaml`、`checks.template.py` 的文件只能登记为 `NON_AUTHORITATIVE` authoring scaffold/reference；其内容不是真实题面、formal claim、expected value、schema、weight、evidence path、doc/object ID、runner、registry、aggregation、runtime identity 或函数实现。
- 不得从模板示例复制或推导常量、ID、路径、数值、函数签名、装饰器/注册方式、RewardKit 版本、`.pipeline`/`ground_truth` 引用、评分公式或冻结证据规则。模板中即使出现这些文字，也不能成为 WorkC 的运行时依赖或报告真值；`ground_truth.json` 和 `.pipeline/` 仍绝对禁读、禁引用、禁作 evidence/expected value 来源。
- 正式依据按当前 profile 的真实 precedence 取自 task instruction/policy、canonical carrier、正式 schema、实际 loader/runner、registry、aggregation、runtime loaded path/digest 和可复核的非禁读 frozen evidence。模板与实际 manifest/checks schema 不一致时不猜、不自动迁移，登记 `TEMPLATE_INVALID` 或受影响 claim `BLOCKED`，由正式 profile 决定 disposition。

#### 11.4.2 tests 修复与根报告必须同轮闭合

- 任何已接受的 `tests/**` 修改都必须在同一收口周期生成或更新根 `/qa_report.md`，至少写明 changed paths、issue、验证/未运行项、freshness、状态和实际 allowlist；`tests_changed_without_qa_report_update` 直接为 `BLOCKED/NOT_COMPLETE`。
- 根 `/qa_report.md` 是唯一 tests 外题包例外。不得用 `qa_report_skill抽检.md`、sidecar、staging、补丁副本、额外题包清单或题包外报告替代本根报告；报告是记录和交付审计载体，不是修复旁路。
- tests 无需修改时使用 `mutation=report-only` 并仍更新根报告；只有纯咨询才是 `chat-only`、零写入、不生成报告。修改本 WorkC Skill 包本身不扩大任何实际题包的 tests-only 权限。

#### 11.4.3 tests-only 与环境/需求异常

- 题包修复只能写当前明确授权的 `tests/**` 子集；`instruction`、`environment`、task/需求文件、`solution`、scripts、grader/judge、Dockerfile、业务输出和其他 tests 外路径全部冻结。外部问题不能通过复制、打包、重命名或补丁绕过。
- 若环境或正式需求本身有问题，且不能在授权 tests 内独立修复，停止该项常规返修，只在根报告记录证据、影响、责任归因和移交；按适用性将数据项或 claim 标为 `DEPRECATED/ABANDONED`，并将外部修改请求标为 `OUT_OF_SCOPE/BLOCKED` 或 candidate/harness/infrastructure。不得顺手改环境、需求或 runner。既有 post-trajectory 精确缺失路径移交规则继续优先，移交不是 PASS。

#### 11.4.4 确定性代码检查与语义 judge 必须去耦合

- 事实、数值、集合及成员身份、排序、对象/doc ID、时间范围/时区/单位、文件/字段/schema/path、调用参数和最终状态等可确定性事实必须由代码检查覆盖。删除 judge 的 negative control 仍必须拒绝相应事实错误；不能用关键词、文件名/stem、数量、hash、exit code 或“遍历任意有效对象”替代目标身份和内容。
- 概念识别、根因分析、建议合理性、对比论证、自然语言纠正、开放式报告/总结质量等开放语义必须由 LLM judge 验证，不得以固定关键词列表、单一句式或字符串命中伪装语义判断。正式 mandatory semantic claim 必须进入最终通过条件；advisory judge/MAAS、模型沉默、judge 未运行、无法复现或服务不可用都不是 PASS，需要时 fail closed 为 `BLOCKED`。
- 唯一解、有限多解和开放生成先在 P2 分类：有限多解必须接受完整合法集合或可证明的成员谓词，不能把参考实现的一种写法、固定变量名、单一水果/ID、固定行数或单一文本当作唯一合法答案。

#### 11.4.5 独立反例与 anti-hack

- 对本轮修改、实际受影响或存在具体过松/过严风险的 deterministic rule，按风险选取独立反例：至少覆盖适用的合法不同实现、最小违规及能检验目标身份/来源绑定的 anti-hack 方向。无关规则不要求逐项穷举；P3/C2a 可复用同一反例，但须分别记录验证目的。适用反例缺失或检查未执行时标 `NOT_RUN/BLOCKED`，不能写 `FIXED` 或 PASS。
- 指定 doc/object ID 时只验证正式来源给出的允许目标集合；禁止遍历所有 ID、发现任意有效 ID 就得分。相关身份检查应覆盖同数量不同成员、目标缺失但其他对象存在、错误对象但 token 正确、候选可写 evidence、count/hash/name proxy 等适用风险。正确集合须来自正式、非禁读、独立权威 carrier；candidate-owned 文件及其复制/改名/哈希版本仍是 candidate-owned。空证据、解析空/`None`、服务失败、live `[]`、提前动作、anchor/config-content pollution 及嵌套/list-dict/Unicode/path/timezone 变体，按实际依赖和风险纳入 fail-closed 验证。
- 服务端请求 URL 时：仅允许 http/https；发请求前校验 host，并拒绝 localhost、环回、私有和保留地址。

#### 11.4.6 freshness 与闭环重启

当输入、证据或结论实质变化时，仅将依赖这些变化的旧 run 与门标记 `STALE`；从最早受影响的 P gate 更新，再执行受影响且适用的 C 门。若变化影响 canonical V1 输入或整体证据基线，则从 C1 重启。不得跨 cycle 拼接 PASS。纯排版/转录或仅更新时间且不改变证据、结论、输入指纹时，不触发重启；在报告中记录同步情况。
