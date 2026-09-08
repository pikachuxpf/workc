# workc

面向 ZCode 的通用单题 WorkC / ClawEval / Seal 工作流 Skill。它既支持按题目要求完成业务代码与交付物，也支持旧式和 RewardKit 架构的判分器 QA。

## 使用方式

在 ZCode 中使用 `/workc`，或在以下场景中触发：

- 完成 WorkC、ClawEval 或 Seal 单题；
- 审查或修订 rubric、criterion、tests 或 checks；
- 运行 Oracle、nop、judge 或 RewardKit；
- 编写 QA 报告、审计冻结边界或制作交付包。

Skill 首先做两个判断，不会看到 `tests/` 就直接改测试：

| 用户请求 | 工作模式 | 默认处理 |
|---|---|---|
| 完成页面、服务、脚本或业务产物 | 业务实现 | tests 只读；修改明确允许的业务源码和交付物 |
| 审查、质检或报告判分器问题 | 判分器 QA / `audit-only` | 识别实际 runner，只读检查并报告 |
| 明确要求修复、返修、增强或更新判分器 | 判分器 QA / `fix-and-validate` | 获得写入授权后，再确定判分文件 allowlist |
| 只问需要做什么、文件如何对应、是否可交付，或明确要求不修改 | 只读分析 | 只读取并回答，不修改、运行或打包 |

完整规则见 [SKILL.md](./SKILL.md)。

## 支持的评测架构

### 旧式 ClawEval

典型信号：

```text
tests/rubrics.py
tests/test_outputs.py
```

`rubrics.py` 定义评分题干；`test_outputs.py` 实现 pytest 检查，并可能结合 `judge.py`、`test.sh` 和类名/tier 映射。

### Seal / RewardKit

典型信号：

```text
tests/criteria_manifest.yaml
tests/process/checks.py
tests/output/checks.py
tests/safety/checks.py
tests/reward.toml
tests/test.sh
```

`criteria_manifest.yaml` 定义 criterion 契约；分维度 `checks.py` 实现并注册检查；`reward.toml` 与 runner 决定聚合。它们共同承担旧架构中 rubric、test 和评分聚合的职责，但不是两个旧文件的一对一改名。

详细映射和 QA 清单见 [references/seal-rewardkit.md](./references/seal-rewardkit.md)。除非实际 runner 明确要求，不为 Seal 题补建 `rubrics.py` 或 `test_outputs.py`，也不把旧题擅自迁移为新版。

若两套信号并存或结构不完整，必须读取 `task.toml`、`test.sh` 和实际加载链；不能凭文件名猜主架构。

## 核心流程

1. 分离评测语义、修改授权、冻结边界和外部操作授权。
2. 识别业务实现、判分器 QA 或只读分析角色。
3. 识别旧式 ClawEval、Seal/RewardKit、混合或未知架构。
4. 核对 instruction、项目规范、fixtures、载体映射、输出 schema 和 runner。
5. 从当前材料独立推导业务真值，建立覆盖矩阵或验收清单。
6. 在业务实现模式完成业务源码、报告、归档包和必要 API 收口；tests 保持只读。
7. 在判分器 QA 模式审查 criterion 与 check 的一一对应、evidence、数值真值和权重聚合。
8. 按需执行静态校验、隔离动态探针、Oracle/nop 或 RewardKit runner。
9. 按 `audit-only`、`changed-files`、`full-package` 或 `platform-submit` 模式交付。

## 默认边界

修改范围由当前用户请求和题目级规则的较窄交集决定。候选 allowlist 只能在获得写入授权后缩小范围，不能自行产生写入授权：

- 业务实现：只修改 instruction、项目规范与载体权限共同允许的业务文件和产物；`tests/` 默认只读，`instruction.md` 本身通常也是只读规则源。
- 旧式判分器 QA：进入 `fix-and-validate` 后，若没有更具体的范围，`tests/rubrics.py` 和 `tests/test_outputs.py` 可作为最小候选 allowlist。
- Seal/RewardKit 判分器 QA：进入 `fix-and-validate` 后，从 runner 实际加载链确定候选文件，可能涉及 manifest、被加载的 checks 和 reward 配置，但不自动修改全部文件。
- `qa_report.md` 仅在项目或用户明确要求时创建。

`instruction.md`、fixtures、environment、solution、ground truth、task/materialization 配置、runner、类名、criterion 注册或权重是否冻结，必须从当前题材料确认。

本地修改授权不包含上传、平台提交或 Git push；这些外部动作需要用户明确授权。

## Judge secrets

### 文件布局

真实 judge 配置只放在本地安装目录：

```text
~/.agents/skills/workc/.secrets/judge.env
```

Windows 中对应 `%USERPROFILE%\.agents\skills\workc\.secrets\judge.env`，Git Bash 中仍可使用上面的 `~` 路径。

GitHub 只保存占位模板：

```text
.secrets/judge.env.example
```

`.gitignore` 会忽略 `.secrets` 下的真实 `*.env`，只允许显式的 `*.env.example` 模板进入版本库。

### 初始化

新环境中复制模板后，只在本地文件填写真实配置：

```bash
mkdir -p ~/.agents/skills/workc/.secrets
cp .secrets/judge.env.example ~/.agents/skills/workc/.secrets/judge.env
```

模板包含判分器支持的变量名：

- `JUDGE_BASE_URL`
- `JUDGE_API_KEY`
- `JUDGE_MODEL_ID`
- `JUDGE_TIMEOUT_SEC`
- `JUDGE_MAX_TOKENS`
- `JUDGE_CACHE_DIR`
- `JUDGE_DISABLE_CACHE`
- `JUDGE_MAX_ATTEMPTS`
- `JUDGE_RETRY_BASE_DELAY`

模板值均为无效占位符或公开运行默认值，不可直接用于真实 judge 请求。

### 使用约束

- 不读取、打印、转写、`source` 或逐项展开真实 env-file 的值；
- 仅在实际运行 judge 时通过 `--env-file` 或 runner 等价参数注入；
- 不将真实 env-file 复制到题目目录、GitHub、日志、QA 报告、临时文件或容器镜像；
- 不把 judge secrets 传给候选 solution、脚本或动态探针；
- 轮换密钥时只更新本地 `judge.env`，不修改模板；
- 本地文件缺失时停止需要 judge 的运行并报告 `BLOCKED`，不得用模板回退；
- Seal manifest 没有 judge scorer 时不调用 judge，也不需要注入 judge secrets。

## 关键规则

- 当前正式规则和题包决定正确性，不能用 Oracle 分数反推或放宽规则；
- Oracle 不要求必须为 1，nop 不要求机械为 0；
- 精确数字、集合、时间、字段、归档和 API 调用使用确定性检查；
- 语义解释、冲突识别和沟通质量才使用 LLM judge；
- 同一业务事实只能计权一次；
- 可选 evidence 缺失与核心输出缺失必须分类处理；
- 历史材料不可用时可以继续局部验证，但不得声称完整合规；
- judge、runner 或 harness 故障与候选业务失败必须分开报告；
- 业务实现不得为了过测修改 tests，也不得用被禁止的安装、构建、联网或发布动作做验证。

## 目录结构

GitHub 仓库：

```text
workc/
├── SKILL.md
├── README.md
├── .gitignore
├── .secrets/
│   └── judge.env.example
└── references/
    └── seal-rewardkit.md
```

本地安装目录可额外包含被忽略的真实配置：

```text
workc/
├── SKILL.md
├── README.md
├── references/
│   └── seal-rewardkit.md
└── .secrets/
    ├── judge.env.example
    └── judge.env
```

## 团队维护

修改后至少检查：

- YAML frontmatter 中 `name` 与目录名一致；
- description 能覆盖 WorkC、Seal、业务实现、判分器 QA、两套文件结构和交付场景；
- `SKILL.md` 少于 500 行，所有相对引用存在；
- 三类提示分别走业务实现、Seal 判分器 QA 和旧式判分器 QA 分支；
- 混合结构先读取 runner，只读询问不产生修改；
- 没有写入具体题目的固定答案或真实密钥；
- `git ls-files` 不包含 `.secrets/judge.env`；
- `git check-ignore .secrets/judge.env` 能命中忽略规则；
- 本地安装版与发布版公开文件逐字节一致。
