# WorkC 交付前 QA 融合门

本参考定义 WorkC 在最终 tests-side 差异冻结后的 C1–C4 收口。它把结构审计、设计复审、独立数值复算与 QA 平账接到既有 P0–P4 后面，目标是提前发现需要返修的问题，而不是增加另一套规则或报告。

## 1. 边界与非目标

- 题包内写入仍只允许实际授权的 `tests/**` 子集与根目录 `qa_report.md`。
- C1–C4 不新增 criterion、check、权重、runner、sidecar、题包内清单或隐藏真值权限。
- 不读取 `ground_truth.json`，不读取或引用 `.pipeline/` 内容；正式来源与当前 runner 优先于历史质检示例。
- 不固定维度名称/数量、RewardKit 版本、canary GUID、覆盖百分比或历史题角度。
- 不把 candidate-owned evidence、Oracle 分数、judge 结论或摘要变成独立真值。
- 独立 reviewer 的 PASS 不等于人工、技术负责人、轨迹阶段或算法验收 PASS。

## 2. Canonical 输入映射

C1–C4 只读取 P0–P4 已建立或当前正式载体直接产生的事实：

| 键 | canonical 输入 | 禁止替代 |
|---|---|---|
| scope | P0 actual allowlist、execution ceiling、delivery、禁读项 | 用户措辞扩权、临时目录默认可写 |
| baseline | P1 revision、结构/身份库存、runtime loaded path/digest | 单一总 hash、manifest 表面行数 |
| claim | 正式 carrier、precedence、原子 claim、适用条件 | Oracle/GT 反推、reviewer 建议升级 |
| evidence | P2 authority/producer/writeability、endpoint/mount、fallback | candidate 文件经复制或 hash 后冒充 authority |
| controls | P3 正例、最小反例、空集/伪造/不可达/漂移控制 | 只跑 happy path、异常吞成候选 0 分 |
| freshness | P4 change-impact、run ID、全部输入与结果 digest | 跨 run 拼接、较新时间戳替代 digest |
| report | issue 台账、计数、状态向量、ready 状态、差异审计 | 第二份摘要覆盖底层 evidence |

## 3. C1 — Canonical V1 Hard Gate

1. 沿真实 `test.sh`、validator 与 tests-side self-test 找到一个 canonical V1 入口；没有现成唯一入口时，只能在正式 schema、实际 allowlist 和 runner 允许的位置建立，否则 `BLOCKED`。
2. 入口必须 fail-closed，并覆盖当前任务适用的：
   - Python/shell/TOML/YAML/schema 可解析性；
   - identity exact-once、scorer target、weight/aggregation closure；
   - manifest/quality/prompt/checks/reward/runtime 映射；
   - source/evidence carrier 的精确路径、producer 与 consumer 闭合；
   - validator 自身的单变量 drift controls。
3. 记录 command、工作目录、输入 digest、开始/结束时间、返回码、输出摘要、结果 digest 与实际 scope。
4. 多个局部脚本全部通过不自动等于 C1 PASS；只有 canonical 入口完整执行并返回成功才通过。
5. C1 状态按执行事实派生：没有合法入口、缺授权/隔离或尚未执行为 `NOT_RUN` 并附 blocker（结论需要该门时 readiness 记 `BLOCKED`）；入口已执行且发现 schema/contract/control defect 或返回非零为 `FAIL`；入口执行中断于非测试侧 infrastructure 为 `BLOCKED`；完整成功才为 `PASS`。同一轮同时有“未建立入口”和静态已知 schema defect 时，C1 仍为 `NOT_RUN`，schema defect 单列 `FAIL` issue，不用聚合状态掩盖它。
6. C1 是非候选的 tests-side 自检门。它不能代替 import/harness、candidate、Oracle、nop 或 judge 运行。

## 4. C2 — 独立设计与载体覆盖复审

由未参与本轮修复的 reviewer 只读执行，且不先接受“已修复”结论：

1. 从正式 carriers 重建原子 claim 列表与 requirement kind。
2. 对每个 score-bearing identity 复核 claim、触发条件、正反条件、正式 runner 配置声明的静态证据 owner/候选可写性契约、runtime ID、权重与归因。C2 `PASS` 只证明该静态 provenance 契约在允许载体中闭合；实际 mount/endpoint 是否按契约建立属于 V2+ 观察证据，未授权或未运行时必须阻断 `evaluation_certified`，但不自动否定已闭合的静态 C2。若连静态 owner/writeability 契约也无法建立，P1/P2/C2 均 `BLOCKED`。
3. 建立 carrier inventory：正式 source 的规范化路径、版本/digest、precedence、consumer 与完整性策略；不能用路径子串、display name 或候选自报 source 代替 exact identity。
4. 检查遗漏、重复、空集自证、fallback、锚点污染、跨模式漏召和不受信 evidence。
5. 将新发现写入现有 issue 台账。tests-side 问题返回 P1–P4 修复；冻结路径问题记 `OUT_OF_SCOPE/BLOCKED`。

## 5. C3 — 独立 Expected-value 复算

1. 从正式且允许读取的 instruction/resources/carriers 重新计算 checks 常量、边界值、集合、计数、排序、哈希、权重链与总 reward。
2. 三方比较：独立复算值、tests 实现/manifest/quality 声称值、`qa_report.md` 投影值。
3. 使用与原实现不同的推导路径或最小独立脚本；不得只调用被审实现再抄回结果。
4. 语义 claim 复核判定边界与 evidence sufficiency；可确定事实不得交给 judge 代算。
5. 无法独立推导时写 `BLOCKED/N/A`，不得由 Oracle、nop、judge、GT 或历史题数值填空。
6. 任一不一致成为 issue，并回到 P1–P4；修复后旧 C1–C3 结果全部失效。

## 5a. C2a — 逐判据对抗反例审计（静态审查看不见的行为缺陷）

C2/C3 是静态一致性检查——复算值、checks 常量、manifest、报告四方自洽就判"正确"，于是"四方一致但错"（钉死的合法范围、写死的缺失期望、伪回执照样满分）与"运行时才暴露"的问题（乱码文件名使正确 agent 判 0、真实 evidence 是 list 而解析只收 dict）全部漏网。C2a 只做行为对抗，对**每条** float 判据穷举构造最小反例并尽可能实跑，不抽查：

1. **阶段 0 版本指纹**：审计开始前对 `tests/**` 计算 digest（TESTS_HASH），记录 angle_id 集合与权重、`@criterion` 名集合、reward 权重；与同轮 C2/C3 报告的指纹比对，不一致即停止报错——错版对拍（skill 谈 A、算法谈 B）比不审计更糟。
2. **under-strict 方向**（该低分却得高分）：每条判据构造一个"不该过但可能过"的最小交付物并实跑——空/占位交付、伪回执（键在值错）、同数量不同身份（替换成员保条数/哈希）、抄关键句不内联实质、位置无关拍平扫字、关键词堆砌、计数键存在不查值、解析器少字段（真实 tool_call 但顶层无 path/name）。实际给高分即缺陷，记录输入/期望分/实际分/漏洞行。
3. **over-strict 方向**（该高分却得低分）：先过**等价解枚举门**——每条含硬编码字面量/正则/`==`/精确路径端口变量名的判据，必须构造 ≥3 个合法等价形态实跑（字面量 vs `$VAR` vs `${VAR}`、钉死变量名 vs 同义名、`$(which x)` vs `$(command -v x)` vs 绝对路径、中英同义完成态词、JSON 键序/CSV 列位置合法置换、合法内容在其他章节）；任一等价形态丢分即错杀。穷举未做完不得声明"无 over-strict 漏洞"——算法反馈的最大漏检就是"抓到别的角度，没抓到最典型的合法等价写法"。
4. **生成式双反例门**：疑似生成式对象的 float 判据，构造"内容深 vs 仅关键词堆砌、表层字段全部一致"的 twin（内容必须取自 resources 载体的真实正反例，不得现编；无可抽载体时记 W 跳过，不虚报）；分差 <0.3 = 浅代理生成式判定，建议改 likert judge。twin 差异限定在内容质量单一维度。
5. **运行可达性**：对每个路径常量在真实任务树上解析——常量值对（哈希、计数）≠ 运行可达（按路径取得到）；乱码文件名/层级错/大小写差导致 freeze 落空、正确 agent 判 0 即缺陷。
6. **环境依赖期望对拍**：依赖运行时环境的期望值（工具装没装、时区、探测顺序）与环境实际状态对拍，硬编码且与实测冲突即缺陷。
7. **实跑方法**：构造输入放临时 workspace 直接调判据；rewardkit 导入不可用时用 shim 去除装饰器副作用保留函数本体；判据读固定绝对路径/外部服务不可行时读函数体逐分支推演并标注"静态推演"。静态推演必须列反例本体与预测分，否则视为未审。
8. **反例最小化**：每个反例只改一个维度，证明是判据漏洞而非多因素叠加；同一判据双向都测，不因一边成立放过另一边。
9. **产出下限**：报告发布"实跑覆盖 M/N"与"等价解覆盖 M/N"统计及未实跑清单与理由；无法实跑的逐条说明，不得用"已覆盖"含糊带过。全表零反例时重新逐判据检查，确属穷尽则逐条说明。

C2a 发现的缺陷与 C2/C3 交叉印证：他报已标 W 的升 E 并说明互补；已标 E 的引用编号不重复写。修复后从 C1 重启闭环。

## 6. C4 — QA 平账与状态对账

机械核对以下恒等式与派生关系：

```text
N0 = R0 + T0
A = AR + AT
D = DR + DT
R1 = R0 + AR - DR
T1 = T0 + AT - DT
N1 = N0 + A - D
错误率 = F / N0
漏召率 = A / (N0 + A)
```

同时检查：

- 每个 `FIXED` issue 都有最终授权文件中的修复、常驻回归和 `FRESH/PASS` run；
- 每个 blocker 都反映到受影响的状态，且没有被 `overall_status` 隐藏；
- `F/AR/AT/A/DR/DT/D` 与 issue/case 明细一致，无法可靠重建时为 `N/A`；
- C1–C3、P0–P4、三分归因、allowlist diff 与报告时间/digest 一致；
- `test_delivery_handoff_ready` 与 `evaluation_certified` 分开派生；V1 PASS 不冒充 V2+ certification；
- platform/external status 只反映真实授权和已发生动作。

任何矛盾都使报告未闭合。只降级受影响结论，不按“多数通过”认证。

## 7. 冲突与重启策略

优先级依次为：当前正式规则/schema/runner → P0–P4 的可复核事实 → C1–C3 原始证据 → QA 报告摘要。摘要永远不能覆盖底层 evidence。

若 C1–C4 任一阶段引发 tests 或报告证据输入变化：

1. 将受影响的旧 run、复算和复审标记 `STALE`；
2. 回到最早受影响的 P gate 更新契约；
3. 冻结新差异；
4. 从 C1 重新完整执行，不能只补跑失败项；
5. 每轮保留独立 cycle ID、输入 digest、发现、修复和最终 disposition。

禁止把旧 C1、当前 C2、另一轮 C3 和新报告拼成一次 PASS。

## 8. 输出投影

C1–C4（含 C2a）不创建第二份报告。仅投影到根目录 `qa_report.md`：

- canonical V1 command/result/scope/digest；
- carrier inventory 与完整性结论；
- 独立 reviewer identity、复审 scope、findings 与 disposition；
- expected-value 三方比较与不一致；
- C2a 对抗反例表（angle_id、方向 under/over-strict、反例类型、构造输入、期望分、实际分、结论）、实跑覆盖 M/N、等价解覆盖 M/N、未实跑清单与理由、TESTS_HASH 指纹；
- cycle/restart 表；
- accounting/status reconciliation；
- 四个既有交付状态及其 reason codes/blockers。

最终差异审计仍要求实际 changed paths 属于 actual tests allowlist 加根目录 `qa_report.md`；否则 handoff 不可 READY。