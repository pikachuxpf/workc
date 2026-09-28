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
→ 更新根目录 qa_report.md
→ C4 QA 平账与状态对账
→ 交付退出门与差异审计
```

开始前固定：

- `target`：`test-delivery` / `test-harness` / `consultation` / `package`；
- `mutation`：`none` / `tests-allowlist-plus-report` / `report-only`；
- `execution-ceiling`：V0 text-only、V1 parser-only、V2 harness-import、V3 candidate-run、V4 judge-run、V5 external-action；
- `delivery`：`chat-only` / `completed-assignment` / `full-package` / `platform-submit`；
- `architecture`：`legacy` / `seal-rewardkit-0917` / `hybrid` / `unresolved`。

候选运行、judge 和外部动作分别需要当前题目与用户授权。完整包只能写到题包外或用户明确指定的外部位置；打包不扩大写权，也不能替代 QA 报告。详细边界见 [routing-and-authority.md](references/routing-and-authority.md)。

当前批次正式指令：评分容器运行 `harbor-rewardkit==0.2.0`，题包须统一适配并精确固定到该版本——0.2.0 与 0.2.1 对"装饰器自动注册后再显式注册"的处理不同，会影响准则数量与权重；`0.2.*` 等前缀写法视为未固定，本地验证与每个 run 都必须标注实际精确版本。规则细节见 [seal-rewardkit.md](references/seal-rewardkit.md) 的"7.0 RewardKit 版本固定"。

### 2.1 P0–P4 Contract Gates（先建契约，后允许返修）

这五个产物可以先保存在工作笔记，并在交付时投影到 `qa_report.md`；不在题包内创建额外清单文件。**没有完成受影响的前置门，不得编辑评分文件；前置门失败时标 `BLOCKED`、`DEPRECATED` 或 `ABANDONED`，不得通过放宽 test、猜测 schema、伪造 evidence 或修改冻结路径绕过。**

| 门 | 编辑/认证前必须形成的最小产物 | 未通过时的处置 |
|---|---|---|
| P0 Scope Card | target、mutation、实际 tests allowlist、V0–V5 上限、delivery、禁读项、动态运行授权与隔离前提 | 超出范围或缺授权：停止该动作；冻结路径问题记 `OUT_OF_SCOPE/BLOCKED` |
| P1 Baseline Contract | 正式载体与 precedence、architecture/真实加载链、canonical 结构、`R0/T0/N0`、runner/聚合、runtime loaded path/digest、冻结输入与 evidence root 的 owner/writeability | identity、结构或 runtime 不能可靠建立：不猜数，指标 `N/A`；不能做 profile-specific 修复 |
| P2 Claim–Evidence–Scorer Topology | 每个 score-bearing identity 的 formal claim、触发条件、权威真值源、producer、候选可达/可写性、runtime ID、权重链、fallback 和三分归因 | 正向 claim 没有可信真值源、service 可达性或唯一 authority：该 claim `BLOCKED`，不能由候选日志/自述补足 |
| P3 Invariant / Mutation Matrix | 受影响不变量、最小正反例、伪造/空集/服务失败等适用控制及其 expected result | 控制缺失、空集自证或 evidence 可伪造：不能标 FIXED 或认证 |
| P4 Change-Impact / Freshness Ledger | 每次改动→受影响 claim、identity、validator、control、aggregation、必跑 run；所有引用 run 的 digest 与 freshness | 任一适用 run 旧、范围不足或来自不同环境拼接：`STALE/UNVERIFIED`，不能认证 |

P1 不是只记录一个总 hash：它必须足以重建“什么在运行、什么在计分、谁生产证据、候选能否改写”。正式 source 版本变化时新建 revision baseline，不覆盖旧基线。P2 的 evidence 只有三类：**verifier/authority-owned**（可建立真值）、**candidate-owned**（只能证明候选行为）、**infrastructure-owned**（不可用时归 infrastructure）。候选可写路径即使被 verifier 复制、重命名或加 hash，也不会变成独立真值。

P3 的不变量按受影响面选择，不要求盲跑大而无关的全量套件：范围隔离、source authority、topology/weight closure、正向非空性、live service 无回退、双模式 trajectory、锚点污染、归因和 report freshness 是常见集合。发现的每个 tests-side 缺陷在关闭前必须晋升为常驻回归：保留最小反例、正例、预期、issue ID、run ID 和 freshness；确实无法构造时维持 `BLOCKED`，不得写 `FIXED`。

P4 的 `FRESH` 只在全部会影响结论的输入、runtime loaded path/digest 和 run scope 一致时成立。不得把不同 run 的局部 PASS 拼成完整认证。若 P0–P4 的强制行不完整，范围与报告可以支持 `test_delivery_handoff_ready`，但 `evaluation_certified` 必须为 `NO/BLOCKED`。

### 2.2 C1–C4 交付闭环（冻结差异后再认证）

P0–P4 约束返修过程；C1–C4 负责在最终差异冻结后发现遗漏、陈旧结果和报告自相矛盾。它们只消费现有正式载体、validator、回归和报告，不新增写权、评分身份、隐藏真值权限、固定 canary、全局 RewardKit 版本或第二份 QA 报告。详细算法见 [pre-delivery-qa-fusion.md](references/pre-delivery-qa-fusion.md)。

| 门 | 必须闭合的交付事实 | 失败/变更后的处置 |
|---|---|---|
| C1 Canonical V1 Hard Gate | 从真实 runner/validators/self-tests 识别唯一 canonical V1 入口；覆盖适用 schema/TOML/YAML、identity、mapping、aggregation、carrier/path 和 fail-closed drift controls；命令、输入 digest、RC、输出与 scope 可复核 | 无唯一入口、局部脚本拼接、validator 未实际阻断或任一项失败：V1 不通过，不得把局部 PASS 写成 tests-side 完整自检 |
| C2 Independent Design / Carrier Re-audit | 由未参与当前修复的独立 reviewer 从正式 claim 重新审查 score identity、正反条件、authority/producer/writeability、source carrier 清单、manifest/runtime closure 与遗漏角度；只读复审且不继承“已修复”结论 | 发现新 defect 或载体/claim 漏项：登记 issue，回到受影响的 P1–P4 修复；最终差异改变后此前 C1–C4 全部 `STALE` 并从 C1 重启 |
| C3 Independent Expected-value Recalculation | 对 checks 常量、manifest/quality 文本、边界值、集合、计数、权重与总 reward，从正式非禁读载体独立复算并与实现、报告三方比对；无法独立推导写 `BLOCKED/N/A` | 不一致不能用 Oracle/GT/judge 分数覆盖；修复后重跑 C1、C2、C3，所有引用旧 digest 的结果失效 |
| C4 QA Accounting / Status Reconciliation | 机械核对 `R0/T0/N0`、`F/AR/AT/A/DR/DT/D`、issue 状态、run freshness、三分归因、C1–C3、allowlist diff 与四个交付状态；结论只由底层证据派生 | 任一计数、issue、run、blocker 或状态矛盾：报告不闭合；只降级受影响结论，不以多数通过或摘要覆盖底层 evidence |

独立 reviewer 可以是未参与当前修复的子代理或人员，但其结果不等于 `human_review_status` 或 `technical_lead_review_status`。修改后必须“重启闭环”，不能只补跑失败项后与旧 PASS 跨 run 拼接。

#### Schema-safe manifest / validator placement

当前任务正式 schema 与实际 runner 优先于历史示例。只有正式 schema 明示允许扩展时，才能向 `criteria_manifest.yaml` 添加 evidence registry 或 validator metadata；**不得为了满足 WorkC 抽象要求添加未知顶层字段。**若 schema 不允许或 runner 不加载该位置，registry/validator 必须位于 runner 已批准、不会被自动发现为 scoring module 的 tests-side 位置，或由不可变 harness 提供。找不到合法位置即 `BLOCKED`。无论落位何处，validator 必须在 scoring runner 前 fail-closed 执行，记录路径、digest、启动命令及至少两项漂移负控结果。

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
9. **双模式轨迹解析（常驻）**：轨迹判据必须同时接受 solution 模式与 agent 模式两种证据形态——solution 模式常带 process-events.json 紧凑轨迹或自带 `{action,target}` 参数的 ATIF；agent 模式只有真实会话导出的 ATIF，tool_calls 仅携带 `function_name` 与 provider 形态参数（如 `file_path/path/url/command/code`），永远没有 `{action,target}` 键。只读 `args.action/args.target` 或匹配 solution 专有动作令牌（如 `cleanup_after_confirmed`）的判据在 agent 模式下恒 False/漏计。凡 manifest 行 evidence 含 `trajectory` 的判据，交付前必须用 agent 形态的合成 ATIF 夹具跑过解析断言；清理/落点类动作优先以工作区终态（policy active naming 声明的路径存在性）为模式无关证据，叙事令牌只能作辅助。仅用 oracle 轨迹验证的轨迹判据视为 UNVERIFIED。
10. **权重单一口径（常驻）**：先从已验证的实际 RewardKit/runner 版本、加载路径与 runtime result 确认逐项 weight 语义，再要求 manifest/索引投影与运行时单条评分单元一致；例如仅在已验证为 rewardkit 0.2 对应行为时，deterministic 行映射 checks.py 注册权重、judge criterion 行映射 quality.toml `[[criterion]].weight`，缺省 1.0 并按实际维度规则归一。桶级（`$checks`/quality）与维度级权重按当前 runner/reward.toml 的真实层级处理，禁止把归一化值或上层权重泄漏进行内。版本或封装不同时必须通过 runtime discovery 重建映射，不能套用 0.2 或历史示例。跨层混用多套口径会使"行和恰为 1"的错误校验自洽通过——核对时必须沿 criterion→bucket→dimension→reward 真实链逐层复算，并逐行与运行时注册权重比对，不做聚合和校验替代。

`ground_truth.json` 的禁读规则继续优先。两个正式载体无法消解时，只阻断受影响 claim。

### 4.1 判据自证与空集护栏（常驻，20260920 批次起）

每条确定性判据交付前逐项过完这组检查，任何一条不满足即视为判据缺陷：

1. **空证据集不得自证**：正向、序列、完成度或过程型谓词含 `all(...)`、`any(...)`、`sum(checks)` 时，必须先回答“集合为空时结果是什么”。凡空集能使分数非 0 或直接满分（如 `all(x in eps for x in business if x in eps)` 在无任何业务调用时恒真），必须显式前置“关键证据存在”门（核心动作集合非空、目标文件可解析等），否则 0.0。空集通过 = 判据为空壳，与关键词空壳同罪。**例外只能是正式规则本身为负向安全事实**（如“未调用禁调 endpoint”）：此时服务可用且权威审计明确返回空 list 可以证明未发生该动作；服务不可达/载荷无效不是空 list，绝不可借此给分。
2. **判据证据不可由被评者写就**：沿生产者链核对每个 evidence 文件——谁创建、挂在哪个卷、agent 进程是否持写权。agent 可写卷（如 `/logs/agent/**`、`/tmp`）上的文件只能作 candidate-attributable 行为证据，不得作为判据真值来源；verifier 侧“复制/改名/算哈希”不改变来源可伪造性。修复方向按优先级：服务进程内查询端点（例如 `/v1/audit`）且其**底层审计状态也必须由服务/verifier 持有，候选不能通过其他 endpoint、共享卷或挂载修改、删除或回滚** > 挂载在 verifier 侧、agent 无路径可达的副本 > 原则上不用（见下）。仅 GET/“只读”路由本身不是 authority 证明，P2 必须核验 producer、backing state、候选 reachability 与 mutation path。一旦采用服务活真值，**禁止任何文件回退**：成功响应（含空列表，即真实 nop 状态）必须原样当真返回——把合法“空真值”误判为服务不可用而回退读文件，等价于给伪造证据留门（20260920 返修实测缺陷）；连接失败/超时/无效载荷一律 fail closed（判据按缺证据记 0，基础设施归因交 runner/报告），不得改读任何 agent 可及副本。行形状校验（int `seq` + str `ts` 之类的“生产者盖章”）不构成担保——这些字段同样可被伪造，只许作纵深防御，禁止作 fallback 准入条件。禁调/完整性类负向判据（如 forbidden-call purity）优先“读活真值”而非“文件里没出现坏行”，避免判据逻辑向 agent 泄漏。
3. **正控与负控判定**：验证预期必须匹配 claim，而非机械要求 oracle 满分或 nop 为 0（WorkC 总则：Oracle 不必为 1，nop 不必为 0）。正向过程/完成度 claim 在没有必要的肯定性证据时须为 0；负向安全 claim 可在**可达且格式有效的权威 live audit**明确显示无违例时合规，即使该 audit 为 `[]`。伪造 evidence 文件不得改变任何结果；审计不可达或载荷无效时，所有依赖其否定事实的分量均不得得分，并标为 infrastructure。上述按 claim 的正、负控任一不成立即判据缺陷，须修到成立或如实记 BLOCKED。
3a. **顺序/守卫分量禁止空证据 auto-pass（20260920 返修常驻项）**：形如 `not (sends and cleans) or cleans[-1]>sends[-1]` 的空集合守卫在动作缺席时恒真——模式专属令牌（如 solution-only 的 `cleanup_after_confirmed`）在另一模式下不被解析时，`sends`/`cleans` 均为空，守卫放行，把"无顺序证据"当"顺序正确"（实测：premature cleanup 先删 pending 再取得成功回执仍得满分）。顺序分量必须要求两侧证据同现（`bool(a) and bool(b) and a[-1]>b[-1]`）；反例夹具必须含 premature 顺序（先清理后确认）与正例（确认后清理）各一条，只测正例测不出 vacuous truth。每次返修判据后，上轮失败反例必须转为常驻回归断言。
3b. **manifest 契约机检前门（常驻）**：当前正式 schema 明示支持时，manifest 顶层应声明 `evidence_sources` 注册表，行内 evidence 只能引用已注册源；schema 不支持扩展时，必须在 runner 已批准、不会被自动 discover 为 scoring module 的 tests-side 位置，或不可变 harness，提供等价 registry。两种落位都要在 scoring runner 启动前执行只读 mapping validator（fail-closed，非零退出终止评分，置于 test.sh 内 `rewardkit` 之前），至少校验：angle_id/注册身份 1:1（无 orphan/ghost/重复注册）、逐行 weight==运行时 Score.weight、维度/桶/root 权重链、checks.py 默认证据路径与 runner 冻结目标三方一致。没有 schema-safe 落位即 `BLOCKED`，不得添加未知 YAML 字段。validator 零第三方依赖（官方镜像可能无 PyYAML，需内置确定性子集解析器或逐行正则），加载 checks 模块用 importlib 固定路径、禁止 eval/exec 动态执行。validator 自身须附两类漂移负控（改一个行权重、改一个未声明 evidence 名）证明其真的会失败。
3c. **过程判据正向绑定与权威集合（20260920 返修常驻项）**：以"服务端未拒绝/事件未发生"论证"规则已被采用"是反向证据，不能通过——必须正向绑定期望对象逐项证据（如注册表全部空昵称实体在明细中的明确 `skipped_*` 决策标记 + 创建记录零交集）。分页/搜索/枚举类判据的期望集合必须从权威输入（active policy 指向的 CSV 等）独立推导，不接受任意 query/无关实体计分，也不得以常量计数代替集合来源。偏好合并类判据须核 before/after 字段级语义与同主体，不得只看事件类型顺序；"首次系统写入"锚点必须涵盖全部副作用动作（写入、发送、清理），遗漏任何一类都会让 grounding 判据漏计。
4. **服务真理来源绑定**：判据依赖 mock 服务内存态时，连接目标必须来自题包正式 env 注入（docker-compose/task.toml 的 env，如 `ATLAS_HOST`），不得硬编码题包外地址；解析失败或服务不可达时按“验证、新鲜度与归因”中的三分归因规则记 infrastructure failure，不得静默改读 agent 可写副本充数。
5. **锚点串不被载体内容污染（20260920 返修常驻项）**：轨迹/审计类判据用锚点串（文件路径、成员签名、endpoint 等）定位”agent 做了某事”时，交付前必须反向检索一遍——把每个锚点串在题包业务文件（config、policy、handoff、SKILL、契约 XML 等被读对象）正文里 grep。锚点串若原样出现在被读文件正文里，整段轨迹文本的 `str.find` 子串匹配会”读到配置即误判为真调用”：free-reading 该配置就拿到行动分量（本题 `config/alias-review.yaml` 正文含 `data/registry/existing-handles.yaml`、`format-handoff.yaml` 正文含 `intermediate/source-index-working.docx`、`registry-api.xml` 契约正文含三个 `M:AliasRegistry.*` 成员签名，均属此类）。修复以结构性解析为准，且须同时满足四个子条件：(a) 双栏匹配——锚点只匹配 agent 自身产出文本，与文件正文（工具结果 content、文件体）分栏；(b) 动作通道只含执行记录——command、tool name、工具调用 arguments 可作动作证据，agent 叙述/计划文本（ATIF `message`）不算：叙述里说”我将 POST /v2/search”不是已调用；(c) 网关/服务调用锚点必须”请求形式 + endpoint”同现才算真调用——`NEXUS_HOST`、裸 endpoint 字符串只是配置字段名或路径，单独出现不得作为调用点（配置正文常含二者）；(d) 配置字段名（如 env 变量名）永远不得单独作为动作锚点。确需正文匹配时必须前置”该文件被 agent 主动打开”的独立证据门。验证必含三用例：污染探针（轨迹仅引用正文、零真实动作 → 相关分量全 0）、叙述探针（真实读取 + 叙述宣布调用但无调用记录 → 调用分量 0 且读取分量按实得计）、动作正例（真实执行 → 满分），缺一即验证不闭合。另须源码级确认 runner 发现路径只消费 canonical `checks.py`（如 rewardkit `_discover_group` 单层 `glob(“*.py”)`），编辑工具的 baseline 快照与 `.pipeline` 历史副本不会被任何 loader 加载——残留副本只审计、不依赖，冻结区不改动。

适用验证至少包含：空证据集用例、伪造文件 + 服务在线用例（证伪“改文件得分”）、**活真值为空探针**（服务正常返回空审计 + 磁盘放伪造文件：正向过程/完成度及肯定性安全分量必须为 0；负向安全分量仅可按 live `[]` 与其余正式本地条件得分，绝不可读文件回退）、服务不可达或无效载荷的 fail-closed 用例（伪造文件在场：所有依赖审计的分量为 0，并归因为 infrastructure）、oracle/nop 回归、锚点污染探针与动作正例。

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

本批复核结论：错误点不在轨迹，而在规则本身——“硬规则匹配、固定格式过严、错杀合法等价表达”，即用”要求文本里有没有出现某个字/某个数”验证答案。每个 score-bearing check 交付前按四类自查；无法构造对应正反探针时，该 check 视为未闭合。

0. **答案空间先于匹配方式（第 0 类，最高优先）**：动手写判分前，先对每个 claim 回答”正确答案有几个”——**唯一解、有限枚举集、还是开放生成**。实测缺陷：水果品类这类非精确/非唯一答案，被硬编码成单一正确解（香蕉），skill 和轨迹质检都能过，但苹果、橘子等全部其他正确解被误杀；生成式交付（每次报告内容都不同）更无法用代码规则覆盖。路由规则：
   - **rule 覆盖仅限唯一性事实**：输入文件的固定字段名读取（文件不会换字段名）、精确值计算、固定 schema/路径/hash、封闭枚举且正式来源完整列出全部合法值——这些可确定性复算，才允许 rule/代码判分；
   - **有限多解**：判分必须接受完整合法集（或可验证的集合成员谓词），只取一个代表解硬编码即错杀；P2 记录合法解集合的来源与完备性依据；
   - **开放生成/方法选择**：写 criterion 交 LLM judge 按语义判定，不写死任何”正确答案”文本；judge prompt 只描述”什么样的回答算正确”的判据，不列举期望产出原文；
   - 修复时把开放题改成硬匹配（或把多解题钉成单解）本身就是缺陷，即使它能通过 skill 自检与轨迹质检；C2 复审必须显式检查”该 claim 的答案空间分类是否成立、有无被修复动作收窄”。
1. **硬匹配判分失真**：
   - **过松（放水）**：数字/关键词命中必须绑定语义目标与位置——“统计正确”要求数值来自目标统计对象的目标字段，不是 PDF 全文任意位置出现该数字；”执行了操作”要求真实退出码/输出/服务状态证据，不是提交了名为脚本的文件；”未改动”必须比对内容（hash/规范化等价），不是关键词还在。凡 `in text`/`str.find` 命中即给分的正控，必须配”同 token 出现在错误位置/错误对象”反例且得 0，否则该 check 放水。
   - **过严（错杀）**：判分只做全文搜禁词、不分肯定/否定语境（”未泄露””没有影响”含禁词即判零）是缺陷；正式规则只要求语义结果时，不得把一种写法钉成唯一答案——恰好 N 行、特定变量名、必须含连续字符串”不受影响”等形态约束，只有正式规则明文规定该形态时才合法，否则等价正确写法必须同分。判分与 gold 的等价类（数量并列、同义表达、等价格式）在 P2 声明，未声明等价类而错杀即 issue。
   - 每个匹配型 check 交付前必须跑**等价表达正控**（换一种合规写法应得满分）与**位置/语境负控**（token 在错误位置或否定语境应得 0 分或按规则计分），两个探针缺一即不闭合；有限多解题的等价表达正控必须覆盖至少两个不同的合法解（多解正例夹具），只测代表解测不出单解钉死。
2. **判分程序自身 bug（整题零分型）**：解析器必须对真实产物结构做**双向覆盖断言**——解析成功且提取到非空目标集合。实测缺陷：PPT 解析只遍历最外层 shape、组内文字全漏（必须递归进 group shape）；对话文件是 list 结构却按 dict 读取（必须按实际 JSON 结构分派，list/dict 各自处理）；文件名含非 ASCII/编码漂移导致基线对不上（路径匹配必须规范化编码后比较，不得裸 `==`）。解析器必须配**结构反例**（group 内文字、list 型对话、乱码文件名夹具）；解析结果为空/None 时 fail closed 记 0 并单独归因，不得静默按通过或把异常吞成候选 0 分（三分归因见“验证、新鲜度与归因”）。
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

当前新版要求全部 LLM 评分项的最终有效 reward 占比合计 `≤40%`。沿真实 criterion→group→dimension→reward 链复算；同一项不能因 prompt、quality、manifest 和 runtime 多层出现而重复计权。关键词空壳、错误数值、关键内容缺失及移除全部 judge 的事实检查消融是必需负控；缺授权或隔离时如实记 `BLOCKED/NOT_RUN`。

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

完成、返修或作业交付自检必须使用 [qa_report.template.md](assets/qa_report.template.md) 生成或更新根目录 `qa_report.md`。报告至少包含：

- 固定最大写入边界、实际 test allowlist、allowlist 外零变化审计；
- `.pipeline` 引用审计：work 数据零引用或已删除引用的清单；冻结路径上的残留引用逐条记录；
- 规则、架构与 profile；三维目录及每维 checks cardinality；
- quality/reward/react prompt 库存、配对、弃用状态和 manifest–quality–prompt–checks–reward–runtime 一致性；
- `R0/T0/N0`、physical/discarded/active 库存、manifest/prompt 零计数；
- issue 台账、`F/AR/AT/A`、删除量与两项指标；
- run freshness、HTML evidence 方法、服务/凭据 preflight；
- candidate failure、harness noise、infrastructure failure 三分归因；
- post-trajectory 环境事件、精确缺失路径和 repair disposition；
- LLM 最终有效占比、四类负控、人工/负责人/轨迹/算法状态；
- C1 canonical V1 入口与完整结果、C2 独立设计/载体复审、C3 独立 expected-value 复算、C4 计数/issue/freshness/status 对账及每轮 restart-on-change 记录；
- `.pipeline` 引用审计必须覆盖 `tests/**` 与 `qa_report.md`，只记录零引用或已删除/冻结残留，不读取或转述 `.pipeline/` 内容；
- 差异、阻塞项、限制与外部提交真实状态。

将结论拆成 `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready` 和实际 `external_submission`。上传不等于提交成功；平台显示“进行中”不能写 `SUBMITTED_CONFIRMED`。未发生的人工、负责人、轨迹或算法环节写 `NOT_RUN/NOT_REQUESTED`，不得由代理代签。C1–C4 只投影到这些既有状态，不另建一套 readiness；tests-side handoff 要求四门均 `PASS`，但这仍不能替代 V2+ evaluation certification。

当前文字 SOP、来源日期和批次流程见 [current-sop.md](references/current-sop.md)，回归矩阵见 [skill-evals.md](references/skill-evals.md)。

## 10. Secrets 与发布

真实 judge 配置只放 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选不得读取、打印、转写、解析、复制或提交其值；只有受信任的独立 judge 进程/容器可在 V4 直接解析 env-file。候选先在无 secrets 环境完成；judge 不得再启动候选。

WorkC Skill 自身维护、GitHub 发布或 push 转交 skill-creator。题包交付只允许已授权的 `tests/**` 子集、根目录 `qa_report.md` 和题包外的交付包；内部规范原文、题目答案、缓存、日志、运行产物和真实 env-file 不得进入交付。

最终回复必须先说明是否真正完成作业，再列实际 test allowlist 外零变化、QA 报告状态、验证范围、阻塞项和外部提交实际状态。
