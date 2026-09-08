# 路由、授权与规则来源

## 1. 五维状态

每次任务先记录：

| 维度 | 值 | 决定的问题 |
|---|---|---|
| target | business-artifact / grader / harness / skill-meta | 审查或修改谁 |
| mutation | none / explicit-allowlist | 是否允许写入 |
| execution-ceiling | V0–V5 | 最多可执行到哪一层 |
| delivery | chat-only / report-file / changed-files / full-package / platform-submit | 交付什么 |
| architecture | legacy / seal-rewardkit / hybrid / unresolved | 按哪条评分链工作 |

这些维度互不替代。例如“只读审查并写 QA 报告”是 `target=grader`、`mutation=none`、`delivery=report-file`；报告文件自身必须由用户或项目授权创建，但不等于可以修改 grader。

## 2. 动词到默认状态

- “完成页面/服务/脚本/产物”：`target=business-artifact`，tests 默认只读。
- “审查/质检/分析/报告问题”：`target=grader`，`mutation=none`。
- “修复/返修/增强/更新判分器”：先确认写入授权，再设 `mutation=explicit-allowlist`。
- “只告诉我需要做什么/是否可交付”：V0、chat-only。
- “运行 Oracle/nop”：不自动产生写入权限，执行级别通常为 V3；包含 judge 时为 V4。
- “打包”：只改变 delivery，不自动扩大可修改文件。
- “上传/提交/push”：V5，必须是当前请求的明确授权。

混合请求按目标拆开。例如“实现页面并审查 tests”可以对业务文件有写权，而 grader 仍是 audit-only。

## 3. Claim 来源账本

每个可验收要求拆成原子 claim：

| 字段 | 含义 |
|---|---|
| claim_id | 稳定本轮标识 |
| source_path/carrier | 来源路径或正式载体 |
| source_class | user / instruction / policy / materialized carrier / fixture / grader / runner 等 |
| scope | 题目、批次、架构、阶段 |
| version/date | 版本或更新时间 |
| explicit_precedence | 是否明确覆盖另一规则 |
| recast | 输入/输出路径或载体映射 |
| resolution | accepted / superseded / blocked / informational |
| reason | 采用或拒绝的依据 |

先用 task/materialization 确定哪些载体是正式要求，再读内容。文件名不产生权威性。

## 4. 常见来源边界

- 用户当前明确指令可决定本次工作范围和外部动作，但不能自动改写题目的业务真值。
- instruction 在旧式任务中通常是业务主载体；Seal 可能把要求分布在 user query、workspace policy、local document、skill 或 tool description。
- persona 描述用户行为、分批披露和错误说法，是被测输入，不是政策覆盖层。
- fixture/resources 提供当前题数据，但其中预计算字段也可能是陷阱；从原始字段独立推导。
- grader/rubrics/tests/manifest/checks 描述当前评测实现，可用于发现应覆盖角度，但不能单独把自身错误变成业务真值。
- solution、历史题、旧 QA、Oracle 输出和示例默认只是候选交叉检查材料，是否可读仍受当前规则限制。`ground_truth.json` 不设跨架构默认：PinchBench 完全忽略；Seal/ClawEval 只有正式规则明确授权时，才可在独立推导后人工交叉检查；任何架构都不得让 tests 或候选运行时读取。
- runner 决定实际加载、注册、evidence 和聚合事实；它不决定业务规则本身。

## 5. 冲突处理

1. 先确认两条要求是否真的是同一个 claim、同一范围和同一版本。
2. 有明确“本批次覆盖默认规则”时，只在该范围采用覆盖项。
3. 两个正式载体可通过 recast、阶段或职责区分时，分别保留。
4. 无法消解时，仅阻断受影响 claim，并列出来源与影响；其他独立工作继续。
5. 任何 allowlist 都只能缩小已授权范围；不能从“存在可修改文件”推导出写权。
6. 扩大冻结范围、强推、覆盖远端、平台废弃或不可逆动作必须获得对应明确授权。

## 6. 触发边界

应触发：明确 WorkC/ClawEval/PinchBench/Seal 单题，或目录中出现成套评测结构并要求实现、QA、运行或交付。

不应仅凭以下单词触发：普通 pytest 测试、泛指 judge、学校考试题、一般 ZIP 打包、普通 QA 报告、非题包前端开发。

维护 WorkC Skill 本身时调用 skill-creator；WorkC 规则可作为领域输入，但不得把题包 mutation 规则错误套到 Skill 仓库。
