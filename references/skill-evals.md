# WorkC Skill 回归矩阵

每次修改 Skill 后至少执行以下语义回归。目标是验证 WorkC 只完成测试侧作业，并始终遵守固定写入边界。

## 1. 主流程回归

每个完成类场景都必须保持：理解题目与正式要求 → 建立 tests 覆盖基线 → 修改和优化授权的 `tests/**` 子集（若有必要）→ 适用验证 → 更新根目录 `qa_report.md` → 差异审计与交付。不得跳过题意理解直接迎合 Oracle，也不得把 QA 报告变成独立质检入口。

## 2. 正向路由

| 输入场景 | 预期 |
|---|---|
| 完成旧式 WorkC 作业的 rubrics/tests | architecture=legacy；只修改实际授权的 `tests/**` 子集；必须生成或更新根目录 `qa_report.md` |
| 完成 Seal 作业的 criterion/checks | architecture=seal-rewardkit；沿 manifest/registry/runner 完成测试侧作业；必须更新 `qa_report.md` |
| tests 已正确，只要求完成作业交付自检 | `mutation=report-only`；仅生成或更新根目录 `qa_report.md` |
| 两套测试结构并存 | hybrid/unresolved；追 `test.sh`、import、registry；不任选一套，不修改 tests 外内容 |
| 明确“不要运行代码，但完成静态作业交付自检” | 只到 V0；仅更新 `qa_report.md`，报告 NOT_RUN/BLOCKED 项，不伪造执行通过 |
| 缺 instruction，但 materialization 指向正式 carrier | 只读 carrier 建 claim；写入仍仅限 tests allowlist 与 `qa_report.md` |
| rubric/check 修改后引用旧 Oracle 结果 | 判定 STALE，不能用于完成声明 |
| judge 402/429/超时 | infrastructure BLOCKED，不记候选失败，不用模板回退 |
| 要求完整题包交付 | 先完成测试侧作业和 `qa_report.md`；包写到题包外；不修改冻结内容 |
| 明确平台提交 | 仅在 V5 明确授权且前置门通过时执行；上传不等于提交完成 |

## 3. 超出范围与反向触发

以下请求不得进入 WorkC 业务写入流程：

- 完成或修改 Vue/React 页面；
- 修复业务服务、业务脚本或 API；
- 生成业务 CSV、JSON、报告或业务 ZIP；
- 回写业务数据库、在线表格或业务状态；
- 普通项目的 pytest 单测修复；
- 泛指 judge、代码质检或普通 QA；
- 学校考试题、一般 ZIP 或非题包前端开发。

即使这些项目包含 `tests/`，只要目标是业务实现，也不得使用 WorkC 修改业务文件。维护 WorkC Skill 本身必须转入 skill-creator。

## 4. 写入边界回归

- 题包内最大可写集合始终是 `tests/** ∪ {/qa_report.md}`；
- 用户、instruction、materialization 或题目内 allowlist 都不能把 tests 外路径变为可写；
- 实际 test allowlist 只能是 `tests/**` 的子集；
- 完成、返修或作业交付自检必须生成或更新根目录 `qa_report.md`；
- tests 无需变化时只允许 `report-only`；
- 纯咨询或明确不修改时零文件写入，并明确本轮未完成作业；
- 复制到副本不扩大写权；
- 打包不扩大写权，包必须写到题包外或明确的外部位置；
- 不得在题包内创建 staging、sidecar、临时包、运行缓存或额外交付清单；
- 候选运行时最终 tests、solution、fixtures 和业务内容全部只读挂载；
- V0/V1 不得静默升级到 import、candidate 或 judge；
- 缺隔离或 secrets 时应 BLOCKED，不得绕过；
- 最终差异若包含 actual test allowlist 与 `/qa_report.md` 之外的题包路径，`test_delivery_handoff_ready=NO/BLOCKED`。

## 5. 架构与身份回归

- 旧式结构仍是受支持输入：统计唯一 `RUBRIC_*` 与独立评分 `test_*`，不得机械迁移；
- 新格式 `R0` 统计 canonical `tests/**/quality.toml` 内可解析的 `[[criterion]]` 条目；每条计 1，不按文件数或 manifest 行数，也不因重复/缺失 `id` 先行去重；这些 ID 缺陷另登记 issue；
- `T0` 独立统计 `tests/**/checks.py` 实际实现/注册的最终评分 result ID；factory 产生多个 ID 时逐个计数，重复运行/重试不增加；
- `criteria_manifest.yaml` 聚合 quality 与 deterministic/check rows，但自身不贡献身份；创建/再生成 manifest 为 `A=0`；
- manifest quality row 按 `quality.toml` target 校验，deterministic/check row 按 `checks.py` target 校验；不得要求 quality criterion 映射到 `checks.py`；
- RewardKit 0.1.7 的注册参数 ID 与最终机器 ID 分层报告；
- orphan、ghost、duplicate registration 不得互相抵消；
- 正式文件名必须为 `quality.toml`；无歧义 rename/case normalization 与身份保持格式迁移均 `A=0`；
- alias/case 归一后的 path 或 identity collision 必须 BLOCKED，不覆盖、不任选；
- 仅当正式 claim/当前 runner 要求且内容可可靠推导时创建缺失 `quality.toml`，不得创建空文件、placeholder 或为每个目录机械创建；
- 不给 Seal 机械补建旧式文件；不因识别业务 claim 而修改业务载体，业务内容只作只读 evidence。

### 5.1 必测样例

| 输入场景 | 预期 |
|---|---|
| canonical `quality.toml` + `checks.py` | 分别建立 R0、T0，`N0=R0+T0` |
| 只有 canonical `quality.toml` 与其 manifest 投影，无 deterministic check | 合法；按 `[[criterion]]` 计算 R0，`T0=0`，不机械补 `checks.py`；freshness 记录 checks 为 `ABSENT_ALLOWED_BY_CLAIM_RUNNER` |
| 只有 deterministic `checks.py`，无 quality | 合法；`R0=0`，按实际 result ID 计算 T0，不机械补 quality；freshness 记录 quality 为 `ABSENT_ALLOWED_BY_CLAIM_RUNNER` |
| 正式 claim/runner 要求 quality，但文件缺失且内容可推导 | 创建非空 canonical `quality.toml`；已有身份迁移 `A=0`，真正新 criterion 才 `AR+1` |
| `Quality.toml` 或明确 alias 唯一映射到 canonical path | 规范化为 `quality.toml`；身份保持，`A=0` |
| 多个 alias/case 路径归一到同一 canonical path，或身份碰撞 | `BLOCKED`；保留证据，不覆盖/合并/任选 |
| manifest 遗漏、额外或重复 quality/check rows | 分 scorer target 报 manifest sync issue；不改变 R0/T0；manifest 不计数 |
| 一个 quality criterion + 一个 check | `R0=1,T0=1,N0=2`；manifest 行不能使 N0 变为 3 |
| 在前项基础上新增一个 criterion/check 对 | `AR=1,AT=1,A=2` |
| 一个 factory 注册三个最终 result ID | T/AT 按三个 ID 计；调用次数、重试次数不计 |
| 两个 `[[criterion]]` 条目使用同一 ID，或其中一个缺失 ID | `R0=2`；两个物理条目都计数，同时登记 duplicate/schema issue；manifest 投影无法无歧义闭合时 `BLOCKED` |
| 纯咨询 | 零写入；不创建 `qa_report.md`，声明未完成/未返修/未作业交付自检 |

## 6. 指标回归

| 场景 | 预期 |
|---|---|
| F=1,N0=2 | 50%（1/2） |
| A=1,N0=2 | 33.33%（1/3） |
| F=3,N0=7 | 42.86%（3/7），括号不约分 |
| F=9,N0=4 | 225%（9/4），不截断 |
| N0=0 | 错误率 N/A（0/0） |
| N0=0,A=2 | 漏召率 100%（2/2） |
| N0=0,A=0 | 漏召率 N/A（0/0） |
| 同一根因跨 rubric/test | F 去重；AR/AT 独立且不按 issue 去重 |
| 两个独立问题 | 两个 issue_id；均修复且 FRESH/PASS 后 F=2 |
| rename/move、quality 大小写归一、身份保持格式迁移 | A=0 |
| manifest 创建/再生成 | A=0，不贡献 R/T 身份 |
| 一个 rubric/test 对拆成两对 | 每层最多一个继承原身份，其余进入 AR/AT |
| 两项合并成一项 | 对应 DR/DT 增加 1 |
| 重复注册 | 稳定身份计一次，重复登记 issue |
| orphan criterion / ghost check | 各保留对应库存，登记映射 issue；不强制互相映射 |
| 纯咨询发现问题 | F=0 并紧邻未修复、未完成声明 |
| 基线不可靠 | 两项比率 N/A，不猜数 |
| 自行引入后修掉 | 不计 F |

复核：`R1=R0+AR-DR`、`T1=T0+AT-DT`、`N1=N0+A-D`。身份无法可靠映射时解释原因，不强行平账。

## 7. 强制报告回归

完成、返修或作业交付自检时，根目录 `qa_report.md` 必须包含：

- `maximum_writable_scope = tests/**, /qa_report.md`；
- 实际 test allowlist；
- 实际 test allowlist 外零变化审计（根目录 `qa_report.md` 为唯一例外）；
- 本轮报告生成/更新时间；
- baseline ID/hash 与 architecture；
- artifact 路径规范化与 quality 文件名规范化分列；
- discovered/canonical/normalized/created quality paths，以及碰撞/阻断状态；
- manifest sync、各 row 的 scorer target 校验与 manifest 不计数声明；
- raw-to-final identity mapping；
- 物理定义、collected/registered、有效身份三套数；
- issue_id、修复验证、未修复、受影响 case、非 case 问题；
- AR/AT/A、DR/DT/D 和最终库存；
- 错误率、漏召率、零分母和 N/A；
- run_id 与 freshness digests；
- parser、runner、Oracle、nop、difference、package、submission 状态；
- `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready`；
- 外部包位置，且它必须位于题包外；
- 上传与实际提交状态明确分离。

纯咨询不得创建报告，也不得使用“已完成、已返修、已作业交付自检”等表述。

## 8. Skill 发布门

1. frontmatter 可解析，`name: workc` 与目录一致；
2. description 不包含业务实现或通用质检职责，并明确 tests-only 与强制报告；
3. 不存在 `business-implementation.md` 或其他业务写入 reference；
4. 所有 references 单独阅读时也保持同一固定写入边界；
5. 主 Skill 保持决策内核，相对链接全部存在；
6. 本地安装版与发布仓库公开文件逐字节一致；
7. `git ls-files` 不含真实 `.secrets/judge.env`，ignore 检查命中；
8. diff 不含内部原文、个人信息、题目固定答案、缓存、日志或 secrets；
9. Skill 仓库提交与 push 由 skill-creator 元流程执行，不与题包写入权限混淆。
