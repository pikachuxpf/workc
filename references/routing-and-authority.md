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
- “打包”：只改变 delivery，不扩大写权。完整包交付前必须在本轮生成或更新根目录 `qa_report.md`；tests 未变化时用 `mutation=report-only`，不得以 `mutation=none` 或 chat-only 声称完成。包只能写到题包外或用户明确指定的外部位置；不得在题包内创建 staging、sidecar、manifest、临时包或补充业务产物。
- “上传/提交”：V5，必须有本次请求的明确授权，且前置测试侧交付与报告已完成。
- “完成页面/服务/业务脚本/业务 CSV/JSON/ZIP/API”：超出 WorkC 范围。可以说明边界，但不得使用 WorkC 修改这些文件。
- “维护或发布 WorkC Skill”：转入 skill-creator；WorkC 题包权限不适用于 Skill 仓库。

混合请求必须拆开。WorkC 只承接其中测试侧部分；业务实现部分不得获得写入，也不能把业务写权传播给 WorkC。

## 5. Claim 来源账本

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

## 6. 来源边界

- 用户当前指令可以在固定最大写入集合内继续收窄范围，并决定是否运行、打包或提交；不能授权 tests 外题包写入。
- instruction 在旧式任务中通常是业务主载体；Seal 可能把要求分布在 user query、workspace policy、local document、skill 或 tool description。
- persona 描述被测输入，不是政策覆盖层。
- fixtures/resources 和业务文件提供只读 evidence；即使发现问题，WorkC 也不修复它们。
- grader、rubrics、tests、manifest 和 checks 描述当前评测实现，可用于发现覆盖缺陷，但不能让自身错误变成业务真值。
- solution、历史题、旧 QA、Oracle 输出和示例默认只是候选交叉检查材料。PinchBench 完全忽略 `ground_truth.json`；其他架构只有正式规则明确授权时才可在独立推导后人工交叉检查。tests、候选与通用 runner 都不得运行时读取 ground truth。
- runner 决定实际加载、注册、evidence 和聚合事实，不决定业务真值，也不扩大写权。

## 7. 冲突与阻断

1. 先确认两条要求是否属于同一 claim、同一范围和版本。
2. 批次规则明确覆盖通用规则时，只在该范围生效。
3. 无法消解时，只阻断受影响 claim，其余测试侧工作继续。
4. 任何要求修改 tests 外文件的 claim 都标为 `OUT_OF_SCOPE/BLOCKED`，不得通过复制到副本、生成补丁或打包绕过。
5. 根目录 `qa_report.md` 是完成、返修和作业交付自检的强制例外；不授权其他根目录文件。
6. 最终差异只允许实际授权的 `tests/**` 子集和 `/qa_report.md`。发现其他变化即阻断交付，并报告来源；不得擅自覆盖用户已有变化。
7. 强推、覆盖远端、平台提交或其他不可逆动作仍需独立明确授权。

## 8. 触发边界

应触发：明确 WorkC/ClawEval/PinchBench/Seal 单题，并要求测试侧完成、返修、作业验证、运行、强制 QA 报告或交付。

不应触发：业务实现、普通 pytest 修复、泛指 judge、学校考试题、一般 ZIP、普通 QA 报告或非题包前端开发。即使业务目录中存在 `tests/`，只要请求目标是页面、服务或业务产物，也不使用 WorkC 完成它。
