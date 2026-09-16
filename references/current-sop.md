# 当前文字 SOP 对齐与供应商交付流程

本参考是 WorkC Skill 维护中的流程摘要，不是内部 SOP 原文镜像。核对日期：2026-09-16。题包作业仍只可修改实际授权的 `tests/**` 子集与根目录 `/qa_report.md`；本参考不授权业务实现、冻结路径修改或外部提交。

## 1. 来源与适用范围

| 文字来源 | 页面显示更新时间 | 用途 |
|---|---|---|
| [Work项目-作业SOP](https://docs.xiaohongshu.com/doc/e9c39a5c3309db4149d4cd46e5ca6f30) | 9月14日 16:44 | 当前主流程、人员收口、平台提交、指标登记 |
| [RewardKit 判分与人工标注对齐](https://docs.xiaohongshu.com/doc/1a42e805086c3a943b112d67d80201e6) | 9月10日 14:44 | 新版交付结构、事实/judge 分工、40%上限、防空壳验证 |
| [quality.toml内容格式](https://docs.xiaohongshu.com/doc/d0a8d61b948587efc66d25521e3392a2) | 9月10日 13:47 | quality 与 manifest 字段示例、缺失 quality 的判断 |
| [Openclaw 题目 Refine SOP](https://docs.xiaohongshu.com/doc/1b8a26c2e1115ae58c4e74be8fa23464) | 7月7日 14:57 | 失败清单、跨轨迹归因、返修描述 |
| [ClawEval质检标准](https://docs.xiaohongshu.com/doc/87e590f1ae4512468d08bba78e9f9c73) | 5月20日 19:46 | legacy 原子性、覆盖与 evidence 分工 |

以上更新时间按页面显示记录，页面未显示年份的字段不自行补成年份。视频属于历史说明，本轮未观看；附件 skill、示例题包与视频均未作为已验证的实现。后续批次若更新，重新核对受影响 claim，不把本次摘要当永久最新规则。

按 claim、架构、批次与阶段处理来源：新版允许 Likert 的示例不能推广到要求 yes/no 的 legacy rubric；旧 Refine 中修改 instruction/environment 的建议在 WorkC 内只能登记并移交。示例中的 GT source 字符串、canary、固定模型和题目路径不构成 GT 读取授权，不复制到新生成的正式标准。

## 2. 当前主流程与角色收口

1. 标注人员理解当前规则、instruction、persona、fixtures 和正式 materialized carriers，建立覆盖基线，修复授权 tests，生成 `/qa_report.md`。AI/skill 只辅助发现问题；输出必须由人工回到正式规则、原始 evidence 和实际 runner 逐项核查。
2. 技术负责人汇总交付并批量复核；这是独立收口环节，不能把单题代理自检写成负责人已验收。记录包摘要、复核人、结果和未处理问题；无证据时写待复核。
3. 首轮轨迹评估由项目收口方交给算法侧运行，不是标注人员必做的启动步骤。主 SOP 的“问题数≤5%”只约束这一阶段；页面未明确其完整分子、分母和样本范围，不能替换 `F/N0`、漏召率、reward 或单题通过阈值。正式口径缺失时保留阶段条件并记录未核实。
4. 被轨迹打回后，对反馈逐项判断是否真实存在；修复后个人多轮复测，再由技术负责人批量复核，通过后移交项目收口方。当前主 SOP 指出该返修收口不再由项目收口方重跑轨迹，而直接交算法验收；这不等于本地评测已认证或算法已验收。
5. 当前项目指定的辅助 skill 与 WorkC 不是同一个安装身份。若批次要求使用指定 skill，记录其版本/摘要和实际复核证据；未运行不能声称已通过它，也不在不可信或缺隔离环境执行下载附件。

没有人工复核证据时，`human_review_status=NOT_RUN`，自动化产物可说明已生成，但不得声称已人工验收；若当前交付门明确要求人工/负责人收口，则相应 ready 为 `BLOCKED`。批量复核、首轮轨迹评估与算法验收分别记录，不合并成一个 PASS。

## 3. 轨迹返修的三段式判断

先读反馈清单（如正式提供的 `refine.json`），校验 task identity/path、`always_failing_tests`、`num_runs_with_ctrf`、`num_always_failing` 与 `traj_path`。这些是反馈线索，不是测试期望值或新计分身份。新版失败 ID 沿实际 registry、manifest scorer 和结果命名映射定位，不机械创建 legacy 文件。

对每个反馈项记录：

- **测试在检查什么**：实际通过条件、评分身份、evidence 和权重。
- **Agent 实际做了什么**：逐条引用提供的所有相关轨迹、输出或工具调用；写清计算参数、正确公式/值、实际公式/值或字段映射。缺失轨迹明确列出，不把只读一条写成已分析全部。
- **正式规则是否支持该要求**：对照题面、persona、正式输入与环境；区分候选真错、测试过严/过松、隐藏约束、隐藏白名单、规则歧义、环境故障和标准/实现不一致。

多个失败项按根因归组，不机械按失败 test 数计 `F`。合理多解有正式依据时调整 tests 接受等价结果，同时验证明确错误仍会失败；自然语言不可穷尽时不不断扩充个人白名单。必须补 instruction、fixtures、环境或冻结 harness 才能消解的问题，登记 `OUT_OF_SCOPE/BLOCKED` 并交授权负责人，不自行补题面。

报告中的修改情况使用“refine 行为 + 具体操作”：`不修改 test：规则明确且轨迹违反要求`、`修改 test：将原条件改为有依据的等价判定`、`待讨论`、`建议剔除`、`建议授权方修改 instruction/environment（本轮未修改）`。候选真错时只解释不修改测试的依据，不编写候选修复方案。删除或替换无触发/不稳定项须确认正式适用性并记录身份与覆盖变更，不能为了减少问题数删有效 case。

## 4. 新版评分的新增验收要求

- 全部 LLM judge 项合计最终 reward 权重占比不得超过 **40%**。沿当前实际 runner 从 criterion 到组、维度和总 reward 复算，不能按文件数、criterion 数或 manifest 原始 weight 相加估算。无法确认聚合时 `BLOCKED`；调整所需配置位于冻结路径时移交。该上限适用于当前新版对齐规范，不无条件推广到 legacy 或其他正式批次。
- 对照至少包含关键词空壳、错误数值、关键内容缺失；可复用当前题真实产物作单变量变体。记录被影响 checks、分维度和总分，而不只证明参考候选高分。主规范未给出“明显失分”的数值阈值，不擅造统一 cutoff；至少受影响事实项必须正确失分，交付门仍按正式契约。
- 做 **judge 消融**：在题包外隔离验证配置中移除所有 judge 项，保留事实 checks，验证事实错误不能被认证通过。记录消融后的实际分母、是否重新归一及正式通过判据；没有数值通过阈值时记录关键事实失败，不虚构总分门。
- 所有对照使用一致的适用 evidence、候选基线与环境；只改变预定变量。不能污染 trajectory 后将分数下降归因于输出判据修复。隔离或可信 evidence 不足时记 `BLOCKED/NOT_RUN`，不在宿主运行候选来补分数。
- Manifest 的 `summary` 与 `partial_credit` 若为当前 schema 字段，逐项核对与真实检查及部分分算法一致；manifest 仅用于定位、速览、对照，真正规则与权重必须读取对应 checks/quality 和 runner。格式参考中的 `angle/rule_hint` 形态与对齐页中的 `summary/partial_credit` 形态是不同示例，按当前 schema 判定，不盲目合并字段。
- 若当前正式契约要求 tests manifest 与根目录 manifest 字节一致，先只读比对。根目录副本始终冻结；需要同步根目录才能闭合时标记 `BLOCKED` 并移交，不能扩大写权，也不为所有题新建根目录副本。

## 5. 平台与表格登记

当前主 SOP 使用[星标平台](https://star.annoti.com/)下载、上传题包。平台只用于收发题，不替代评测或人工复核。

- 指派题：按当前实际 UI 从“我的任务→领取新题”定位对应题包；上传后还需点击“领取并提交下一题”。上传动作和提交动作分开观察。
- 自动领取的题允许在上述入口或历史任务上传。显示“进行中”意味着尚未完成提交；不能写 `SUBMITTED_CONFIRMED`。
- 提交后验证正确 task ID、包摘要、回执/提交 ID 和最终状态。若点击可能顺带领取下一题，外部动作授权还须覆盖该副作用；不足则停在 `UPLOADED_NOT_SUBMITTED/NOT_AUTHORIZED`。
- 批次标注表实时登记完成状态和两项指标，采用 `50%（1/2）` 格式。未授权表格写回时仅在 QA 报告提供待登记值，记录 `NOT_REQUESTED/NOT_AUTHORIZED`，不自动回写。
- 主 SOP 公式与现有 Skill 一致：错误率 `F/N0`，漏召率 `A/(N0+A)`。5%轨迹阶段条件是独立流程规则，不是这两项指标的默认门。

## 6. 本次维护的差异结论

已一致：tests-only 与强制 QA 交付、人工核查原则、quality 小写命名、缺失 quality 按需创建、事实与语义分工、manifest 不重复计数、两项公式与展示格式。

本次新增/强化：来源版本记录、角色和阶段分离、反馈项三段式归因、多轨迹对照、多轮复测稳定性台账、40%有效占比、伪造产物与 judge 消融、summary/partial_credit 和根 manifest 同步规则、平台确实提交与批次表格登记证据。

保留的安全差异：只按正式 claim/runner 迁移；不机械补每个目录的 quality/checks；不复制固定模型/路径/canary/GT 引用；instruction、environment、scripts 与其他冻结路径问题仅报告移交。当前 SOP 中更宽的题包建议不解除 WorkC 固定边界。
