# workc

面向 ZCode 的 WorkC、ClawEval、PinchBench 与 Seal 单题 Skill。它同时支持业务实现、判分器 QA、Oracle/nop、QA 报告和交付，但会先识别目标与架构，不会看到 `tests/` 就改测试。

## 何时使用

应使用：

- 明确要求完成或审查 WorkC、ClawEval、PinchBench、Seal 单题；
- 题包出现 `rubrics.py + test_outputs.py`，并要求评分 QA、修复或运行；
- 题包出现 `criteria_manifest.yaml + 分维度 checks.py`，并要求 RewardKit QA、修复或运行；
- 对上述题包做 Oracle/nop、QA 报告、冻结审计、打包或平台收口。

不因单个通用词触发：普通 pytest、泛指 judge、学校考试题、一般 QA 报告、普通 ZIP 或无题包信号的前端开发。维护 Skill 自身时使用 skill-creator 元流程。

## 五维决策

每次先固定：

```text
target: business-artifact / grader / harness / skill-meta
mutation: none / explicit-allowlist
execution-ceiling: V0 text-only ... V5 external-action
delivery: chat-only / report-file / changed-files / full-package / platform-submit
architecture: legacy / seal-rewardkit / hybrid / unresolved
```

仅“审查、质检、分析、检查、报告问题”默认 `mutation=none` 且 V0；修改、候选运行、judge 和平台动作分别需要相应授权。allowlist 只能收窄写权，不能产生写权。

完整决策规则见 [SKILL.md](./SKILL.md) 和 [路由与来源](./references/routing-and-authority.md)。

## 两套评测架构

### 旧式 ClawEval / PinchBench

```text
tests/rubrics.py
tests/test_outputs.py
```

`RUBRIC_*` 与评分 `test_*` 一一对应，并可能结合 `judge.py`、`test.sh`、class/tier、conversation 与 audit。多轮对话型和输出文件型的证据规则不同，详见 [旧式参考](./references/legacy-claw-eval.md)。

### Seal / RewardKit

```text
tests/criteria_manifest.yaml
tests/<dimension>/checks.py
tests/reward.toml
tests/test.sh
```

Manifest、实际注册 checks、runner 和聚合共同构成评分契约，不是旧式两个文件的机械改名。除非实际 runner 要求，不补建 `rubrics.py` 或 `test_outputs.py`。详见 [Seal / RewardKit 参考](./references/seal-rewardkit.md)。

两套信号并存时必须追实际 import、registry 和聚合链，不能凭文件名任选一套。

## 业务实现与判分器 QA

- 业务实现：tests 默认只读；按正式载体完成页面、服务、脚本、CSV/JSON/ZIP、报告或 API 收口。见 [业务实现参考](./references/business-implementation.md)。
- 判分器 QA：只读请求默认 audit-only；明确要求修复后才可在 explicit allowlist 内编辑。
- 只问“需要做什么/是否可交付”：只读回答，不运行候选、创建报告或打包。

正确性从当前正式规则和原始数据独立推导。persona、tests、ground truth、solution、旧 QA、历史题和 Oracle 输出默认不是业务真值。Seal 的正式要求可能分布在多个 materialized carrier，按 claim 级来源消解。

## 错误率与漏召率

任务级 QA 从修改前冻结基线记录：

```text
R0 = 原始 rubric/manifest criterion 数
T0 = 原始 scoring test/registered check 数
N0 = R0 + T0
F  = 已找到、修复并验证通过的独立问题数
A  = AR + AT（新增 criterion/rubric + 新增 scoring check/test）

错误率 = F / N0
漏召率 = A / (N0 + A)
```

展示如 `50%（1/2）`、`33.33%（1/3）`。`F` 按 issue 根因去重，`A` 按新增计分 case 计数；同一遗漏补 rubric 和 test 通常 `A=2`。错误率可能超过 100%，不截断。指标是描述性 QA 数据，不是 PASS/FAIL 或质量阈值。

完整计数、零分母、audit-only、拆分/合并和运行新鲜度见 [验证与报告](./references/verification-and-reporting.md)。项目或用户要求报告文件时，使用 [QA 报告模板](./assets/qa_report.template.md)；只要求聊天时不创建文件。

## Judge secrets

真实配置只放：

```text
~/.agents/skills/workc/.secrets/judge.env
```

GitHub 只保存 `.secrets/judge.env.example`。真实 env-file：

- 代理、通用编排层和候选不读取、打印、解析、转写、复制或提交其值；
- 仅允许受信任的独立 judge 进程/容器在实际 V4 运行时直接解析 env-file；
- 不注入通用 runner/orchestrator，不传给候选；
- 缺失时将需要 judge 的步骤标为 `BLOCKED`，不使用模板回退。

新环境可手工复制模板后只在本地填写：

```bash
mkdir -p ~/.agents/skills/workc/.secrets
cp .secrets/judge.env.example ~/.agents/skills/workc/.secrets/judge.env
```

## QA 报告和交付

报告把“可交付”拆成：

- `artifact_handoff_ready`：文件/包可交接；
- `evaluation_certified`：适用评测完整、健康且结果新鲜；
- `platform_submission_ready`：具备平台提交前提。

保存或上传不等于提交完成；只有验证最终平台状态后才能报告实际提交成功。内部规范只做 claim 级摘要，不把长段原文、视频、个人信息或具体题答案发布到仓库。

## 目录

```text
workc/
├── SKILL.md
├── README.md
├── .gitignore
├── .secrets/
│   └── judge.env.example
├── assets/
│   └── qa_report.template.md
└── references/
    ├── routing-and-authority.md
    ├── business-implementation.md
    ├── legacy-claw-eval.md
    ├── seal-rewardkit.md
    ├── verification-and-reporting.md
    └── skill-evals.md
```

## 发布前检查

按 [Skill 回归矩阵](./references/skill-evals.md) 验证触发、权限、架构、指标、报告和发布门。至少确认：frontmatter 可解析、相对链接存在、本地与发布版公开文件逐字节一致、真实 `judge.env` 被 ignore 且未跟踪、公开 diff 不含内部资料或题目答案。
