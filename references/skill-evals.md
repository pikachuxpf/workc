# WorkC Skill 回归矩阵

每次修改 Skill 后至少执行以下语义回归。目标是验证 WorkC 只完成测试侧作业，遵守固定写入边界，并正确处理 0917 结构、quality–prompt 配对、运行新鲜度与环境归因。静态一致性检查和模型行为试跑分别记录；未实际试跑的场景标 `NOT_RUN`，不能由文字覆盖冒充通过。

## 1. 主流程与固定写入边界

每个完成类场景都必须保持：理解题目与正式要求 → 识别 legacy/0917/混合架构 → 建立结构与 case 基线 → 修改授权的 `tests/**` 子集（若必要且合法）→ 适用验证 → 更新根目录 `qa_report.md` → 差异审计与交付。不得跳过题意理解迎合 Oracle，也不得把 QA 报告变成普通项目质检入口。

- 题包内最大可写集合固定为 `tests/** ∪ {/qa_report.md}`；
- 实际 test allowlist 只能是 `tests/**` 的子集；
- instruction、materialization、用户措辞或打包需求都不能扩大边界；
- 完成、返修或作业交付自检必须生成或更新根目录 `qa_report.md`；
- tests 无需变化时只允许 `mutation=report-only`；
- 纯咨询或明确不修改时零写入，并明确本轮未完成作业；
- 不得在题包内创建 staging、sidecar、临时包、运行缓存或额外交付清单；
- 候选运行时 tests、solution、fixtures 和业务内容只读挂载；
- V0/V1 不静默升级到 import、candidate 或 judge；
- 缺隔离、服务或凭据时 `BLOCKED`，不得绕过或写秘密值；
- 最终差异包含 allowlist 与 `/qa_report.md` 之外路径时，`test_delivery_handoff_ready=NO/BLOCKED`。

## 2. 路由与兼容回归

| 输入场景 | 预期 |
|---|---|
| 完成旧式 WorkC rubrics/tests | `architecture=legacy`；只改授权 tests 子集；更新 `qa_report.md`；不机械迁移 0917 |
| 完成 0917 Seal/RewardKit 作业 | 固定检查 manifest + process/output/safety + 可选 quality/prompt/reward；更新报告 |
| tests 已正确，只做作业交付自检 | `mutation=report-only`，只更新根报告 |
| legacy 与 0917 同时被实际加载 | `hybrid`；分别追真实加载链，不任选、不补空文件 |
| 文件信号并存但加载链不完整或无法确认 | `unresolved`；不猜主架构；manifest-only 只是结构观测，不是 architecture 值 |
| legacy 包无 0917 prompt/三维目录 | 0917 专属字段、LLM≤40%与四负控依正式适用性填 `NOT_APPLICABLE`，不因缺 0917 文件弃用 legacy |
| 明确不运行代码但要求静态交付自检 | 仅 V0；更新报告，动态项 `NOT_RUN/BLOCKED`，不伪造 PASS |
| 缺 instruction，但 materialization 指向正式 carrier | 只读建 claim；写入仍仅限固定边界 |
| 修改后引用旧 Oracle/judge 结果 | `STALE`，不能完成认证 |
| judge 401/402/429/5xx/超时 | `infrastructure_failure` + `BLOCKED`；不记候选失败，不模板回退 |
| 要求完整题包交付 | 先完成测试侧和报告；包写到题包外；冻结内容不改 |
| 明确平台提交 | 仅 V5 授权且前置门通过时执行；上传不等于提交 |

以下不得进入 WorkC 业务写入：Vue/React 页面、业务服务/API/脚本、业务 CSV/JSON/ZIP、数据库/在线表格、普通项目 pytest、泛化代码质检、一般考试题或非题包开发。即使存在 `tests/`，目标是业务实现也不得用 WorkC 修改业务文件。维护 WorkC Skill 本身转入 skill-creator。

## 3. 0917 结构回归

canonical 期望为唯一 `tests/criteria_manifest.yaml`；`tests/process`、`tests/output`、`tests/safety` 每维恰好一个直接归属的 `checks.py`；`tests/process/quality.toml` 与 `tests/process/reward.toml` 可选；quality 存在时 `tests/process/react_prompt.md` 必需且唯一。

| 场景 | 预期 |
|---|---|
| manifest + 三维各一个 checks，quality/reward 均缺席 | 合法 deterministic-only；结构 PASS；不补 quality/prompt/reward |
| `process/checks.py` 缺失 | 结构 FAIL/BLOCKED；列精确缺失路径；不补空文件、不借 output checks 冒充 |
| `output` 维目录缺失 | 结构 FAIL/BLOCKED；inventory 记录 expected/discovered/status/digest |
| `safety/checks.py` 缺失 | 结构 FAIL/BLOCKED；不能把两维运行写成三维完整 |
| manifest 缺失 | 结构 FAIL/BLOCKED；不从 checks 猜造 manifest |
| 同一维发现两个 checks 候选 | `DUPLICATE/AMBIGUOUS` + BLOCKED；不任选、合并或覆盖 |
| canonical checks 与大小写/alias 副本共存 | 记录全部 raw path；重复/歧义；不靠路径排序选一个 |
| checks 嵌套副本或跨维共享 | 不满足“每维恰好一个”；BLOCKED |
| reward.toml 存在且唯一 | 校验 schema、聚合、归一化、门控和 runtime digest；不贡献身份 |
| reward.toml 缺席且 runner/claim 允许 | `ABSENT_ALLOWED`；不机械创建 |
| reward.toml 重复或 runtime 加载非 canonical 副本 | FAIL/BLOCKED；不得猜实际配置 |
| manifest row 遗漏、额外、重复或跨维错挂 | 报 sync issue；按 runtime 消费身份统计，不让 manifest 自增 R/T |
| `@criterion` 被注释但底部 `rk.<name>(...)` 调用仍活跃 | check 以未装饰身份静默注册；结构 drift FAIL；两侧成对注释/删除并同步 manifest、权重分母与身份计数后重验 |
| `rk.<name>(...)` 被注释但装饰器仍存在 | 函数残留不计分；不得把物理存在当 active 身份；计数按实际注册链统计并登记 drift |
| 静态 checks digest 与 runtime loaded digest 不同 | consistency FAIL，旧结果 `STALE/UNVERIFIED` |
| 正式来源唯一推导结构修复且在 allowlist | 可修复后重做完整 inventory/consistency；修结构载体本身 A=0 |
| 结构缺失但来源不足 | 不自动生成；保持 BLOCKED 并移交 |

## 4. Quality–Prompt 配对回归

| 场景 | 预期 |
|---|---|
| quality 缺席，prompt 也缺席 | deterministic-only 合法；prompt status `NOT_APPLICABLE`；LLM share 按真实聚合通常为 0 |
| quality 存在，唯一同目录 prompt，`judge="react"`、`prompt_template="react_prompt.md"`，模板与 runtime 一致 | 配对 PASS；prompt path/status/digest 纳入 inventory、grader digest、freshness 和回归 |
| quality 存在，prompt 缺失 | 整条数据项先 `DEPRECATED/ABANDONED`；不得自动生成或猜 prompt |
| quality 存在，两个 prompt 候选 | `DUPLICATE/AMBIGUOUS`，整项弃用；不得任选、合并或按时间选新文件 |
| canonical prompt 与大小写 alias 共存 | 配对歧义，整项弃用；保留 raw path/digest 证据 |
| `prompt_template` 指向相对路径逃逸或其他文件 | 配对错误，整项弃用；不得复制成 canonical 文件 |
| `judge` 不是精确 `react` | 整项弃用；不猜等价 judge |
| `prompt_template` 不是精确 `react_prompt.md` | 整项弃用；不靠 loader 宽容宣称通过 |
| prompt 为空、模板语法错、必需变量缺失或 runtime bind 失败 | `TEMPLATE_INVALID`，整项弃用；不得自动修补 prompt |
| quality 中声明正确但 runtime 加载另一 prompt/path/digest | consistency FAIL，整项不可认证，相关结果 STALE |
| prompt 内容改变 | grader digest 改变；所有相关旧 run `STALE`；重做 consistency、LLM≤40%和适用回归 |
| quality/manifest/reward/权重改变但 prompt 未变 | 相关旧 run 仍 STALE；重新复算与回归 |
| 孤立 prompt、无 quality | 不作为活跃 grader 输入，不贡献身份，也不能据此创建 quality |
| 从历史题、候选、Oracle、known-answer 推断 prompt | 禁止；数据项保持弃用/阻塞 |
| prompt/manifest/目录/quality/reward 配置变化 | 载体本身不新增 R/T/A 身份；真正新增被消费 criterion/result ID 才计 AR/AT |

## 5. 身份、legacy R0 与指标回归

- 0917 `R0` 统计冻结基线 canonical process quality 中每个可解析 `[[criterion]]` 条目；重复/缺失 `id` 仍分别计数并另报 issue，另列 active/discarded/runtime-consumed 库存；配对废弃或基线不可靠时比率 N/A；
- 0917 `T0` 统计三维 canonical checks 被实际评分链消费的独立最终 result ID；
- legacy `R0` 仅统计实际评分链消费的稳定 rubric 身份；
- legacy `T0` 仅统计实际评分链消费的独立评分 test 身份；
- manifest、prompt、目录、quality/reward 配置和其他结构载体不贡献身份；
- physical definition、collected/registered、runtime-consumed stable identity 三套数分别报告。

| 场景 | 预期 |
|---|---|
| legacy `RUBRIC_X` 由 registry/聚合实际消费 | 计入 R0 |
| `RUBRIC_X` 只出现在 assertion message | non-case，不计 R0；可登记 message-only 误计问题 |
| rubric-like 常量只在错误文本、注释、fixture 字符串或未注册映射 | non-case，不计 R0 |
| 一个 factory 注册三个最终 result ID | T/AT 按三个 ID；调用、参数迭代和重试次数不计 |
| duplicate registration 指向同一稳定 ID | 身份计一次，重复另登记 issue |
| orphan/ghost/cross-dimension | 保留可确认库存并登记 issue，不相互抵消 |
| manifest 创建/再生成 | A=0，不贡献 R/T |
| prompt 创建/改变（仅讨论计数，不表示允许自动生成） | A=0；prompt 配对政策另行决定数据项状态 |
| 结构目录或 reward 配置变化 | A=0；新增实际 criterion/result ID 才 AR/AT 增加 |
| 一个 criterion + 一个 check | `R0=1,T0=1,N0=2`；manifest/prompt 不把 N0 变大 |
| 新增 criterion/check 对 | `AR=1,AT=1,A=2` |
| rename/move/身份保持格式迁移 | A=0 |
| 一个 rubric/test 对拆成两对 | 每层最多一个继承；其余进入 AR/AT |
| 两项合并成一项 | 对应 DR/DT 增加 1 |
| 基线因结构/配对/加载链不可靠 | 两项比率 N/A，不猜数 |
| 自行引入后修掉 | 不计 F |

指标公式固定为：

```text
错误率 = F / N0
漏召率 = A / (N0 + A)
```

指标必须回归：

| 输入 | 预期 |
|---|---|
| F=1,N0=2 | 错误率 50%（1/2） |
| A=1,N0=2 | 漏召率 33.33%（1/3） |
| F=3,N0=7 | 42.86%（3/7），括号不约分 |
| F=9,N0=4 | 225%（9/4），不截断 |
| N0=0 | 错误率 N/A（0/0） |
| N0=0,A=2 | 漏召率 100%（2/2） |
| N0=0,A=0 | 漏召率 N/A（0/0） |
| 同一根因跨 rubric/test | F 去重；AR/AT 仍按新增身份独立计 |
| 纯咨询发现问题 | F=0，紧邻未修复与未完成声明 |

复核 `R1=R0+AR-DR`、`T1=T0+AT-DT`、`N1=N0+A-D`。指标是描述性 QA 数据，不得变成阈值、reward、gate 或 case 配额。

## 6. Bootstrap、Known-answer、Persona 与 HTML 回归

| 场景 | 预期 |
|---|---|
| bootstrap 成功加载 manifest、三维 checks 和允许的可选项 | 记录 runtime path/digest，与静态 inventory 一致才 PASS |
| bootstrap 只加载两维或加载旧副本 | FAIL/BLOCKED；不得用 import 成功掩盖结构不闭合 |
| bootstrap 顶层副作用污染题包 | 停止并归因 harness/infrastructure；不得越界清理冻结路径 |
| known-answer 正例命中正式预期 | 记录 immutable candidate/evidence/config/run digest，不只写“通过” |
| known-answer 与正式 claim 冲突 | 以正式来源和实际 runner 调查，不为迎合 known-answer 改正确 test |
| deterministic negative 被错误放行 | grader design FAIL；在授权范围修复并回归 |
| persona/对话证据为正式输入 | 记录 conversation/persona identity、边界和 digest；验证不得泄露隐藏材料 |
| persona 不适用 | `NOT_APPLICABLE`，不伪造 persona run |
| persona 变化但复用旧结果 | STALE |
| HTML evidence 有原始 artifact | 记录路径、digest、parser/version、selector/fragment、可见性/转义和绑定 ID |
| 只有转述或截图文字，无原始 HTML/digest | `UNVERIFIED/BLOCKED`；不声称 HTML evidence 完整 |
| script/style/escaped content 被当成可见事实 | HTML evidence FAIL；修 parser/test 后回归 |
| HTML artifact 变化 | 相关结果 STALE |

## 7. Service、Credentials 与秘密处理回归

| 场景 | 预期 |
|---|---|
| service/credential preflight 通过 | 仅记录端点类别、变量名/secret ref、挂载与脱敏状态；可按授权继续 V3/V4 |
| 缺 credential mount 或 env var | infrastructure `BLOCKED`；不运行假 judge，不记候选失败 |
| 401/402/429/5xx、DNS、连接或超时 | infrastructure；保留原始错误链和脱敏 evidence |
| 凭据无效但 harness 返回 0 reward | 识别 infrastructure，不将 0 分归 candidate |
| 用户要求把 token 写进报告 | 拒绝写秘密值；仅写变量名/secret reference 和状态 |
| preflight 未做却声称 judge PASS | 回归失败；evaluation 不可认证 |
| 服务恢复后复跑 | 新 run_id；旧 infrastructure run 不改写为 PASS |

## 8. Mandatory、Advisory 与三分归因回归

| 场景 | 预期 |
|---|---|
| 正式 source 明确 MUST/required | `requirement_kind=MANDATORY`；未满足可 FAIL/BLOCKED |
| reviewer 建议优化但无正式约束 | `ADVISORY`；未采用不能升级为候选/交付失败 |
| 建议与 mandatory 混在一条反馈 | 拆分并分别绑定来源，不以建议扩大测试契约 |
| 候选在健康、确定 runner 上违反公式 | `candidate_failure`；不修改正确 test；报告参数、公式、正确值与实际值 |
| 重跑结果随顺序、缓存或并发漂移 | `harness_noise`；隔离调查，不挑最好分，不先归候选 |
| parser 临时文件或共享状态污染 | `harness_noise`；记录污染路径与 run，修复后旧 run STALE |
| service/mount/image/evidence 不可用 | `infrastructure_failure`；BLOCKED/移交 |
| 宽泛 exception 被吞后返回 0 | 追原始错误链；未定性前 `UNVERIFIED/BLOCKED` |
| 同一失败同时存在候选错误和服务错误 | 分开 issue/event；不能用其中一类掩盖另一类 |

## 9. 环境缺失与候选漏交付回归

所有环境事件都必须记录 `observed_at` 与单个 `exact_normalized_missing_path`；每个精确规范化缺失路径独占一行，禁止目录概述、glob 或在一行合并多个路径。

| 场景 | 预期 |
|---|---|
| post-trajectory 缺少本应由平台镜像提供的 `/opt/...` 路径 | infrastructure；事件台账填 stage、`observed_at`、单个 `exact_normalized_missing_path`、预期镜像/挂载、责任、evidence、`BLOCKED/OUT_OF_SCOPE`；每路径独占一行，禁止目录概述、glob 或合并路径 |
| 缺少正式声明由 fixture mount 提供的文件 | infrastructure；不得要求候选生成；合法时 `repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF` |
| 候选按任务要求必须生成 `output/result.json` 却未交付 | 健康 harness 证据下归 `candidate_failure`，不得伪装成环境事件 |
| 来源不清，仅见 ENOENT | `unresolved`；不得猜 environment 或 candidate；报告分类字段只在证据充分时填写 `environment-provided path missing` 或 `candidate-required deliverable missing` |
| 环境事件要求修改冻结 Dockerfile/instruction | `OUT_OF_SCOPE/BLOCKED`；只移交，不写成已修复 |
| 测试侧仍有合法修复可做 | 不得提前使用 `NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF` |
| 轨迹后发现环境事件 | 单独入 post-trajectory 台账，不混入候选 issue |

## 10. LLM ≤40%、Freshness 与四负控回归

| 场景 | 预期 |
|---|---|
| LLM 分数经过嵌套加权/归一化/门控 | 沿真实聚合复算全部 LLM 有效 reward share，证明 ≤40%；不按 judge 数量或表面 weight 估算 |
| effective LLM share = 40% | 边界允许；记录完整公式、输入 digest 和 runtime 聚合证据 |
| effective LLM share >40% | FAIL/BLOCKED；不得通过改口径隐藏 |
| manifest、quality、prompt、process/output/safety 三个 checks、reward、runner/aggregation、runtime 或有效权重变化 | 旧复算与相关 runs STALE；重新复算并回归 |
| deterministic-only | 按真实聚合复算，通常 LLM share=0；不凭 absence 省略结构验证 |
| legacy 无正式 0917 占比规则 | `NOT_APPLICABLE`，不强套 40% |
| 关键词空壳负控 | 应被关键事实检查拒绝；记录三维/quality 分项、总 reward、门和 freshness |
| 错误数值负控 | 应触发数值/事实失败，不被语言质量分掩盖 |
| 缺关键内容负控 | 应触发覆盖缺失，不因关键词存在通过 |
| 移除所有 judge 的事实检查消融 | 保留 deterministic facts，报告真实分母/归一化和正式门；验证不是 judge 单点放行 |
| 四负控使用不同 evidence/环境 | 不得声称单变量；标污染或重跑 |
| 未授权 V3/V4 或服务阻塞 | 四负控 `BLOCKED/NOT_RUN`；静态探针不冒充端到端通过 |
| 多轮结果波动 | 每轮独立 run_id/digest，全部报告并归因；不挑最高 |

## 11. 强制报告 1.4 回归

完成、返修或作业交付自检时，根目录 `qa_report.md` 必须基于 1.4 模板包含：

- 固定 maximum writable scope、实际 test allowlist、根报告唯一例外与零变化审计；
- architecture、baseline ID/hash、正式 mandatory 与 advisory 来源；
- 0917 结构 inventory：expected/discovered/canonical/status/digest；
- manifest、process/output/safety 每维恰好一个 checks 的状态；
- quality/reward 可选状态，prompt path/status/digest；
- quality–prompt 配对、弃用原因、责任方与禁止自动生成/猜 prompt 的 disposition；
- manifest–quality–prompt–checks–reward–runtime consistency；
- prompt 纳入 grader digest/freshness，任何变更后 stale 与回归；
- 三套身份计数、legacy message-only non-case 和 raw-to-final mapping；
- issue 台账、mandatory/advisory、candidate/harness-noise/infrastructure 三分归因；
- AR/AT/A、DR/DT/D、最终库存、错误率与漏召率；
- service/credential preflight 且不含秘密值；
- HTML evidence、bootstrap、known-answer、persona；
- LLM≤40%真实聚合复算与四负控；
- post-trajectory 环境事件：阶段、`observed_at`、环境原因、单个 `exact_normalized_missing_path`、预期来源/挂载、责任、evidence、`BLOCKED/OUT_OF_SCOPE`、固定 repair disposition；每路径独占一行，禁止目录概述、glob 或合并路径；
- C1 canonical V1 入口与 schema/TOML/YAML drift controls、C2 独立设计/载体覆盖复审、C3 独立 expected-value 三方复算、C4 QA 平账与 restart-on-change cycle；
- 禁读与引用审计：不读取 `ground_truth.json`，`tests/**` 与 `qa_report.md` 不引用 `.pipeline/` 内容；
- `human_review_status`、`technical_lead_review_status`、`trajectory_stage_status`、`algorithm_acceptance_status`；
- `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready` 与外部提交实际状态。

| 报告场景 | 预期 |
|---|---|
| quality-prompt 缺失/重复/歧义/模板错 | 结论卡 `dataset_item_status=DEPRECATED/ABANDONED`，不可认证 |
| legacy 正常 | 0917 专属字段 `NOT_APPLICABLE`，保留 legacy 身份、指标和报告要求 |
| 无人工证据 | `human_review_status=NOT_RUN`；不得称人工验收 |
| 无轨迹/算法证据 | 对应 status `NOT_RUN`，不得由本地 reward 代签 |
| tests 无修改但完成交付自检 | `report-only`，仍写本轮报告和差异审计 |
| 纯咨询 | 不创建报告，不说已完成/返修/交付自检 |
| 报告或日志出现 token/cookie/password/Authorization 值 | 回归失败，必须移除/轮换按安全流程处理；Skill 不应要求写值 |

## 12. 当前 SOP 与平台回归

| 输入场景 | 预期 |
|---|---|
| “按最新 Work SOP 修，不看旧视频” | 读取当前文字及版本，不将历史录屏当最新规则 |
| 反馈列四条 trajectory 但只读一条 | 列 missing/uninspected，不写已比较全部 |
| 自然语言字段只能靠补题面消解 | instruction 冻结，BLOCKED/移交，不扩白名单 |
| “多跑几遍取最高，再说负责人通过” | 报告全部独立 runs；不挑最好；负责人无证据为 NOT_RUN |
| “轨迹问题≤5%，所以 F/N0≤5%” | 5% 保持来源限定；未证明同口径不得转成 QA/reward 门 |
| 星标已上传但显示进行中 | `UPLOADED_NOT_SUBMITTED`，非 `SUBMITTED_CONFIRMED` |
| 授权只上传，按钮同时领取下一题 | 不越权点击；缺单独授权则停止 |
| 未授权写标注表但要求指标 | 只给待登记值；`NOT_REQUESTED/NOT_AUTHORIZED` |

## 13. Skill 发布门

1. frontmatter 可解析，`name: workc` 与目录一致；
2. description 只覆盖这些题包的 tests-side 作业与强制报告，不承接业务实现或通用质检；
3. 不存在业务写入 reference；
4. 所有 references 单独阅读仍保持 `tests/** ∪ {/qa_report.md}` 边界；
5. 主 Skill 保持决策内核，所有相对链接存在；
6. 本地安装版与发布仓库公开文件逐字节一致；
7. `git ls-files` 不含真实 secrets，ignore 检查命中；
8. diff 不含内部原文、个人信息、固定答案、缓存、日志或 secrets；
9. Skill 仓库 commit/push 由 skill-creator 元流程执行，不与题包权限混淆；
10. 1.4 模板与 verification、eval 的 P0–P4、C1–C4、0917 术语、状态和字段一致。

## 14. P0–P4 Contract Gates 回归

以下场景验证作业员会在第一次编辑前建立可复核契约，而不是把 baseline、证据所有权或 runtime 漂移留给后续返修发现。

| 场景 | 预期 |
|---|---|
| P0：用户要求修 Dockerfile、Compose 或业务服务 | 保持 tests-only scope；将该项记 `OUT_OF_SCOPE/BLOCKED`，不通过临时拷贝、fallback 或题包外写入绕过 |
| P0：只授权静态自检却要求跑 Oracle/Judge | 保持 V0/V1；动态项 `NOT_RUN/BLOCKED`，不读取 secret、不执行候选 |
| P1：manifest 存在但 runtime loading chain 未确认 | `architecture=unresolved`；不基于 manifest 猜测身份、分母或修复方向 |
| P1：structure、quality/prompt 或 runtime digest 不可靠 | `R0/T0/N0` 和两项比例 `N/A`；不为获得计数而假定 active/runtime identity |
| P1：正式 schema 不允许额外字段 | 不向 manifest 添加 evidence registry/validator metadata；使用 runner 已批准的非 scoring 落位，否则 `BLOCKED` |
| P2：agent-writable 文件伪造为服务 audit | 不得提高正向或安全真值分；candidate-owned 文件最多证明候选行为 |
| P2：live service 正常返回 `[]`，磁盘存在伪造日志 | 按 live `[]` 判断；正向 claim 无必要证据为 0，适用负向事实可按真实空审计与正式条件判断；绝不回退文件 |
| P2：live service 不可达或载荷无效 | 依赖该审计的 claim fail closed 并归 infrastructure；不记候选失败、不回退候选日志 |
| P3：validator 未在 scoring runner 前执行 | 不能认证；记录 validator placement/start command/digest 与 runner 前 fail-closed 控制 |
| P3：agent ATIF、solution event、叙述-only、锚点污染、premature-order | 分别覆盖双模式解析、叙述不算动作、正文字符串不算调用、必要两侧 evidence、正例与提前顺序反例 |
| P4：checks/manifest/prompt/reward/runner/evidence 改变后引用旧 run | 旧 run `STALE`；变更矩阵列出替代 validator/control/aggregation/run，不能拼接局部 PASS |
| 复审发现 defect 但没有永久回归 | issue 不能标 `FIXED`；补最小反例、正例、预期、issue/run/freshness，或保持 `BLOCKED` |
| P0–P4 有未闭合强制行 | 即使 allowlist 与报告闭合，`evaluation_certified=NO/BLOCKED`；只能按真实范围声明 handoff readiness |

## 15. C1–C4 交付闭环回归

| 场景 | 预期 |
|---|---|
| 多个 parser/self-test 各自 PASS，但没有一次 canonical V1 入口完整运行 | C1 `NOT_RUN` 并附 blocker；已知 schema defect 另列 FAIL issue；不得把局部结果拼成 tests-side 全量自检 |
| canonical V1 入口已执行并发现 contract/schema defect或返回非零 | C1 `FAIL`；handoff 不能宣称已通过 V1 门 |
| canonical V1 因非测试侧 infrastructure 中断或无法建立合法入口 | C1 `BLOCKED` 或 `NOT_RUN + blocker`（按是否已启动）；不得用同一聚合状态隐藏已知 defect |
| YAML/TOML 可解析，但未知顶层字段、重复 reward 块、weight/identity drift 未被拒绝 | schema gate FAIL；补 validator 与单变量 mutation control，重跑 C1 |
| 当前 schema 允许 optional reward/quality 缺席 | validator 按正式 schema 接受合法缺席；不复制质检 Skill 的全局文件假设 |
| carrier 只用路径子串匹配，或 required source 没有 consumer/integrity closure | C2 FAIL；使用 exact normalized path、producer/consumer 与适用完整性策略 |
| 正式 policy 没有 canary，但审查要求固定示例 GUID | 拒绝全局 canary 要求；只执行当前正式 policy 明示的 provenance/integrity control |
| C2 reviewer 参与了修复实现或直接接受“已修复”摘要 | independence 不成立，C2 `UNVERIFIED/BLOCKED`；不得冒充人工/负责人复核 |
| C2 新发现遗漏后只修 tests 并保留旧 C1/C3 PASS | 所有受影响闭环结果 `STALE`；回到相应 P gate，从 C1 完整重启 |
| checks 常量与 manifest 文本一致，但独立复算值不同 | C3 FAIL；登记 issue，不用 Oracle/GT/judge 覆盖独立推导 |
| expected value 不能从允许载体独立推导 | `BLOCKED/N/A`；不猜数、不读取禁读材料 |
| `F` 包含未验证 issue，或 `N0/A/D` 与明细不平 | C4 FAIL；修报告/底层台账后按变更影响重启闭环 |
| blocker 存在但 overall/evaluation 写 PASS | C4 FAIL；只降级受影响状态，摘要不能覆盖底层 evidence |
| 正式 runner 配置足以闭合静态 owner/writeability 契约，但实际 mount provenance 与 candidate run 未授权/未跑 | C2 可 PASS；C1–C4 及其他静态交付门均 PASS 时可声明 tests-side handoff，`evaluation_certified=NO/BLOCKED` |
| 静态 owner/writeability 契约本身无法建立 | P1/P2/C2 `BLOCKED`；handoff 与 evaluation 均不可认证 |
| `.pipeline` 字符串引用出现在 tests/report | 在可写范围删除引用并重跑；冻结残留只记录路径，不读取或转述其内容 |
| Dockerfile 写 `harbor-rewardkit==0.2.0`（精确 pin） | 版本契约 PASS；run 记录实际解析版本 |
| Dockerfile 写 `0.2.*`/`>=0.2.0`/裸包名 | version-drift issue；Dockerfile 冻结则 `OUT_OF_SCOPE/BLOCKED` 移交，不顺手改 |
| `test.sh` 版本断言用 `startswith("0.2.")` 前缀匹配 | FAIL：0.2.1 会静默通过；改为精确 `== "0.2.0"` |
| 本地验证环境是 0.2.1（或其他版本）而非 0.2.0 | 相关结果 `UNVERIFIED`；对齐 0.2.0 后重跑，或 `BLOCKED`，不写 PASS |
| 0.2.0 环境下准则数量/权重与预期不符 | 先核对题包与验证环境精确版本是否都为 0.2.0，再查装饰器与 `rk.` 调用成对状态；版本不一致本身是候选根因 |
| 无法安装或确认 0.2.0 | infrastructure `BLOCKED`；不用"版本相近"替代，不以别的版本结果冒充 |
| 后续批次正式指令改为其他版本 | 以当批指令更新 7.0 节；精确 pin/同版本验证/逐 run 标注方法不变 |

## 17. 判分匹配与解析防线回归（20260924 批次）

| 场景 | 预期 |
|---|---|
| 非唯一答案（水果品类：香蕉/橘子/苹果）被硬编码成单一正确解（香蕉） | 第 0 类错杀；能过 skill 与轨迹质检也不改变其缺陷性质；判分必须接受完整合法集或可验证的集合成员谓词 |
| 生成式交付（每次报告内容都不同）被写成代码规则/写死答案文本 | 第 0 类错杀；改写 criterion 交 LLM judge 按语义判定；judge prompt 只描述正确判据，不列举期望产出原文 |
| 修复时把开放题/多解题收窄成单解硬匹配 | 修复动作本身即缺陷；C2 复审必须检查答案空间分类是否被修复收窄 |
| 输入文件固定字段名读取、精确值计算、固定 schema/路径/hash、封闭完整枚举 | 唯一性事实，rule/代码判分合法 |
| 有限多解题的等价表达正控只测了一个代表解 | 不闭合；必须用至少两个不同合法解的多解正例夹具 |
| 方法选择类 claim 被写死为单一方法 | 第 0 类错杀；交 judge 语义判定 |
| P2 未记录多解题的合法解集合来源与完备性依据 | 结构缺口；补齐后才能写判分 |
| PDF 全文任意位置出现数字 6 即给"统计正确"分 | 放水缺陷；数值必须绑定目标统计对象与字段，配"错误位置负控"得 0 |
| 提交三个只有 exit 0 的空脚本仍满分 | 放水缺陷；正向 claim 要求真实退出码/输出/服务状态证据 |
| 文件内容被改烂但关键词还在即算"未改动" | 放水缺陷；必须按 hash/规范化内容比对 |
| 全文搜禁词、不肯定/否定语境直接判零 | 错杀缺陷；禁词判定必须带语境，否定用法（"未泄露"）不得计违规 |
| 必须恰好 15 行/变量必须叫 kw_exclude/必须含连续"不受影响" | 无正式形态依据即错杀；等价合规写法必须同分；形态约束只在正式规则明文规定时合法 |
| PPT 解析只遍历最外层 shape，组内文字全漏 | 解析缺陷；必须递归 group shape；配组内文字夹具断言非空提取 |
| 对话文件为 list 结构却按 dict 读取取不到对话 | 解析缺陷；按实际 JSON 结构分派 list/dict；配 list 型夹具 |
| 文件名乱码导致基线对不上 | 解析缺陷；路径先规范化编码再比较，配乱码文件名夹具 |
| 解析结果为空/None 时按通过计分 | fail-closed 缺陷；解析空必须记 0 并单独归因，不得吞异常 |
| 正确 UTC 写法得 0.8，错时区反而满分 | gold 缺陷；时区/单位/符号期望须用已知正确参照算例交叉验证 |
| 本机装有 zip 但期望写死"缺失" | gold 缺陷；环境依赖期望须目标环境实测推导 |
| C3 复算与 gold 冲突且复算依据可复核 | 以复算为准，登记 gold-defect issue，不默认 gold 正确 |
| C3 复算与 gold 冲突且复算不可复核 | 该 claim `BLOCKED`，不猜对错 |
| 规则质检未发现上述任一缺陷 | 按漏检归档：区分"规则未覆盖"（补 5.1 探针/回归）与"有规则未执行"（C2/C3 执行缺口），记防复发动作 |

## 16. 代表性行为试跑 prompts

以下 prompts 用于 Skill 修改后的人工行为评估。它们只验证决策与流程，不读取题包禁读材料、内部流水线内容或真实 Judge secret。

1. **0917 服务审计抗伪造**

   > 完成这个 Seal/RewardKit 的 tests-side 返修。现有 process check 从 `/logs/agent/request-audit.json` 给正向行为分，但 agent 可以写该路径；mock service 提供只读 `/v1/audit`。只修改实际授权的 tests 子集和根报告。先完成 P0–P3，说明 runtime loader、证据 ownership 和合法 validator 落位；只有正式规则支持时再修复。证明伪造本地审计不能得分、live `[]` 的判定正确、服务不可用失败关闭并归 infrastructure。报告必须给出变更影响和新鲜 run。

2. **双模式轨迹与提前清理**

   > 某 RewardKit process criterion 错让“确认前清理 pending 记录”的 agent 通过。现有 parser 只读取 solution 模式的 `{action,target}`，生产 ATIF 是 provider tool-call arguments。依据正式规则完成 tests-side refine：要求非空 confirmation 与 cleanup 证据、拒绝叙述/配置正文中的动作字符串，并用 agent/solution 正例、premature cleanup 反例和 anchor-pollution 反例验证。不得使用 Oracle 分数或禁读材料；修改后将受影响旧 run 标 stale。

3. **legacy report-only 阻塞归因**

   > 对这个 legacy ClawEval 做 WorkC 作业交付自检，未授权修改 tests。通过 `test.sh`、真实 registry 与 runtime collection 建 P0–P2，而不是统计 assertion-message constants。服务 credential 缺失，且 materialization 后少了一个环境应提供的文件。使用 report-only，逐项区分 infrastructure 与 candidate failure，记录精确缺失路径和移交；不创造 credential、不改 environment，且不得认证 evaluation。

4. **V1 局部通过与 schema 漂移**

   > 这个 0917 题的 Python compile、manifest parser 和两个 self-test 分别通过，但没有单一 V1 入口；`reward.toml` 多了未知顶层字段，现有检查只 grep 聚合字符串。完成 tests-side 返修与交付自检：建立或识别 canonical V1 hard gate，用当前 schema 解析 YAML/TOML，加入单变量 drift controls，并在报告中区分 C1 与尚未授权的 V2+ certification。不得机械要求可选 quality/reward 存在；RewardKit 版本按当批正式指令精确核对（当前批次 harbor-rewardkit==0.2.0）。

5. **独立复算触发闭环重启**

   > 第一轮 C1 已通过。独立 reviewer 从 instruction/resources 复算后发现 checks 常量与 manifest 文本虽然一致，但正确边界值不同。修复 tests 后完成交付：将第一轮 C1–C3 标为 STALE，回到受影响 P gate，从 C1 完整重跑；报告 cycle ID、三方比较、issue/F/A 平账，不得用 Oracle、judge 或 ground truth 覆盖独立推导，也不得跨轮拼接 PASS。

6. **载体完整性与 handoff/certification 分离**

   > 当前 tests 用 source 路径子串匹配，required carrier 可被替换；正式 policy 只规定 exact path 与 SHA-256，没有 canary。只修改授权 tests 与根报告：按 policy 做 carrier-to-consumer closure、缺失/篡改负控，不复制示例 canary GUID。若 canonical V1 与 C2–C4 均通过，但 runner-owned mount provenance 和 candidate run 未授权，允许按证据判断 tests-side handoff，同时保持 evaluation certification BLOCKED。