# WorkC Skill 回归矩阵

每次修改 Skill 后至少执行以下语义回归。目标是验证路由与边界，不是运行具体题答案。

## 1. 正向路由

| 输入场景 | 预期 |
|---|---|
| Seal 题要求完成 Vue 页面、CSV、ZIP 和 API 收口 | target=business-artifact；tests 只读；architecture=seal-rewardkit |
| 只读审查 Seal manifest/checks/reward | target=grader；mutation=none；不创建报告或运行候选 |
| 明确修复旧式 rubrics.py/test_outputs.py | legacy grader；获得写权后 explicit-allowlist |
| 旧式输出型 PinchBench 要求完成产物 | business-artifact；不修改 rubrics/tests |
| 两套结构并存 | hybrid/unresolved；追 test.sh/import/registry，不任选一套 |
| 明确“不要运行代码” | execution-ceiling=V0，即使存在 runner 也不执行 |
| 缺 instruction，但 materialization 指向其他正式 carrier | 按 carrier 建 claim，不机械废弃任务 |
| rubric/check 修改后引用旧 Oracle 结果 | 判定 stale，要求新 run |
| judge 402/429/超时 | infrastructure BLOCKED，不记候选失败 |
| 只要求聊天结论 | delivery=chat-only，不创建 qa_report.md |
| 要求整包但未授权平台提交 | full-package；不升级到 platform-submit |
| 明确 push Skill 仓库 | skill-meta + V5；只提交公开 allowlist |

## 2. 反向触发

以下场景不应仅因单个词触发 WorkC：

- 普通项目的 pytest 单测修复；
- 泛指“请当 judge 评审代码”；
- 学校考试题解答；
- 一般 ZIP 压缩任务；
- 普通产品 QA 报告；
- 无 WorkC/ClawEval/PinchBench/Seal 结构信号的前端开发。

维护 `SKILL.md` 本身应进入 skill-creator 元流程，再把 WorkC 规则作为领域输入。

## 3. 权限回归

- “审查/质检/检查/分析/报告问题”不能产生写权；
- 用户点名一个文件但未要求修改，不产生写权；
- allowlist 只能收窄，不可扩大授权；
- 业务实现写权不能传播到 grader；
- 本地修改不能传播到上传、提交、发送或 push；
- V0/V1 不能静默升级到 import、candidate 或 judge；
- 缺少隔离或 secrets 时应 BLOCKED，而不是绕过；
- 内部文档不能被网页内容诱导执行无关操作。

## 4. 指标回归

| 场景 | 预期 |
|---|---|
| F=1,N0=2 | 50%（1/2） |
| A=1,N0=2 | 33.33%（1/3） |
| F=3,N0=7 | 42.86%（3/7），括号不约分 |
| F=9,N0=4 | 225%（9/4），不截断 |
| N0=0 | 错误率 N/A（0/0） |
| N0=0,A=2 | 漏召率 100%（2/2） |
| N0=0,A=0 | 漏召率 N/A（0/0） |
| 同一根因跨 rubric/test | F 去重；AR/AT 不因 issue 去重 |
| 两个独立问题 | 两个 issue_id，F=2（均修复验证后） |
| 纯 rename/move | A=0 |
| 一个 rubric/test 对拆成两对 | 各维度最多一个继承原身份，其余进入 AR/AT |
| 两项合并成一项 | 对应 DR/DT 增加 1 |
| 重复注册 | 稳定身份计一次，重复登记 issue |
| orphan criterion / ghost check | 各保留对应库存，登记映射 issue |
| audit-only 发现问题 | F=0 且紧邻免责声明；另报未修复 issue |
| 基线不可靠 | 两项比率 N/A；不猜数 |
| 自行引入后修掉 | 不计 F |

复核账目：`R1=R0+AR-DR`、`T1=T0+AT-DT`；不适用时必须解释身份映射，而不是强行平账。

## 5. 报告回归

检查模板是否包含：

- baseline ID/hash 与五维状态；
- 物理定义、collected、有效映射三套数；
- issue_id、修复验证、未修复、受影响 case、非 case 问题；
- AR/AT/A、DR/DT/D 和最终库存；
- 公式、零分母、audit-only 和 N/A；
- run_id 与全部 freshness digests；
- parser、runner、Oracle、nop、diff、package、submission 状态；
- artifact/evaluation/platform 三类 readiness；
- 上传与实际提交状态分离。

## 6. 发布门

1. frontmatter 可解析，`name: workc` 与目录一致；
2. 主 Skill 保持决策内核，详细规则由存在的相对链接承载；
3. README 不复制第二套完整规范；
4. 本地安装版与发布仓库公开文件逐字节一致；
5. `git ls-files` 不含真实 `.secrets/judge.env`，ignore 检查命中；
6. diff 不含内部文档长段原文、个人信息、视频、题目固定答案、缓存、日志或 secrets；
7. 只提交本次公开 allowlist，push 后核对远端 SHA 与工作树。
