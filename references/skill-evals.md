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

## 5. 架构回归

- 旧式结构：统计唯一 `RUBRIC_*` 与独立评分 `test_*`；
- Seal：统计唯一 manifest `angle_id` 与真实 registry/final result ID；
- RewardKit 0.1.7 的注册参数 ID 与最终机器 ID 分层报告；
- orphan、ghost、duplicate registration 不得互相抵消；
- 不给 Seal 机械补建旧式文件；
- 不因识别业务 claim 而修改业务载体；业务内容只作为只读 evidence。

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
| 同一根因跨 rubric/test | F 去重；AR/AT 不按 issue 去重 |
| 两个独立问题 | 两个 issue_id；均修复且 FRESH/PASS 后 F=2 |
| 纯 rename/move | A=0 |
| 一个 rubric/test 对拆成两对 | 每层最多一个继承原身份，其余进入 AR/AT |
| 两项合并成一项 | 对应 DR/DT 增加 1 |
| 重复注册 | 稳定身份计一次，重复登记 issue |
| orphan criterion / ghost check | 各保留对应库存，登记映射 issue |
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
- 物理定义、collected/registered、有效映射三套数；
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
