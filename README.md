# workc

面向 ZCode 的 WorkC、ClawEval、PinchBench、Seal 与 RewardKit 单题测试侧作业 Skill。它只完成或返修题包中的测试、验证、QA 报告和交付，不承接页面、服务、脚本、业务数据、业务 ZIP、API 状态等业务实现，也不是普通项目的通用质检 Skill。新格式以 `quality.toml` 承载语义/judge criterion、以 `checks.py` 承载确定性/程序化 check，并由 `criteria_manifest.yaml` 聚合摘要；manifest 不定义身份，也不增加 case。

## 不可解除的写入边界

题包内最大可写范围固定为：

```text
tests/**
/qa_report.md
```

- 实际 allowlist 只能在 `tests/**` 内继续收窄。
- 完成、返修或作业交付自检作业时，根目录 `qa_report.md` 必须生成或更新。
- 其余题包路径全部冻结；用户、题目配置、materialization、复制副本和打包请求都不能解除冻结。
- 纯咨询或明确不修改时可以只在聊天中回答，但不得声称完成、返修完成或作业交付自检完成。
- 完整包交付前必须在本轮生成或更新 `qa_report.md`；tests 未变化时使用 `report-only`。包可以读取冻结文件，但只能写到题包外或明确的外部交付位置，不能借打包修改题包内容。

## 何时使用

应使用：

- 明确要求完成、返修或验证 WorkC、ClawEval、PinchBench、Seal 单题的测试侧作业；
- 题包出现 `rubrics.py + test_outputs.py`，并要求测试侧修复、验证或交付；
- 题包出现 quality-only、`quality.toml + checks.py`、确定性-only 的 `checks.py + criteria_manifest.yaml` 或相关 Seal/RewardKit runner 信号，并要求测试侧作业；
- 对上述测试侧作业运行 Oracle/nop、编写强制 QA 报告、审计冻结差异或制作外部交付包。

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

WorkC 理解业务材料是为了把测试写对，不是为了修改业务文件。QA 报告是完成测试侧作业后的必交付收尾，不是独立质检服务。若 tests 已正确，可以不编辑 tests，但仍须验证并更新 `qa_report.md`；纯咨询则不进入完成流程，也不生成报告。

## 作业状态

每次先固定：

```text
target: test-delivery / test-harness / consultation / package
mutation: none / tests-allowlist-plus-report / report-only
execution-ceiling: V0 text-only ... V5 external-action
delivery: chat-only / completed-assignment / full-package / platform-submit
architecture: legacy / seal-rewardkit / hybrid / unresolved
```

纯咨询默认 `mutation=none` 和 V0。完成、返修或作业交付自检必须包含根目录 `qa_report.md`；需要修 tests 时，仅将明确授权的 `tests/**` 子集加入实际 allowlist。候选运行、judge 和外部动作需要各自授权。

完整规则见 [SKILL.md](./SKILL.md) 和 [路由、来源与写入边界](./references/routing-and-authority.md)。

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
tests/<dimension>/quality.toml   # 仅语义/judge 评分单元需要
tests/<dimension>/checks.py      # 确定性/程序化检查
tests/test.sh                    # 以实际 runner 为准
```

`quality.toml` 定义语义/judge 质量 criterion，`checks.py` 定义确定性/程序化 check，`criteria_manifest.yaml` 聚合摘要当前实际存在的两类评分项。Manifest 不是身份权威，每行增加零个 case；按正式 claim 与 runner，quality-only、quality + checks 和确定性-only 的 `checks.py + manifest` 都可合法，manifest 单独存在不能建立评分身份。旧式 `rubrics.py + test_outputs.py` 继续受支持；只有当前任务正式使用或明确要求新格式时才规范化或迁移。详见 [Seal / RewardKit 参考](./references/seal-rewardkit.md)。

两套信号并存时必须追实际 import、registry、scorer target 和聚合链。architecture 保持 `legacy` / `seal-rewardkit` / `hybrid` / `unresolved`；架构识别只决定如何完成测试侧作业，不产生 tests 外写权。

新格式规则：

- 文件名严格为小写 `quality.toml`。可写完成/返修时，仅在实际 tests allowlist 内自动规范化一个语义明确的替代 TOML 质量文件名或大小写变体；目标已存在或多个别名冲突则不覆盖、不合并，标记 `BLOCKED`。咨询只报告。
- 仅当正式当前 claim/runner 要求该评分单元具备语义/judge criterion 且内容可权威推导时，才可创建缺失的 `quality.toml`；禁止空文件、占位文件和逐目录机械补建。
- 常见 schema：`[judge]` 使用 `judge`、`files`、`atif-trajectory`、`mode`、`timeout`；重复 `[[criterion]]` 使用 `name`、`id`、`description`、`type`、`points`、`weight`；`[scoring]` 使用 `aggregation`。实际任务 schema 与 runner 优先，不包含 canary 注释。
- Manifest 常见顶层字段是 `version`、`score_range`、`dimensions`、`criteria`；行常见 `angle_id`、`angle`、`rule_hint`、`dimension`、`weight`、`evidence`、`scorer`、`score_type`、`source`。质量 scorer 如 `output/quality.toml::output.narrative_quality`，确定性 scorer 如 `output/checks.py::delivery_form`。须验证源身份到行的 exact-once projection、scorer target 及 dimension/weight/evidence/source 一致性；不要求质量 criterion 映射到 `checks.py`。

## 测试侧完成、返修与作业验证

- 完成或返修：仅修改实际授权的 `tests/**` 子集，并必须生成或更新根目录 `qa_report.md`。
- 作业交付自检且 tests 无需修复：题包内仅写根目录 `qa_report.md`。
- 纯咨询或明确不修改：chat-only，不创建报告，不得声称完成作业。
- 业务实现请求：退出 WorkC 写入流程；最多只读说明为何超出范围。
- Seal/RewardKit 按评分单元盘点 canonical `quality.toml`、`checks.py`、manifest 投影、scorer target 与 runner 注册，再修 criterion/check 或重建摘要；不得用 manifest 补行替代真实身份。

正确性从当前正式规则与原始 evidence 独立推导。业务源码、业务产物、persona、fixtures 和正式载体可以只读用于建立预期，但不能由 WorkC 修改。tests、ground truth、solution、旧 QA、历史题和 Oracle 输出默认不是业务真值。

## 错误率与漏召率

从修改前冻结基线记录：

```text
R0 = legacy 稳定 RUBRIC_*；或 canonical quality.toml 中可解析 [[criterion]] 条目数（每条均计 1，重复/缺失 id 另报 issue）
T0 = legacy 独立评分 test_*；或 checks.py 实现/注册的独立实际评分 check 数
N0 = R0 + T0（manifest 每行增加零个 case）
F  = 已找到、修复并完成 FRESH 验证的独立问题数
AR = 新增 rubric/criterion 身份数
AT = 新增 scoring test/check 身份数
A  = AR + AT

错误率 = F / N0
漏召率 = A / (N0 + A)
```

展示如 `50%（1/2）`、`33.33%（1/3）`。`F` 按 issue 根因去重，`AR/AT` 独立、`A=AR+AT`；缺一个质量 criterion 并缺一个 check 通常 `A=2`。文件名规范化、manifest 创建/再生成、身份不变的迁移均为 `A=0`。错误率可能超过 100%，不截断。这些指标是描述性 QA 数据，不是 PASS/FAIL、reward 或 gate。

完整计数、零分母、拆分/合并和运行新鲜度见 [验证与报告](./references/verification-and-reporting.md)。完成、返修或作业交付自检时必须使用 [QA 报告模板](./assets/qa_report.template.md) 生成或更新根目录 `qa_report.md`。

## Judge secrets

真实配置只放：

```text
~/.agents/skills/workc/.secrets/judge.env
```

GitHub 只保存 `.secrets/judge.env.example`。真实 env-file：

- 代理、通用编排层和候选不读取、打印、解析、转写、复制或提交其值；
- 仅允许受信任的独立 judge 进程/容器在实际 V4 运行时直接解析；
- 不注入通用 runner/orchestrator，不传给候选；
- 缺失时将需要 judge 的步骤标为 `BLOCKED`，不使用模板回退。

新环境可手工复制模板后只在本地填写：

```bash
mkdir -p ~/.agents/skills/workc/.secrets
cp .secrets/judge.env.example ~/.agents/skills/workc/.secrets/judge.env
```

## QA 报告和交付

完成类作业必须报告：

- `test_delivery_handoff_ready`：测试侧文件与强制 QA 报告可交接；
- `evaluation_certified`：适用评测完整、健康且结果新鲜；
- `platform_submission_ready`：具备外部提交前提。

报告还必须明确实际 test allowlist、该 allowlist 外零变化（根目录 `qa_report.md` 为唯一例外）、架构与 canonical quality/别名处理、`R0/T0/N0` 及 manifest 零计数、manifest exact-once projection 与 scorer target 校验、`F/AR/AT/A`、确定性-only 单元依据、运行范围、freshness 和未运行项。`quality.toml`、`checks.py`、manifest、scorer target、runner 或其他绑定输入变化都会使旧结果 `STALE`。保存、打包或上传不等于提交成功；只有验证平台最终状态后才能报告实际提交成功。

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
    ├── legacy-claw-eval.md
    ├── seal-rewardkit.md
    ├── verification-and-reporting.md
    └── skill-evals.md
```

## 发布前检查

按 [Skill 回归矩阵](./references/skill-evals.md) 验证触发、固定写入边界、架构、指标、强制报告和发布门。至少确认：frontmatter 可解析、相对链接存在、本地与发布版公开文件逐字节一致、真实 `judge.env` 被 ignore 且未跟踪、公开 diff 不含内部资料或题目答案。
