# {{task_id}} QA 报告

## 0. 结论卡

| 字段 | 值 |
|---|---|
| overall_status | {{PASS / FAIL / PARTIAL / BLOCKED / NOT_RUN}} |
| dataset_item_status | {{ACTIVE / DEPRECATED / ABANDONED / NOT_APPLICABLE；quality-prompt 配对违规时先 DEPRECATED/ABANDONED}} |
| test_delivery_handoff_ready | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| evaluation_certified | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| platform_submission_ready | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| external_submission | {{NOT_REQUESTED / NOT_AUTHORIZED / READY_NOT_SUBMITTED / UPLOADED_NOT_SUBMITTED / SUBMITTED_UNCONFIRMED / SUBMITTED_CONFIRMED / FAILED / BLOCKED / NOT_APPLICABLE}} |
| blocking_issue_ids | {{IDs / none}} |
| C1 canonical V1 hard gate | {{PASS / FAIL / BLOCKED / NOT_RUN；command/run/digest refs}} |
| C2 independent design/carrier re-audit | {{PASS / FAIL / BLOCKED / NOT_RUN；reviewer/scope refs}} |
| C3 independent expected-value recomputation | {{PASS / FAIL / BLOCKED / NOT_RUN；comparison refs}} |
| C4 QA accounting/status reconciliation | {{PASS / FAIL / BLOCKED / NOT_RUN；reconciliation refs}} |
| report_generated_at | {{ISO-8601 with timezone}} |
| reviewer/tool_version | {{value}} |
| template_version | 1.4 |
| human_review_status | {{PASS / FAIL / PARTIAL / BLOCKED / NOT_RUN / NOT_APPLICABLE；无人工证据不得写 PASS}} |
| technical_lead_review_status | {{同上；不得由代理代签}} |
| trajectory_stage_status | {{同上；不得由本地 reward 代替}} |
| algorithm_acceptance_status | {{同上；须有正式验收证据}} |

{{用 2–4 句说明完成、未完成、弃用/阻塞和不能声称的事项。}}

## 1. 任务状态与固定边界

| 维度 | Requested | Actual | 依据/偏差原因 |
|---|---|---|---|
| target | {{test-delivery / test-harness / package}} | {{value}} | {{value}} |
| mutation | {{tests-allowlist-plus-report / report-only}} | {{value}} | {{value}} |
| execution_ceiling / reached | {{V0–V5}} | {{V0–V5}} | {{value}} |
| delivery | {{value}} | {{value}} | {{value}} |
| architecture | {{legacy / seal-rewardkit-0917 / hybrid / unresolved}} | {{value}} | {{真实加载链证据}} |

- task_id：{{value}}
- final_worktree：{{path/commit/snapshot}}
- maximum_writable_scope：`tests/**` 与根目录 `/qa_report.md`
- actual_test_allowlist：{{必须是 tests/** 的子集}}
- required_report_path：`/qa_report.md`（完成/返修/作业交付自检必须本轮生成或更新）
- frozen_paths：除实际 test allowlist 与 `/qa_report.md` 外的全部题包路径
- prohibited_runtime_dependencies：{{value}}
- external_action_authorization：{{source/time or none}}
- rule_sources / claim_ledger：{{versions, carriers, mandatory claims, advisory items, blocked claims}}
- current_sop_source / checked_at / displayed_updated_at：{{URL、核对时间、页面显示日期；不自行补年份}}
- applicable_batch / workflow_stage：{{初次修复 / 轨迹打回返修 / 负责人复核 / 算法验收；适用依据}}
- designated_auxiliary_skill / version / evidence：{{正式要求的辅助 skill；未运行不得写已通过}}
- delivery_inventory：{{legacy rubric/test，或 0917 manifest + process/output/safety checks + optional quality/prompt/reward，以及 qa_report.md}}
- secret_handling：{{确认报告和日志未写 token/cookie/password/Authorization/秘密值；仅列变量名或 secret reference}}
- prohibited_input_audit：{{确认未读取 ground_truth.json；tests/** 与 qa_report.md 对 `.pipeline/` 内容零引用，或列出已删除引用/冻结残留路径但不读取或转述其内容}}

## 2. 基线、结构库存与一致性

### 2.1 基线

| 字段 | 值 |
|---|---|
| baseline_kind | {{original package / normalized directory / pre-fix worktree / commit / platform snapshot}} |
| baseline_source / id | {{value}} |
| digest_algorithm / digest | SHA-256 / {{value}} |
| artifact_path_normalization | {{path separators/case policy; archive member policy; exclusions; traversal/duplicate checks}} |
| captured_at | {{ISO-8601}} |

### 2.1a P0 Scope Card 与 P1 Baseline Contract

| 项目 | 记录 |
|---|---|
| P0 scope card | {{target / mutation / actual tests allowlist / V0–V5 authorization / delivery / prohibited inputs / dynamic isolation preconditions}} |
| baseline revision / immutable source | {{baseline revision ID；正式来源变化时新建 revision，不覆盖旧基线}} |
| formal claim carriers / precedence / digests | {{逐项 carrier、版本/日期、SHA-256、precedence}} |
| runner / aggregation / runtime loader | {{entry command、loader path/digest、registry/aggregation path、version}} |
| score identity baseline | {{R0/T0/N0、raw→runtime identity mapping、reliability}} |
| frozen authority inputs / ownership | {{path/digest、producer、candidate reachability/writeability、mount/endpoint}} |
| candidate / service / verifier evidence roots | {{each root, producer, writeability, separation status}} |
| P1 gate disposition | {{PASS / BLOCKED / DEPRECATED / ABANDONED；缺项不得做 profile-specific 修复}} |

### 2.2 0917 结构库存（legacy 填 NOT_APPLICABLE，不机械迁移）

0917 canonical 结构固定为唯一 `tests/criteria_manifest.yaml`，以及 `tests/process`、`tests/output`、`tests/safety` 每维恰好一个 `checks.py`；`tests/process/quality.toml` 与 `tests/process/reward.toml` 可选。quality 存在时，同目录必须恰好一个 `react_prompt.md`。

| artifact / dimension | expected canonical path | discovered raw paths | canonical count | status | SHA-256 / reason |
|---|---|---|---:|---|---|
| manifest | `tests/criteria_manifest.yaml` | {{paths}} | {{0/1/>1}} | {{PASS/MISSING/DUPLICATE/AMBIGUOUS/NOT_APPLICABLE}} | {{digest/reason}} |
| process checks | `tests/process/checks.py` | {{paths}} | {{0/1/>1}} | {{status}} | {{digest/reason}} |
| output checks | `tests/output/checks.py` | {{paths}} | {{0/1/>1}} | {{status}} | {{digest/reason}} |
| safety checks | `tests/safety/checks.py` | {{paths}} | {{0/1/>1}} | {{status}} | {{digest/reason}} |
| process quality | `tests/process/quality.toml` | {{paths}} | {{0/1/>1}} | {{ABSENT_ALLOWED/PASS/DUPLICATE/AMBIGUOUS/INVALID/NOT_APPLICABLE}} | {{digest/reason}} |
| process prompt | `tests/process/react_prompt.md` | {{paths}} | {{0/1/>1}} | {{NOT_APPLICABLE/PASS/MISSING/DUPLICATE/AMBIGUOUS/TEMPLATE_INVALID}} | {{digest/reason}} |
| reward config | `tests/process/reward.toml` | {{paths}} | {{0/1/>1}} | {{ABSENT_ALLOWED/PASS/DUPLICATE/AMBIGUOUS/INVALID/NOT_APPLICABLE}} | {{digest/reason}} |

- structure_inventory_digest：{{value}}
- dimension_exactly_one_checks_status：{{PASS/FAIL/BLOCKED/NOT_APPLICABLE}}
- structure_missing / duplicate / alias / case_collision：{{exact paths and issue IDs / none}}
- structure_repair_authority：{{formal source and allowlist / none；不得补空文件、任选副本或猜加载目标}}
- deterministic_only_status：{{YES/NO/NOT_APPLICABLE；quality 缺席合法时 prompt 不得作为活跃输入}}

### 2.3 Quality–Prompt 原子配对与弃用

| 字段 | 值 |
|---|---|
| quality_path / status / digest | {{canonical path / status / SHA-256 or NOT_APPLICABLE}} |
| prompt_path / status / digest | {{canonical path / status / SHA-256 or NOT_APPLICABLE}} |
| quality_prompt_cardinality | {{0:0 deterministic-only / 1:1 / invalid details}} |
| judge | {{必须精确为 `react` / NOT_APPLICABLE / actual invalid value}} |
| prompt_template | {{必须精确为 `react_prompt.md` / NOT_APPLICABLE / actual invalid value}} |
| prompt_template_schema | {{PASS / FAIL / BLOCKED / NOT_APPLICABLE；必需变量、格式、非空}} |
| static_path_vs_runtime_loaded_path | {{MATCH / MISMATCH / UNVERIFIED / NOT_APPLICABLE}} |
| static_digest_vs_runtime_digest | {{MATCH / MISMATCH / UNVERIFIED / NOT_APPLICABLE}} |
| pairing_status | {{PASS / FAIL / BLOCKED / NOT_APPLICABLE}} |
| deprecation_trigger | {{missing / duplicate / ambiguous / judge mismatch / prompt_template mismatch / template invalid / none}} |
| dataset_item_status / disposition | {{ACTIVE / DEPRECATED / ABANDONED / NOT_APPLICABLE；违规时先弃用，不自动生成或猜 prompt}} |
| responsible_party / handoff | {{value}} |

禁止从历史 prompt、候选、Oracle、known-answer 或其他题目生成/复制/合并/猜测 prompt。配对违规的数据项不得继续声明可交付或可认证。

### 2.4 Manifest–Quality–Prompt–Runtime 一致性

| 检查 | 状态 | evidence / mismatch |
|---|---|---|
| manifest 唯一且 schema 可解析 | {{status}} | {{refs}} |
| manifest dimension/scorer/result ID ↔ 三维 checks 注册 | {{status}} | {{refs}} |
| manifest weight/source/evidence ↔ 正式 claim | {{status}} | {{refs}} |
| quality criterion ↔ manifest quality row | {{status}} | {{refs}} |
| quality judge/prompt path/digest ↔ runtime loaded input | {{status}} | {{refs}} |
| checks static/import registry ↔ runtime loaded path/digest | {{status}} | {{refs}} |
| reward config ↔ 实际聚合/归一化/门控 | {{status}} | {{refs}} |
| end-to-end manifest–quality–prompt–checks–reward–runtime consistency | {{PASS/FAIL/BLOCKED/NOT_APPLICABLE}} | {{refs}} |

- manifest–quality–prompt–checks–reward–runtime consistency：{{PASS/FAIL/BLOCKED/NOT_APPLICABLE；与上表及 runtime loaded path/digest 一致}}

`criteria_manifest.yaml`、`react_prompt.md`、维度目录、quality/reward/结构文件本身均不新增 R/T/A 身份；创建、再生成或修改这些载体本身 `A=0`。

## 3. 身份基线、物理定义与计数

### 3.1 数据字典与恒等式

| 符号 | 定义 | 数值 |
|---|---|---:|
| R0 | 0917：冻结基线 canonical process quality 中每个可解析 `[[criterion]]` 条目均计 1（重复/缺失 id 仍计并另报 issue）；legacy：被实际评分链消费的稳定 rubric 身份 | {{R0}} |
| T0 | 0917：三维 canonical checks 中被实际评分链消费的独立最终 result ID；legacy：被实际评分链消费的独立评分 `test_*` | {{T0}} |
| N0 | R0 + T0 | {{N0}} |
| AR | 新增且被评分链消费的 rubric/criterion 身份 | {{AR}} |
| AT | 新增、注册且被评分链消费的 scoring test/check result ID | {{AT}} |
| A | AR + AT | {{A}} |
| DR | 删除/合并的原始 rubric/criterion 数 | {{DR}} |
| DT | 删除/合并的原始 test/check 数 | {{DT}} |
| D | DR + DT | {{D}} |
| R1 | R0 + AR - DR | {{R1}} |
| T1 | T0 + AT - DT | {{T1}} |
| N1 | R1 + T1 = N0 + A - D | {{N1}} |
| F | 已确认、修复且适用验证 PASS/FRESH 的独立 issue 数 | {{F}} |

- identity / dedup rule：{{0917 R0 按冻结基线 canonical quality 的可解析 [[criterion]] 条目计数，重复/缺失 id 仍分别计入且另报 issue，不得按稳定 ID 去重；T0、legacy 及 runtime-consumed 库存按实际评分链消费的稳定身份统计；factory multi-ID 按 ID；repeat/retry 不增加}}
- legacy R0 rule：{{仅实际评分链消费的稳定 rubric；assertion-message-only、错误文本、注释、fixture 字符串或未注册常量为 non-case}}
- structural-non-identity rule：manifest、prompt、目录、quality/reward 配置及其他结构载体不单独贡献 R/T/A 身份
- excluded non-cases：helper、fixture、setup、diagnostic、preflight、未注册/未消费项、禁用项、assertion-message-only constants 及 {{others}}
- raw-to-final identity mapping：{{raw path/ID → runtime-consumed stable identity → inherited/new/deleted/blocked；逐项列出}}
- baseline reliability / ratio disposition：{{RELIABLE / N/A with reason}}
- 恒等式例外：{{none / explanation}}

### 3.2 物理、状态与运行时计数

| 快照 | 层级 / 状态 | Rubric/Criterion | Test/Check | 总计 | 条目或异常 ID |
|---|---|---:|---:|---:|---|
| 基线 | physical definitions | {{value}} | {{value}} | {{value}} | {{IDs；0917 quality 按物理 criterion 条目列出}} |
| 基线 | active inventory | {{value}} | {{value}} | {{value}} | {{IDs/entry refs}} |
| 基线 | discarded inventory | {{value}} | {{value}} | {{value}} | {{IDs/entry refs + discard reasons}} |
| 基线 | collected/registered | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 基线 | runtime-consumed stable identities | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终 | physical definitions | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终 | active inventory | {{value}} | {{value}} | {{value}} | {{IDs/entry refs}} |
| 最终 | discarded inventory | {{value}} | {{value}} | {{value}} | {{IDs/entry refs + discard reasons}} |
| 最终 | collected/registered | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终 | runtime-consumed stable identities | {{value}} | {{value}} | {{value}} | {{IDs}} |

0917 `R0` 取冻结基线 physical quality criterion 条目数，不以 active、discarded、registered 或 runtime-consumed 数替代；重复/缺失 ID 逐条计入并另报。弃用或 discarded 条目不得冒充 active/runtime 身份；配对门失败、整项弃用或基线不可靠时两项比率仍为 `N/A`。

异常：orphan={{IDs}}；ghost={{IDs}}；duplicate identity={{IDs}}；duplicate registration={{IDs}}；cross-dimension={{IDs}}；unknown registration={{IDs}}；message-only rubric constants={{IDs}}；invalid mapping={{IDs}}。

## 4. Issue、要求与归因台账

| issue_id | root_cause_key | invariant_id | 类别 | formal source | requirement_kind | 受影响 case / non-case | attribution | 状态 | 修复位置 | permanent_regression_ref | change-impact / refreshed-run | verification_refs | freshness |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {{ISSUE-001}} | {{key}} | {{P3-I#}} | {{漏检/过松/过严/结构/配对/映射/基础设施/冻结/非case}} | {{source}} | {{MANDATORY/ADVISORY}} | {{IDs/scope}} | {{candidate_failure/harness_noise/infrastructure_failure/not_applicable}} | {{OPEN/FIXED/BLOCKED/DEPRECATED/ABANDONED/ACCEPTED/OUT_OF_SCOPE/DISPUTED}} | {{仅 tests/** 授权位置；只读发现可列冻结证据}} | {{minimal counterexample + positive case + expected + run ID；无法构造则 BLOCKED}} | {{changed path/field → invalidated controls/runs → fresh replacements}} | {{run IDs}} | {{FRESH/STALE/UNVERIFIED}} |

- 已发现 issue：{{count}}
- mandatory 未满足：{{count and IDs}}
- advisory 建议：{{count and IDs；未采用不升级为失败}}
- `F`（FIXED + PASS + FRESH）：{{F}}
- OPEN / BLOCKED / DEPRECATED / ABANDONED / ACCEPTED / DISPUTED：{{counts and IDs}}
- 受影响唯一原始 case：{{count and IDs}}
- 非 case issue：{{count and IDs}}
- 去重说明：{{same root cause / independent fixes}}

### 4.1 轨迹反馈逐项归因

- feedback_source / task identity / digest：{{refine.json 或正式反馈}}
- provided_trajectory_refs / inspected / missing：{{列出全部；不将一条冒充全部}}

| test/check ID | 正式条件与计算链 | Agent 实际行为 / 输出 | 跨轨迹比较 | 三分归因 | refine 行为 + 操作/不修改依据 | evidence refs |
|---|---|---|---|---|---|---|
| {{ID}} | {{参数→公式→正确值/判据}} | {{逐轨迹事实}} | {{一致/波动/污染}} | {{candidate_failure/harness_noise/infrastructure_failure}} | {{修改授权 test / 不修改正确 test / BLOCKED / OUT_OF_SCOPE}} | {{refs}} |

候选真错只解释测试为何不改，不写候选修复方案。必须改 instruction、环境或冻结 harness 才能消解的问题不得写成已修复。

### 4.2 Candidate / Harness-noise / Infrastructure 汇总

| attribution | issue/event IDs | evidence | 对 overall/evaluation 的影响 | disposition |
|---|---|---|---|---|
| candidate_failure | {{IDs}} | {{refs}} | {{value}} | {{value}} |
| harness_noise | {{IDs}} | {{refs}} | {{value}} | {{isolate/retry/fix/block}} |
| infrastructure_failure | {{IDs}} | {{refs}} | {{value}} | {{handoff/block}} |

## 5. Case 变化与 QA 指标

### 5.1 新增/删除明细

| case_id | 类型 | 动作 | 来源 claim / authority | 原身份或 replacement | 实际消费/绑定 | 适用验证 |
|---|---|---|---|---|---|---|
| {{ID}} | {{rubric/criterion/test/check}} | {{add/delete/merge/split/rename/move}} | {{source}} | {{IDs}} | {{yes/no}} | {{run ref}} |

纯改名、移动、描述调整、身份保持格式迁移，以及 manifest/prompt/reward/结构文件创建或变更不计新增。新 criterion 身份计 `AR+1`，新 check result ID 计 `AT+1`；拆分时每层最多一个后继继承原身份。

### 5.2 指标

- **错误率 = F / N0 = {{percent}}（{{F}}/{{N0}}）**
- **漏召率 = A / (N0 + A) = {{percent}}（{{A}}/{{N0 + A}}）**

使用原始整数计算后乘 100，常规四舍五入至最多两位并去尾零，括号整数不约分。错误率可超过 100% 且不截断；两项均为描述性 QA 数据，不是阈值、PASS/FAIL、Oracle/nop、reward、gate 或 runner 分母。

{{N0=0：错误率 N/A（0/0）；A>0 时漏召率 100%（A/A），否则 N/A（0/0）。基线不可靠、结构或配对未决时两项均 N/A，不猜数。}}

## 6. Service / Credential Preflight

不得写秘密值；只记录变量名、secret reference、挂载状态和脱敏结果。

| preflight item | expected source/mount | status | evidence (redacted) | failure attribution |
|---|---|---|---|---|
| service endpoint / connectivity | {{value}} | {{PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE}} | {{ref}} | {{infrastructure_failure/none}} |
| credential reference / mount | {{env var name or secret ref, no value}} | {{status}} | {{ref}} | {{infrastructure_failure/none}} |
| model / judge availability | {{value}} | {{status}} | {{ref}} | {{infrastructure_failure/none}} |
| runner/image/evidence mounts | {{value}} | {{status}} | {{ref}} | {{infrastructure_failure/none}} |
| isolation / writable output | {{value}} | {{status}} | {{ref}} | {{harness_noise/infrastructure_failure/none}} |

- preflight_overall：{{PASS/BLOCKED/NOT_RUN/NOT_APPLICABLE}}
- secret_redaction_check：{{PASS/FAIL}}
- dynamic_execution_disposition：{{PROCEED/BLOCKED/NOT_APPLICABLE}}

### 6.1 P2 Evidence Trust Ledger

每个 score-bearing identity 一行。candidate-owned evidence 只能证明候选行为，不能成为独立真值；live service 成功响应（包括 `[]`）是权威结果，禁止回退到 candidate-writable 文件。

| criterion / runtime ID | formal claim / trigger | authority truth source | producer / ownership | candidate reachable or writable | mount / endpoint / digest | fallback policy | live-empty / forged-file / unavailable expected result | run IDs / freshness |
|---|---|---|---|---|---|---|---|---|
| {{ID}} | {{claim / applicability}} | {{source}} | {{verifier/authority-owned / candidate-owned / infrastructure-owned}} | {{yes/no + basis}} | {{value}} | {{NONE or formally allowed behavior}} | {{expected values and attribution}} | {{refs}} |

- P2 gate disposition：{{PASS / BLOCKED / DEPRECATED / ABANDONED}}。
- 每条正向过程或完成度 claim 若没有非空、可信的 authority truth source，必须写 `BLOCKED`；不得借 agent 日志、文件副本、叙述或 hash 转化为 PASS。

## 7. 验证证据、HTML Evidence 与新鲜度

| run_id | 验证项 | scope | authority | 状态 | 时间 | 结果摘要 / RC | evidence_ref | freshness |
|---|---|---|---|---|---|---|---|---|
| {{run-id}} | {{structure/parser/bootstrap/collect/known-answer/persona/runner/oracle/nop/etc.}} | {{targeted/full}} | {{local-wrapper/official-runner/platform}} | {{status}} | {{start/end}} | {{summary}} | {{artifact}} | {{FRESH/STALE/UNVERIFIED}} |

每个 run 绑定：

```text
structure_inventory_digest = manifest + canonical path/status inventory
grader_digest          = legacy consumed rubrics/tests；0917 manifest + 3 checks + optional quality + paired prompt + reward + judge helpers
manifest_digest        = SHA-256 or NOT_APPLICABLE
quality_digest         = SHA-256 or ABSENT_ALLOWED/NOT_APPLICABLE
prompt_path / prompt_status / prompt_digest_or_NOT_APPLICABLE = canonical path + status + SHA-256 or NOT_APPLICABLE
checks_digests         = process/output/safety
reward_digest          = SHA-256 or ABSENT_ALLOWED/NOT_APPLICABLE
runtime_loaded_paths_and_digests = actual loader observations
runner_digest          = test.sh / runner / aggregation config
rules_digest           = active claim carriers and versions
fixture_digest         = inputs and formal mappings
candidate_digest       = candidate / Oracle / nop / control artifact
candidate_identity     = role and immutable identifier
conversation_digest    = conversation evidence when applicable
evidence_digest        = audit / trajectory / frozen evidence
probe_digest           = dynamic probe and isolation wrapper
environment_digest     = image / lockfile / verifiable environment identity
config_digest          = non-secret effective settings
service_credential_preflight_status = redacted result
result_digest          = result artifact
```

`FRESH` 要求当前全部适用输入摘要、路径和 runtime 加载一致且范围足够；任一变化使旧结果 `STALE`。不得把定向回归写成全量，不得拼接不同 run。

### 7.0 P3 Invariant / Mutation Matrix 与 P4 Change-Impact Ledger

| invariant_id | 不变量 / 正式依据 | 最小正反例或变异 | expected result | changed path/field | 失效的 claim / identity / validator / aggregation | 必跑 control / run | replacement run / freshness |
|---|---|---|---|---|---|---|---|
| {{I#}} | {{scope/source/topology/weight/non-vacuity/no-fallback/trajectory/anchor/attribution/freshness}} | {{single-variable mutation}} | {{PASS/FAIL/BLOCKED and attribution}} | {{path/field}} | {{refs}} | {{refs}} | {{run ID / FRESH or remaining BLOCKED}} |

- 每个确认的 tests-side 缺陷必须关联一个常驻回归：最小反例、正例、预期、issue ID、run ID 和 freshness。无法构造时保持 `BLOCKED`，不得标 `FIXED`。
- P4 exit disposition：{{PASS / BLOCKED / UNVERIFIED}}。任何受影响行 `STALE/UNVERIFIED`，或不同 run 被拼接为整体 PASS 时，`evaluation_certified` 必须为 `NO/BLOCKED`。

### 7.0b RewardKit 版本契约（批次指令：harbor-rewardkit==0.2.0）

| 检查 | 状态 | evidence / mismatch |
|---|---|---|
| 题包依赖声明确切 pin `==0.2.0`（非 `0.2.*`/范围/裸包名） | {{status}} | {{Dockerfile/依赖位置与原文；冻结路径问题记 OUT_OF_SCOPE/BLOCKED}} |
| `test.sh` 版本断言为精确比较（非前缀匹配） | {{status}} | {{断言语句}} |
| 本地验证环境 harbor-rewardkit 实际版本 | {{0.2.0 / 其他}} | {{解析方式与输出；非 0.2.0 则相关结果 UNVERIFIED}} |
| 每个 run 标注实际解析版本 | {{status}} | {{run digest 中的版本记录}} |
| 版本差异导致的准则数量/权重影响已排查 | {{status}} | {{0.2.0 vs 0.2.1 注册差异；装饰器/`rk.` 成对状态核查}} |

- rewardkit_version_contract：{{PASS / FAIL / BLOCKED / NOT_APPLICABLE（legacy 题）}}；返修"准则数量/权重不符"时，版本核对先于注册写法修改。

### 7.0a C1–C4 交付前 QA 融合

#### C1 Canonical V1 Hard Gate

| canonical command / entrypoint | workdir | input/grader/validator digests | scope | started/finished | RC | output/result digest | status |
|---|---|---|---|---|---:|---|---|
| {{value}} | {{value}} | {{value}} | {{schema/parser/mapping/aggregation/carrier/drift controls}} | {{times}} | {{RC}} | {{refs}} | {{PASS/FAIL/BLOCKED/NOT_RUN}} |

- canonical-entry discovery basis：{{actual runner/validator/self-test chain；不得只把多个局部 PASS 拼成入口}}
- C1 execution status / validation result：{{未建立/未运行入口 = NOT_RUN + blocker；已运行发现测试侧 defect = FAIL；非测试侧 infrastructure 中断 = BLOCKED；完整成功 = PASS；静态已知 defect 另列 issue，不被 NOT_RUN 隐藏}}
- schema/TOML/YAML inventory and mutation controls：{{carriers, allowed keys/cardinality/types, unknown-field policy, single-variable failures}}
- C1 limitations：{{V1 不替代 V2+ import/harness/candidate/Oracle/nop/judge certification}}

#### C2 独立设计与 Source-carrier 覆盖复审

| reviewer / independence basis | scope / input digests | carrier inventory / integrity | score-identity and authority closure | new or remaining findings | disposition |
|---|---|---|---|---|---|
| {{value；不是人工/负责人代签}} | {{claims, identities, carriers, runtime}} | {{exact normalized paths, versions/digests, consumers, policy-gated integrity/canary}} | {{PASS/FAIL/BLOCKED}} | {{issue IDs/none}} | {{PASS/FAIL/BLOCKED/NOT_RUN}} |

#### C3 独立 Expected-value 复算

| value/claim ID | formal non-prohibited source | independent derivation / tool | recomputed value | implementation/manifest/report values | three-way result | issue/run refs |
|---|---|---|---|---|---|---|
| {{ID}} | {{carrier/version/digest}} | {{formula/script/ref}} | {{value or BLOCKED/N/A}} | {{three values}} | {{MATCH/MISMATCH/BLOCKED}} | {{refs}} |

不得用 Oracle、nop、judge、ground truth 或历史题数值替代独立推导。无法独立推导时保持 `BLOCKED/N/A`。

#### C2a 逐判据对抗反例审计

- TESTS_HASH / 与同轮 C2/C3 指纹一致：{{digest；不一致即停止报错，不生成错位报告}}
- 实跑覆盖 / 等价解覆盖：{{M/N 条 float 判据 ≥1 实跑反例；M/N 条硬编码判据 ≥3 等价形态；未实跑清单与理由}}
- 宿主环境声明：{{bash/jq/docker/rewardkit 可用性；可能因宿主-容器差异失真的反例}}

| angle_id | 方向 | 反例类型 | 构造输入 | 期望分 | 实际分 | 实跑/静态推演 | 结论 / issue refs |
|---|---|---|---|---|---|---|---|
| {{ID}} | {{under-strict / over-strict / 可达性 / 环境期望 / SHALLOW}} | {{占位/伪回执/同数量异身份/等价形态/twin/乱码路径/…}} | {{最小反例}} | {{value}} | {{value}} | {{run/推演}} | {{E/W/通过 + refs}} |

静态推演必须列反例本体与预测分，否则视为未审。全表零反例时重新逐判据检查，确属穷尽须逐条说明。

#### C4 QA 平账、状态对账与重启轮次

| cycle_id | frozen-input/diff digest | C1 | C2 | C3 | findings / changed evidence | restart_from | final disposition |
|---|---|---|---|---|---|---|---|
| {{cycle}} | {{digest}} | {{status/run}} | {{status/review}} | {{status/ref}} | {{IDs/none}} | {{P gate/C1/none}} | {{PASS/STALE/BLOCKED}} |

| reconciliation | expected relation | observed | status / evidence |
|---|---|---|---|
| identity counts | `N0=R0+T0`；`R1=R0+AR-DR`；`T1=T0+AT-DT`；`N1=N0+A-D` | {{value}} | {{PASS/FAIL/N/A + refs}} |
| issue metrics | `A=AR+AT`；`D=DR+DT`；`F` 仅 FIXED+PASS+FRESH | {{value}} | {{status}} |
| issue/run freshness | 每个 FIXED issue 有常驻回归与当前 digest 的 FRESH run | {{value}} | {{status}} |
| blockers/status | blocker 必须投影到受影响状态；overall 不得覆盖底层 evidence | {{value}} | {{status}} |
| readiness separation | V1 handoff 与 V2+ evaluation certification 分开 | {{value}} | {{status}} |
| allowlist/prohibited references | changed paths 闭合；tests/report 不引用 `.pipeline/` 内容 | {{value}} | {{status}} |

任何 C2/C3/C4 发现导致 tests 或结论证据变化时，旧 C1–C4 全部 `STALE`，回到最早受影响的 P gate，并从 C1 完整重启；禁止跨 cycle 拼接 PASS。

### 7.1 HTML Evidence

| evidence_id | source artifact/path | artifact digest | parser/method | selector/fragment | escaping/visibility check | bound criterion/check | status |
|---|---|---|---|---|---|---|---|
| {{HTML-001}} | {{path/ref}} | {{SHA-256}} | {{method/version}} | {{selector/fragment}} | {{PASS/FAIL/BLOCKED}} | {{ID}} | {{PASS/FAIL/BLOCKED/NOT_APPLICABLE}} |

记录原始 HTML artifact、解析方式、可见文本/属性边界、转义/脚本内容处理和绑定关系；只粘贴转述文本不能替代原始证据 digest。

### 7.2 0917 Bootstrap / Known-answer / Persona

| 场景 | 输入/身份 digest | 预期 | 实际 | run_id / evidence | 状态 / freshness |
|---|---|---|---|---|---|
| bootstrap / loader closure | {{value}} | {{manifest、三维 canonical checks、可选 quality–prompt、可选 reward 与 runtime 加载/聚合全部闭合}} | {{value}} | {{refs}} | {{value}} |
| known-answer positive | {{value}} | {{formal expected}} | {{value}} | {{refs}} | {{value}} |
| deterministic negative | {{value}} | {{formal expected}} | {{value}} | {{refs}} | {{value}} |
| persona / conversation boundary | {{value}} | {{formal expected or NOT_APPLICABLE}} | {{value}} | {{refs}} | {{value}} |

## 8. LLM ≤40% 复算与四负控

- applicability / formal source：{{0917 适用依据；legacy 填 NOT_APPLICABLE}}
- llm_effective_reward_share / bound：{{沿真实嵌套聚合、归一化、门控、fallback 的公式与最终占比；必须 ≤40%，未知 BLOCKED}}
- calculation_inputs_digests：{{manifest / quality / prompt / process-checks / output-checks / safety-checks / reward / runner-and-aggregation-config / runtime-result digests}}
- aggregation_input_change_recalculation（manifest / quality / prompt / process-output-safety 3 checks / reward / runner-and-aggregation / runtime / effective weights）：{{任一适用输入变化时，旧占比复算与相关 runs 均 STALE，必须重新复算并回归；PASS/STALE/NOT_APPLICABLE}}
- acceptance_rule / source：{{正式通过判据；未给统一数值门不得擅造 cutoff}}

| 负控 | 单变量变更 / candidate digest | 一致 evidence / environment refs | process/output/safety/quality 分项 | 总 reward / 正式门 | 状态 / run_id / freshness |
|---|---|---|---|---|---|
| 关键词空壳 | {{value}} | {{value}} | {{value}} | {{value}} | {{value}} |
| 错误数值 | {{value}} | {{value}} | {{value}} | {{value}} | {{value}} |
| 缺关键内容 | {{value}} | {{value}} | {{value}} | {{value}} | {{value}} |
| 移除所有 judge 的事实检查消融 | {{保留 deterministic facts；隔离外部配置}} | {{value}} | {{value}} | {{实际分母/归一化/正式门}} | {{value}} |

四负控未执行如实列 `BLOCKED/NOT_RUN`。局部静态探针不能认证完整 runner，不同 evidence 上的分数下降不能宣称单变量因果。

### 8.1 多轮复测稳定性

- requested / actual repeat count：{{实际记录；不得虚构固定轮数}}
- independent_run_ids / scopes / digests：{{每轮独立证据}}
- all_results / inconsistent_items / attribution / disposition：{{全部结果；修改后旧轮次 STALE；不挑最好}}

## 9. Post-trajectory 环境事件台账

| event_id | stage | trajectory/run_id | observed_at | environment_cause | exact_normalized_missing_path | expected_source_or_mount | responsible_party | evidence | status | repair_disposition |
|---|---|---|---|---|---|---|---|---|---|---|
| {{ENV-001}} | `post-trajectory` | {{ref}} | {{ISO-8601 with timezone}} | {{verified cause}} | {{单个精确规范化路径}} | {{image/platform/mount/source}} | {{party}} | {{refs}} | {{BLOCKED/OUT_OF_SCOPE}} | `NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF` |

- missing_path_classification：{{environment-provided path missing / candidate-required deliverable missing / unresolved}}
- classification_basis：{{formal source + healthy-harness evidence；不得仅凭 ENOENT 猜测}}
- candidate_missing_delivery_issues：{{若本应由候选交付，列 candidate_failure IDs，不写入环境移交}}

每个精确规范化缺失路径单独占一行；不得使用目录概述、glob，或在一个单元格中合并多个路径。仅在环境根因已证实、责任归属明确且测试侧无进一步合法修复时使用固定 `repair_disposition`。

## 10. 状态向量与收口状态

| 维度 | 状态 | 证据 | 限制/阻塞 |
|---|---|---|---|
| review_completeness | {{PASS/FAIL/PARTIAL/BLOCKED/NOT_RUN/NOT_APPLICABLE}} | {{refs}} | {{value}} |
| structure_inventory | {{status}} | {{refs}} | {{value}} |
| quality_prompt_pairing | {{status}} | {{refs}} | {{value}} |
| manifest_runtime_consistency | {{status}} | {{refs}} | {{value}} |
| grader_design | {{status}} | {{refs}} | {{value}} |
| parser_static | {{status}} | {{refs}} | {{value}} |
| runner_health | {{status}} | {{refs}} | {{value}} |
| bootstrap | {{status}} | {{refs}} | {{value}} |
| known_answer | {{status}} | {{refs}} | {{value}} |
| persona | {{status}} | {{refs}} | {{value}} |
| html_evidence | {{status}} | {{refs}} | {{value}} |
| service_credential_preflight | {{status}} | {{refs}} | {{value}} |
| llm_share_and_negative_controls | {{status}} | {{refs}} | {{value}} |
| oracle | {{status}} | {{refs}} | {{value}} |
| nop | {{status}} | {{refs}} | {{value}} |
| difference_audit | {{status}} | {{refs}} | {{value}} |
| package_integrity | {{status}} | {{refs}} | {{value}} |
| external_submission | {{status}} | {{refs}} | {{value}} |
| P0–P4 contract gates | {{PASS/BLOCKED/UNVERIFIED}} | {{baseline/topology/invariant/freshness refs}} | {{missing gate or none}} |
| C1 canonical V1 hard gate | {{status}} | {{command/run/digest refs}} | {{missing coverage or none}} |
| C2 independent design/carrier re-audit | {{status}} | {{review refs}} | {{findings/blocker or none}} |
| C3 independent expected-value recomputation | {{status}} | {{comparison refs}} | {{mismatch/blocker or none}} |
| C4 QA accounting/status reconciliation | {{status}} | {{reconciliation/cycle refs}} | {{contradiction or none}} |

- `test_delivery_handoff_ready=YES` 的前提：授权 tests/report、P0–P4 静态交付契约、allowlist diff 与 C1–C4 均闭合且四门均 `PASS`。`evaluation_certified=YES` 还要求全部适用 V2+ 动态门 `FRESH/PASS`，并且没有把不同 run/cycle 的局部结果拼接成整体认证。实际 mount/endpoint provenance 或 candidate run 未授权/未执行时，handoff 可按静态契约判断，但 evaluation 必须为 `NO/BLOCKED`。

| 收口环节 | 状态 | 复核人/授权来源 | artifact digest / evidence refs | 未完成原因 |
|---|---|---|---|---|
| human_review_status | {{value}} | {{value}} | {{value}} | {{value}} |
| technical_lead_review_status | {{value}} | {{value}} | {{value}} | {{value}} |
| trajectory_stage_status | {{value}} | {{value}} | {{value}} | {{value}} |
| algorithm_acceptance_status | {{value}} | {{value}} | {{value}} | {{value}} |

- trajectory_5_percent_rule：{{仅适用阶段；来源、真实分子/分母/范围、是否核实；不等于 F/N0 或 reward}}
- batch_table / task_row / authorization：{{value}}
- batch_table_completion / error_rate / miss_rate / writeback_status：{{未授权仅列待登记值，NOT_REQUESTED/NOT_AUTHORIZED}}

无人员或阶段证据不得写 PASS；overall_status 是状态向量摘要，必须附派生理由。

## 11. Ready、平台与最终差异审计

| 判定 | 状态 | reason_codes | blocking_issue_ids | evidence_refs |
|---|---|---|---|---|
| test_delivery_handoff_ready | {{YES/NO/BLOCKED/NOT_APPLICABLE}} | {{codes}} | {{IDs}} | {{refs}} |
| evaluation_certified | {{YES/NO/BLOCKED/NOT_APPLICABLE}} | {{codes}} | {{IDs}} | {{refs}} |
| platform_submission_ready | {{YES/NO/BLOCKED/NOT_APPLICABLE}} | {{codes}} | {{IDs}} | {{refs}} |

- platform/task ID / environment：{{value}}
- authorization source / time：{{value}}
- upload_at / submit_at：{{value}}
- receipt/submission ID：{{value}}
- platform artifact digest：{{value}}
- displayed final status / last_verified_at：{{value}}
- artifact missing / changed / unexpected_extra：{{normalized paths}}
- actual_changed_paths：{{必须满足 ⊆ actual tests/** allowlist ∪ {/qa_report.md}}}
- tests allowlist 外零变化审计：{{PASS/FAIL；/qa_report.md 为唯一例外}}
- qa_report 本轮生成/更新时间与状态：{{value}}
- ZIP CRC / traversal / duplicate members / top-level：{{result}}
- 外部包输出位置：{{题包外或用户明确指定的外部位置}}
- excluded run artifacts：{{paths}}
- artifact_digest（排除报告）：{{value}}
- 题包外交付清单中的 report_digest（如要求）：{{external path/value；不得在题包内创建 sidecar}}
- 外部动作实际执行情况：{{value}}
- 明确 NOT_RUN 项及原因：{{items}}
- 最终声明：{{确认本轮已生成/更新 /qa_report.md，说明零变化审计、弃用/阻塞、完成状态与不能声称事项。}}

“保存”“已上传”“本地打包完成”或平台显示“进行中”均不能写成 `SUBMITTED_CONFIRMED`；领取/提交下一题须另有授权。