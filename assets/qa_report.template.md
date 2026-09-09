# {{task_id}} QA 报告

## 0. 结论卡

| 字段 | 值 |
|---|---|
| overall_status | {{PASS / FAIL / PARTIAL / BLOCKED / NOT_RUN}} |
| test_delivery_handoff_ready | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| evaluation_certified | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| platform_submission_ready | {{YES / NO / BLOCKED / NOT_APPLICABLE}} |
| platform_status | {{NOT_REQUESTED / NOT_AUTHORIZED / READY_NOT_SUBMITTED / UPLOADED_NOT_SUBMITTED / SUBMITTED_UNCONFIRMED / SUBMITTED_CONFIRMED / FAILED / BLOCKED / NOT_APPLICABLE}} |
| blocking_issue_ids | {{IDs / none}} |
| report_generated_at | {{ISO-8601 with timezone}} |
| reviewer/tool_version | {{value}} |
| template_version | 1.0 |

{{用 2–4 句说明完成了什么、未完成什么、不能声称什么。}}

## 1. 任务状态与边界

| 维度 | Requested | Actual | 依据/偏差原因 |
|---|---|---|---|
| target | {{test-delivery / test-harness / package}} | {{value}} | {{value}} |
| mutation | {{tests-allowlist-plus-report / report-only}} | {{value}} | {{value}} |
| execution_ceiling / reached | {{V0–V5}} | {{V0–V5}} | {{value}} |
| delivery | {{value}} | {{value}} | {{value}} |
| architecture | {{value}} | {{value}} | {{真实加载链证据}} |

- task_id：{{value}}
- final_worktree：{{path/commit/snapshot}}
- maximum_writable_scope：`tests/**` 与根目录 `/qa_report.md`
- actual_test_allowlist：{{必须是 tests/** 的子集}}
- required_report_path：`/qa_report.md`（完成/返修/作业交付自检必须为本轮生成或更新）
- frozen_paths：除实际 test allowlist 与 `/qa_report.md` 外的全部题包路径
- prohibited_runtime_dependencies：{{value}}
- external_action_authorization：{{source/time or none}}
- rule sources / claim ledger：{{versions, carriers, blocked claims}}

## 2. 基线与计数口径

### 2.1 基线

| 字段 | 值 |
|---|---|
| baseline_kind | {{original package / normalized directory / pre-fix worktree / commit / platform snapshot}} |
| baseline_source / id | {{value}} |
| digest_algorithm / digest | SHA-256 / {{value}} |
| normalization_profile | {{path case/separator; exclusions; ZIP raw bytes or normalized member manifest; duplicate/path traversal checks}} |
| captured_at | {{ISO-8601}} |

### 2.2 数据字典与恒等式

| 符号 | 定义 | 数值 |
|---|---|---:|
| R0 | 冻结基线中 rubric/criterion 稳定计分身份数 | {{R0}} |
| T0 | 冻结基线中 scoring test/registered check 稳定计分身份数 | {{T0}} |
| N0 | R0 + T0 | {{N0}} |
| AR | 新增且有效的 rubric/criterion 数 | {{AR}} |
| AT | 新增且有效的 scoring test/registered check 数 | {{AT}} |
| A | AR + AT | {{A}} |
| DR | 删除/合并的原始 rubric/criterion 数 | {{DR}} |
| DT | 删除/合并的原始 test/check 数 | {{DT}} |
| D | DR + DT | {{D}} |
| R1 | R0 + AR - DR | {{R1}} |
| T1 | T0 + AT - DT | {{T1}} |
| N1 | R1 + T1 = N0 + A - D | {{N1}} |
| F | 已确认、修复且 fresh 适用验证通过的独立 issue 数 | {{F}} |

- identity / dedup rule：{{stable IDs; F by root cause; A by scoring case}}
- rename / move / split / merge rule：{{mapping}}
- excluded non-cases：helper、fixture、setup、diagnostic、preflight、未注册且不属于正式 manifest/评分契约的实现、禁用项及 {{others}}
- orphan 口径：正式 manifest/rubric 身份即使未注册/未映射，仍保留在 R0 并登记 issue；不得作为 non-case 排除
- 恒等式例外：{{none / explanation}}

## 3. 物理定义、收集与有效映射

| 层级 | Rubric/Criterion | Test/Check | 总计 | 异常稳定 ID |
|---|---:|---:|---:|---|
| 基线物理定义 | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 基线 collected/registered | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 基线有效闭合映射 | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终物理定义 | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终 collected/registered | {{value}} | {{value}} | {{value}} | {{IDs}} |
| 最终有效闭合映射 | {{value}} | {{value}} | {{value}} | {{IDs}} |

异常：orphan={{IDs}}；ghost={{IDs}}；duplicate identity={{IDs}}；duplicate registration={{IDs}}；unknown registration={{IDs}}；invalid weight/evidence mapping={{IDs}}；helper miscount={{IDs}}。

## 4. Issue 台账

| issue_id | root_cause_key | 类别 | 规则来源/claim | 受影响原始 case | 新增 case | 非 case 范围 | 状态 | 修复位置 | verification_refs | freshness |
|---|---|---|---|---|---|---|---|---|---|---|
| {{ISSUE-001}} | {{key}} | {{漏检/过松/过严/映射/基础设施/冻结/非case}} | {{source}} | {{IDs}} | {{IDs}} | {{scope}} | {{OPEN/FIXED/BLOCKED/ACCEPTED/OUT_OF_SCOPE/DISPUTED}} | {{FIXED 仅可填写 tests/** 内位置；只读发现可填 tests 外证据路径}} | {{run IDs}} | {{FRESH/STALE/UNVERIFIED}} |

汇总：

- 已发现 issue：{{count}}
- `F`（FIXED + 适用验证 PASS + FRESH）：{{F}}
- 未修复 OPEN / BLOCKED / ACCEPTED / DISPUTED：{{counts and IDs}}
- 受影响唯一原始 rubric/criterion：{{IDs}}
- 受影响唯一原始 test/check：{{IDs}}
- 受影响唯一原始 case 并集：{{count and IDs}}
- 非 case issue：{{count and IDs}}
- 去重说明：{{same root cause / independent fixes}}

## 5. Case 变化与 QA 指标

### 5.1 新增/删除明细

| case_id | 类型 | 动作 | 来源 claim / authority | 原身份或 replacement | 有效注册/绑定 | 适用验证 |
|---|---|---|---|---|---|---|
| {{ID}} | {{rubric/criterion/test/check}} | {{add/delete/merge/split/rename/move}} | {{source}} | {{IDs}} | {{yes/no}} | {{run ref}} |

纯改名、移动、描述调整、helper、未注册/未绑定或未验证项不计新增。拆分时最多一个后继项继承原身份；删除必须说明替代项、权威来源和覆盖是否保留。

### 5.2 指标

- **错误率 = F / N0 = {{percent}}（{{F}}/{{N0}}）**
- **漏召率 = A / (N0 + A) = {{percent}}（{{A}}/{{N0 + A}}）**

错误率表示“已修复验证问题密度”，会受修复授权影响；`F` 按 issue，`A` 按新增计分 case。使用原始整数计算后乘 100，常规四舍五入至最多两位并去掉末尾零，括号整数不约分。错误率可超过 100% 且不截断；漏召率超过 100% 表示计数或公式错误。两项均是描述性 QA 数据，不是阈值、PASS/FAIL、Oracle/nop、reward、gate 或 runner 分母。

{{N0=0：错误率 N/A（0/0）；A>0 时漏召率 100%（A/A），否则 N/A（0/0）。基线不可靠时两项均 N/A，不猜数。}}

## 6. 验证证据与新鲜度

| run_id | 验证项 | scope | authority | 状态 | 时间 | 结果摘要 / RC | evidence_ref | freshness |
|---|---|---|---|---|---|---|---|---|
| {{run-id}} | {{parser/collect/runner/oracle/nop/etc.}} | {{targeted/full}} | {{local-wrapper/official-runner/platform}} | {{status}} | {{start/end}} | {{passed/failed/skipped/reward/gate/num-den/RC}} | {{artifact}} | {{FRESH/STALE/UNVERIFIED}} |

每个 run 绑定：

```text
grader_digest         = rubric/criterion + test/check + judge helper/prompt
runner_digest         = test.sh / runner / reward and aggregation config
rules_digest          = active claim carriers and versions
fixture_digest        = input resources and formal mappings
candidate_digest      = candidate / Oracle / nop artifacts
candidate_identity    = role and immutable identifier
conversation_digest   = conversation evidence when applicable
evidence_digest       = audit / trajectory / frozen evidence
probe_digest          = dynamic probe and isolation wrapper
environment_digest    = image / lockfile / verifiable environment identity
config_digest         = non-secret effective runtime settings
result_digest         = result artifact
```

`FRESH`：当前适用输入摘要完全一致且运行范围足够；`STALE`：任一适用输入变化或后续修改影响覆盖；`UNVERIFIED`：摘要、证据或范围无法确认。时间新不等于 fresh。不得把定向回归写成全量，不得拼接不同 run。

报告自引用：`artifact_digest` 排除 `qa_report.md` 和允许的运行产物；报告完成后只能在题包外的交付清单或外部包元数据中记录 `report_digest`，不得在题包内创建 sidecar，也不得把完整文件 hash 写回被散列的报告正文。最终差异审计在报告写完后执行。

## 7. 状态向量

| 维度 | 状态 | 证据 | 限制/阻塞 |
|---|---|---|---|
| review_completeness | {{PASS/FAIL/PARTIAL/BLOCKED/NOT_RUN/NOT_APPLICABLE}} | {{refs}} | {{value}} |
| grader_design | {{status}} | {{refs}} | {{value}} |
| parser_static | {{status}} | {{refs}} | {{value}} |
| runner_health | {{status}} | {{refs}} | {{value}} |
| oracle | {{status}} | {{refs}} | {{value}} |
| nop | {{status}} | {{refs}} | {{value}} |
| difference_audit | {{status}} | {{refs}} | {{value}} |
| package_integrity | {{status}} | {{refs}} | {{value}} |
| external_submission | {{status}} | {{refs}} | {{value}} |

基础设施错误与候选失败分别列出：{{details}}。overall_status 只是上述向量的摘要，必须附派生理由。

## 8. Ready 与平台状态

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

“保存”“已上传”或“本地打包完成”均不能写成 `SUBMITTED_CONFIRMED`。

## 9. 差异、交付审计与最终声明

- missing / changed / unexpected_extra：{{normalized paths}}
- actual_changed_paths：{{必须满足 ⊆ actual tests/** allowlist ∪ {/qa_report.md}}}
- tests allowlist 外零变化审计：{{PASS/FAIL；/qa_report.md 为唯一例外}}
- qa_report 本轮生成/更新时间与状态：{{value}}
- ZIP CRC / path traversal / duplicate members / top-level：{{result}}
- 外部包输出位置：{{必须位于题包外或用户明确指定的外部位置}}
- excluded run artifacts：{{paths}}
- artifact_digest（排除报告）：{{value}}
- 题包外交付清单中的 report_digest（如项目要求）：{{external path/value；不得在题包内创建 sidecar}}
- 外部动作实际执行情况：{{value}}
- 明确 NOT_RUN 项及原因：{{items}}
- 最终声明：{{确认本轮已生成/更新 /qa_report.md，说明实际 test allowlist 外是否零变化、完成状态、限制与不能声称的事项。}}
