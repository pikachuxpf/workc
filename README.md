# workc

面向 ZCode 的通用单题 ClawEval/WorkC 评测、修订与 QA Skill，供团队协作维护。

## 使用方式

在 ZCode 中使用 `/workc`，或在单题评测、rubrics/tests 检查、Oracle/nop、judge、QA 报告及交付打包场景中触发。Skill 会：

1. 分离评测语义、修改授权、冻结边界和外部操作授权；
2. 核对当前题的 instruction、persona、fixtures、输出 schema、判分文件和运行入口；
3. 从当前材料和可用的同前缀历史基线建立覆盖矩阵；
4. 逐项完成 A–H 安全分析；
5. 审查或修订 `tests/rubrics.py` 与 `tests/test_outputs.py`；
6. 检查 rubric/test 一一对应、evidence、数值真值和 runner 权重；
7. 按需隔离运行 Oracle、nop 或动态探针；
8. 按 `audit-only`、`changed-files`、`full-package` 或 `platform-submit` 模式交付。

完整规则见 [SKILL.md](./SKILL.md)。

## 默认边界

默认只把以下文件作为最小候选修改集合，当前题的更严格规则会继续收窄范围：

```text
tests/rubrics.py
tests/test_outputs.py
```

`qa_report.md` 仅在项目或用户明确要求时创建。`tests/test.sh`、`tests/judge.py`、类名、environment、solution、fixtures、ground truth、题目说明和运行脚本是否冻结，以当前题材料为准。

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
- 本地文件缺失时停止需要 judge 的运行并报告 `BLOCKED`，不得用模板回退。

## 关键规则

- 当前正式规则和题包决定测试，不能用 Oracle 分数反推或放宽规则；
- Oracle 不要求必须为 1，nop 不要求机械为 0；
- 精确数字、集合、时间、字段和 API 调用使用代码断言；
- 语义解释、冲突识别和沟通质量才使用 LLM judge；
- 可选 conversation 缺失与核心输出缺失必须分类处理；
- 每条 rubric 只检查一个事实，并恰好对应一个评分测试；
- 历史材料不可用时可以继续局部验证，但整体不得声称完整合规；
- judge 服务错误与候选业务失败必须分开报告。

## 目录结构

GitHub 仓库：

```text
workc/
├── SKILL.md
├── README.md
├── .gitignore
└── .secrets/
    └── judge.env.example
```

本地安装目录可额外包含被忽略的真实配置：

```text
workc/
├── SKILL.md
└── .secrets/
    └── judge.env
```

## 团队维护

修改后至少检查：

- YAML frontmatter 中 `name` 与目录名一致；
- description 能覆盖 workC、单题评测、rubrics、tests、Oracle、nop、judge 和 QA 场景；
- `SKILL.md` 少于 500 行；
- 没有写入具体题目的固定答案或真实密钥；
- `git ls-files` 不包含 `.secrets/judge.env`；
- `git check-ignore .secrets/judge.env` 能命中忽略规则；
- 本地安装版与发布版的 `SKILL.md` 一致；
- 用不同类型的真实提示验证触发和执行顺序。
