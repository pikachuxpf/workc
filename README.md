# workc

面向 ZCode 的通用单题 ClawEval/WorkC 评测、返修与 QA Skill，供团队协作维护。

## 使用方式

在 ZCode 中使用 `/workc` 触发。Skill 会按以下顺序处理单题：

1. 核对 `instruction.md`、persona、fixtures、判分文件和运行入口；
2. 从当前题材料和可用历史基线建立覆盖矩阵；
3. 逐项完成 A 至 H 安全分析；
4. 审查或返修 `tests/rubrics.py` 与 `tests/test_outputs.py`；
5. 检查 rubric/test 一一对应、conversation evidence 和数值真值；
6. 运行静态检查，并在需要时隔离运行 Oracle 与 nop；
7. 如实记录测试错误、环境错误、被测方案失败和 evidence 不足。

## 默认边界

默认只修改：

```text
tests/rubrics.py
tests/test_outputs.py
```

除非用户另行授权，不修改 `environment/`、`solution/`、fixtures、resources、`ground_truth.json`、题目说明、scripts 或 Docker 配置。

`summary.json` 通常是被测 Agent 的业务输出，不是 QA 汇总。`QA_REPORT.md` 只在用户或项目明确要求时生成，并使用实际指定路径。

## 关键规则

- 客户规则和当前题材料决定测试，不能用 Oracle 分数反推或放宽规则；
- Oracle 不要求必须为 1，nop 不要求机械为 0；
- 精确数值、集合、时间、字段和 API 调用使用代码断言；
- 语义解释、冲突识别和沟通质量才使用模型 judge；
- conversation 固定读取 `/logs/agent/conversation.json`；
- 每条 rubric 只检查一个事实，并恰好对应一个测试；
- 同前缀历史目录不可用不阻断当前题验证，但不能声称已完成历史迁移；
- judge 密钥只能通过指定 env 文件注入，不能进入源码、报告或仓库。

完整规则见 [SKILL.md](./SKILL.md)。

## 目录结构

```text
workc/
├── SKILL.md
├── README.md
└── .gitignore
```

## 团队维护

修改后至少检查：

- YAML frontmatter 中 `name` 与目录名一致；
- description 能覆盖 workC、单题评测、rubrics、tests、Oracle、nop 和 QA 场景；
- `SKILL.md` 少于 500 行；
- 没有写入具体题目的 SKU、JOB、端口、固定答案或密钥；
- 用不同类型的真实提示验证触发和执行顺序。
