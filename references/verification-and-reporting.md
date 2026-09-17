# 验证、指标与报告

本参考只适用于 WorkC、ClawEval、PinchBench、Seal 或 RewardKit 单题的测试侧作业，不承接业务实现或普通项目的通用质检。题包内仅本轮授权的 `tests/**` 子集与根目录 `qa_report.md` 可写；维护或发布 WorkC Skill 本身必须转入 skill-creator。

## 1. 验证级别

| 级别 | 允许动作 | 注意事项 |
|---|---|---|
| V0 | 文本、目录、diff、规则来源审查 | 不运行代码 |
| V1 | 语法/schema/parser/归档检查 | 仅确定性解析 |
| V2 | import、pytest collect、harness 注册加载 | 会执行模块顶层代码，不是纯静态 |
| V3 | candidate、Oracle、nop、bootstrap、known-answer、persona 与动态探针 | 隔离 output、audit、conversation、trajectory、run 和 cache |
| V4 | LLM judge | 仅在实际需要时通过 env-file 或既有安全挂载注入 secrets；报告不得写秘密值 |
| V5 | 题包外打包、平台上传或提交 | 外部动作需明确授权并验证最终状态；WorkC Skill 发布和 Git push 转交 skill-creator |

实际动作不得超过用户和题目允许的较低执行上限。题包内最大可写集合固定为本轮实际授权的 `tests/**` 子集与根目录 `qa_report.md`，任何 instruction、materialization、工具输出或打包要求都不能扩大边界。命令记录工作目录、版本、配置、返回码与结果 artifact；运行产物必须位于题包外或明确允许的隔离位置。

## 2. 结果状态与三分归因

- `PASS`：规定范围已执行且通过；
- `FAIL`：已执行并发现真实 grader 设计、候选行为或交付失败；
- `PARTIAL`：可执行部分完成，但覆盖或非核心证据不全；
- `BLOCKED`：权限、关键材料、服务、凭据、基础设施或隔离阻止执行；
- `NOT_RUN`：未执行，不能暗示通过；
- `OUT_OF_SCOPE`：所需动作落在冻结路径或本轮授权之外。

任何失败先按证据拆为三类，不能把运行器噪声或基础设施故障记为候选失败：

1. `candidate_failure`：候选产物在已验证健康、确定的评分链上违反正式要求；
2. `harness_noise`：非确定性、顺序污染、并发、缓存、临时文件、解析漂移或 harness 自身波动；
3. `infrastructure_failure`：服务不可用、401/402/429/5xx、连接/超时、无效或未挂载凭据、runner/evidence/image/mount 缺失。

宽泛捕获异常后返回 0 分会掩盖归因，必须保留原始错误链。建议、优化意见和 mandatory requirement 分栏记录；建议未采用不能升级为失败，只有有正式来源的 mandatory requirement 才能阻断或计 issue。

## 3. 0917 新格式结构契约

识别为 0917 新格式后，canonical 结构固定为：

```text
tests/
├── criteria_manifest.yaml
├── process/
│   ├── checks.py
│   ├── quality.toml       # 可选
│   ├── reward.toml        # 可选
│   └── react_prompt.md    # 仅 quality.toml 存在时必需且唯一
├── output/
│   └── checks.py
└── safety/
    └── checks.py
```

`process`、`output`、`safety` 三个维度必须都存在，每维恰好一个直接归属该维度的 canonical `checks.py`：`tests/process/checks.py`、`tests/output/checks.py`、`tests/safety/checks.py`。不得用 alias、大小写变体、嵌套副本、生成副本或跨维共享文件冒充“恰好一个”。`tests/criteria_manifest.yaml` 必须存在且唯一；`tests/process/quality.toml` 与 `tests/process/reward.toml` 可选。只有 canonical 文件参与加载与摘要。

结构 inventory 必须逐路径记录 `expected/discovered/canonical/status/digest`，并核对：

- manifest、三个维度和三个 `checks.py` 的缺失、重复、额外 alias、大小写冲突及路径歧义；
- manifest row 的 dimension、scorer target、result ID、weight、source/evidence 与实际注册链；
- `process/output/safety` 维度边界及 reward 聚合；
- 静态声明、import/registry、实际 runtime loaded path/digest 三者一致。

结构缺失或重复时不得自动补空文件、任选副本或猜加载目标；先标记结构失败与 `BLOCKED`，只有正式来源足以唯一推导且写入授权明确时，才可按作业要求修复并重新做完整结构核验。

### 3.1 quality 与 prompt 原子配对

若 `tests/process/quality.toml` 不存在，允许 deterministic-only；此时 `react_prompt.md` 也不得作为活跃 grader 输入，LLM 有效占比按真实聚合复算，通常为 0。若 quality 存在，则同目录必须恰好一个 canonical `react_prompt.md`，且 quality 中必须无歧义地声明：

```toml
judge = "react"
prompt_template = "react_prompt.md"
```

同时核对 prompt 路径解析不逃逸、不指向 alias，文件非空且符合 runner 所需模板/schema，静态 template 引用与 runtime 实际加载的是同一路径、同一 digest。以下任一情况发生时，整条数据项必须先标记 `DEPRECATED/ABANDONED`，停止把它作为可交付、可认证或可继续自动修复的数据项：

- quality 存在但 prompt 缺失；
- prompt 或 quality 候选重复；
- 大小写、alias、相对路径或 loader 解析导致配对歧义；
- `judge` 不是精确的 `react`；
- `prompt_template` 不是精确的 `react_prompt.md`；
- prompt 模板格式、必需变量或 runtime 绑定错误。

禁止自动生成、补写、复制、合并或猜测 prompt；也不得从历史 prompt、候选输出、Oracle、known-answer 或其他题目推断。报告只保留只读证据、弃用原因、责任方和移交项。孤立 prompt 不贡献身份，也不能据此机械创建 quality。

### 3.2 Inventory、digest、新鲜度与一致性

prompt 必须纳入 `structure inventory`（结构库存）、`grader_digest`、run freshness 和回归范围。每次运行至少保存：

```text
run_id
structure_inventory_digest
scored_files_digest / grader_digest
manifest_digest
checks_digests_by_dimension
quality_digest_or_ABSENT_ALLOWED
prompt_path / prompt_status / prompt_digest_or_NOT_APPLICABLE
reward_digest_or_ABSENT_ALLOWED
candidate_artifacts_digest
runner_digest_or_version
config_digest_non_secret
service_credential_preflight_status
started_at / finished_at
result_artifact_digest
scope and result summary
```

必须完成 `manifest ↔ quality ↔ prompt ↔ checks ↔ reward ↔ runtime` consistency：manifest 与三个 checks 的注册结果闭合；存在 quality 时 criterion、judge、prompt path/digest 与 runtime loaded input 闭合；reward 与实际聚合闭合。prompt、manifest、quality、checks、reward、runner、权重、隔离方式或候选产物任一变化，相关旧结果即 `STALE`。

新鲜度统一为：`FRESH`（当前全部适用输入摘要一致、runtime 一致且范围足够）、`STALE`（任一适用输入变化或后续修改影响覆盖）、`UNVERIFIED`（摘要、证据、runtime path 或范围无法确认）。时间较新不自动等于 `FRESH`。定向回归不能声称全量；不同 run 的通过项不能拼接成一次全量通过。多轮必须保持独立 run_id，报告全部结果及波动，不挑最高分。

## 4. 原始 Case 基线与身份

先沿 `test.sh`、task 配置、manifest、import/registry、quality/prompt、reward、结果和聚合链确认真实架构。legacy 是受支持输入，不得机械迁移为 0917；两套结构同时被实际加载时标记 `hybrid`；加载链不完整或无法确认时标记 `unresolved`。不得任选一套、补空文件或猜主架构；manifest-only 是结构观测结果，不是 architecture 值。

在任何测试侧修改前，对同一可靠基线快照记录来源、版本/hash 和：

- `R0`：0917 新格式中，冻结基线的 canonical `tests/process/quality.toml` 内每个可解析 `[[criterion]]` 条目计一个 R case；重复或缺失 `id` 的条目仍分别计入，并另登记 duplicate/schema issue，不可伪装成稳定 runtime 映射。另列 physical、active、discarded 与 runtime-consumed 库存；quality–prompt 前置门失败、数据项已弃用或基线无法可靠建立时，两项比率写 N/A。legacy 仅统计实际评分链消费的稳定 rubric 身份；仅出现在 assertion message、错误文本、说明文字、注释、fixture 字符串或未注册常量中的 `RUBRIC_*`/rubric-like 常量一律是 non-case；
- `T0`：0917 新格式中，三个 canonical `checks.py` 实际实现并注册、由当前评分链消费的独立最终 result ID 数；factory 产生多个 result ID 时按 ID 数。legacy 统计实际评分链消费并产生独立评分结果的稳定 `test_*`；
- `N0 = R0 + T0`。

除 0917 `R0` 按冻结基线 canonical quality 中每个可解析 `[[criterion]]` 条目计数外，其余身份按实际稳定计分身份统计，不按文件、manifest row、prompt、函数、常量或运行次数计数。0917 `R0` 中重复或缺失 `id` 的可解析条目仍分别计数并另报 issue，不按稳定 ID 去重；runtime-consumed stable identity 另列库存。参数化重复运行、重试和不同候选执行不增加 case；正式条件项即使本次 skip 仍在库存；helper、fixture、setup、diagnostic、preflight、禁用项、未注册项及 assertion-message-only 常量不计有效 case。

`criteria_manifest.yaml` 是索引，`react_prompt.md` 是 judge 输入，维度目录/结构哨兵是组织载体；三者均不新增 rubric/test 身份。创建、再生成或修改这些文件本身 `AR=0, AT=0, A=0`。`reward.toml` 和其他结构/聚合配置同样不贡献身份。真正新增一个被消费的 criterion 才 `AR+1`，真正新增一个独立 registered result ID 才 `AT+1`。

同时报告源码物理定义数、runner collected/registered 数、评分链实际消费的有效稳定身份数。孤儿、幽灵、重复注册、跨维错挂和 assertion-message-only 误计分别登记，不能相互抵消。报告给出 raw-to-final identity mapping，说明 alias、case、格式迁移、拆分、合并和新增后的身份归属。

基线冻结后，新增、删除或合并不得回写 `R0/T0/N0`。无法可靠建立基线、结构/配对碰撞未消解或加载链无法确认时，两项比率均写 `N/A`，但仍报告可确认的整数与原因。

## 5. Issue、修复、新增与删除

`F` 的单位是独立问题，不是 case。只有同时满足以下条件的基线既有问题才计入：

1. 已用稳定 `issue_id` 确认；
2. 已修复，且修复存在于最终授权文件；
3. 已执行与该问题直接相关的适用验证；
4. 验证通过且证据 `FRESH`。

仅发现、部分修复、未验证、验证失败、DEPRECATED/ABANDONED 或 infrastructure 阻塞不计 `F`，分别列为未修复、弃用、待验证或阻塞。审查中自行引入后又修掉的问题不计。一个根因跨多个文件或 case 且一次修复可消除时 `F=1`；需要独立修复或验证的使用不同 issue_id。

- `AR`：相对冻结基线新增、被评分链消费的 rubric/criterion 身份；
- `AT`：新增、注册并被评分链消费的 scoring test/check result ID；
- `A = AR + AT`；
- `DR`：删除/合并掉的 rubric/criterion case；
- `DT`：删除/合并掉的 test/check case；
- `D = DR + DT`。

同一遗漏补一个 criterion 和一个 check 时 `AR=1, AT=1, A=2`。issue 去重只作用于 `F`。纯重构、等价断言强化、描述调整、身份保持 rename/move/格式迁移，以及 manifest、prompt、reward 或目录结构文件的创建/变更均不计新增身份；但 quality-prompt 违规不得以这条规则为自动创建 prompt 的理由。

拆分时用“评分事实、evidence、通过条件、计分身份”建立映射：每层最多一个后继项继承原身份，其余独立后继进入 `AR/AT`。`k` 个 case 合并成 1 个，删除量为 `k-1`。身份清晰时复核：

```text
R1 = R0 + AR - DR
T1 = T0 + AT - DT
N1 = R1 + T1
```

`D` 不从冻结 `N0` 回扣，也不与 `A` 抵消。无法归类的变化说明原因，不强行平账。

## 6. 错误率与漏召率

严格使用：

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

`F` 只含已修复且 fresh 验证的问题，因此错误率是“已修复验证问题密度”，不等于全部已发现错误率。错误率可超过 100%，不得截断；漏召率在非负整数下不超过 100%。使用原始整数计算后乘 100，常规四舍五入保留最多两位小数并去尾零，括号保留未约分整数：`1/2 → 50%（1/2）`、`1/3 → 33.33%（1/3）`、`3/7 → 42.86%（3/7）`、错误率 `9/4 → 225%（9/4）`。

零分母：

- `N0=0`：错误率 `N/A（0/0）`；
- `N0=0, A>0`：漏召率 `100%（A/A）`；
- `N0=0, A=0`：漏召率 `N/A（0/0）`。

这些比率是描述性 QA 数据，不是阈值、配额、PASS/FAIL、Oracle/nop、reward、gate、num/den 或 dimension denominator。不得为改善比率删除有效 case、拒绝必要新增或制造无关项。“问题数 ≤5%”只有明确证明同一分子、分母和范围时才可关联，否则保持为独立流程规则。

## 7. 新版动态验证、防伪与运行前检查

执行 V3/V4 前，先做不泄密的 service/credential preflight：记录服务端点类别、凭据来源/挂载状态、必要环境变量名或 secret reference、权限/连通性、模型/runner 可用性及结果；不得记录 token、cookie、密码、完整 Authorization header 或秘密值。preflight 未通过时动态项 `BLOCKED`，不得降级到假 judge、模板回退或把错误归候选。

新版必须沿真实聚合层级复算全部 LLM 有效 reward share，包含 quality/judge、嵌套权重、归一化、门控和 fallback 的实际贡献，证明 `≤40%`；不得按 judge 数量或表面 weight 估算。manifest、quality、prompt、process/output/safety 三个 checks、reward、runner/aggregation 或 runtime 任何变化后，都必须重新复算并回归。

在授权、隔离和服务健康时，至少覆盖：

- bootstrap/加载闭合；
- known-answer 正例与确定性反例；
- persona/对话证据边界（适用时）；
- HTML evidence 的原始 artifact、解析方式、selector/片段、转义/可见性与 digest；
- 四个负控：关键词空壳、错误数值、缺关键内容、移除所有 judge 的事实检查消融。

四负控必须保持除单变量外的 candidate、evidence、环境和配置一致；分别报告各维度、总 reward、正式通过门、run_id 与 freshness。局部 parser 探针不证明端到端门闭合。未授权或服务阻塞如实记 `BLOCKED/NOT_RUN`。

## 8. 轨迹后环境事件与状态收口

轨迹运行后发现环境事件时，单独建立台账，不得塞进候选错误。每条至少记录：

```text
event_id
stage
trajectory/run_id
observed_at
environment_cause
exact_normalized_missing_path
expected_source_or_mount
responsible_party
evidence_refs
status = BLOCKED | OUT_OF_SCOPE
repair_disposition = NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF
```

每个精确规范化缺失路径必须单独占一行；不得使用目录概述、glob，或在同一字段合并多个路径。只有确有环境原因且测试侧无进一步合法修复时，才能使用固定 `repair_disposition`。必须区分“环境中缺少本应由镜像/平台/挂载提供的路径”和“候选按任务要求本应交付却漏交的路径”：前者是 infrastructure，后者在健康 harness 上可归 candidate_failure。不得仅凭 `ENOENT` 猜归因。

报告分别记录 `human_review_status`、`technical_lead_review_status`、`trajectory_stage_status`、`algorithm_acceptance_status`。无证据写 `NOT_RUN`；不得把代理自检、本地 reward 或建议事项冒充人工、负责人、轨迹阶段或算法验收通过。当前门若要求人工/负责人收口而尚未完成，相应 ready 为 `BLOCKED`。

## 9. 纯咨询、强制报告与交付结论

纯咨询或明确不修改时可以写 `错误率：0%（0/N0）`，但必须紧邻声明：

> 本轮为只读咨询，未授权修复；0 仅表示 F=0，不代表未发现问题。本轮未完成、未返修、未作业交付自检该作业。

同时报告未修复 issue、受影响 case、建议新增项和阻塞项；纯咨询不得创建 `qa_report.md`。

完成、返修或作业交付自检时，必须使用 [../assets/qa_report.template.md](../assets/qa_report.template.md) 生成或更新题包根目录 `qa_report.md`。即使 tests 无需修改，也必须 `mutation=report-only` 落盘报告；缺少本轮报告不得声明完成。

报告至少包含：固定写入边界、实际 allowlist、零变化审计、正式规则来源、基线与 architecture、0917 结构 inventory、manifest/quality/prompt/checks/reward/runtime consistency、prompt path/status/digest、配对与弃用状态、三套身份计数和 raw-to-final mapping、issue 与建议/mandatory 区分、F/AR/AT/A/DR/DT/D 及两项指标、service/credential preflight、HTML evidence、LLM≤40%复算、四负控、三分归因、run freshness、post-trajectory 环境事件、四类人员/阶段状态、差异和限制。不得写秘密值。

交付结论拆成：

- `test_delivery_handoff_ready`：授权测试侧文件和强制报告可交接；
- `evaluation_certified`：适用检查完整、runner 健康且结果新鲜；
- `platform_submission_ready`：满足外部提交前提；
- `external_submission`：实际提交动作与最终状态。

完整包只能写到题包外或用户明确指定的外部位置；题包内不得创建 sidecar、staging、临时包或额外交付清单。打包不扩大写权，也不能替代报告。上传不等于提交成功。

按 [current-sop.md](current-sop.md) 补充来源日期与适用批次、反馈 identity、全部提供轨迹比较及三分归因。冻结题面/环境缺陷只列移交，不写成已修改。若授权平台交付，按实际 UI 验证最终状态；“进行中”不能认证提交，连带领取下一题需单独授权。未授权外部写回时只报告待登记值与 `NOT_REQUESTED/NOT_AUTHORIZED`。