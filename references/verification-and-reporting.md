# 验证、指标与报告

本参考只适用于 WorkC、ClawEval、PinchBench 或 Seal 单题的测试侧作业，不承接业务实现或普通项目的通用质检。题包内仅本轮授权的 `tests/**` 子集与根目录 `qa_report.md` 可写；维护或发布 WorkC Skill 本身必须转入 skill-creator。

## 1. 验证级别

| 级别 | 允许动作 | 注意事项 |
|---|---|---|
| V0 | 文本、目录、diff、规则来源审查 | 不运行代码 |
| V1 | 语法/schema/parser/归档检查 | 仅确定性解析 |
| V2 | import、pytest collect、harness 注册加载 | 会执行模块顶层代码，不是纯静态 |
| V3 | candidate、Oracle、nop、动态探针 | 隔离输出、audit、conversation、run 和 cache |
| V4 | LLM judge | 仅在实际需要时通过 env-file 注入 secrets |
| V5 | 题包外打包、平台上传或提交 | 外部动作需明确授权并验证最终状态；WorkC Skill 发布和 Git push 转交 skill-creator |

实际动作不得超过用户和题目允许的较低执行上限。文件写入另受不可覆盖的 WorkC 边界约束：题包内仅本轮授权的 `tests/**` 子集和根目录 `qa_report.md` 可写。命令要记录工作目录、版本、配置、返回码与结果 artifact。

## 2. 结果状态

- `PASS`：规定范围已执行且通过；
- `FAIL`：已执行并发现真实设计/候选/交付失败；
- `PARTIAL`：可执行部分完成，但覆盖或非核心证据不全；
- `BLOCKED`：权限、关键材料、基础设施或隔离阻止执行；
- `NOT_RUN`：未执行，不能暗示通过。

Judge 401/402/429/5xx、连接、超时、无效凭据和 runner 未挂载 evidence 属于 infrastructure，不直接算候选失败。宽泛捕获异常后返回 0 分也可能掩盖基础设施故障，必须核对原始错误链。

## 3. 运行新鲜度

每次运行保存：

```text
run_id
scored_files_digest
candidate_artifacts_digest
runner_digest_or_version
config_digest
started_at / finished_at
result_artifact_digest
scope and result summary
```

rubric/criterion、test/check、权重、judge prompt、隔离方式、runner 配置或候选产物变化后，相关旧结果过期。定向回归不能声称全量；不同 run 的通过项不能拼接成一次全量通过。为检查模型波动可重复完整运行，但每次保持独立 run_id，并报告稳定性而不是挑选最好结果。

新鲜度统一为：`FRESH`（当前全部适用输入摘要一致且范围足够）、`STALE`（任一适用输入变化或后续修改影响覆盖）、`UNVERIFIED`（摘要、证据或范围无法确认）。时间较新不自动等于 `FRESH`。

## 4. 原始 Case 基线

先沿 `test.sh`、task 配置、import/registry、结果和聚合链确认真实架构；文件名只作候选信号。两套结构并存或加载链不完整时标记 `hybrid/unresolved`，不得任选一套或机械迁移；尤其不得给 Seal 补旧式文件，也不得把 legacy 机械改成 Seal。

在任何测试侧修改发生前，对同一份可靠基线快照记录来源、版本/hash 和：

- `R0`：legacy 中唯一、正式计分的原始 `RUBRIC_*`；Seal 中唯一、正式计分的 manifest `angle_id`；
- `T0`：legacy 中产生独立计分结果的原始 `test_*`；Seal 中唯一实际注册并产生独立计分结果的 check/registry 身份；
- `N0 = R0 + T0`。

按实际计分身份，不按文件、函数或运行次数计数：一个函数注册多个计分 ID，按 ID 数；参数化运行、重试、不同候选的重复执行不增加 case；正式条件项即使本次 skip 仍在库存；helper、fixture、setup、diagnostic、preflight、禁用项和未注册项不计有效评分 case。

同时分别报告：源码物理定义数、runner collected 数、有效一一映射数。重复身份只按稳定身份计一次，但重复是 issue。孤儿定义和幽灵 check 分别保留在其原始库存并登记映射问题，不能通过相互抵消隐藏。

基线一旦冻结，后续新增、删除或合并不得回写 `R0/T0/N0`。无法可靠建立基线时，两项比率均写 `N/A`，但仍报告可确认的原始整数与原因。

## 5. Issue、修复与新增

`F` 的单位是独立问题，不是 case。只有同时满足以下条件的基线既有问题才计入：

1. 已用稳定 `issue_id` 确认；
2. 已修复，且修复存在于最终文件；
3. 已执行与该问题直接相关的适用验证；
4. 验证通过。

仅发现、部分修复、未验证、验证失败或 infrastructure 阻塞不计 `F`，分别列为未修复/待验证/阻塞。审查过程中自行引入后又修掉的问题不得计入。一个根因跨多个文件或 case、且一次修复可消除时，`F=1`；需要独立修复或验证的真实问题使用不同 issue_id。

`AR/AT/A` 的单位是新增计分 case：

- `AR`：相对冻结基线新增的 rubric/manifest criterion；
- `AT`：新增的 scoring test/registered check；
- `A = AR + AT`。

同一遗漏补 criterion 和 check 时通常 `AR=1, AT=1, A=2`。issue 去重只作用于 `F`，不作用于 `AR/AT/A`。新增观察窗口从基线快照到最终审查截止点；新增必须有当前 claim 来源、有效身份、实际注册/绑定并完成适用验证。

纯重构、等价断言强化、格式/描述调整、临时诊断、语义与身份不变的 rename/move 不计新增。名为 helper 但独立注册或产生分数的仍计 `AT`。

拆分时用“评分事实、evidence、通过条件、计分身份”建立基线到最终映射：最多一个后继项继承原身份，其余独立计分后继项进入 `AR/AT`。

删除与合并分别记录：

- `DR`：删除/合并掉的 rubric/criterion case；
- `DT`：删除/合并掉的 test/check case；
- `D = DR + DT`；
- `k` 个 case 合并成 1 个，删除量为 `k-1`。

若身份映射清晰，可复核：

```text
R1 = R0 + AR - DR
T1 = T0 + AT - DT
N1 = R1 + T1
```

`D` 不从冻结 `N0` 回扣，也不与 `A` 抵消。无法归类的身份变化要说明，不强行套恒等式。

## 6. 错误率与漏召率

严格使用用户指定公式：

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

因 `F` 只包含已修复并验证的问题，错误率实际是“已修复验证问题密度”，会受 mutation 授权影响，不等于全部已发现错误发生率。纯咨询的 `0/N0` 不能用于表示“未发现错误”，也不能与完成返修后的值直接比较。

错误率可以超过 100%，不得截断；漏召率在非负整数计数下不会超过 100%，若超过说明公式或计数有误。报告另列受影响的唯一原始 case 数帮助解释。

展示规则：用原始整数计算后乘 100，按常规四舍五入保留最多两位小数，去掉末尾零；括号保留未约分整数，不用四舍五入的中间值继续计算。例如：

- `1/2 → 50%（1/2）`；
- `1/3 → 33.33%（1/3）`；
- `3/7 → 42.86%（3/7）`；
- 错误率 `9/4 → 225%（9/4）`。

零分母：

- `N0=0`：错误率 `N/A（0/0）`；
- `N0=0, A>0`：漏召率 `100%（A/A）`；
- `N0=0, A=0`：漏召率 `N/A（0/0）`。

这些比率是描述性 QA 数据，不是阈值、配额、PASS/FAIL、Oracle/nop、RewardKit reward、gate、num/den 或 dimension denominator。不得为了改善比率删除有效 case、拒绝必要新增或制造无关项。其他流程文件中的“问题数 ≤ 5%”只有在明确证明使用同一分子、分母和范围时才可作为本指标阈值；否则保持来源受限的独立流程规则。

## 7. 纯咨询模式

纯咨询或用户明确要求不修改时，可以按公式写：`错误率：0%（0/N0）`，但必须紧邻注明：

> 本轮为只读咨询，未授权修复；0 仅表示 F=0，不代表未发现问题。本轮未完成、未返修、未作业交付自检该作业。

同时报告已确认未修复 issue 数、issue_id、受影响 case 和阻塞项。漏召率只有在实际新增有效 case 时才非零；纯咨询通常 `A=0`，不能用 0 掩盖建议新增项。

## 8. 强制报告和测试侧交付结论

完成、返修或作业交付自检 WorkC 作业时，必须使用 [../assets/qa_report.template.md](../assets/qa_report.template.md) 生成或更新题包根目录 `qa_report.md`。即使 tests 无需修改，作业交付自检也必须落盘报告；缺少本轮报告不得声明作业完成。只有纯咨询或明确不修改时才可 chat-only，并必须使用上一节的未完成声明。

报告至少包含：最大可写边界、实际 `tests/**` allowlist、根目录报告状态、实际 test allowlist 外零变化审计（根目录 `qa_report.md` 为唯一固定例外）、正式规则来源、基线 hash、case 三套计数、issue 台账、F/未修复/受影响 case/非 case 问题、AR/AT/A/DR/DT/D/R1/T1/N1、两项指标、run freshness、差异和限制。

把结论拆成：

- `test_delivery_handoff_ready`：授权的测试侧文件和强制 `qa_report.md` 可交接；
- `evaluation_certified`：适用检查完整、runner 健康且结果新鲜；
- `platform_submission_ready`：满足外部提交前提；
- `external_submission`：实际提交动作与最终状态。

完整包可以读取冻结内容，但交付前必须在本轮生成或更新根目录 `qa_report.md`，且只能生成在题包外或用户明确指定的外部位置；tests 未变化时使用 `mutation=report-only`，不得以 `mutation=none` 或 chat-only 声称完整包已完成。不得在题包内创建 sidecar、staging 或临时包。打包不扩大写权，也不能替代报告。上传文件不等于提交成功。
