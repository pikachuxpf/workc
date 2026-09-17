# workc

面向 ZCode 的 WorkC、ClawEval、PinchBench、Seal 与 RewardKit 单题测试侧作业 Skill。它只完成或返修题包中的测试、验证、QA 报告和交付，不承接页面、服务、脚本、业务数据、业务 ZIP、API 状态等业务实现，也不是普通项目的通用质检 Skill。

## 不可解除的写入边界

题包内最大可写范围固定为：

```text
tests/**
/qa_report.md
```

- 实际 allowlist 只能在 `tests/**` 内继续收窄。
- 完成、返修或作业交付自检时，根目录 `qa_report.md` 必须生成或更新。
- 其余题包路径全部冻结；复制副本、materialization 和打包不能扩大写权。
- tests 已正确时使用 `report-only`；纯咨询不生成报告，也不得声称完成作业。
- 完整包只写到题包外或明确的外部位置。

## 何时使用

应使用：

- 明确要求完成、返修或验证 WorkC、ClawEval、PinchBench、Seal 或 RewardKit 单题的测试侧作业；
- 题包出现 legacy `rubrics.py + test_outputs.py`；
- 题包出现 0917 RewardKit 的 `criteria_manifest.yaml`、`process/output/safety`、`checks.py`、可选 `quality.toml`/`reward.toml` 或 React runner 信号；
- 对这些测试侧作业运行 Oracle/nop、编写强制 QA 报告、审计冻结差异或制作外部交付包。

不应使用：

- 完成页面、服务、业务脚本、业务 CSV/JSON/ZIP 或 API 回写；
- 普通项目的代码质检、pytest 修复、judge 评审或 QA 报告；
- 学校考试题、一般 ZIP 打包或无 WorkC 题包信号的前端开发。

维护本 Skill 自身时使用 skill-creator 元流程。

## 核心流程

```text
理解题目与正式要求
→ 建立 tests 覆盖基线
→ 修改和优化实际授权的 tests/** 子集
→ 执行适用验证
→ 生成或更新根目录 qa_report.md
→ 差异审计与交付
```

每次先固定 target、mutation、V0–V5 execution ceiling、delivery 和 architecture。候选运行、judge、打包、上传和提交分别受独立授权约束。完整规则见 [SKILL.md](./SKILL.md) 和 [路由、来源与写入边界](./references/routing-and-authority.md)。

## 两套兼容架构

### Legacy ClawEval / PinchBench

```text
tests/rubrics.py
tests/test_outputs.py
```

只统计被实际评分链消费的 rubric 和独立评分 test；仅作为 assertion message、日志或显示名的 `RUBRIC_*` 常量不是评分身份。Legacy 继续受支持，不因 0917 新格式而机械迁移，也不要求创建三维目录、quality 或 React prompt。详见 [旧式参考](./references/legacy-claw-eval.md)。

### 0917 Seal / RewardKit

```text
tests/
├── criteria_manifest.yaml
├── process/
│   ├── checks.py
│   ├── quality.toml       # optional
│   ├── reward.toml        # optional
│   └── react_prompt.md    # quality.toml 存在时 required
├── output/
│   └── checks.py
└── safety/
    └── checks.py
```

`process`、`output`、`safety` 每个目录在规范化后必须恰好有一个 `checks.py`；缺失、重复、大小写或归档成员碰撞都 fail closed。三个 checks 文件可以没有独立评分项，但物理结构不能缺失。

`process/quality.toml` 与 `process/reward.toml` 都是可选项。Deterministic-only 可以没有 quality、reward 和 prompt；若存在 `quality.toml`，同目录必须恰好存在一个 canonical `react_prompt.md`，且使用：

```toml
[judge]
judge = "react"
prompt_template = "react_prompt.md"
```

Prompt 缺失、重复、关联歧义或模板指向不一致时，先将整条数据项标为 `DEPRECATED/ABANDONED`，停止常规返修、评分和交付认证。不得自动创建、猜写、改名、拼接、合并或从其他 Markdown 文件选择 prompt。Prompt 是文件级配对，不是每个 criterion 一个文件；它、manifest 行和结构文件都不增加 case 或直接定义最终权重。

Manifest 只用于定位 scorer、速览和核对 partial credit；实际权威仍是 `checks.py`、`quality.toml`、配对 prompt、runner 和真实聚合。详见 [Seal / RewardKit 参考](./references/seal-rewardkit.md)。

## 0818 后续批次防回归护栏

- bootstrap、身份建立和平台接入问题不占任务问题上限；混合问题按任务意图计。
- instruction/input 已有答案时不得强制 ask-first；真实缺失且影响结果的信息仍可澄清。
- 模拟用户 persona 不得错施于 agent。
- HTML 语义 judge 使用可见、相关内容，不用固定字符盲切或 CSS/JavaScript 偶然关键词。
- 未披露/不可用服务和缺可信凭据属于不适用或 infrastructure，不是候选硬失败。
- 建议研究不升级为 mandatory。
- 候选输出、harness/exec 噪声和 infrastructure failure 分开归因。
- assertion-message-only rubric 常量不算评分身份。

详细来源与 claim 规则见 [当前 SOP 摘要](./references/current-sop.md) 和 [路由参考](./references/routing-and-authority.md)。

## Post-trajectory 环境缺失

轨迹生成后若返修环境因解包、materialization、挂载、快照或平台问题无法修复或缺少必要文件，`qa_report.md` 必须记录环境/阶段、`observed_at`、原因、单个 `exact_normalized_missing_path`、预期来源或挂载及 evidence；每个精确规范化缺失路径独占一行，禁止目录概述、glob 或合并多个路径。状态记 `BLOCKED/OUT_OF_SCOPE`，并使用：

```text
repair_disposition=NO_FURTHER_REPAIR_REQUIRED_ENVIRONMENT_HANDOFF
```

记录完成后该反馈项无需其他修复，不得创建 placeholder 或放宽 test；这不是 PASS。健康环境中正式要求候选生成但未交付的文件仍是 candidate delivery missing，可判 FAIL。

## Case、指标与新鲜度

```text
R0 = legacy 中实际评分链消费的 rubric；或冻结基线 canonical quality.toml 中每个可解析 [[criterion]] 条目（重复/缺失 id 仍计数并另报 issue）
T0 = legacy 独立评分 test_*；或 checks.py 实际注册的独立 check result
N0 = R0 + T0
F  = 已修复且直接适用验证为 FRESH/PASS 的独立 issue
A  = AR + AT

错误率 = F / N0
漏召率 = A / (N0 + A)
```

Manifest、React prompt 和结构文件增加零个 case。Prompt 配对修复、文件名规范化、manifest 重生成和身份不变的迁移均为 `A=0`。已废弃项单列 physical/discarded 库存，不冒充 active identity。

0917 run freshness 必须绑定三维目录/cardinality、三个 checks、quality 或合法缺席、React prompt 或合法缺席、`prompt_template`、reward、manifest、runner 和聚合。任一相关输入或映射变化，旧结果即 `STALE`。完整规则见 [验证与报告](./references/verification-and-reporting.md)。

## Judge 与 LLM 权重

全部 LLM 项的最终有效 reward 占比合计不得超过 40%，必须沿真实聚合链复算，同一项不能因 prompt、quality、manifest 和 runtime 多层出现而重复计权。关键词空壳、错误数值、关键内容缺失和移除全部 judge 的事实检查消融是新版必需负控。

真实 judge 配置只放在 `~/.agents/skills/workc/.secrets/judge.env`。代理、通用编排层和候选不得读取、打印、解析、转写、复制或提交其值；仅受信任的独立 judge 进程/容器可在 V4 使用。缺失时将需要 judge 的步骤标为 `BLOCKED`，不使用模板回退。

## QA 报告和交付

完成类作业必须使用 [QA 报告模板](./assets/qa_report.template.md)。模板 1.3 要求记录：

- 三维结构与 checks cardinality；
- quality/reward/react prompt 库存、digest、配对、弃用和 consistency；
- physical/discarded/active 身份与 `R0/T0/N0`；
- HTML evidence 和 service/credential preflight；
- candidate failure、harness noise、infrastructure failure；
- post-trajectory 环境事件、精确缺失路径和 repair disposition；
- LLM 占比、四类负控、freshness 和未运行项；
- `test_delivery_handoff_ready`、`evaluation_certified`、`platform_submission_ready` 与实际提交状态。

保存、打包或上传不等于提交成功；只有验证平台最终状态后才能报告提交成功。

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
    ├── current-sop.md
    ├── routing-and-authority.md
    ├── legacy-claw-eval.md
    ├── seal-rewardkit.md
    ├── verification-and-reporting.md
    └── skill-evals.md
```

## 发布前检查

按 [Skill 回归矩阵](./references/skill-evals.md) 验证触发、固定写入边界、架构、React 配对、0818 防回归、环境移交、指标、强制报告和发布门。至少确认：frontmatter 可解析、相对链接存在、真实 `judge.env` 被 ignore 且未跟踪、公开 diff 不含内部原文、题目答案、日志、缓存或 secrets。Skill 发布和 Git push 必须另行授权。
