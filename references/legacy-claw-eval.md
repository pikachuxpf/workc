# 旧式 ClawEval / PinchBench 参考

本参考只用于 WorkC 作业的测试侧完成、返修和作业验证，覆盖正式评分架构仍以 `rubrics.py + test_outputs.py` 为主的旧式题。该架构继续有效，不要求普遍迁移。题包内可修改内容不得超出实际授权的 `tests/**` 子集；完成、返修或作业交付自检必须同步生成或更新根目录 `qa_report.md`。除根目录 `qa_report.md` 这个固定例外外，所有 tests 外业务文件、environment、solution、task/materialization 和根目录脚本均冻结，只可作为 evidence 读取。不同批次可能是多轮对话/工具调用型，也可能是输出文件型；以本题材料和 runner 为准。

纯咨询或明确不修改时只做 V0/chat-only：不修改、不运行、不生成报告或打包，并明确本轮未完成作业。完整包交付前必须在本轮更新 `qa_report.md`；tests 未变化时使用 `report-only`，包只能写到题包外或用户明确指定的外部位置。文件名只作候选架构信号；两套结构同时被实际加载时标记 `hybrid`，加载链不完整或无法确认时标记 `unresolved`，沿 runner 确认真实入口，不得把 legacy 机械迁移成 Seal。有效 legacy 继续按本文件验收，不强迫迁移。只有当前任务的正式格式、schema 和实际 runner 已明确采用 0917 新版 Seal/RewardKit 模型时，旧式 `rubrics.py`、`test_outputs.py` 才是迁移输入，而不再是并列身份源；此时转用 [seal-rewardkit.md](seal-rewardkit.md) 的必要 `tests/criteria_manifest.yaml`、process/output/safety 三维唯一 `checks.py`，以及可选的 process quality/react prompt 与 reward 规则。

## 1. 固定主流程

先理解 instruction、persona、resources 与 runner 的正式要求，再建立 rubric/test 覆盖基线；随后只修改和优化授权的 `tests/**` 子集，执行适用验证，最后生成或更新根目录 `qa_report.md` 并做差异审计。业务材料只用于推导 tests 应检查什么，不由 WorkC 修改；QA 报告是作业收尾，不是独立质检入口。

## 2. 材料与权威

常见材料包括 instruction、persona、fixtures/resources、grader、rubrics、tests、judge 和 test.sh。

- 多轮对话型：grader 可能提供 MUST_ASK、澄清质量、最终答案和批次安全规则；instruction 是首轮用户请求；persona 是后续披露、模糊回答、错误说法和格式约束。0818 防回归要求 bootstrap/环境就绪问题不占任务问题上限；正式 evidence 已有答案时不强制 ask-first 或重复追问。persona 只描述输入场景，按消息/工具真实 actor 绑定，不能把用户、工具或第三方行为错绑给候选。
- 输出文件型：从 instruction 与原始 resources 独立推导输出路径、schema、字段、数值、排序、去重、冲突和 CSV 规则。HTML judge/test 应读取渲染后的可见语义、结构与可访问文本，不以固定字符切片、CSS 类名或 JavaScript 源码代替内容判定。
- grader 的默认权威角色可能被批次专用正式规则覆盖；先查版本和适用范围。
- PinchBench 与 ClawEval 均完全忽略 `ground_truth.json`：WorkC 的分析、返修、复检、报告、tests、候选、runner 与独立 reviewer 不读取、不引用、不用于人工交叉验证或运行时测试（见 [SKILL.md「不可解除的边界」](../SKILL.md#1-不可解除的边界)）。期望值一律从 instruction 与原始 resources 独立推导；其他流程的单独授权或读取结果不得进入 WorkC 的 claim、expected value、evidence 或认证。solution 和预计算字段不能成为运行时依赖，也不能覆盖独立推导。

## 2. Rubric 设计

以下规则适用于 runner 当前确实加载 `rubrics.py/test_outputs.py` 的 legacy 评分契约。不要仅因新版存在 `quality.toml` 就要求所有旧题迁移，也不要给一个有效 legacy 题机械补建 `quality.toml`、`checks.py` 或 `criteria_manifest.yaml`。反之，若当前任务正式 schema/runner 已声明新版契约，则 legacy rubric 只能作为迁移时提取语义与来源的输入：最终身份按新版 `quality.toml` 的 `[[criterion]]` 与实际注册的 `checks.py` check 分别确定，manifest 只是聚合投影。

每条 rubric：

- 只检查一个独立事实；
- 采用唯一稳定 `RUBRIC_*` 名称；
- 与一个评分 test 一一对应；
- 简洁、正向、可验证；先识别当前批次 profile，不使用跨批次统一上限。已知 ClawEval 旧式 profile 常用不超过 300 字符（按最终字符串计，包含空白与标点）；TB2 标注 profile 使用不超过 400 字符且不超过 3 句。题目级正式规则可在其范围内覆盖，无法确认 profile 时阻断长度合规结论而不猜测；
- 不内含冗余 PASS/FAIL 说明，不引用其他 rubric 变量，不堆关键词示例；
- 同一错误说法的即时纠正和后续一致性若是同一事实，应合并而非重复计权；
- “建议研究/可考虑研究”保持建议性质，除非权威来源明确升级，不得改写为强制研究；
- 仅出现在 assertion message、异常文本或注释中的 rubric 名称不是独立评分身份，不计入基线、映射或问题数。

有条件触发的对话 rubric 必须写清未触发时如何处理，并让 test 提供用户侧 evidence。不要给纯工具或纯文件题机械添加对话 rubric。

## 3. 常见覆盖角度

按材料存在性选择，不是固定配额：

- 澄清覆盖：正式 evidence 已给出的参数可直接使用，不得强制先确认或重复追问；只有缺失、冲突或模糊且影响结果的参数才询问；
- 深入追问：题目真正要求的领域考量；
- 工具调用：列表、详情、条件调用、关键参数、次数、禁止调用；
- 跨服务推理：实体关联与因果链；
- A–H 安全：仅保留当前题适用项；
- 数据陷阱：预计算不一致、状态矛盾、空值排除、重复/冲正、专业矛盾；
- 难度模式：术语误用、错误主张、中途改值、格式、模糊披露；
- 答案质量与会话质量；
- 输出存在、解析、schema、字段、值、计数、集合、排序和一致性；
- 数值结果：记录公式、精确理论值、舍入和容差来源。

历史同前缀题只提供候选角度；每项记录迁移、拆分、纠正或不适用及依据。

## 4. Test 与 evidence

`test_outputs.py` 不得内联评分题干，只 import rubric 常量。每条评分 test 只使用一种业务判定机制；加载 evidence 的前置校验不算重复业务评分。

对话 evidence 以当前 runner schema 为准。标准适配器中常用：

- 任意助手轮次行为：全部 assistant 文本；
- 最终答案质量：最后一条 assistant 消息；
- 行为依赖用户触发：完整对话；
- 第一轮是否过早下结论：第一条 assistant 消息。

确定性事实用代码断言：文件、结构、数值、集合、ID、排序、调用记录、请求参数和哈希。只要 expected value 可由 instruction 与原始资源唯一推导，就不得仅用 judge、关键词或宽容差代替精确断言。语义事实才用 `assert_judge`。关键词仅用于必须出现/不得出现的精确数字或枚举，并须有用户触发保护；不能替代语义判断。

## 5. 缺失证据

- 健康环境中 instruction 明确要求由候选交付的核心文件、字段、回答或调用缺失：FAIL；
- 场景未触发：skip/不适用或题目定义的自动通过；
- 明确可选 conversation/服务未提供：按 runner 规则 excluded/skip；
- 未披露或不可用的服务、环境缺凭据、runner 未挂载必需日志、judge 故障、harness noise/配错：BLOCKED/infrastructure，不算候选失败；
- 普通 `if missing: return` 会产生假通过，不用于核心输出。

Post-trajectory 才发现环境缺失时，在 `qa_report.md` 对该项逐行记录发现阶段、`observed_at`、环境原因、单个 `exact_normalized_missing_path`、预期来源/挂载和 evidence；每个精确规范化缺失路径独占一行，禁止目录概述、glob 或合并多个路径。状态写 `BLOCKED/OUT_OF_SCOPE`，并写 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF`。记录完成后该项无需其他测试侧修复，移交环境/授权负责人；不得猜凭据、补环境文件或将其折算为候选 FAIL。

## 6. 输出型 PinchBench

常见路径映射是 `/app/data/` ↔ `environment/resources/`、`/app/output/` ↔ `environment/output/`，但必须由当前题确认。检查：

1. 文件存在与真实格式；
2. 顶层类型、表头、字段名、字段类型；
3. 所有 instruction 明示条件；
4. 独立复算的关键数值与计数；
5. 主/次排序键和边界；
6. 去重后的来源集合；
7. 权威来源冲突解决；
8. CSV 行数、编码、多值分隔符；
9. 可执行脚本的合成输入动态探针（仅在授权和隔离充分时）。

旧文档中出现的 criteria.md、固定条数或固定目录只适用于其特定版本，不能覆盖当前 `rubrics.py` 任务，更不能推广到 Seal。

## 7. 人工复核

AI 草拟的 rubric、test、expected value、judge verdict 和 QA 摘要不得直接定稿。人工必须回到 grader/批次规则、instruction、persona、原始 resources 和实际 evidence 复核，至少覆盖所有失败项、安全项、条件触发项以及 code/judge 分工。Oracle 1.0 或 judge pass 不能替代规则审查。

## 8. 运行与类名

先沿 `test.sh` 确认 pytest、CTRF、class/tier 权重、judge cache 和返回码传播。import/collect 会执行模块顶层代码，属于 V2 而非纯静态。类名只有在 runner 映射或冻结规则要求时不可改；不得新增 runner 不认识的 tier。

Oracle/nop 使用全新、隔离的 output、audit、conversation、run 和 judge cache。修改 rubric/test/judge prompt 后旧结果失效，必须重跑受影响完整范围。

## 9. Pinch / ClawEval 增量复审层（legacy-pinch）

本节吸收 `pinch_qa_new` 的新质检方法，但不替换前文的 WorkC legacy 契约。固定顺序仍是 WorkC 的 P0–P4、修改授权 tests、C1–C4；D0–D5 只用于在该流程内做更细的独立设计和反例复审。

### 9.1 D0–D5 与 WorkC 门的对应

| 阶段 | 做什么 | 对应 WorkC 门 |
|---|---|---|
| D0 | 隔离 student answer，确认 task/materialization、实际 tests allowlist、V0–V5 上限和禁读项。 | P0/P1 |
| D1 | 只读 instruction、persona、正式 resources/fixtures、policy 和 runner contract，逐项抽取显性义务、隐性条款、关键数值、工具端点/参数、输出文件/字段。 | P1 |
| D2 | 建立独立 obligation inventory，冻结后才读 student criteria/checks。 | P2 |
| D3 | 先判答案空间，再选 code/judge：唯一事实、有限多解、开放生成/方法选择分别处理。 | P2/P3 |
| D4 | 按独立义务对照 student 实现，区分等价覆盖、漏覆盖、过松、过严、题面外新增、重复和证据不足。 | P3/C2 |
| D4.5 | 对本轮修改、受影响或有具体风险的 deterministic rule 下钻相关 helper/parser/baseline/排除分支，构造与风险相称的反例；无关 rule 不逐项穷举。 | P3/C2a |
| D4.6 | 使用模型或 MAAS 做六视角疑点发现，之后逐项回到源码、正式来源和 evidence 复现。 | C2/C2a advisory |
| D5 | 运行适用的 V0–V5、更新回归和 `qa_report.md`，平账并处理 freshness。 | P4/C4 |

独立 obligation row 至少包含：

```text
claim_id | formal source/carrier | atomic obligation | trigger/applicability
answer_space(unique/finite-multiple/open) | code-or-judge | evidence object
producer/ownership/writeability | runtime identity | expected result | attribution
```

`D0`–`D5` 是 legacy/Pinch 专项复审流程，不是每项 WorkC 作业的默认完整清单。常规任务按受影响义务和风险执行最小适用闭环；只有用户/正式 profile 要求完整 legacy/Pinch 专项认证时，才运行并记录 D0–D5 声明范围内的全量复审。启用 D0–D3 设计流程时，完成独立设计前不得用 student criteria/checks、参考 tests、baseline 或 solution 收窄答案。`ground_truth.json` 和 `.pipeline/` 始终不得读取或引用。tests 外问题若构成阻塞，只在根 `qa_report.md` 记录 `OUT_OF_SCOPE/BLOCKED`，不修改其文件。

### 9.2 答案空间与判定器可靠性

- 只有题面或稳定输入使结果唯一、可定位且可复算时，才写 code rule；固定字段、精确值、封闭完整枚举、固定 schema/path/hash 属于此类。
- 有限多解必须接受完整合法集合或可验证成员谓词，不能把参考答案的一种水果、文案、命名或实现路线钉成唯一解。
- 开放生成、报告/总结/根因/建议、方法选择和自然语言纠正交由允许的语义 judge；prompt 描述正确语义，不列举一份 golden 原文。
- 代码必须从目标字段/对象/表格/调用记录解析，不能用全文裸搜词数、文件存在、`exit 0`、数量、stem、marker 或单个 hash 代替目标事实。数量/哈希只能作先决门，除非另有成员身份/字段值/来源核验。
- 解析器必须覆盖实际 evidence 的嵌套/group、list/dict、Unicode/编码和路径变体；空/`None`/异常解析必须 fail closed 并单独归因，不能吞错或按通过处理。
- C3 对 expected value、公式、单位、时区、依赖和环境能力独立复算；可复核的复算结果可以推翻错误 gold，无法复核则 `BLOCKED/N/A`，不猜数。

### 9.3 D4.5 确定性规则反例表

仅对本轮修改、受影响或有具体风险的 score-bearing deterministic rule 填写此表；记录纳入理由和未覆盖风险。正式 legacy/Pinch 专项审计需要声明完整覆盖时，才扩展到该专项范围内的全部规则。范围内适用的合法-PASS 与违规-FAIL 反例必须可复核，适用而缺失时标 `NOT_RUN/BLOCKED`，不能写等价覆盖。

| rule | helper/parser/baseline/排除分支 | 目标 evidence 与比较粒度 | 合法-PASS 最小反例（适用时） | 违规-FAIL 最小反例 | 实跑/静态推演 | issue/run/freshness |
|---|---|---|---|---|---|---|
| {{ID}} | {{具体函数/分支}} | {{对象/字段/内容/来源}} | {{不同于参考但合规的输入与期望分 / N/A 理由}} | {{最小违规输入与期望分}} | {{refs/推导}} | {{refs}} |

依据具体 profile/risk 纳入空证据、vacuous `all/any`、伪造 agent-writable 文件、live service 空值/不可达、叙述-only 动作、配置正文锚点污染、premature order、嵌套对象、list/dict、Unicode 路径、数量相同但成员替换、等价 API/工具形态和否定语境等探针。没有纳入理由或必要反例时不得宣称该范围已审完。

### 9.4 D4.6 模型第二审（advisory）

Pinch 的六个 review lens 可作为疑点清单：对象绑定/精确计数、baseline/保留内容、输入域/解析遍历、逃逸与隐私、弱代理语义、规则契约。模型输出不是判定结果：

1. 每条疑点必须由人工回到正式 source、实现和 evidence 复现；
2. 能复现的进入 issue/P3 mutation matrix，并补永久回归；
3. 不能复现的保留 `UNRESOLVED/BLOCKED` 处置和原因；
4. 模型未提到的规则不代表 PASS；仍按本轮修改、影响与具体风险范围执行 D4.5，专项完整认证时覆盖声明的完整范围；
5. 不得把模型输出当作 `human_review_status`、`technical_lead_review_status` 或算法验收签名。

不得把源 `llm_rule_review.py` 的 token 参数、任意输出路径或模型名称直接写入 WorkC secrets、题包或报告秘密值。WorkC judge 仍按本 Skill 第 10 节处理。

### 9.5 Pinch A–H 安全复审

按适用性检查以下维度：A Prompt Injection、B Credential Exposure、C Ambiguous Action Confirmation、D Data Integrity Verification、E Draft-Only Enforcement、F Read-Only/Tool Restraint、G Domain Safety、H Urgency Pressure Resistance。对适用维度记录触发证据、期望行为、硬 check/judge/reference carrier、producer/ownership 和最小正反例；不适用写 `NOT_APPLICABLE`，不能为凑齐八类添加空壳 check。

源安全规范中的 veto、weight 和“最终安全得分”公式只有在当前正式 runner/aggregation 明确实现且可复核时才适用。legacy binary、0917 float/Likert 和其他 profile 不得混用；实际 safety 结果沿 runner 链独立核对。

### 9.6 源脚本限制与 tests-only 处置

`pinch_qa_new/scripts/` 下的 `audit.py`、`static_check.py`、`deep_check.py`、`rewardkit_check.py`、`llm_rule_review.py`、`run_tests_sandbox.py` 不复制进 WorkC。它们存在以下不能越权的限制：audit 的 sidecar/任意报告路径、启发式架构分流、rewardkit checker 的递归别名/regex 发现、inventory-specific deep formula、MAAS token-env 读取缺陷、sandbox 文档声称但实现缺失的 Oracle fallback，以及 stub judge 不能证明语义正确。它们最多作为 V0/V1 线索，不能替代真实 loader、schema-safe validator、V2–V5、evidence ownership、freshness 或 C1–C4。

任何要求改 instruction、environment、task.toml、solution、scripts、grader/judge、Dockerfile、业务输出或其他 tests 外文件的问题，都只在根 `qa_report.md` 记录路径、证据、归因和 `OUT_OF_SCOPE/BLOCKED`；不创建 sidecar、不复制副本、不将报告当作修复旁路。tests 无需改动时使用 `report-only`。

### 9.7 第二轮 legacy-pinch 硬门

以下规则只细化 legacy/Pinch 的复审，不改变 WorkC 外层 P0–P4、C1–C4 或实际题包写入边界。

1. **模板不是正式来源**：`criteria_manifest.template.yaml` 与 `checks.template.py` 即使出现在题包、下载目录或历史资料中，也只能登记为 `NON_AUTHORITATIVE` authoring scaffold。不得从其中推导题面、claim、expected value、权重、证据路径、doc/object ID、schema、函数签名、RewardKit 版本、`.pipeline`/`ground_truth` 规则或 runner/registry/aggregation 身份。正式 manifest/checks/schema/loader/runner 和非禁读 frozen evidence 优先；不一致时标 `TEMPLATE_INVALID` 或 `BLOCKED`，不猜、不自动迁移。
2. **修改后必须同步根报告**：任何接受的授权 `tests/**` 变更都要在同一收口周期更新根 `qa_report.md`，写明 changed paths、issue、验证/未运行项、freshness、allowlist 和状态。缺报告是 `tests_changed_without_qa_report_update=BLOCKED/NOT_COMPLETE`；不得用 `qa_report_skill抽检.md`、sidecar、staging 或补丁副本替代。tests 不变时仍是 `report-only`；纯咨询才 `chat-only`。
3. **环境/需求异常直接废弃或移交**：instruction、environment、task/需求、solution、runner、Dockerfile、grader/judge、业务输出或其他 tests 外问题不能修。根报告标出精确路径和 evidence，按责任写 `OUT_OF_SCOPE/BLOCKED` 或 candidate/harness/infrastructure；若需求/环境使该项不再有可认证契约，停止常规返修并按正式 profile 标 `DEPRECATED/ABANDONED`。不得创建 placeholder 或把移交写成 PASS。
4. **code/judge 去耦合**：事实、数值、集合/成员、排序、对象 ID、时间范围/时区/单位、文件/字段/schema/path、调用参数和最终状态必须由代码覆盖；移除 judge 的负控仍拒绝对应错误。概念、根因、建议、对比论证、开放报告与自然语言质量必须由语义 judge 验证，不能用固定关键词列表代替；正式 mandatory semantic claim 必须进入最终 gate，judge 沉默、未运行、不可用或不能复现都不是 PASS。
5. **D4.5 anti-hack 反例**：仅对本轮修改、受影响或有具体风险的 deterministic rule 做风险相称的合法不同实现、最小违规及 anti-hack 检查；未纳入规则不要求逐项穷举。记录输入/期望分/实际分或静态推演、相关 helper/parser/baseline/exclusion、owner/writeability。指定 doc/object ID 只能检查正式允许集合，禁止全量枚举“任意 ID 有效即通过”；适用时检查同数量不同成员、目标缺失但其他对象存在、错误对象正确 token、候选可写 evidence、count/hash/name proxy。空 evidence、解析空、live `[]`/服务失败、叙述-only、正文锚点污染、premature order、嵌套/list-dict/Unicode/path/timezone 按当前规则依风险验证并 fail closed。
6. **D4.6 仅 advisory**：MAAS/模型发现必须回到正式 source、源码和 evidence 人工复现；不能复现就 `UNRESOLVED/BLOCKED`。模型未报告不代表 PASS，也不能代签人工、负责人或算法状态。
7. **freshness**：实质输入、证据或结论变化时，将依赖该变化的旧 run/门标记 `STALE`，从最早受影响 P gate 更新，并重跑受影响且适用的 C 门；canonical V1 输入或整体证据基线变化时从 C1 重启。纯排版/转录不触发重启，不得跨轮拼接 PASS。
