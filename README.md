# workc

通用的单题评测 QA、Oracle、nop 与判分交付 Skill，供 ZCode 团队协作维护。

## 使用方式

在 ZCode 中使用 `/workc` 触发。该 Skill 会引导完成：

- 阅读任务说明、参考文档和 resources；
- 推导当前题目的规则与可验证真值；
- 审查 `tests/rubrics.py`、`tests/test_outputs.py` 和 judge evidence；
- 执行快速 QA、Oracle 与 nop；
- 做有证据的最小修复；
- 生成中文 `environment/QA_REPORT.md` 并汇总 `summary.json`。

## 默认边界

默认只修改任务目录下的 `tests/` 和 `environment/`。`solution/`、fixtures、`ground_truth.json` 和 `scripts/` 不会在没有明确授权时修改。

## 目录结构

```text
workc/
├── SKILL.md
├── README.md
└── .gitignore
```

## 团队维护

修改 `SKILL.md` 后，请用 2–3 个不同类型的任务提示进行验证，重点检查：

1. 是否先阅读规则而不是套用旧题答案；
2. 是否把精确事实交给代码断言，把主观语义交给 judge；
3. 是否如实区分测试缺陷、环境问题、证据不足和被测方案失败；
4. 是否保留 Oracle/nop 的真实结果；
5. 是否没有越过用户授权范围。

## 触发命令

```text
/workc
```
