# 本机运行环境定位与已实测范围

这是 2026-10-13 的环境快照，不是跨机器默认配置，也不是真实题包验收凭证。执行前重新确认当前任务的正式 profile、版本、镜像和入口；不得为了复用本机镜像替换正式环境。

## 现行范围替代说明（2026-10-14，不改写历史能力事实）

以下环境、adapter、合成测试、已发现未修框架行为及维护证据均保留其当时事实，不表示本轮运行或修复。本页历史维护记录中的“全部 instruction 只读”等旧权限表述，不作为现行 tests 内部冻结清单：当前 task 全部 `tests/**` 内容与同一根 `qa_report.md` 由作业员/协调者集中修复；FULL_ACCEPTANCE/无人值守无明示更窄限制时，`tests_allowlist=tests/**` 并映射同根 QA，不另设内部子集批准门。tests 内 test.sh、judge.py、runner、helper、shim、instruction、config 均可按正式依据修复；tests 外除同根 QA 均只读/移交，外侧 runner、环境、SDK/依赖、根 manifest 等冻结，不据 tests 写权编写业务实现。用户显式局部、只读或路径限制优先；按真实规范化目标判权，tests 内别名/链接指向外侧目标仍不可写。

tests 内正式 instruction 的合法修订须写前保全完整 preimage、正式来源/映射与版本，记实际变更及影响；由未接触隐藏答案的设计角色从获授权正式来源重新独立推导义务与评分设计，双冻结受影响范围，旧依赖运行标 STALE 并按影响重新验证。已接触答案的 QC reviewer 只按新冻结核终态，不承担独立设计；新合同不追认旧候选违规。详见 [runtime-acceptance.md §2](runtime-acceptance.md#2-模式和证据效力)。

QC 对整个 task（含 tests、QA、cache、日志、字节码、结果及真实别名/链接/挂载目标）仍绝无写权，不参与返修、不生成/应用补丁、不写任务 QA；仅实际作业允许执行且隔离有效时按 [质检合同 §1.1](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 核验。`.pipeline/`、秘密、隐藏 GT/oracle 读取与角色隔离、当前 FULL/历史主张依赖分流、生产证据及全部技术验收门不变。该替代说明不授权命令、真实任务、网络、外部 QC 或发布，也不复验下列历史能力。

**现行修复/移交接口**：写范围以 [主文第2节](../SKILL.md#2-先选本次作业固定验收范围) 为准，闭环及 QA 复用 [执行 SOP](execution-sop.md) 与 [报告合同](verification-and-reporting.md#7-报告与qc接口)。完整 tests 内 runner/judge/helper/shim/config/instruction 的确认缺陷，在获准范围内须 worker 实际修复、验证正式接入并写同根 QA；不能仅因环境/入口名义给建议、移交、登记或标 OUT_OF_SCOPE。可修的内部验证入口缺陷先保全修验，不以当前入口失效自动判定无法生产验证；QC 只核验，不写任务。无安全入口不先试跑，明示局部/只读/RUN_ONLY、真实目标、preimage 及答案隔离仍优先。

相关允许的 tests 外环境/SDK/配置等发现直接写同根 QA，列精确规范化路径/版本、证据、影响和责任/移交方，不改外侧；仅实际当前必需依赖缺口限制对应结论，其余记录后继续 tests 修验，不等待外侧整改。历史 adapter 或合成 PASS 不等于已修正式入口，本页后文旧“全部 instruction 只读”不作现行 tests 内冻结规则。不新增安装、执行、网络、业务实现或外侧写权，不重跑下述历史能力。

## 非秘密定位

| 对象 | 本机位置/状态 |
|---|---|
| WorkC Skill | `C:/Users/DELL/.agents/skills/workc` |
| judge 配置引用 | `C:/Users/DELL/.agents/skills/workc/.secrets/judge.env`；代理只能检查存在性、传路径，不读值 |
| Docker | `C:/Program Files/Docker/Docker/resources/bin/docker.exe`；客户端/daemon 27.5.1，desktop-linux，Linux amd64 |
| Harbor | `C:/Users/DELL/AppData/Roaming/Python/Python312/Scripts/harbor.exe`；0.18.0 |
| 合成 judge/离线 parser 镜像 | `workc-hiwork146-react-core:local`；实查 harbor-rewardkit 0.2.0、jx-react-agent 0.1.0、LiteLLM 1.103.0 |
| 本轮维护证据 | `E:/work-C/.workc-skill-validation-20261013`；独立合成夹具和报告，不是题包副本或真实 attempt |

镜像身份、命令、分数和失败记录见维护证据，不能仅凭标签认定版本未变。宿主 Python 3.12.7 不代替 Linux 声明 verifier。Windows 下先确认实际 shell；当前 Git Bash 直接传 Docker 的 `/path` 可能被 MSYS 改写，使用审过的参数列表调度或明确处理路径转换，不靠吞掉失败取得 PASS。

## 当前 React 配置对接

本机 env-file 的非秘密键名是 `JUDGE_API_KEY`、`JUDGE_BASE_URL`、`JUDGE_MODEL_ID`、`LITELLM_LOCAL_MODEL_COST_MAP`。jx-react-agent 0.1.0 实际使用 `REACT_JUDGE_API_KEY`、`REACT_JUDGE_API_BASE`，模型由 `AgentJudge.model` 或 `REACT_JUDGE_MODEL` 提供；RewardKit loader 支持 `REWARDKIT_MODEL` 覆盖 quality 模型、`REWARDKIT_JUDGE` 覆盖 backend。仅传 env-file 不代表这些路由已经匹配。

本轮合成测试在**不会启动候选的独立受信任 judge 容器内部**完成以下显式映射：JUDGE_API_KEY→REACT_JUDGE_API_KEY，JUDGE_BASE_URL→REACT_JUDGE_API_BASE，JUDGE_MODEL_ID→REWARDKIT_MODEL/REACT_JUDGE_MODEL；无 provider 前缀时按当前 OpenAI-compatible 路由补 `openai/`。模型身份非秘密，可记录；端点只记脱敏标识。此 adapter 未改正式 runner，不能当原题配置已修。

正式任务必须核其实际 backend 和允许配置：不是所有 judge 都使用这些变量，也不能对已有 `provider/model` 再拼前缀。不要在代理、宿主 Python、通用 Harbor 调度或 shell 中解析秘密做映射；env-file 只传给受信任独立 judge，候选及其工具子进程不得继承。若正式 runner 不能保证该隔离或模型/配置映射，先由 worker 按主文第2节修验获准且可修的 tests 内缺陷并写同根 QA；真实外侧缺口直接记 QA 的路径/版本、证据、影响及责任，不改外侧。确无合法安全路径且影响当前必需调用时，仅对应动态结论 BLOCKED；其余工作继续，不用另一端点救绿灯。

## 能力证据及限制

本轮用合成解释/建议义务和独立数值 check，走实际 RewardKit loader→React→只读 view→submit_score→parser→聚合：合法、等价措辞、错根因、错建议、关键词空壳、错数值、缺内容七组调用验证通过，另有无网络的完整消息/evidence/关联/原分复验及去 judge 的事实反例。两项语义在共享批次中独立绑定，权重合计 40%，事实正确但任一必达语义错误时最终合成 gate 拒绝。

只读 view 是本次 smoke 的受限工具 profile，不证明 shell/MCP/文档渲染等其他工具的安全与能力。SDK 调用及响应回执不独立证明外部/provider 缓存行为，未测层保留 UNVERIFIED。parser 已发现的非法分数接纳及部分分门控风险见 [judge-chain.md](judge-chain.md)，未修改冻结 SDK。Harbor 0.18.0 经独立合成 nop 正/负两次 trial 实测：同一算术义务、单变量输出变更，reward 分别为 1/0，verifier rc 分别为 0/1，阶段完成且 exception_info 为 null；算术测试只证明编排/挂载/verifier/结果采集能力，未调用 RewardKit scorer 或 judge API。随后另建合成交接测试，用正式 `verifier.collect` hook 冻结并实际收集合法/错根因产物，manifest 状态 `ok` 且源/快照/收集字节一致；将实际收集目录只读挂载到独立真实 React judge 后，合法输入 accepted=1、事实正确但错根因输入 accepted=0，完整原消息/evidence/raw/关联/聚合复验通过。该合成 Harbor→freeze/collection→独立 judge 的交接已实测，不是拼接两份不相干 smoke；Harbor 原 reward 仍仅确定性计分，独立 judge 的聚合另存，未回写为原 trial reward。失败预检/环境设置和修复后的结果均保留在维护报告，不用 CLI help 或直接 Docker 成功替代。

真实题包按本次作业清单与 [runtime-acceptance.md](runtime-acceptance.md) 取证：局部核目标与依赖，完整验收核全题；两 attempt、负控和外部 QC 须分别有正式采用依据。无实际 judge 不访问秘密。现行报告按 [verification-and-reporting.md §7.1–7.4](verification-and-reporting.md#7-报告与qc接口) 分本轮报告质量与历史失败 A/B 归因两层：本轮新写/更新 QA 均审实质主张、事实、状态、运行与限制，不因无 always-failing、零缺陷或仅运行而 N/A；REPORT_QC 明示窄范围优先，未指定时识别两层。关键缺陷/修法/有效性主张缺证质量 UNVERIFIED、确证错误 FAIL；准确报告技术/历史未证可质量 PASS，不等于技术、候选或历史 PASS。协调者全部报告写入自查；FULL_ACCEPTANCE/UNATTENDED 有报告写入须未参与修复的非写入 QC reviewer 独立质量审核，标准局部自查、按影响/风险复核，不新增全题独立门。开工及收口从请求、正式映射/失败标记、允许 artifact、已有 QA 历史核对象，记 history_object_status=APPLICABLE/CONFIRMED_ABSENT/UNDETERMINED 与来源版本/已查结果及影响；历史对象状态、证据状态与本次必需门按 [报告合同 §7.2](verification-and-reporting.md#72-先发现对象不能用报告自证不适用) 分开：明确历史验收请求、适用正式采用条款或当前主张依赖才产生对应历史门，FULL_ACCEPTANCE/无人值守/模板本身不增门。只有确认无对象才历史 N/A，报告自 N/A 不自证；已审未知/缺证历史保留 UNVERIFIED，未审且未请求明确记本次未请求，不改成 PASS。相应依赖历史 NOT_ADMITTED，不阻独立当前范围（包括全题）修验/报告/独立QC；全部当前必需门闭合且无必需历史门可报当前全题 PASS/UNATTENDED_COMPLETE，确有未闭合历史门仍阻包含该门的原请求全通过，不删门或自行换验收口径。保留历史行与来源；纠正无依据旧结论须说明原因和未证范围，不删行逃避实际错误修法/分类。合法查源确已 EXHAUSTED 后仅新来源、权限或版本变化时重试。本轮 preimage 不自动等于旧原题；权威原task_path用于旧修改对照，旧轨迹用于旧行为，按具体主张依赖核。当前 preimage 漏留、必需 CURRENT_RUN 缺失与真实输入 parser 兼容性未证仍按 runtime-acceptance 的当前门处理，不享历史灭失免责；本轮漏留是 WorkC 生产缺口，合法查源不倒填。复用技术、issue/轮次证据；任何报告变更核对应内容，技术按依赖失效不空重跑，仅追加准确回执不无限自指。tests/同根 QA 写入硬锁、全部 instruction 只读、独立非写入QC不参与返修、不生成/应用补丁、不写任务QA；按 [§1.1 质检可执行核验，但题包不写](qc-exceptions-and-admission.md#11-质检可执行核验但题包不写) 可非破坏性核环境、局部解析允许文本/内存探针及运行Skill检查，实际作业允许执行时才经已有有效隔离入口运行必要已获准parser/回归/verifier-only及本地oracle；QC对整个任务含tests/QA/cache/日志/字节码/结果及别名/链接/挂载落点绝无写权，须实际文件系统只读边界，-B/cache开关不足以防写，scratch仅题包外独立已获准位置且不作源码副本/补丁/staging；先核入口/import/collect/子进程副作用，无安全入口不动态运行并移交，协调者仍守自身权限/隔离；CONSULT/READ_ONLY及默认静态REPORT_QC不运行，不新增安装/配置修改/重启/候选/网络/外部judge权；.pipeline 全角色禁读、GT 独立双冻结与秘密隔离均不变。此历史合成快照不替代任何真实题证据，也不授权新的外部调用、候选或规范门；本轮 Skill 文字优化未重跑本页历史能力测试。
