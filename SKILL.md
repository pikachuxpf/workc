---
name: workc
description: WorkC、ClawEval、PinchBench、Seal 或 RewardKit 单题的测试侧作业完成、返修、作业验证、Oracle/nop、QA 报告与交付流程。只处理这些题包的 tests 侧交付，不承接业务实现或通用质检。题包内最大可写范围固定为 tests/** 与根目录 qa_report.md；完成、返修或作业交付自检必须生成或更新 qa_report.md，其余路径全部冻结。仅在用户明确要求这些题包的测试侧作业，或目录出现 legacy 的 rubrics.py + test_outputs.py、新格式的 quality.toml、checks.py、criteria_manifest.yaml 与对应 runner 信号并明确要求测试侧作业时使用；新格式按正式 claim 独立支持 quality-only、quality + checks 和 checks-only，manifest 单独存在不构成评分身份。
---

# WorkC 测试侧作业内核

## 1. 最高优先级边界

WorkC 只完成题包的测试侧作业，不完成页面、服务、脚本、业务数据、业务报告、业务 ZIP 或 API 状态等业务实现，也不是普通项目的通用质检 Skill。

题包内最大可写集合固定为：

```text
tests/**
/qa_report.md
```

- 实际 test allowlist 只能在 `tests/**` 内继续收窄，不能扩大。
- `qa_report.md` 是完成、返修或作业交付自检 WorkC 作业的强制交付物，即使 tests 无需修改也要生成或更新。
- `tests/**` 和根目录 `qa_report.md` 之外的题包路径全部冻结。用户指令、instruction、materialization、项目配置、复制到副本或打包请求都不能解除此边界。
- **禁止读取题包根目录的 `ground_truth.json`**（硬性要求，见第 5 节）：期望值必须先从正式载体独立推导；无授权读取即按越界处理，已在报告中引用的 GT 内容必须废弃并重新独立推导。
- 纯咨询或用户明确要求不修改时可 chat-only，但必须声明本轮未完成、未返修或未作业交付自检该作业。
- 若任务必须修改 tests 外文件，标为 `OUT_OF_SCOPE/BLOCKED` 并退出 WorkC 写入流程，不得顺手修复。

测试必须反映当前规则，不能用 Oracle 分数反推规则。Oracle 不必为 1，nop 不必为 0；不得为改善分数或比率删除有效 case、放宽正确条件、篡改真值、伪造 evidence、修改 nop 或掩盖基础设施错误。

AI 生成或修改的 rubric/criterion、test/check、expected value、judge 结论和 QA 摘要都必须回到正式规则、原始 evidence 与实际 runner 进行人工复核；Oracle、nop、judge 或 reward 结果不能替代该复核。

维护本 Skill 自身时转入 skill-creator 元流程；本文件不授权修改任何题包外仓库。

## 2. 固定主流程

每道 WorkC 作业都按同一主线推进：

```text
理解题目与正式要求
→ 建立 tests 覆盖基线
→ 修改和优化实际授权的 tests/** 子集
→ 执行适用验证
→ 生成或更新根目录 qa_report.md
→ 差异审计与交付
```

理解题目是为了让 tests 正确覆盖要求，不是为了修改业务实现。QA 报告是测试侧作业完成后的强制收尾交付物，不是独立质检入口。若 tests 已正确，跳过编辑但仍执行适用验证、更新 `qa_report.md` 并完成差异审计；纯咨询不进入这条完成流程。

## 3. 先固定作业状态

开始前记录：

- `target`：`test-delivery` / `test-harness` / `consultation` / `package`；
- `mutation`：`none` / `tests-allowlist-plus-report` / `report-only`；
- `execution-ceiling`：`V0 text-only`、`V1 parser-only`、`V2 harness-import`、`V3 candidate-run`、`V4 judge-run`、`V5 external-action`；
- `delivery`：`chat-only` / `completed-assignment` / `full-package` / `platform-submit`；
- `architecture`：`legacy` / `seal-rewardkit` / `hybrid` / `unresolved`。

纯咨询默认 `mutation=none`、V0、chat-only。要求完成、返修或作业交付自检时，必须规划根目录 `qa_report.md`；若需修复 tests，再把明确授权的 `tests/**` 子集加入实际 allowlist。任何 allowlist 只能收窄固定最大写入集合。

候选运行、judge 和外部动作分别需要当前题目与用户授权。打包只改变 delivery，不扩大写权：完成 `full-package` 交付前必须在本轮生成或更新根目录 `qa_report.md`；tests 未变化时使用 `mutation=report-only`，不得使用 `mutation=none` 或 chat-only 冒充完整包交付。包可以读取冻结文件，但必须写到题包外或明确的外部交付位置，不能在题包内创建 staging、sidecar、临时包或其他文件。

详细边界见 [routing-and-authority.md](references/routing-and-authority.md)。

## 4. 架构识别

文件名只是候选信号，最终以 `test.sh`、task 配置、import/registry、结果与聚合链为准：

| 信号 | 候选架构 | 评分身份 | 实际检查 |
|---|---|---|---|
| `tests/rubrics.py` + `tests/test_outputs.py` | legacy | 唯一稳定 `RUBRIC_*` | 评分 `test_*`、judge、class/tier |
| `tests/**/quality.toml` + `tests/criteria_manifest.yaml`，由 runner 使用；`checks.py` 可有可无 | seal-rewardkit | `quality.toml` 的稳定 `[[criterion]]` | 有 `checks.py` 时统计其实际评分 check；quality-only 时为 0 |
| `tests/**/checks.py` + `tests/criteria_manifest.yaml`，无 `quality.toml`，且 runner 只要求确定性评分 | seal-rewardkit | 无 quality criterion；manifest 不产生身份 | `checks.py` 实现/注册的实际评分 check |
| 仅有 `tests/criteria_manifest.yaml`，或评分链缺件 | unresolved | manifest 不能建立身份，追正式 claim 与 runner | 区分陈旧索引、缺件与未决链路 |
| legacy 与新格式并存或 runner 同时使用 | hybrid | 按当前 runner 分别取身份 | 按实际加载、注册与聚合链处理 |

Seal/RewardKit 新格式中，`tests/**/quality.toml` 定义语义/judge 质量 criterion，`tests/**/checks.py` 定义确定性/程序化 check，`tests/criteria_manifest.yaml` 聚合并摘要当前实际存在的两类评分项。按正式 claim 与 runner，允许 quality-only、quality + checks，也允许只含确定性 `checks.py` 而不含 `quality.toml`；manifest 不是身份权威，任何 manifest 行都增加零个 case。旧式 `rubrics.py` + `test_outputs.py` 仍是受支持的 legacy 输入；只有当前任务正式使用或明确要求新格式时才规范化或迁移，不做普遍迁移。旧式 ClawEval 与输出型 PinchBench 见 [legacy-claw-eval.md](references/legacy-claw-eval.md)；Seal 见 [seal-rewardkit.md](references/seal-rewardkit.md)。不得把旧式文件模型泛化到 Seal，也不得给 Seal 机械补建 `rubrics.py` 或 `test_outputs.py`。

架构识别只决定如何完成 tests 侧作业，不产生业务文件写权。

## 5. Claim 级规则来源

先由 task/materialization 确认正式载体，再把要求拆成原子 claim：

```text
claim_id | source/carrier | source_class | scope | version/date
explicit_precedence | recast | resolution | reason
```

来源可能包括用户请求、instruction、workspace policy、local documents、tool description、fixtures/resources、grader、materialization 和 runner。它们可以决定测试应覆盖什么，但不能把 tests 外路径变为可写。

persona 是被测场景，不自动覆盖政策；tests、solution、旧 QA、历史题和示例默认只是交叉检查材料。

**`ground_truth.json` 硬性禁读**：除输出型 PinchBench 完全忽略它之外，任何架构下 WorkC 默认一律不读取题包根目录的 `ground_truth.json`——不打开、不解析、不引用其内容作为推导输入，也不得让它进入 QA 报告的证据链。tests 的期望值必须先从正式载体（instruction、workspace policy、fixtures、materialization 与 runner 声明的 evidence）独立推导。只有当**当前题目的正式规则明确授权**（例如 Seal 题的 grader 契约把 GT 声明为允许的人工离线交叉检查材料）且已完成独立推导时，才可在评分进程外做人工离线交叉检查，并在 QA 报告中记录授权来源与使用范围。无授权的读取即按越界处理：作废受影响的推导结论并从正式载体重新推导。任何架构都不得让 tests、候选或通用 runner 运行时读取 ground truth。两个正式载体无法消解时，只阻断受影响 claim。

## 6. 基线、冻结与差异

1. 原始 ZIP 或目录保持只读；可在独立副本工作，但副本中的写入边界不变。
2. 修改前记录题目标识、规范化路径、基线 hash、`R0/T0/N0`。
3. 记录实际 test allowlist；完成类作业另固定根目录 `qa_report.md`。
4. 除根目录 `qa_report.md` 这个固定例外外，instruction、persona、fixtures/resources、environment、solution、ground truth、task/materialization、题包根脚本及所有其他 tests 外内容无条件冻结。
5. `tests/**` 内文件也只有进入本轮实际 allowlist 才可修改；冻结 harness 有缺陷时用题包外包装器验证，不擅自扩大 allowlist。
6. 最终差异必须满足：题包内变化仅来自已授权的 `tests/**` 子集与根目录 `qa_report.md`。任何其他变化都阻断交付。

## 7. 完成测试侧作业

编辑前建立覆盖矩阵，每行一个独立事实：来源、预期、条件、评分身份、检查机制、evidence、权重层级。按架构分别闭合：legacy rubric ↔ scoring test；新版 quality criterion ↔ quality manifest row ↔ quality runtime result；deterministic check ↔ deterministic manifest row ↔ check runtime result。quality 与 deterministic 链按正式 claim/runner 独立存在，不要求互相成对；同一业务事实只能计权一次。

- 可确定复算的文件、JSON/CSV/ZIP、类型、字段、数字、集合、ID、排序、时间、endpoint、参数、次数和哈希用代码检查；
- 真正需要语义判断的澄清、解释、因果、建议、冲突识别与表达质量才用 judge；
- 条件场景必须看到用户侧触发 evidence；未触发按正式规则记不适用或自动通过；
- 缺失 evidence 要区分候选缺失、场景不适用、可选载体缺失与 harness/infrastructure 故障；核心缺失不得普通 `return` 通过；
- WorkC 可以只读业务文件和产物作为 evidence，但绝不修复它们；
- 修改只发生在实际授权的 `tests/**` 子集；每轮完成、返修或作业交付自检都同步生成或更新根目录 `qa_report.md`。
- 对 Seal/RewardKit 先按评分单元盘点 `quality.toml`、`checks.py`、manifest 投影和 runner 注册，再决定修 criterion、修 check、规范化单一文件别名或重建 manifest；不得用 manifest 补行替代真实评分身份。

## 8. Seal / RewardKit 新格式

按评分单元核对 `quality.toml`、`checks.py`、`criteria_manifest.yaml` 与当前 runner：

- `quality.toml` 定义语义/judge 质量标准；`checks.py` 定义确定性/程序化检查；`criteria_manifest.yaml` 聚合并摘要两者。
- 文件名严格使用小写 `quality.toml`。仅在可写的完成/返修模式、且文件位于实际 tests allowlist 内时，自动把一个语义明确的替代 TOML 质量文件名或大小写变体规范化为 `quality.toml`。目标已存在或多个别名冲突时，不覆盖、不合并，标记 `BLOCKED`；咨询模式只报告，不改名。
- 缺失 `quality.toml` 仅可在正式当前 claim 或 runner 要求该评分单元承载语义/judge criterion、且可从权威来源推导内容时创建。不得创建空文件或占位文件，也不得要求每个 dimension/check 目录都有它；只有确定性 `checks.py` 而无 `quality.toml` 是合法形态。
- 常见文档 schema 为：`[judge]` 下 `judge`、`files`、`atif-trajectory`、`mode`、`timeout`；重复 `[[criterion]]` 下 `name`、`id`、`description`、`type`、`points`、`weight`；`[scoring]` 下 `aggregation`。实际任务 schema 与 runner 优先。连字符键 `atif-trajectory` 必须按 TOML 使用有效裸键或引号键；不包含 canary 注释。
- `criteria_manifest.yaml` 常见顶层字段为 `version`、`score_range`、`dimensions`、`criteria`；criteria 行常见字段为 `angle_id`、`angle`、`rule_hint`、`dimension`、`weight`、`evidence`、`scorer`、`score_type`、`source`。实际任务 schema 与 runner 仍优先。
- Manifest 不是身份权威，所有行都增加零个 case。质量行 scorer 形如 `output/quality.toml::output.narrative_quality`；确定性行形如 `output/checks.py::delivery_form`。验证源身份到 manifest 行的 exact-once projection、每行 scorer target 存在且正确，并闭合已加载 check 与运行时结果；不得要求质量 criterion 映射到 `checks.py`。
- manifest 缺失、陈旧或单独存在时，先依正式 claim 和 runner 判断是应创建/再生成摘要、合法无 quality、缺失 criterion，还是链路未决；不得把 manifest 行反向当作 criterion 真值。

## 9. 安全与候选隔离

旧式规范要求时逐类判断 A–H：提示注入、凭据泄露、歧义操作确认、数据完整性、草稿限制、只读/工具克制、领域安全、紧迫压力抵抗。Seal 按 manifest、工具合同和实际 safety evidence 处理，不机械套旧式名称。

“完成正向动作”和“没有执行危险动作”通常是两个事实。只有 runner 明确实现时才能称 `safety gate`。

返修阶段可修改 allowlist 内的 `tests/**`；候选运行时必须把最终 tests 只读挂载。候选执行前还须验证：禁网；solution、fixtures 和全部 tests 外内容只读；临时 HOME/CWD/output；不挂载用户目录或 Skill secrets；环境变量显式 allowlist；超时、进程数和文件大小限制；运行前后冻结 hash。隔离不足时标记 `BLOCKED`，不能直接在宿主降级执行。

## 10. 错误率与漏召率

沿用历史公式，修改前冻结：

- `R0`：legacy 的唯一稳定原始 `RUBRIC_*`；Seal 中所有 canonical `quality.toml` 内可解析的 `[[criterion]]` 条目数，一个 criterion 条目算一个 rubric case；重复或缺失 `id` 仍各计一个 R，并另登记 schema/duplicate issue，不先按 ID 去重；
- `T0`：legacy 的独立实际评分 `test_*`；Seal 中由 `checks.py` 实现/注册的每个独立实际评分 check；
- `N0 = R0 + T0`；manifest 不是身份来源，每行增加零个 case；
- `F`：基线既有、已确认并修复、修复保留在最终文件中，且直接适用验证为 FRESH/PASS 的独立 issue 数；
- `AR/AT`：新增 rubric/criterion 与 scoring test/check；`A = AR + AT`。

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

`F` 按 issue 根因去重，`A` 按新增计分身份计数。缺一个质量 criterion 并缺一个 `checks.py` check 通常 `A=2`。文件名规范化、manifest 创建/再生成和保持身份不变的格式迁移均为 `A=0`。纯 rename/move、helper、diagnostic、未注册或未验证项不计新增。删除/合并另记 `DR/DT/D`，不回写冻结基线。

百分比最多两位小数，括号保留未约分整数，如 `50%（1/2）`、`33.33%（1/3）`。错误率可超过 100%，不得截断。无可靠基线时写 N/A。纯咨询可报告 `F=0`，但必须紧邻说明“未授权修复，不代表未发现问题”，且不能声称完成作业。完整规则见 [verification-and-reporting.md](references/verification-and-reporting.md)。

## 11. 验证与新鲜度

- V0：文本、目录、diff 与规则来源；
- V1：语法、schema、归档和确定性 parser；
- V2：import、collect 或 harness 加载；会执行模块顶层代码；
- V3：隔离 candidate、Oracle、nop；
- V4：judge；
- V5：外部打包、上传或提交。

优先使用项目 runner。每次运行绑定 grader、runner、rules、fixture、candidate、conversation、evidence、probe、environment、config 和 result digest；Seal/RewardKit 按正式 claim/runner 分别绑定适用的 canonical `quality.toml`、实际加载的 `checks.py`、manifest 与 scorer target，并把合法缺席记为 `ABSENT_ALLOWED_BY_CLAIM_RUNNER`，同时验证适用条目的 exact-once projection。任一相关输入、criterion 身份、check 注册、manifest 投影、scorer target 或合法缺席依据变化，即使旧结果时间较新也变为 `STALE`；范围不足为 `UNVERIFIED`。不得把定向回归冒充全量，也不得拼接不同 run。

统一状态：`PASS`、`FAIL`、`PARTIAL`、`BLOCKED`、`NOT_RUN`。Judge 401/402/429/5xx、连接和超时是 infrastructure failure，不直接算候选失败。

## 12. 强制 QA 报告与交付

完成、返修或作业交付自检 WorkC 作业时，必须用 [qa_report.template.md](assets/qa_report.template.md) 生成或更新题包根目录 `qa_report.md`。报告至少包含：固定最大写入边界、实际 test allowlist、实际 test allowlist 外零变化审计（根目录 `qa_report.md` 为唯一例外）、规则与架构、canonical quality 文件及别名处理结果、`R0/T0/N0` 与 manifest 零计数、case 库存、manifest exact-once projection/scorer target 校验、issue 台账、`F/AR/AT/A` 和两项指标、run freshness、差异、阻塞项与限制。确定性-only 单元须明确其无 `quality.toml` 是否由当前 claim/runner 允许。

只读咨询不创建报告，但必须明确本轮不是完成、返修或作业交付自检。

将“可交付”拆成：

- `test_delivery_handoff_ready`：测试侧文件和强制 QA 报告可交接；
- `evaluation_certified`：适用评测完整、runner 健康且结果新鲜；
- `platform_submission_ready`：满足外部提交前提。

完整包可读取冻结文件，但交付前必须在本轮生成或更新根目录 `qa_report.md`，且包只能生成到题包外或用户明确指定的外部位置。tests 未变化时使用 `report-only`；打包不扩大题包写权，也不能替代报告。上传不等于提交成功。

## 13. Secrets 与发布

真实 judge 配置只放 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选绝不读取、打印、转写、解析、复制或提交其值；只有受信任的独立 judge 进程/容器可在 V4 直接解析 env-file。候选先在无 secrets 环境完成；judge 不得再启动候选。

WorkC Skill 自身维护、GitHub 发布或 push 转交 skill-creator 元流程。题包交付只允许已授权的 `tests/**` 子集、根目录 `qa_report.md` 和题包外的交付包；内部规范原文、题目答案、缓存、日志、运行产物和真实 env-file 不得进入交付。

回归矩阵见 [skill-evals.md](references/skill-evals.md)。最终回复必须先说明是否真正完成作业，再列实际 test allowlist 外零变化（根目录 `qa_report.md` 为唯一例外）、QA 报告状态、验证范围、阻塞项和外部提交实际状态。
