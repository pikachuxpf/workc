# WorkC

WorkC/ClawEval/Seal/RewardKit 单题 tests 侧技能。修复、交付和无人值守作业的主角色是**作业员/协调者**，不是 QC：主动查找、确认、修复授权 tests/根 QA 的问题并真实验证；独立 QC 是未参与修复、题包全路径不写的专职 reviewer。现行操作顺序以 [WorkC 作业员执行 SOP](references/execution-sop.md) 为准；内外问题处置统一按 [SKILL §2](SKILL.md#2-先选本次作业固定验收范围)，实际修法、验证及外侧发现的登记按 [报告合同 §2](references/verification-and-reporting.md#2-状态归因与证据范围)，不另加审批或保护子集。修复/交付范围内已确认的 tests 内缺陷必须实际修复、完成适用合法验证并在同根 QA 登记实际修改/结果，记录、建议或移交不替代返修；明示只读、局部、指定运行及真实证据/安全限制仍优先。不承诺任何题无条件修到整题 PASS。

## 作业与结论

| 请求 | 本次对象 |
|---|---|
| 只分析/解释差异 | 咨询评估，不写不运行 |
| 静态只读、不产生文件 | 指定范围静态审核，不import/collect或写报告 |
| 修一条规则/几项反馈 | 局部修复、共享依赖、相关回归及根报告；未审全题不称全题PASS |
| 整题tests完整验收/交付自检 | 全题义务、所有规则双向、真实注册聚合、正式verifier、必需judge及已采用门 |
| 核qa_report的归因或质量 | REPORT_QC默认静态、不写题包、不运行；本轮报告质量与适用历史失败A/B分别核，明示窄范围优先，不要求候选满分；角色核验能力不生运行权 |
| 指定verifier或已有轨迹重评分 | 仅获准运行模式，不自动新rollout |

最终先回答本次对象。局部验证完成可以明确说完成；缺必需动态证据则先完成尚可合法执行的补验，仅真实受阻或用户要求阶段性交接时交接补验。报告QC、候选评分、整题技术验收与人工/平台状态分开，不成为四套额外门。

STANDARD 与 UNATTENDED 都遵守 [连续执行合同](references/continuous-execution.md)：获准 Docker 验证遇已安装组件停止，作业员自主启动、核 daemon 就绪后续跑；缺当前运行元数据则合法查源/必要重跑。阶段通过、静态 PASS 或报告准确披露未证均不允许提前结束仍可执行的必需工作。静态 qc-qa-report 与独立运行复核分流，按实际入口分别给结论；最终停止先核必需项及剩余合法路径，不靠改 QA 标签取得完成。

## 无人值守模式

下达“无人值守”或明确等价的执行指令即开启，不必逐轮催促。已有唯一明确当前task、且用户没有明确更窄范围、只读或禁写限制时，默认 `FULL_ACCEPTANCE`：当前全题tests侧自动修复验收，本请求许可整个tests/**与同根qa_report.md写入，worker将tests_allowlist映射为本次实际操作范围（默认tests/**+根QA），不另设受保护子集或逐项审批。用户明确限制优先，早前仅作业标签不阻新默认；无唯一当前task不猜题，Skill维护或纯咨询不启动题包。用户退出即停止，仅当前会话有效，不建立后台常驻或绕过工具权限提示。

worker先从允许正式材料独立推导并双冻结，核准入、备证，主动自查修 tests/QA 并真实验证，记录实际修复及有依据的不改；随后默认只读检查当前task tests外相关允许正式材料，在同根QA记录范围及问题的路径、证据、影响、责任和移交，未发现也记范围。不扫工作区，不读.pipeline或秘密；GT及oracle答案由独立QC角色核。然后派独立非写入QC实际读QC文档，核当前task、报告及外侧记录；worker核实反馈→集中tests/QA修复→真实验证→独立复检循环。显式局部/只读等限制仍按其上限，普通“直到pass”不自动启用模式。

不再默认8轮或连续2轮无进展停止。无显式预算时，尚有合法可修或补证路径就持续处理；重复无效动作不算进展，须换查证、归因或修法，只有真实无法继续才停止对应范围。尊重用户显式预算及退出：`STOPPED_BUDGET`只用于显式预算耗尽，真实无法继续为`STOPPED_BLOCKED`，不因仅计数停。准入、双冻结、真实验证、答案隔离、候选及外发标准不降，内部自动核查不变成逐项用户审批。tests外相关允许发现直接写同根QA的精确位置、证据、影响与责任，不改外侧、不等待外部先修；只有实际依赖的必需项限制对应结论，不把全部外侧缺陷变成交付门。tests侧通过与整题外部阻塞分报，移交不算修复；全部本次必需门及当前版本独立复检闭合才可`UNATTENDED_COMPLETE`，本轮新写/更新QA必须独立核本轮报告质量QC；历史失败A/B另核对象，确认无对象才历史N/A，对象未知或关键旧证据缺失UNVERIFIED；对象状态、历史审核状态与当前门的必需性分判，按 [报告合同 §7.2](references/verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 及 [§7.2.1](references/verification-and-reporting.md#721-历史未证只限制实际依赖的结论) 复用验收矩阵的 required、权威来源/采用依据和实际依赖，不另设门控状态。只有明确历史验收请求、正式采用且适用的历史条款或当前交付主张真实依赖旧失败/旧修改，才要求相应旧证据；FULL_ACCEPTANCE、无人值守、模板历史栏和旧候选失败本身均不是通用历史门。不能用报告自述N/A跳过本轮质量；非必需历史保留UNVERIFIED，当前FULL tests、当前报告及真实独立QC的自身必需门闭合后可PASS/UNATTENDED_COMPLETE，不静默降为LOCAL。明确历史门未闭合时不得称原请求全要求完成。

示例：已有唯一当前task时，`无人值守`即采用上述默认；`无人值守，静态只读，不产生文件`只审不写不跑。必需judge缺对应外发权限仍如实报告未完成，不从模式名称推导外发/候选权限。现行默认范围见 [路由与依据](references/routing-and-authority.md)，作业员自查修验、外侧只读记录、独立质检及反馈返修细则见 [无人值守闭环](references/unattended-mode.md)。旧维护记录中的作业沿用和默认轮次停止仅是历史事实，不恢复现行限制。

## 不变边界

只做测试侧作业，不做业务实现。题包由协调者单点写整个tests/**与同一根qa_report.md，写集合硬锁；tests/test.sh、tests/judge.py及tests内runner/shim/helper/instruction/config的确认缺陷均属修复责任，不另设冻结子集或allowlist审批；可在本次范围合法修复的内部验证入口缺陷先留证修复并验证，不冒称外部环境阻塞。tests_allowlist映射实际操作范围，默认tests/**+根QA；用户明示局部、只读、禁改或更窄路径限制仍约束本次操作。tests外除根QA均只读、记录移交，包括外侧instruction、runner及环境依赖；别名/链接解析后的规范化真实目标若在tests外，不因表面tests路径获写权；根QA仅授权真实同根qa_report.md，不借其别名/链接扩至其他外侧目标。独立非写入QC不参与返修、不生成或应用补丁、不写任务QA；角色可核验不等于作业获准运行。按 [质检可执行核验，但题包不写](references/qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)，可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查；仅本次实际作业允许执行时，才经已有有效隔离入口独立运行必要且已获准的parser/回归/verifier-only及本地oracle。任务所有路径（含tests、QA、cache、日志、字节码、结果及别名/链接/挂载落点）均不可被QC写入，须实际文件系统只读边界，不能仅靠-B/cache开关；scratch仅题包外独立已获准位置，不作源码副本、补丁或staging。先核入口/import/collect/子进程副作用；无安全入口就不动态运行并交协调者，后者仍遵守自身权限/隔离。CONSULT/READ_ONLY及默认静态REPORT_QC不运行；不新增安装、配置修改、重启、候选、网络/外部judge权限。独立QC reviewer在义务/评分设计双冻结后可默认静态核当前题相关GT/oracle，不需要逐题读取批准；协调者/修复角色不读GT、不接隐藏答案，不runtime依赖或外发。实际作业允许执行且必要、合法隔离可核时，本地oracle验证默认许可；独立非写入QC可在双冻结及答案输出隔离后经已有有效入口直接执行，协调者可在自身权限/隔离内编排已获准运行而不读隐藏答案，只收脱敏状态/引用。用户明示只读/禁改/禁运行、更窄范围和工具权限仍优先。`.pipeline/`全参与者始终禁读；tests外的runner/shim、环境依赖等及用户明示禁改对象保持只读，不用副本、构建或挂载绕过。整个tests写权不授权秘密/GT读取或答案暴露。秘密不读值，judge与候选隔离。外部模型上传、候选、提交/登记与领取下一题需对应授权。详见 [质检默认许可与开工准入](references/qc-exceptions-and-admission.md)。

执行 `.sh` 前先确认实际 shell；当前 Windows 工作站显式使用 Git Bash。正式 Linux verifier 不用宿主 import 冒充。

## 质量流程

为减少逐条修复后反复打回，按 [SOP §6.1–7.1](references/execution-sop.md#61-首轮完整审核与集中反馈) 首轮覆盖本次全部适用项、集中给根因清单，作业员成批修验；复检新问题说明首轮漏检、返修引入、新证据或正式新增要求，依据不明先待证，不因分类停掉真实修复。按实际依赖定向复检，未变兼容证据复用；真实新反例仍处理，建议不变门，不承诺固定轮数通过。

judge 预检先查正式配置及既有 `~/.agents/skills/workc/.secrets/judge.env`（本机 `C:/Users/DELL/.agents/skills/workc/.secrets/judge.env`），不要忘记位置就报缺配置。仅查存在性、传引用及看可信脱敏状态，不读值；正式来源优先，无 judge 不访问，存在不代替调用授权或验收。配置恢复细则见 [judge-chain §2](references/judge-chain.md#2-配置模型与真实调用预检)，真实配置不入 GitHub。

独立推导本次范围正式义务，冻结后再看当前实现；评分设计也独立冻结后才可启用质检读取例外，同版返修可重核复用。合法变更tests内正式instruction（由作业员在本次授权内修复）或外部有权负责人变更tests外instruction，导致正式合同变化后，记录授权正式来源、版本前后及实际diff；由未接隐藏答案的设计角色从授权正式来源独立重推并双冻结受影响范围，旧相关义务/评分设计及运行证据标STALE后真实重验并独立复核。不得以GT污染修法、用新instruction追认旧candidate失败或放宽仍有效的义务。事实用解析/复算，有限多解用合法集/性质，开放实现可行为验证；必要语义才用正式允许judge，不关键词/参考原文钉死。确认缺陷集中修复并保留正反例，运行证据真实、新鲜且范围足够；QC仅给缺陷位置、正式来源可独立推导的方向及脱敏状态/引用，保持不参与返修。实际核验回执复用现有运行/轮次表，记执行者、无秘密命令/模式/版本、输入输出范围及实际隔离、结果/freshness，由协调者写授权根报告，QC不写QA、不新增审批/台账。

完整验收先读 [逐项技术清单](references/pre-delivery-qa-fusion.md)：逐义务追正式来源、证据控制权、实际评分身份及聚合；全部可复算项独立参照值—实现/配置—报告三方比对；全部确定性与语义判据双向/合法等价审核，含未改项；真实输入对拍解析器，fixture不冒充真实兼容。逐项记录适用轴、预期/实际、run/版本与已实测/适用总数，缺项准确留未证，不仅追反馈，不用零发现制造缺陷。P/C仅为旧步骤映射，依赖变化才失效对应证据，不恢复旧审批或机械配额。

STANDARD 的完整验收同样必须独立复核；明确“直到 pass”或要求完成交付时，作业员按请求范围核实逐项反馈、修授权 tests/QA、补真实验证、更新报告并独立复检，直到当前版本实际通过或真实停止，不必另说“无人值守”。局部按影响和风险，不默认新增全题/QC门；其他作业上限不变。独立非写入QC实际阅读原有权威 QC 主文档及已采用条款，按当前 tests、QA 与外侧记录给逐项发现，不代写修复、不每轮重启整题；无需技术重跑不等于无需审核报告。未复现猜测不自动打回，建议不门控。有效本地真实链认可；Oracle/nop非默认。两attempt、80%/等价样本、LLM≤40%和负控按具体规范采用依据启用，不由RewardKit名字触发。已采用门严格落实。

## 材料准备与自动补证

独立义务/评分设计双冻结后、首次授权tests写入前先判定admission_status：本次必需权威原task_path、反馈映射及旧轨迹先实际VERIFIED或有正式接受替代记录，才准入依赖返修/历史QC；每个目标先保全本轮原内容/preimage。修前核future_run_plan的入口、实际授权、版本/服务/隔离及证据可生产条件，修后实际取当前正式run，不要求修前已有修后结果。评分身份台账另建，不替代历史准入；不创建.bak、整题副本或sidecar。

缺项先沿授权正式映射查源、核已有artifact，按获准模式正式重评分/生产新证据，实际核验后才闭合。只读不运行不写；新run不能替代旧行为。确已穷尽才记EXHAUSTED，逐项列精确来源/版本与实际动作/结果、缺失对象、受限主张、门控影响及required依据、责任和恢复条件；缺权限另记具体阻止，不把未查写穷尽。无新来源、权限或相关版本/依赖变化，不每轮复查同一已穷尽历史，继续当前完整修复、真实验证及独立QC；不准入只限实际依赖的历史认证/主张。旧修改对比须权威原task_path，旧行为归因须对应旧轨迹；当前修法用正式输入、本轮真实preimage/diff/终态、当前必需验证和独立QC，不捆绑全部旧材料。无当前历史必需门时当前FULL tests可PASS及UNATTENDED_COMPLETE，历史仍UNVERIFIED，不降为LOCAL，不删真门或冒全历史通过。当前引用错误/未证旧行须有据纠正或撤回依赖，保留原行、来源及纠正原因，不擦除/换标签逃避当前错误修法或分类；本轮漏留preimage、漏登记或缺必需run仍是WorkC生产缺陷，合法恢复并核实，不倒填免责。准入/计划均不是最终PASS，修后仍需实际运行证据。详见 [备证与补证](references/evidence-preparation.md)。

## 报告与指标

授权写作业维护唯一根报告，标题稳定、当前范围+轮次历史。核心结构含本轮报告质量审核；历史A/B、judge、外部门、人工平台等条件模块按需展开，不机械填全表、重排全部历史或另造sidecar。按 [报告双层合同](references/verification-and-reporting.md#7-报告与qc接口) 分列本轮质量与历史失败A/B；本轮报告写入即适用质量自查，FULL_ACCEPTANCE/UNATTENDED须独立审核，标准局部按影响复核。历史以history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED查证，只有确认无对象才历史N/A；未找清单/原题不等于无对象。历史条件表对应失败行、实际断言、可推导性、跨轨迹归因、A/B、真实修改与终态，本轮质量复用技术/issue/轮次证据，不依赖always-failing表存在。历史对象状态、历史审核状态与当前必需性分判，按 [§7.2](references/verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 和 §7.2.1 复用验收矩阵required/authority/dependency，核来源/版本/对象与受影响主张；缺manifest/旧轨迹、模板行或普通旧候选低分不创设当前门。本轮漏留preimage是WorkC生产缺口，合法恢复不倒填；无旧轨迹不编Agent失败。质量PASS不等于技术/历史PASS，关键当前主张缺证UNVERIFIED。只读不产生报告。

沿用户约定累计 `错误率=F/N0`、`漏召率=A/(N0+A)`，格式 `50%（1/2）`。原基线固定，F根因去重且修复新鲜验证，A相对基线最终新增评分身份，不按回归函数或改动次数计。原累计基线确不可恢复仍N/A，但可另立明确接手阶段基线计算后续阶段比例，不冒充原题累计。两个指标分别按已证数据计算，不因整题未PASS一律N/A；新增身份已完整核为0就填0。stdin辅助check_qa_ledger.py核对声明、身份继承/删除和算式，不读取题包、取证或认证PASS。它们不是通常的误判/漏检率或任何通过门。

本轮变化与既有用户/历史/平台异常分开，只按实际影响限制结论，不擅删未知文件或要求本轮恢复全历史。

交付前及首次独立QC前，由作业员做 [回顾登记](references/verification-and-reporting.md#731-回顾登记先对账不能把漏写当灭失)：将相关发现、反馈、实际变更、不改/撤回决定和验证与QA对账。证据还在只漏写就核来源补齐，标事后登记，不凭回忆造历史、不倒填保全、不重复计指标；缺证和错误修法另处理，补齐不等于QC通过。局部不扩全题，只读只回复，返修仅核新增/受影响项。

## 文件导航

- [WorkC 作业员执行 SOP](references/execution-sop.md)：现行操作顺序与主角色职责；不等于外部 SOP 的采用或验收证明。
- [连续执行、环境恢复与验收交接](references/continuous-execution.md)：自主启动已安装环境、静态/动态 QC 分流与最终停止闸门。
- [SKILL.md](SKILL.md)：入口、作业路由及安全边界。
- [路由与采用依据](references/routing-and-authority.md)：固定本次对象/门。
- [逐项技术审核与收口](references/pre-delivery-qa-fusion.md)：简化前 SOP 技术内核、全题逐判据、独立复算、真实解析对拍及依赖平账。
- [真实运行](references/runtime-acceptance.md)：模式、attempt、预检、取证。
- [质检默认许可与开工准入](references/qc-exceptions-and-admission.md)：无需逐题批准的GT/oracle静态核查、本地oracle验证；[§1.1 质检可执行核验，但题包不写](references/qc-exceptions-and-admission.md#11-质检可执行核验但题包不写)统一独立非写入QC、实际只读隔离与操作权限；整个tests/根报告写范围硬锁及tests外instruction只读移交；双冻结、范围审计、必需旧证据准入与修后运行时序。
- [材料准备与补证](references/evidence-preparation.md)：写前留证、合法查源/获准补跑、评分身份建账。
- [无人值守闭环](references/unattended-mode.md)：自动独立质检、返修、复检及停止。
- [验证/计数/报告](references/verification-and-reporting.md)：状态、累计指标及QC接口。
- [报告模板](assets/qa_report.template.md)：核心结构与条件模块。
- [RewardKit技术](references/seal-rewardkit.md)、[legacy技术](references/legacy-claw-eval.md)、[judge链路](references/judge-chain.md)：按实际架构/影响读。
- [历史SOP摘要](references/current-sop.md)、[本机历史快照](references/local-runtime.md)：仅线索，非当前采用或验收证明。
- [技能评估](references/skill-evals.md)：典型请求与预期。

维护使用skill-creator；相关质检及合法本地oracle验证已获作业内持续默认许可，题包写集合硬锁整个tests/**与同一根qa_report.md（明示更窄限制优先），tests内instruction/runner/config可依法修复，tests外instruction及其他外侧对象仅只读、记录移交；不另设冻结tests子集或allowlist审批；当前无题包目标不会自动启动，不扩其他写入/外发/提交权限。本地修改不等于已发布，推送/发布另需授权。辅助响应校验脚本只验证声明协议，不证明正式生产接入或语义正确。无任务/授权时不为了评估Skill启动真实候选/judge。
