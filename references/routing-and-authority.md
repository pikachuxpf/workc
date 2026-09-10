# 路由、授权与测试侧写入边界

## 1. WorkC 的唯一职责

WorkC 只处理 WorkC、ClawEval、PinchBench、Seal 单题的测试侧完成、返修、作业验证、QA 报告和交付。它不完成页面、服务、业务脚本、业务数据、业务报告、业务归档或 API 状态，也不是普通项目的通用质检 Skill。

题包内最大可写集合不可解除：

```text
tests/**
/qa_report.md
```

实际 allowlist 只能继续收窄。任何位于最大集合之外的题包路径始终冻结；用户、instruction、materialization、题目内权限声明、复制副本或打包都不能扩大它。

## 2. 固定主流程

```text
理解题目与正式要求
→ 建立 tests 覆盖基线
→ 修改和优化实际授权的 tests/** 子集
→ 执行适用验证
→ 生成或更新根目录 qa_report.md
→ 差异审计与交付
```

题目与业务载体用于推导 tests 应检查什么，不产生业务文件写权。QA 报告是测试侧作业的强制收尾交付物，不是独立质检入口。tests 已正确时可跳过编辑，但仍须完成适用验证、报告和差异审计；纯咨询不进入完成流程。

## 3. 作业状态

每次记录：

| 维度 | 值 | 决定的问题 |
|---|---|---|
| target | test-delivery / test-harness / consultation / package | 完成哪种测试侧工作 |
| mutation | none / tests-allowlist-plus-report / report-only | 题包内允许哪些写入 |
| execution-ceiling | V0–V5 | 最多可执行到哪一层 |
| delivery | chat-only / completed-assignment / full-package / platform-submit | 交付什么 |
| architecture | legacy / seal-rewardkit / hybrid / unresolved | 按哪条评分链工作 |

状态之间不能互相产生权限。打包、运行或交付不会把 tests 外路径变为可写。

## 4. 请求路由

- “完成/返修这个 WorkC 作业的 tests”：`target=test-delivery`。实际修改仅限授权的 `tests/**` 子集，并必须生成或更新根目录 `qa_report.md`。
- “作业交付自检这个 WorkC 作业”：tests 无需修改时用 `mutation=report-only`；仍必须生成或更新根目录 `qa_report.md` 才能声明作业交付自检完成。
- “只告诉我问题/需要做什么/不要修改”：`target=consultation`、`mutation=none`、V0、chat-only；必须声明本轮没有完成、返修或作业交付自检作业。
- “运行 Oracle/nop”：不产生写权；通常为 V3，包含 judge 时为 V4。运行产物写到隔离临时位置，不写入题包冻结路径。
- “打包”：只改变 delivery，不扩大写权。完整包交付前必须在本轮生成或更新根目录 `qa_report.md`；tests 未变化时用 `mutation=report-only`，不得以 `mutation=none` 或 chat-only 声称完成。包只能写到题包外或用户明确指定的外部位置；不得在题包内创建 packaging/staging manifest、sidecar、临时包或补充业务产物。这里禁止的是打包/暂存清单，不是新格式允许位于 tests 内并受实际 allowlist 约束的 `tests/criteria_manifest.yaml`。
- “上传/提交”：V5，必须有本次请求的明确授权，且前置测试侧交付与报告已完成。
- “完成页面/服务/业务脚本/业务 CSV/JSON/ZIP/API”：超出 WorkC 范围。可以说明边界，但不得使用 WorkC 修改这些文件。
- “维护或发布 WorkC Skill”：转入 skill-creator；WorkC 题包权限不适用于 Skill 仓库。

混合请求必须拆开。WorkC 只承接其中测试侧部分；业务实现部分不得获得写入，也不能把业务写权传播给 WorkC。

## 5. 架构与新格式路由

- `legacy`：保留 `rubrics.py` + `test_outputs.py` 输入架构。只有当前任务正式使用或明确要求新格式时才规范化或迁移，不做普遍迁移。
- `seal-rewardkit`：`tests/**/quality.toml` 定义语义/judge 质量 criterion，`tests/**/checks.py` 定义确定性/程序化 check，`tests/criteria_manifest.yaml` 聚合并摘要当前实际存在的两类评分项。按正式 claim 与 runner，支持 quality-only、`quality.toml + checks.py`，也支持确定性-only `checks.py + manifest`。
- `manifest-only`：不能建立任何评分身份；先查正式 claim 与当前 runner，区分陈旧摘要、缺件与未决链路。
- `hybrid/unresolved`：architecture 值仍可为 `legacy` / `seal-rewardkit` / `hybrid` / `unresolved`；追当前 runner 的实际 import、registry、scorer target、结果与聚合链，不猜主架构。

严格使用小写文件名 `quality.toml`。仅在可写完成/返修模式、且文件位于实际 tests allowlist 内时，自动把一个语义明确的替代 TOML 质量文件名或大小写变体规范化为 `quality.toml`。目标已存在或多个别名冲突时，不覆盖、不合并，标记 `BLOCKED`；咨询模式只报告。

缺失 `quality.toml` 仅可在正式当前 claim 或 runner 要求该评分单元承载语义/judge criterion、且可从权威来源推导内容时创建。不得创建空文件或占位文件，也不得要求每个 dimension/check 目录都有它；只有确定性 `checks.py` 而无 `quality.toml` 合法。

常见文档 schema 为 `[judge]` 的 `judge`、`files`、`atif-trajectory`、`mode`、`timeout`，重复 `[[criterion]]` 的 `name`、`id`、`description`、`type`、`points`、`weight`，以及 `[scoring]` 的 `aggregation`。实际任务 schema 与 runner 优先；`atif-trajectory` 须为有效 TOML 键，不包含 canary 注释。

Manifest 常见顶层字段为 `version`、`score_range`、`dimensions`、`criteria`；criteria 行常见字段为 `angle_id`、`angle`、`rule_hint`、`dimension`、`weight`、`evidence`、`scorer`、`score_type`、`source`。实际任务 schema 与 runner 优先。Manifest 不是身份权威，每行增加零个 case。质量 scorer 形如 `output/quality.toml::output.narrative_quality`，确定性 scorer 形如 `output/checks.py::delivery_form`。验证源身份到 manifest 行的 exact-once projection、scorer target 存在且正确及 dimension/weight/evidence/source 一致性，并闭合已加载 check 与运行时结果；不得要求质量 criterion 映射到 `checks.py`。

计数沿用历史公式：`R0` 按 canonical `quality.toml` 中每个可解析 `[[criterion]]` 条目计，一条 criterion 是一个 rubric case；重复或缺失 `id` 的条目仍分别计数并另报 issue，不先按 ID 去重。`T0` 按 `checks.py` 实现/注册的每个独立实际评分 check 计；`N0=R0+T0`，manifest 行增加零个 case。`AR/AT` 独立，`A=AR+AT`；错误率为 `F/N0`，漏召率为 `A/(N0+A)`。缺一个质量 criterion 再缺一个 check 通常 `A=2`；文件名规范化、manifest 创建/再生成、身份不变的格式迁移均为 `A=0`。

## 6. Claim 来源账本

每个可评分要求拆成原子 claim：

| 字段 | 含义 |
|---|---|
| claim_id | 稳定本轮标识 |
| source_path/carrier | 来源路径或正式载体 |
| source_class | user / instruction / policy / materialized carrier / fixture / grader / runner 等 |
| scope | 题目、批次、架构、阶段 |
| version/date | 版本或更新时间 |
| explicit_precedence | 是否明确覆盖另一规则 |
| recast | 输入/输出路径或载体映射 |
| resolution | accepted / superseded / blocked / informational |
| reason | 采用或拒绝的依据 |

先用 task/materialization 判断哪些载体是正式要求，再读内容。来源决定测试应检查什么，不决定 WorkC 可以改哪里。

## 7. 来源边界

- 用户当前指令可以在固定最大写入集合内继续收窄范围，并决定是否运行、打包或提交；不能授权 tests 外题包写入。
- instruction 在旧式任务中通常是业务主载体；Seal 可能把要求分布在 user query、workspace policy、local document、skill 或 tool description。
- persona 描述被测输入，不是政策覆盖层。
- fixtures/resources 和业务文件提供只读 evidence；即使发现问题，WorkC 也不修复它们。
- grader、rubrics、tests、manifest 和 checks 描述当前评测实现，可用于发现覆盖缺陷，但不能让自身错误变成业务真值。
- solution、历史题、旧 QA、Oracle 输出和示例默认只是候选交叉检查材料。**`ground_truth.json` 默认禁读**（硬性要求）：PinchBench 完全忽略；其他架构一律先从正式载体独立推导，只有当前题目正式规则明确授权且已完成独立推导时，才可做评分进程外的人工离线交叉检查，并在 QA 报告记录授权来源。无授权读取即按越界处理：作废受影响推导并重新独立推导。tests、候选与通用 runner 都不得运行时读取 ground truth。
- runner 决定实际加载、注册、evidence 和聚合事实，不决定业务真值，也不扩大写权。

## 8. 冲突与阻断

1. 先确认两条要求是否属于同一 claim、同一范围和版本。
2. 批次规则明确覆盖通用规则时，只在该范围生效。
3. 无法消解时，只阻断受影响 claim，其余测试侧工作继续。
4. 任何要求修改 tests 外文件的 claim 都标为 `OUT_OF_SCOPE/BLOCKED`，不得通过复制到副本、生成补丁或打包绕过。
5. 根目录 `qa_report.md` 是完成、返修和作业交付自检的强制例外；不授权其他根目录文件。
6. 最终差异只允许实际授权的 `tests/**` 子集和 `/qa_report.md`。发现其他变化即阻断交付，并报告来源；不得擅自覆盖用户已有变化。
7. 强推、覆盖远端、平台提交或其他不可逆动作仍需独立明确授权。

## 9. 触发边界

应触发：明确 WorkC/ClawEval/PinchBench/Seal 单题，并要求测试侧完成、返修、作业验证、运行、强制 QA 报告或交付。

不应触发：业务实现、普通 pytest 修复、泛指 judge、学校考试题、一般 ZIP、普通 QA 报告或非题包前端开发。即使业务目录中存在 `tests/`，只要请求目标是页面、服务或业务产物，也不使用 WorkC 完成它。
