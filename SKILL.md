---
name: workc
description: WorkC、ClawEval、PinchBench 或 Seal 单题的业务实现、判分器 QA、返修、Oracle/nop、QA 报告与交付流程。仅在请求明确属于这些题包，或目录出现 rubrics.py + test_outputs.py、criteria_manifest.yaml + 分维度 checks.py 等成套信号时使用；普通软件测试、泛指 judge、考试题或压缩包任务不因单个关键词触发。先判定目标、写入授权、执行上限、交付方式和评测架构，再按实际 runner 与正式规则来源工作。
---

# WorkC 单题决策与 QA 内核

## 1. 不变量

测试必须反映当前规则，不能用 Oracle 分数反推规则。Oracle 不必为 1，nop 不必为 0；不得为改善分数或比率删除有效 case、放宽正确条件、篡改真值、伪造 evidence、修改 nop 或掩盖基础设施错误。

Skill 只辅助发现与验证问题。AI 生成的 rubric、test、expected value、judge 结论和 QA 摘要都必须由人回到正式规则与原始 evidence 复核；AI、轨迹或历史报告提出的问题必须核实后才登记为已确认。至少人工复核所有失败项、安全项、条件触发项和 code/judge 边界；修复后做适用回归，不能把多轮不一致结果拼成一次通过。

维护本 Skill 自身时转入 skill-creator 元流程；本文件不授权修改任何题包。

## 2. 先固定五维状态

开始前记录一个正交状态元组，避免把“审查”“交付”和“能否执行”混为一谈：

- `target`：`business-artifact` / `grader` / `harness` / `skill-meta`；
- `mutation`：`none` / `explicit-allowlist`；
- `execution-ceiling`：`V0 text-only`、`V1 parser-only`、`V2 harness-import`、`V3 candidate-run`、`V4 judge-run`、`V5 external-action`；
- `delivery`：`chat-only` / `report-file` / `changed-files` / `full-package` / `platform-submit`；
- `architecture`：`legacy` / `seal-rewardkit` / `hybrid` / `unresolved`。

用户只说“审查、质检、分析、检查、报告问题”时，`mutation=none` 且默认 `execution-ceiling=V0`。只有明确要求修改、修复、返修、增强或更新，才可能进入 `explicit-allowlist`；候选 allowlist 只能收窄既有授权，不能产生写入授权。项目流程或用户必须另行支持 V2/V3/V4，不能因“需要验证”自动执行候选、联网 judge 或产生运行缓存。

本地修改不包含上传、平台提交、发送或 Git push。外部动作必须有本次请求中的明确授权；“已上传”也不等于“已提交”。

详细分流和冲突案例见 [routing-and-authority.md](references/routing-and-authority.md)。

## 3. 架构识别

文件名只是候选信号，最终以 `test.sh`、task 配置、import/registry、结果与聚合链为准：

| 信号 | 候选架构 | 评分身份 | 实际检查 |
|---|---|---|---|
| `tests/rubrics.py` + `tests/test_outputs.py` | legacy | `RUBRIC_*` | 评分 `test_*`、judge、class/tier |
| `tests/criteria_manifest.yaml` + `tests/*/checks.py` | seal-rewardkit | `angle_id` | 实际注册 check、dimension、RewardKit |
| 两套并存或链路不完整 | hybrid/unresolved | 追 runner | 不补文件、不猜主架构 |

旧式 ClawEval 与输出型 PinchBench 的细则见 [legacy-claw-eval.md](references/legacy-claw-eval.md)；Seal 见 [seal-rewardkit.md](references/seal-rewardkit.md)。不得把旧式文档中的“三文件交付”泛化到 Seal，也不得给 Seal 机械补建 `rubrics.py` 或 `test_outputs.py`。

## 4. Claim 级规则来源

先由 task/materialization 确认正式载体，再把要求拆成原子 claim。为每条 claim 记录：

```text
claim_id | source/carrier | source_class | scope | version/date
explicit_precedence | recast | resolution | reason
```

通常可能涉及用户请求、题目 instruction、workspace policy、local documents、tool description、fixtures/resources、grader、materialization 和 runner。`instruction.md` 在旧式题中常是主要业务载体，但在 Seal 中不一定包含全部正式要求。

persona 是被测场景，不自动覆盖政策；tests、solution、旧 QA、历史题和示例默认只是交叉检查材料。`ground_truth.json` 的人工使用权限按架构和批次决定：输出型 PinchBench 完全忽略，不读取、不引用、不交叉验证；其他架构也绝不作为 tests 的运行时依赖，只有正式规则明确允许时才可在独立推导后人工交叉检查。批次专用规则若明确声明覆盖通用规则，只在该批次生效。两个正式载体无法消解时，只将受影响 claim 标为 `BLOCKED`，其余独立部分继续。

## 5. 基线、授权与冻结

有原始 ZIP 或冻结目录时：

1. 原件只读，在独立副本工作；排除 `__MACOSX` 和 `._*` 干扰；
2. 修改前记录题目标识、规范化路径和基线 hash；
3. 只允许 explicit allowlist 差异，报告完成后再做最终差异审计；
4. runner、judge、类名、注册、权重、instruction、persona、fixtures、environment、solution、ground truth、task/materialization 是否冻结，以本题规则为准；
5. 冻结 harness 有缺陷时，用题目录外包装器验证并记录限制，不擅自修补。

缺少某个常见文件不自动废弃任务。先判断是否存在正式替代载体；只有无法建立受影响 claim 的业务依据时才 `BLOCKED`，平台状态变更仍需 V5 授权。

## 6. 按目标执行

### 业务实现

`tests/` 默认只读。按正式载体和 recast 解析可写业务文件、产物、路径、API 收口与归档要求；验证文件存在、解析、schema、字段、数值、集合、排序、同步、ZIP 成员及线上最终状态。不得为了过测改 tests，也不得把题目禁止的安装、构建、联网、发布或 reset 当作普通验证。

详见 [business-implementation.md](references/business-implementation.md)。

### 判分器 QA

编辑前建立覆盖矩阵，每行一个独立事实：来源、预期、条件、身份、检查机制、evidence、权重层级。定义与评分 check 双向一一对应；同一业务事实只能计权一次。

- 可确定复算的文件、JSON/CSV/ZIP、类型、字段、数字、集合、ID、排序、时间、endpoint、参数、次数和哈希用代码检查；
- 真正需要语义判断的澄清、解释、因果、建议、冲突识别与表达质量才用 judge；
- 条件场景必须让判定看到用户侧触发证据；未触发按正式规则记不适用或自动通过，不能让关键词断言误伤；
- 缺失 evidence 要区分候选缺失、场景不适用、可选载体缺失与 harness/infrastructure 故障；核心缺失不得以普通 `return` 记通过；
- 动态探针只在授权执行级别内进行，并区分容器隔离、进程限制和代码内 patch。

## 7. A–H 与安全

旧式规范要求时逐类判断 A–H：提示注入、凭据泄露、歧义操作确认、数据完整性、草稿限制、只读/工具克制、领域安全、紧迫压力抵抗。Seal 不机械套旧式名称，而按 manifest、工具合同和实际 safety evidence 处理。

“完成正向动作”和“没有执行危险动作”通常是两个事实。只有 runner 明确实现时才能称 `safety gate`；否则称 safety dimension 或本地安全检查。

候选执行前必须能验证：禁网；tests/solution/fixtures 只读；临时 HOME/CWD/output；不挂载用户目录和 Skill secrets；环境变量显式 allowlist；超时、进程数与文件大小限制；运行前后冻结 hash。候选代码不得获得 judge secrets、宿主秘密或超出任务所需的环境。缺一项且当前风险不能接受时不降级为宿主直接执行，标记 `BLOCKED`。

## 8. 错误率与漏召率

执行任务级 QA 时必须从修改前冻结基线记录：

- `R0`：legacy 的唯一原始 `RUBRIC_*` 数；Seal 的唯一 manifest `angle_id` 数；
- `T0`：legacy 的独立评分 `test_*` 数；Seal 的唯一实际评分 check/registry 身份数；
- `N0 = R0 + T0`；
- `F`：找到、修复并完成适用验证的独立问题数；
- `AR` / `AT`：新增 rubric/criterion 与新增 test/check 数；`A = AR + AT`。

公式严格固定：

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

每个问题使用稳定 `issue_id`；同一根因跨文件、跨运行只计一次，真正独立的问题分别计数。只有基线既有问题在最终文件中已修复、完成直接适用验证且通过才计 `F`；仅发现、未验证、阻塞或本轮自行引入后又修掉的问题不计。因分子是问题数，错误率可能超过 100%，不得截断；另报“受影响的唯一原始 case 数”。rubric 与对应 test 分别各算一个 case。

`F` 按 issue 去重，但 `AR/AT/A` 按新增计分身份计数，不按 issue 去重；同一遗漏补一条 criterion 和一条 check 时通常 `A=2`。helper、fixture、setup、diagnostic、preflight、纯改名、移动或描述调整不计新增。新增必须有当前规则来源、有效身份、已注册/绑定并完成适用验证。拆分中最多一个后继项继承原身份，超出原身份的新原子项进入 `AR/AT`；删除/合并分别记 `DR/DT`，`D=DR+DT`，不改公式分母。重复 ID 按稳定身份只计一次，但重复本身登记为问题；孤儿 criterion 和幽灵 check 各保留在对应库存并登记映射缺陷。

百分比最多两位小数，去掉末尾零，括号保留未约分整数：`50%（1/2）`、`33.33%（1/3）`。`N0=0` 时错误率为 `N/A（0/0）`；若 `A>0`，漏召率为 `100%（A/A）`，否则 `N/A（0/0）`。无可靠基线时写 `N/A`，不猜数。audit-only 可写 `0%（0/N0）`，但必须紧邻注明“未授权修复，不代表未发现问题”，并报告未修复数。

这些是描述性 QA 指标，不是阈值、PASS/FAIL、Oracle/nop、reward、gate 或 runner 分母。完整边界见 [verification-and-reporting.md](references/verification-and-reporting.md)。

## 9. 验证级别与结果新鲜度

- V0：只读文本/差异审查；
- V1：语法、schema、归档和确定性 parser；
- V2：import、collect 或 harness 加载；这会执行模块顶层代码，不称为纯静态；
- V3：隔离 candidate/Oracle/nop；
- V4：judge，仅在 scorer/流程需要且 secrets 安全注入时；
- V5：上传、提交、发布、push 等外部动作。

优先使用项目自己的 runner。每次运行绑定 `run_id`、被评分文件 digest、候选产物 digest、runner/version、config digest、起止时间和结果 artifact digest；任何相关文件、权重、prompt、隔离方式或产物变化都会使旧结果过期。定向回归不能冒充全量，多个 run 不能拼接。

统一状态：`PASS`、`FAIL`、`PARTIAL`、`BLOCKED`、`NOT_RUN`。Judge 的 401/402/429/5xx、连接与超时是 infrastructure failure，不直接算候选失败。详见 [verification-and-reporting.md](references/verification-and-reporting.md)。

## 10. 报告与交付

仅在用户或项目要求时创建 `qa_report.md`；否则在聊天中报告。使用 [qa_report.template.md](assets/qa_report.template.md)，至少包含状态元组、规则/基线、case 库存、issue 台账、两项指标、运行新鲜度、差异与限制。

把“可交付”拆成：

- `artifact_handoff_ready`：文件与包可交接；
- `evaluation_certified`：适用评测完整且结果新鲜；
- `platform_submission_ready`：已满足平台提交前提。

`full-package` 还要检查 ZIP CRC、重复成员、顶层目录、必需文件、排除项和源文件 hash。`platform-submit` 必须验证最终平台状态；仅保存或上传不能声称提交成功。

## 11. Secrets 与发布

真实配置只放 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选绝不读取、打印、转写、解析、复制或提交其值；只允许受信任的独立 judge 进程/容器在 V4 运行时直接解析该 env-file。候选阶段必须先在无 secrets 环境中完成；env-file 不注入会启动候选的 runner/orchestrator，judge 也不得再启动候选。GitHub 只保存无效占位模板 `.secrets/judge.env.example`。提交前只检查真实文件存在性、ignore 和未跟踪状态，不用秘密内容做搜索样本。

Git 操作仅在明确授权下执行；先确认仓库、分支、remote 和 diff，只提交 allowlist 公开文件。内部规范原文、视频、个人信息、题目固定答案、缓存、日志、run artifacts 和真实 env-file 不得进入发布。

Skill 自身回归矩阵见 [skill-evals.md](references/skill-evals.md)。最终回复必须区分未运行、基础设施故障、候选失败、报告生成、上传和实际提交，先给结果，再给证据与限制。
