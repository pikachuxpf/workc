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
- **禁止读取题包根目录 `ground_truth.json`**。只有当前题目的正式规则明确授权、已从正式载体独立推导且仅作评分进程外人工交叉检查时例外；任何运行时都不得让 tests、候选或通用 runner 读取它。
- 必须修改 tests 外文件才能解决时，记 `OUT_OF_SCOPE/BLOCKED`，不得顺手修复。
- 纯咨询或明确不修改时可以 chat-only，但必须声明本轮未完成、未返修或未作业交付自检。

测试必须反映正式规则，不能用 Oracle 分数反推规则。Oracle 不必为 1，nop 不必为 0；不得为改善分数删除有效 case、放宽正确条件、篡改真值、伪造 evidence、修改 nop 或掩盖基础设施错误。AI 生成或修改的 criterion、check、expected value、judge 结论和 QA 摘要都必须由人工回到正式规则、原始 evidence 与实际 runner 复核。

维护本 Skill 自身时转入 skill-creator 元流程。本文件不授权修改任何题包外仓库。

## 2. 固定主流程与作业状态

```text
理解题目与正式要求
→ 建立 tests 覆盖基线
→ 修改和优化实际授权的 tests/** 子集
→ 执行适用验证
→ 生成或更新根目录 qa_report.md
→ 差异审计与交付
```

开始前固定：

- `target`：`test-delivery` / `test-harness` / `consultation` / `package`；
- `mutation`：`none` / `tests-allowlist-plus-report` / `report-only`；
- `execution-ceiling`：V0 text-only、V1 parser-only、V2 harness-import、V3 candidate-run、V4 judge-run、V5 external-action；
- `delivery`：`chat-only` / `completed-assignment` / `full-package` / `platform-submit`；
- `architecture`：`legacy` / `seal-rewardkit-0917` / `hybrid` / `unresolved`。

候选运行、judge 和外部动作分别需要当前题目与用户授权。完整包只能写到题包外或用户明确指定的外部位置；打包不扩大写权，也不能替代 QA 报告。详细边界见 [routing-and-authority.md](references/routing-and-authority.md)。

## 3. 架构识别与 profile 分流

文件名只是候选信号，最终沿 `test.sh`、task 配置、import/registry、结果与聚合链确认：

| 信号 | profile | 评分身份 | 处理 |
|---|---|---|---|
| `tests/rubrics.py` + `tests/test_outputs.py` | legacy | 实际评分链消费的稳定 `RUBRIC_*` 与独立评分 `test_*` | 保留旧架构，不机械迁移 |
| `tests/criteria_manifest.yaml` + 三个固定维度目录 | seal-rewardkit-0917 | `quality.toml` 的 active `[[criterion]]` 与 `checks.py` 实际注册 check | 执行 0917 结构和 React 前置门 |
| legacy 与新版链同时被加载 | hybrid | 按各自实际加载链取身份 | 分链审查，不任选一套 |
| manifest 单独存在、结构缺件或加载链不明 | unresolved | manifest 不建立身份 | fail closed，追正式 claim/runner |

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

`ground_truth.json` 的禁读规则继续优先。两个正式载体无法消解时，只阻断受影响 claim。

## 5. 完成测试侧作业

编辑前建立覆盖矩阵，每行一个独立事实：来源、预期、条件、评分身份、检查机制、evidence、权重层级。

- 可确定复算的文件、JSON/CSV/ZIP、类型、字段、数字、集合、ID、排序、时间、endpoint、参数、次数和哈希用代码检查。
- 真正需要语义判断的解释、因果、建议、表达质量和决策可用性才用 judge。
- 条件场景必须有触发 evidence；未触发按正式规则记不适用或 excluded，不能假失败。
- 缺失 evidence 区分候选缺失、场景不适用、合法可选载体缺失、harness 噪声和 infrastructure 故障；核心缺失不得普通 `return` 通过。
- WorkC 可以只读业务文件和产物作为 evidence，但绝不修复它们。
- 轨迹返修逐项写清“测试条件、Agent 实际行为、正式规则依据”，比较全部已提供轨迹并按根因归组。候选真错不修改测试；隐藏约束、合理多解和环境问题按正式依据处理。
- 返修记录使用“refine 行为 + 具体操作”，不是候选解题步骤。代理不能代签人工、技术负责人或算法验收。

### Post-trajectory 环境例外

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
- 规则、架构与 profile；三维目录及每维 checks cardinality；
- quality/reward/react prompt 库存、配对、弃用状态和 manifest–quality–prompt–checks–reward–runtime 一致性；
- `R0/T0/N0`、physical/discarded/active 库存、manifest/prompt 零计数；
- issue 台账、`F/AR/AT/A`、删除量与两项指标；
- run freshness、HTML evidence 方法、服务/凭据 preflight；
- candidate failure、harness noise、infrastructure failure 三分归因；
- post-trajectory 环境事件、精确缺失路径和 repair disposition；
- LLM 最终有效占比、四类负控、人工/负责人/轨迹/算法状态；
- 差异、阻塞项、限制与外部提交真实状态。

将结论拆成 `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready` 和实际 `external_submission`。上传不等于提交成功；平台显示“进行中”不能写 `SUBMITTED_CONFIRMED`。未发生的人工、负责人、轨迹或算法环节写 `NOT_RUN/NOT_REQUESTED`，不得由代理代签。

当前文字 SOP、来源日期和批次流程见 [current-sop.md](references/current-sop.md)，回归矩阵见 [skill-evals.md](references/skill-evals.md)。

## 10. Secrets 与发布

真实 judge 配置只放 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选不得读取、打印、转写、解析、复制或提交其值；只有受信任的独立 judge 进程/容器可在 V4 直接解析 env-file。候选先在无 secrets 环境完成；judge 不得再启动候选。

WorkC Skill 自身维护、GitHub 发布或 push 转交 skill-creator。题包交付只允许已授权的 `tests/**` 子集、根目录 `qa_report.md` 和题包外的交付包；内部规范原文、题目答案、缓存、日志、运行产物和真实 env-file 不得进入交付。

最终回复必须先说明是否真正完成作业，再列实际 test allowlist 外零变化、QA 报告状态、验证范围、阻塞项和外部提交实际状态。
