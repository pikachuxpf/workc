# 旧式 ClawEval / PinchBench 参考

本参考覆盖以 `rubrics.py + test_outputs.py` 为主的旧式题。不同批次可能是多轮对话/工具调用型，也可能是输出文件型；以本题材料和 runner 为准。

## 1. 材料与权威

常见材料包括 instruction、persona、fixtures/resources、grader、rubrics、tests、judge 和 test.sh。

- 多轮对话型：grader 可能提供 MUST_ASK、澄清质量、最终答案和批次安全规则；instruction 是首轮用户请求；persona 是后续披露、模糊回答、错误说法和格式约束。
- 输出文件型：从 instruction 与原始 resources 独立推导输出路径、schema、字段、数值、排序、去重、冲突和 CSV 规则。
- grader 的默认权威角色可能被批次专用正式规则覆盖；先查版本和适用范围。
- 输出型 PinchBench 完全忽略 `ground_truth.json`：不读取、不引用、不用于人工交叉验证或运行时测试；ClawEval 是否允许独立推导后人工交叉检查，必须由当前 grader/批次规则明确授权。solution 和预计算字段不能成为运行时依赖，也不能覆盖独立推导。

## 2. Rubric 设计

每条 rubric：

- 只检查一个独立事实；
- 采用唯一稳定 `RUBRIC_*` 名称；
- 与一个评分 test 一一对应；
- 简洁、正向、可验证；当前旧式规范上限为 300 字符（按最终 rubric 字符串计，包含空白与标点），除非题目级规则明确覆盖；句数仅作可读性提示，不替代字符硬限制；
- 不内含冗余 PASS/FAIL 说明，不引用其他 rubric 变量，不堆关键词示例；
- 同一错误说法的即时纠正和后续一致性若是同一事实，应合并而非重复计权。

有条件触发的对话 rubric 必须写清未触发时如何处理，并让 test 提供用户侧 evidence。不要给纯工具或纯文件题机械添加对话 rubric。

## 3. 常见覆盖角度

按材料存在性选择，不是固定配额：

- 澄清覆盖：已知参数只确认，不重复追问；缺失/模糊参数再问；
- 深入追问：题目真正要求的领域考量；
- 工具调用：列表、详情、条件调用、关键参数、次数、禁止调用；
- 跨服务推理：实体关联与因果链；
- A–H 安全：仅保留当前题适用项；
- 数据陷阱：预计算不一致、状态矛盾、空值排除、重复/冲正、专业矛盾；
- 难度模式：术语误用、错误主张、中途改值、格式、模糊披露；
- 答案质量与会话质量；
- 输出存在、解析、schema、字段、值、计数、集合、排序和一致性；
- 数值结果：记录公式、精确理论值、舍入和容差来源。

历史同前缀题只提供候选角度；每项记录迁移、拆分、纠正或不适用及依据。

## 4. Test 与 evidence

`test_outputs.py` 不得内联评分题干，只 import rubric 常量。每条评分 test 只使用一种业务判定机制；加载 evidence 的前置校验不算重复业务评分。

对话 evidence 以当前 runner schema 为准。标准适配器中常用：

- 任意助手轮次行为：全部 assistant 文本；
- 最终答案质量：最后一条 assistant 消息；
- 行为依赖用户触发：完整对话；
- 第一轮是否过早下结论：第一条 assistant 消息。

确定性事实用代码断言：文件、结构、数值、集合、ID、排序、调用记录、请求参数和哈希。只要 expected value 可由 instruction 与原始资源唯一推导，就不得仅用 judge、关键词或宽容差代替精确断言。语义事实才用 `assert_judge`。关键词仅用于必须出现/不得出现的精确数字或枚举，并须有用户触发保护；不能替代语义判断。

## 5. 缺失证据

- instruction 要求的核心文件、字段、回答或调用缺失：FAIL；
- 场景未触发：skip/不适用或题目定义的自动通过；
- 明确可选 conversation/服务未提供：按 runner 规则 excluded/skip；
- runner 未挂载必需日志、judge 故障、harness 配错：BLOCKED/infrastructure；
- 普通 `if missing: return` 会产生假通过，不用于核心输出。

## 6. 输出型 PinchBench

常见路径映射是 `/app/data/` ↔ `environment/resources/`、`/app/output/` ↔ `environment/output/`，但必须由当前题确认。检查：

1. 文件存在与真实格式；
2. 顶层类型、表头、字段名、字段类型；
3. 所有 instruction 明示条件；
4. 独立复算的关键数值与计数；
5. 主/次排序键和边界；
6. 去重后的来源集合；
7. 权威来源冲突解决；
8. CSV 行数、编码、多值分隔符；
9. 可执行脚本的合成输入动态探针（仅在授权和隔离充分时）。

旧文档中出现的 criteria.md、固定条数或固定目录只适用于其特定版本，不能覆盖当前 `rubrics.py` 任务，更不能推广到 Seal。

## 7. 人工复核

AI 草拟的 rubric、test、expected value、judge verdict 和 QA 摘要不得直接定稿。人工必须回到 grader/批次规则、instruction、persona、原始 resources 和实际 evidence 复核，至少覆盖所有失败项、安全项、条件触发项以及 code/judge 分工。Oracle 1.0 或 judge pass 不能替代规则审查。

## 8. 运行与类名

先沿 `test.sh` 确认 pytest、CTRF、class/tier 权重、judge cache 和返回码传播。import/collect 会执行模块顶层代码，属于 V2 而非纯静态。类名只有在 runner 映射或冻结规则要求时不可改；不得新增 runner 不认识的 tier。

Oracle/nop 使用全新、隔离的 output、audit、conversation、run 和 judge cache。修改 rubric/test/judge prompt 后旧结果失效，必须重跑受影响完整范围。
