---
name: workc
description: 通用单题评测 QA 与判分交付流程。用户提到 workC、单个考试题目、评测题、oracle、nop、rubrics.py、test_outputs.py、QA 报告或需要检查并优化一题的判分脚本时使用。适用于不同业务领域和后续批量任务；负责从文档与数据推导规则，运行快速 QA、Oracle、nop，做有证据的最小修复，并交付 summary.json 与中文 QA_REPORT.md。
---

# WorkC 单题 QA / Oracle / Nop 通用 SOP

## 0. 先确定任务边界

本 Skill 处理“一个任务目录、一套判分脚本、一次完整 QA”的闭环。它不是答题 Skill，也不是修改被测 Agent 方案的默认授权。

默认修改范围是：

- `tests/`
- `environment/`

默认不修改：

- `solution/`
- `ground_truth.json`
- `scripts/`
- 原始 fixtures 或题目说明

如果用户没有明确授权更宽的范围，发现问题需要修改上述目录时，先向用户说明原因并询问。不要为了提高 Oracle 分数而降低 rubric 门槛、篡改真值、伪造 evidence 或修改 nop 逻辑。

如果以下信息会改变执行方式，先询问用户，一次只问一个问题：

1. 任务目录不唯一，无法确定要处理哪一题；
2. 用户没有说明是否允许修改 `solution/`、fixtures 或 scripts，但修复确实需要超出默认范围；
3. 需要安装新软件、下载依赖或调用外部服务；
4. Judge 需要密钥，但指定的 env 文件不存在或变量不完整；
5. 运行会产生不可逆或外部发布行为；
6. 参考文档、fixture 和现有 rubric 对同一规则互相矛盾，且无法用权威来源解决。

普通路径错误、Docker 挂载方式、pytest 命令差异、可复现的临时目录等，不要先问，优先自行排查。

## 1. 读取资料：先读规则，再看代码

收到任务路径后，先确认它是单个任务目录，并检查以下结构：

```text
<task-id>/
├── instruction.md
├── environment/
│   ├── resources/
│   └── output/
├── solution/
├── tests/
│   ├── rubrics.py
│   ├── test_outputs.py
│   └── test.sh
├── scripts/
├── task.toml                 # 如果存在
└── ground_truth.json          # 只作 QA 参考，不把它当作自动真值
```

必须通读：

- `instruction.md`；
- `environment/resources/` 中与任务有关的 persona、政策、邮件、数据字典、fixture 和说明；
- 现有 `tests/rubrics.py`；
- 现有 `tests/test_outputs.py`；
- `tests/judge.py`（如果存在）；
- `tests/test.sh` 和运行脚本；
- `task.toml`（如果存在）。

路径映射按题目文档解释：

- 容器内 `/app/data/` 通常对应本地 `environment/resources/`；
- 容器内 `/app/output/` 通常对应本地 `environment/output/`。

如果题目附带 PDF、DOCX、XLSX 或 ZIP，使用对应的文档读取能力提取内容；不要只看文件名。读取时记录版本、日期、权威级别和参考日期，因为这些内容经常决定冲突处理和时间线判断。

`ground_truth.json` 可以帮助理解预期结构，但不能盲信其中的业务答案。真值应优先从正式题目规则和当前 fixtures 推导；如果 ground truth 与正式规则冲突，报告冲突，不要静默选择对分数有利的一方。

## 2. 建立“单题规则卡”

在修改测试前，先在脑中或临时笔记中整理一张规则卡。不要把某一道题的具体 SKU、JOB、端口或公式写进本 Skill。

规则卡至少包括：

### 业务目标

- Agent 需要完成什么任务；
- 需要调用哪些服务、工具或接口；
- 最终交付哪些文件或文本。

### 输入与数据

- 所有输入文件、接口和字段；
- 数据的主键、关联键和单位；
- 参考日期、时区和时间精度；
- 是否存在状态字段、保留量、软删除、重复记录或干扰项。

### 规则与优先级

- 过滤、去重、关联和排序规则；
- 计算公式、舍入、精度和边界条件；
- 正式政策、临时指令、口头要求之间的权威顺序；
- 禁止操作和安全门；
- 输出字段、类型、必填性和允许值。

### 可验证真值

逐条记录如何从当前数据得到：

- 数值；
- 集合和计数；
- 时间先后；
- 状态和分类；
- API 调用参数；
- 输出文件结构。

每个期望值都要能追溯到正式规则和当前数据。不要只复制已有测试中的常量。

## 3. 先做快速 QA，再运行完整流程

快速 QA 的目标是找出会让判分失真或无法运行的问题，而不是先追求高分。

### 3.1 静态检查

检查：

- `rubrics.py` 中所有被测试导入的名称是否真实存在；
- 是否有拼写错误、重复名称、未定义常量或循环导入；
- `test_outputs.py` 是否可以被 pytest 收集；
- fixture、输出路径和端口是否与代码一致；
- JSON、CSV、代码文件是否可以解析；
- 现有期望值是否与规则卡一致；
- 同一业务规则是否在多个测试中使用了不一致的真值；
- judge evidence 是否真的来自 output、audit 或 trajectory。

### 3.2 断言类型检查

按照以下原则重审每个测试：

**优先使用代码断言：**

- 文件存在、JSON 合法、Python 语法；
- 精确数值、金额、计数、集合、字段和枚举；
- 排序顺序；
- API 是否调用、调用次数和参数；
- 状态转换；
- 时间线先后；
- 禁止调用是否发生；
- 由 fixture 可直接推导的结构化事实。

**使用 LLM judge：**

- 是否识别了冲突；
- 是否解释采用某一权威规则的理由；
- 是否对风险、影响、优先级或业务背景作出完整说明；
- 是否完成了无法从结构化输出直接证明的语义沟通。

不要用 LLM judge 验证可以精确计算的事实。不要仅因为字段“看起来正确”就推断助手已经在 trajectory 中说明了理由。

### 3.3 证据完整性

每个 judge 都要明确：

- rubric 要判断什么；
- evidence 来自哪里；
- evidence 是否包含判断所需的完整上下文；
- 是否需要加入 assistant trajectory、API audit、原始记录或响应正文；
- 是否存在长度截断导致关键内容丢失。

证据只能来自真实运行记录或当前任务文件。不能把测试作者的结论伪装成助手的回答，也不能把 fixture 里的备注伪装成 Agent 已经报告过的内容。

## 4. 运行环境与 Docker

优先使用任务自带的运行脚本。如果脚本因任务名大小写、Docker tag、Windows/Git Bash 路径或挂载语法无法运行，先记录原因，再用等价的手动 Docker 命令验证，不要为了绕过问题直接修改 scripts。

Windows + Git Bash 下优先使用显式 bind mount：

```bash
docker run --rm \
  --env-file /e/work-C/.secrets/judge.env \
  --mount type=bind,src=/e/work-C/<task>/solution,dst=/solution \
  --mount type=bind,src=/e/work-C/<task>/tests,dst=/tests \
  <image> \
  bash -c 'mkdir -p /logs/verifier /app/output /app/scripts /app/intermediate && \
           bash /solution/solve.sh && bash /tests/test.sh'
```

根据任务实际入口调整 `solve.py`、`solve.sh`、镜像名称、服务端口和工作目录。不要假设所有题目都使用同一个端口、入口文件或服务。

如需模型 judge：

- 使用用户指定的 env 文件，例如 `E:\work-C\.secrets\judge.env`；
- 不把密钥写入报告、命令输出、源文件或提交内容；
- 检查变量是否足够，缺失时向用户询问；
- 记录“使用了指定 env 文件”，不要记录密钥值；
- 注意 judge 缓存可能影响重复运行，必要时说明是否命中缓存。

## 5. Oracle 与 nop 必须分别运行

### Oracle

Oracle 运行时挂载被测 `solution/` 和 `tests/`，用于检查真实 Agent 方案的结果和轨迹。

记录：

- pytest 总测试数、通过数、失败数；
- reward、gate、num、den（如果评分器输出）；
- 失败测试名称和原因；
- 命令返回码；
- summary.json 的关键字段。

### Nop

nop 是负向基线，按任务提供的 nop 方式运行。它不是“期望值为 0”的硬规则，也不能用 nop 的 shell 返回码推断全部测试失败或全部通过。

记录 nop 的：

- pytest 总数、通过数、失败数；
- reward；
- 返回码；
- 是否存在评分脚本管道吞掉 pytest 失败码的情况。

如果 `test.sh` 使用 `pytest | tee` 而没有 `set -o pipefail`，明确说明 shell 返回码不是测试通过信号。

## 6. 判定失败属于哪一层

每个失败都标注层级：

1. **测试自身错误**：导入错误、属性缺失、错误路径、测试逻辑异常、错误期望值；
2. **环境或运行错误**：服务未启动、依赖缺失、挂载错误、端口错误、容器问题；
3. **被测方案真实失败**：输出、API 调用或助手说明不符合正式规则；
4. **证据不足**：被测方案可能做对了，但 judge 没收到足够的真实证据；
5. **规则冲突未决**：正式文档、fixture、ground truth 或 rubric 无法一致解释。

不要把测试自身异常记成 Agent 失败。不要把证据传递缺陷当成业务错误。相反，也不要为了避免失败而把“证据不足”自动改成通过。

## 7. 最小、可追溯的修复策略

只有在快速 QA 或运行结果提供明确证据时才修改。

常见允许修复：

- 统一 rubric 名称和导入名称；
- 修正与正式规则、fixture 一致的期望值；
- 修正 rubric 中明显写反的业务条件；
- 把精确事实从 judge 改为代码断言；
- 为 judge 补充缺失但真实存在的 audit、trajectory 或原始响应证据；
- 修复测试类初始化和测试辅助函数；
- 在 `environment/` 中修复明确的运行配置或输出准备问题（仅在用户允许时）。

不允许：

- 放宽集合、数量、状态或安全约束只为提高分数；
- 删除失败测试；
- 把失败分支改成自动通过；
- 用 ground truth 覆盖正式规则而不报告；
- 伪造 assistant text 或 API audit；
- 修改 nop 使基线变好看；
- 修改 `solution/`、fixtures 或 scripts 而没有用户授权。

每次修改后都要记录文件、位置、原问题、修复理由和预期影响。

## 8. 修改后复跑与停止条件

修改后至少重新运行受影响题目的：


- Oracle；
- nop（如果测试或评分逻辑发生变化）；
- 快速 QA 或等价静态检查。

比较修改前后：

- 通过/失败数量；
- reward；
- 新增或消失的失败；
- 是否只是测试修复，还是暴露了被测方案真实问题；
- 是否出现测试误报或漏报。

当以下条件满足时停止：

- 结果可复现；
- 所有剩余失败都有明确原因；
- 没有为了分数继续放宽标准的必要；
- 修改范围符合用户授权；
- 报告可以逐项对应实际文件。

Oracle 不要求必须等于 1，nop 也不要求机械地等于 0。真实结果优先于目标分数。

## 9. QA 报告要求

每个任务生成一份中文报告，默认位置为：

```text
<task>/environment/QA_REPORT.md
```

如果任务已有根目录 `QA_REPORT.md`，先确认用户希望更新哪一份；不要悄悄维护两份内容不同的报告。

报告建议结构：

```markdown
# <任务名称> QA 报告

## 一、结论
## 二、检查对象
## 三、规则与输出检查
## 四、Oracle / nop 结果
## 五、发现的问题
## 六、实际修改
## 七、剩余失败与风险
## 八、修改范围说明
```

报告必须写清：

- 任务目录和 summary.json 路径；
- 输入资料和主要规则来源；
- 输出结构及关键结果；
- Oracle、nop 的前后分数和通过数量；
- 快速 QA 结果；
- 每个修改文件、位置和理由；
- 测试自身错误、环境错误、证据不足和被测方案失败的区分；
- judge 是否使用指定 env 文件；
- 剩余失败的具体原因；
- 未修改 `solution/`、fixtures、scripts 等范围声明；
- 如果有结果未重跑，明确写“尚未重跑”，不要用旧结果冒充最终结果。

报告语言跟随用户；中文任务默认使用中文。不要写空泛的“全部正常”，也不要只写 reward 而不写测试数量和失败原因。

## 10. 最终交付检查表

结束前逐项确认：

- [ ] 已通读 instruction 和相关 resources；
- [ ] 已检查现有 rubrics、test_outputs、judge 和运行脚本；
- [ ] 规则卡中的真值来自当前题目，而非写死本 Skill 的示例；
- [ ] 精确事实使用代码断言，主观语义才使用 judge；
- [ ] judge evidence 来自真实记录且上下文完整；
- [ ] 已完成快速 QA；
- [ ] Oracle 已运行并记录 reward、通过数和失败原因；
- [ ] nop 已单独运行并记录结果；
- [ ] 修改前后结果已比较；
- [ ] 已生成或更新中文 `environment/QA_REPORT.md`；
- [ ] 已检查 `environment/output/summary.json`；
- [ ] 已核对修改范围；
- [ ] 没有泄露密钥；
- [ ] 没有把 shell 返回码误当成 pytest 通过结果；
- [ ] 没有为了提高分数而降低标准。

## 11. 最终回复格式

最终回复先给结论，再给简洁表格和文件路径。至少包含：

1. 每个任务的 Oracle / nop reward 和通过数量；
2. summary.json 的路径和关键字段；
3. QA_REPORT.md 的路径；
4. 修改了哪些文件；
5. 仍存在的失败和原因；
6. 修改范围及未修改目录声明。

如果用户只要求处理一个任务，不要主动把其他任务当成已完成结果；只报告当前任务。
