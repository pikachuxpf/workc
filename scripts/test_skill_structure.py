from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    "SKILL.md",
    "README.md",
    "assets/qa_report.template.md",
    "references/routing-and-authority.md",
    "references/runtime-acceptance.md",
    "references/verification-and-reporting.md",
    "references/legacy-claw-eval.md",
    "references/seal-rewardkit.md",
    "references/judge-chain.md",
    "references/current-sop.md",
    "references/local-runtime.md",
    "references/pre-delivery-qa-fusion.md",
    "references/skill-evals.md",
    "references/unattended-mode.md",
    "references/evidence-preparation.md",
    "references/qc-exceptions-and-admission.md",
    "references/execution-sop.md",
    "references/continuous-execution.md",
)
OPERATIONS = (
    "CONSULT", "READ_ONLY", "LOCAL_REPAIR", "FULL_ACCEPTANCE", "REPORT_QC", "RUN_ONLY",
)


def heading_anchor(text: str) -> str:
    text = text.strip().lower().replace(" ", "-")
    return re.sub(r"[^\w\-]", "", text, flags=re.UNICODE)


# Only exact known historical headings WITH an in-section visible current
# supersession notice are omitted. A number/date alone never hides live rules.
HISTORICAL_SECTIONS = {
    "references/skill-evals.md": frozenset((
        "4. 2026-10-13 本次维护验证记录",
        "5. 2026-10-13 无人值守增量维护记录",
        "6. 2026-10-13 材料准备与指标台账维护记录",
        "7. 2026-10-13 质检专用例外与开工准入维护记录",
        "8. 2026-10-13 解除逐题授权条件维护记录",
    )),
    "references/current-sop.md": frozenset((
        "6. 2026-10-13 本地 QC 运行验收补充",
        "7. 历史维护的差异结论",
    )),
}
HISTORICAL_RECEIPT_HEADINGS = frozenset((
    "2026-10-14 无人值守简化维护记录",
    "2026-10-14 简化前 SOP 技术融合维护记录",
    "2026-10-14 自产 QA 报告审核优化维护记录",
    "2026-10-14 回顾登记增量维护记录",
    "2026-10-14 质检子代理执行权限维护记录",
    "2026-10-14 作业员角色与执行 SOP 维护记录",
    "2026-10-14 历史缺证与当前交付分流维护记录",
))
CURRENT_HISTORY_NOTICE = "> 现行范围替代说明："


def current_document_text(name: str, text: str) -> str:
    recognized = set(HISTORICAL_SECTIONS.get(name, ()))
    if name == "references/skill-evals.md":
        recognized.update(HISTORICAL_RECEIPT_HEADINGS)
    current = []
    # Keep each complete section unless BOTH its exact historical identity and
    # its visible current supersession are present. Notices themselves are live.
    sections = re.split(r"(?=^##\s+)", text, flags=re.MULTILINE)
    for section in sections:
        lines = section.splitlines()
        heading = re.match(r"^##\s+(.+)$", lines[0]) if lines else None
        notices = [line for line in lines if line.startswith(CURRENT_HISTORY_NOTICE)]
        historical = bool(heading and heading[1] in recognized and notices)
        current.extend(notices if historical else lines)
    return "\n".join(current)


def compact_rule_text(text: str) -> str:
    """Remove Markdown emphasis/spacing without destroying the tests/** glob."""
    return re.sub(
        r"tests/\*\*|[\s`*]+",
        lambda match: match[0] if match[0] == "tests/**" else "",
        text,
    )


def instruction_write_grants(text: str) -> list[str]:
    """Find unscoped/outside-tests instruction grants and retired write fields.

    Tests-local instruction writes are now within the worker's actual scope,
    not an instruction exception. This is a narrow textual regression detector,
    not a path authorizer: real aliases/symlinks require actual-target checks.
    A tests-local clause must not mask a later outside or generic grant. Oracle
    permissions and explicit denials/retirement explanations are not grants.
    """
    patterns = (
        r"instruction_(?:allowlist|permission_basis)(?:=WORKC_DEFAULT)?",
        r"instruction(?:默认(?:写)?许可|默认可(?:写|修)|写(?:入)?例外)",
        r"instruction.{0,24}?(?:(?<!不)可(?:修改|修复|写入|写)|(?<!不)允许(?:修改|修复|写入)|默认(?:许可|允许))",
        r"(?<!不)(?:可|允许|授权)(?:修改|修复|写入|写)(?:[a-z0-9_.*/-]*?)instruction",
        r"(?:必要|正式|精确)instruction修复.{0,60}?(?:默认许可|WORKC_DEFAULT|由(?:协调者|作业员)写)",
        r"(?:协调者|作业员).{0,40}?(?:修复|写入|写)(?:[a-z0-9_.*/-]*?)instruction",
        r"instruction.{0,24}?(?:(?<!不)由(?:协调者|作业员)(?:修改|写)|(?:自动定位|自动生成).{0,40}?(?:精确目标|精确正式载体|清单|allowlist))",
        r"tests(?:/instruction|、instruction).{0,16}?(?:写入|修改)",
    )
    local_instruction = re.compile(
        r"tests/[a-z0-9_.*/-]*instruction[a-z0-9_.*/-]*"
        r"|tests(?:内|目录内|本地|侧|内部|\*\*内)(?:的|正式|本地|载体)*instruction"
        r"|tests/\*\*(?:内|中)(?:的|正式)*instruction"
        r"|tests-localinstruction"
        r"|位于tests(?:/)?(?:内|目录内)(?:的)?instruction"
        r"|instruction(?:仅位于|位于|在)tests(?:/)?(?:内|目录内)",
        re.IGNORECASE,
    )
    traversal = re.compile(r"tests/(?:[a-z0-9_.-]+/)*\.\./", re.IGNORECASE)
    escape_reference = re.compile(
        r"(?:指向|逃逸|越界|链接到|重定向|别名).{0,24}"
        r"(?:environment|persona|solution|tests外|tests之外|根|题包外)",
        re.IGNORECASE,
    )
    denial = re.compile(
        r"(?:不(?:再)?(?:设|导入|开放|保留|允许|授予|授权|生成|要求|记录|使用)|禁止|取消|撤销).{0,16}$"
    )
    retirement = re.compile(r"^(?:已)?(?:撤销|取消|废止)|^不再(?:使用|要求|生成|记录)")
    grants = []
    # Split before removing whitespace, so a newline does not merge two grants.
    for raw_clause in re.split(r"[。；;，,|\n]", text):
        clause = compact_rule_text(raw_clause)
        # Scope EACH carrier mention, not the clause. A separate outside denial
        # must not reactivate a permitted local grant; a separate outside grant
        # remains visible. A traversal or escape attached to this local carrier
        # is deliberately retained for detection rather than scoped away.
        def mask_local(match: re.Match[str]) -> str:
            following = clause[match.end():]
            next_carrier = re.search(r"instruction", following, re.IGNORECASE)
            related = following[:next_carrier.start()] if next_carrier else following
            if traversal.search(match[0]) or escape_reference.search(related):
                return match[0]
            return "TESTS_LOCAL_CARRIER"

        source = local_instruction.sub(mask_local, clause)
        for pattern in patterns:
            for match in re.finditer(pattern, source, re.IGNORECASE):
                if denial.search(source[:match.start()]) or retirement.search(source[match.end():]):
                    continue
                grants.append(match[0])
    return grants


class SkillStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.documents = {
            name: (ROOT / name).read_text(encoding="utf-8") for name in DOCUMENTS
        }

    def test_frontmatter_and_size(self) -> None:
        skill = self.documents["SKILL.md"]
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter)
        fields = dict(re.findall(r"^(name|description):\s*(.+)$", frontmatter[1], re.MULTILINE))
        self.assertEqual(fields["name"], ROOT.name)
        self.assertTrue(fields["description"].strip())
        self.assertLess(len(skill.splitlines()), 500)

    def test_local_links_and_anchors(self) -> None:
        for name, text in self.documents.items():
            for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                target, _, fragment = unquote(link).partition("#")
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                    continue
                path = (ROOT / name).parent / target if target else ROOT / name
                with self.subTest(document=name, link=link):
                    self.assertTrue(path.is_file(), f"missing local target: {path}")
                    if fragment:
                        content = path.read_text(encoding="utf-8")
                        headings = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)
                        self.assertIn(fragment, {heading_anchor(item) for item in headings})

    def test_safety_boundaries_retained(self) -> None:
        skill = self.documents["SKILL.md"]
        for requirement in (
            "只处理单题 tests 侧评分设计、抽检、修复、验证与报告，不完成业务实现。",
            "禁止 WorkC 的任何参与者读取、引用或依赖 .pipeline/ 内容",
            "作业员可修当前题 `tests/**` **全部内容**及同一题根 `qa_report.md`",
            "不另造更窄保护子集、不索要逐文件批准",
            "tests 内的 instruction/正式需求载体、runner、judge、helper/shim、`test.sh`、配置及依赖描述等均可按正式依据修复",
            "`tests_allowlist` 仅记录实际范围映射，默认 `tests/** + qa_report.md`",
            "tests 外除同根 QA 全部只读、不修改",
            "QC 仍对 task 全路径不写",
            "协调者和修复角色不读 GT、不接收隐藏答案",
            "执行 `.sh` 或容器入口前必须先确认实际 shell",
        ):
            self.assertIn(requirement, skill)

    def test_operations_are_documented_consistently(self) -> None:
        for name in ("SKILL.md", "references/routing-and-authority.md", "references/runtime-acceptance.md"):
            for operation in OPERATIONS:
                with self.subTest(document=name, operation=operation):
                    self.assertIn(operation, self.documents[name])

    def test_report_has_scope_and_qc_interface(self) -> None:
        template = self.documents["assets/qa_report.template.md"]
        self.assertTrue(template.startswith("# {{task_id}} QA报告\n"))
        for heading in (
            "## 当前结论与本次范围",
            "### 本次验收要求与证据矩阵",
            "### 独立义务与覆盖差异",
            "### 逐规则实现与双向证据",
            "### 当前 issue 与移交台账",
            "## 条件证据模块",
            "### 报告逐行 A/B 归因与修改终态",
            "## 轮次记录（追加，不覆盖历史）",
        ):
            self.assertIn(heading, template)
        for column in ("正式输入可推导性", "Agent 实际行为/相关轨迹", "修改前后与终态证据", "QC 裁决"):
            self.assertIn(column, template)

    def test_eval_scenarios_exist(self) -> None:
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-01", "EVAL-02", "EVAL-03", "B31", "B32"):
            self.assertIn(identity, evaluations)

    def test_no_legacy_global_wording(self) -> None:
        retired = (
            "批次指令，常驻",
            "tests 不变时用 `report-only`，纯咨询才 `chat-only`",
            "最终回复先给整题技术验收",
            "任何适用的 V1+ 验证",
            "冻结后的 `R0/T0/N0`、`AR/AT/A` 与以下公式保持不变",
        )
        for name, text in self.documents.items():
            for wording in retired:
                with self.subTest(document=name, wording=wording):
                    self.assertNotIn(wording, text)

    def test_adopted_degraded_scope_is_explicit(self) -> None:
        for name in ("SKILL.md", "references/runtime-acceptance.md", "assets/qa_report.template.md"):
            text = self.documents[name]
            with self.subTest(document=name):
                self.assertIn("reward_degraded", text)
                self.assertRegex(text, r"全部\s*judge|所有\s*judge")

    def test_adopted_tool_field_audit_is_retained(self) -> None:
        for name in ("SKILL.md", "references/runtime-acceptance.md", "assets/qa_report.template.md"):
            with self.subTest(document=name):
                self.assertIn("name/arguments/result", self.documents[name])
                self.assertIn("三字段族", self.documents[name])

    def test_unattended_trigger_and_separate_mode(self) -> None:
        for name in ("SKILL.md", "README.md", "references/routing-and-authority.md"):
            with self.subTest(document=name):
                self.assertIn("UNATTENDED" if name != "README.md" else "无人值守模式", self.documents[name])
        mode = self.documents["references/unattended-mode.md"]
        self.assertIn("咨询", mode)
        self.assertIn("BLOCKED_MISSING_TARGET", mode)
        self.assertIn("只读/不产生文件", mode)
        self.assertIn("不假定跨会话持久开关", mode)

    def test_unattended_independent_qc_and_single_writer(self) -> None:
        mode = self.documents["references/unattended-mode.md"]
        for requirement in (
            "作业员即主 WorkC/协调者", "子代理不写题包，但可执行安全核验",  "首次质检必须真正读取",
            "qc-qa-report/SKILL.md", "当前版本", "NOT_ADMITTED", "相关结论 UNVERIFIED",
        ):
            self.assertIn(requirement, mode)
        self.assertIn("独立质检与返修闭环（完整验收或本次明确要求时；无人值守自动推进）", self.documents["assets/qa_report.template.md"])

    def test_unattended_has_truthful_stops_without_default_count_limits(self) -> None:
        mode = self.documents["references/unattended-mode.md"]
        for requirement in (
            "不设默认轮次上限", "尚有合法可修或补证路径就继续",
            "STOPPED_BLOCKED", "STOPPED_BUDGET", "用户显式预算",
            "UNATTENDED_COMPLETE", "不自动等于 PASS", "不让reviewer写补丁",
        ):
            self.assertIn(requirement, mode)
        for name, text in self.documents.items():
            for retired in ("max_rounds=8", "max_no_progress_rounds=2", "STOPPED_NO_PROGRESS"):
                with self.subTest(document=name, retired=retired):
                    self.assertNotIn(retired, current_document_text(name, text))

    def test_unattended_defaults_to_full_tests_repair_with_explicit_limits_first(self) -> None:
        skill = self.documents["SKILL.md"]
        mode = self.documents["references/unattended-mode.md"]
        self.assertIn("默认 `FULL_ACCEPTANCE`", skill)
        for requirement in (
            "单独“无人值守”默认 FULL_ACCEPTANCE",
            "作业员将 tests_allowlist 映射为本次实际操作范围（默认tests/**+根QA）",
            "不另设冻结子集或逐项审批",
            "用户明确的更窄范围", "此前仅标为局部的作业标签不阻该默认",
            "Skill 维护", "普通新候选执行或外发授权",
        ):
            self.assertIn(requirement, mode)

    def test_unattended_worker_first_external_read_only_and_feedback_loop(self) -> None:
        mode = self.documents["references/unattended-mode.md"]
        steps = (
            "**作业员先自查修验**", "**tests 外只读检查并记录**",
            "**独立质检**", "**作业员核实并处置反馈**", "**反馈返修**",
            "**真实验证**", "**更新并复检**", "**判定并继续**",
        )
        positions = [mode.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for requirement in (
            "未发现也记范围", "精确路径、实际证据", "责任方和移交状态",
            "无关缺陷或建议不阻 tests 闭环", "记录不是修复",
            "tests 侧通过、报告 QC 与整题外部阻塞分别报告",
        ):
            self.assertIn(requirement, mode)

    def test_unattended_eval_scenarios_exist(self) -> None:
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-U01", "EVAL-U02", "EVAL-U03", "U10"):
            self.assertIn(identity, evaluations)

    def test_evidence_preparation_is_routed(self) -> None:
        for name in ("SKILL.md", "README.md", "references/unattended-mode.md", "references/runtime-acceptance.md"):
            with self.subTest(document=name):
                self.assertIn("evidence-preparation.md", self.documents[name])
        evidence = self.documents["references/evidence-preparation.md"]
        for kind in ("ORIGINAL_TASK", "ROUND_PREIMAGE", "HISTORICAL_TRAJECTORY", "CURRENT_RUN", "SCORING_BASELINE"):
            self.assertIn(kind, evidence)
        self.assertRegex(evidence, r"首次\s*(?:授权\s*)?tests\s*写入前")
        self.assertIn("不能替代旧报告历史归因", evidence)

    def test_evidence_gaps_and_metric_ledger_are_explicit(self) -> None:
        evidence = self.documents["references/evidence-preparation.md"]
        for requirement in ("MISSING_RECOVERABLE", "EXHAUSTED", "NEEDS_AUTHORIZATION", "check_qa_ledger.py", "origin=handoff"):
            self.assertIn(requirement, evidence)
        self.assertIn("材料准备、修改前留证与补证结果", self.documents["assets/qa_report.template.md"])
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-E01", "EVAL-E02", "EVAL-E03"):
            self.assertIn(identity, evaluations)

    def test_qc_contract_is_routed_consistently(self) -> None:
        for name in DOCUMENTS:
            if name in ("references/local-runtime.md", "references/qc-exceptions-and-admission.md"):
                continue
            with self.subTest(document=name):
                self.assertIn("qc-exceptions-and-admission.md", self.documents[name])

    def test_qc_exception_requires_role_freezes_and_authority(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        for requirement in (
            "独立 QC reviewer", "obligation_freeze_ref", "scoring_design_freeze_ref",
            "qc_permission_basis=WORKC_DEFAULT", "qc_read_scope", "actual_reads", "未双冻结",
            "本地 oracle 验证默认许可", "QC 执行仍不得写题包", ".pipeline/",
            "协调者/修复角色不直接读 GT", "不接收原文、答案",
            "未授权服务", "不需要逐题读取授权",
        ):
            self.assertIn(requirement, contract)

    def test_write_scope_distinguishes_tests_local_carriers_from_outside(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        self.assertIn("## 2. 写范围接口", contract)
        scope_mapping = self._live_rule_paragraph(
            "references/qc-exceptions-and-admission.md", "## 2. 写范围接口",
            "- 唯一范围定义见",
        )
        for requirement in (
            "仅作业员（协调者）写当前题tests/同根QA",
            "子Agent和QC全路径不写",
            "完整修复/无人值守默认全tests，tests_allowlist仅作实际映射",
            "用户明确更窄限制优先",
        ):
            self.assertIn(requirement, scope_mapping)
        actual_targets = self._live_rule_paragraph(
            "references/qc-exceptions-and-admission.md", "## 2. 写范围接口",
            "- 写前按该节核规范化实际目标",
        )
        for requirement in (
            "核规范化实际目标、链接和重定向",
            "完整tests范围包括instruction、runner/验证入口、judge、helper、shim和config",
            "范围内确认缺陷须由worker实际修复、适用验证并写同根QA",
            "不以类型标OUT_OF_SCOPE，不只给建议/登记/移交",
            "真实目标落到tests外则不写",
            "相关允许材料的发现直接入同根QA",
            "仅当前必需依赖缺口限制对应结论，其余记录后继续，不等待外侧整改",
            "明确局部/只读/RUN_ONLY等上限仍优先",
        ):
            self.assertIn(requirement, actual_targets)
        self.assertIn("SKILL.md#2-先选本次作业固定验收范围", contract)
        skill = self.documents["SKILL.md"]
        scope = re.search(r"^## 2\..*?\n(.*?)(?=^## 3\.|\Z)", skill, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(scope)
        compact = compact_rule_text(scope[1])
        for requirement in (
            "tests/**", "qa_report.md", "tests_allowlist",
            "保全可信preimage", "实际变更、正式来源/版本前后及影响", "STALE",
            "由未接触隐藏答案的设计角色从新正式输入重推并依次双冻结受影响范围",
            "不得据GT放宽规则、以新合同追认旧候选违规或改写旧事实",
            "附带反馈只是起始线索，不因有反馈改成LOCAL_REPAIR",
            "只有用户明确限定某文件、某问题或“仅按这些反馈”时才选局部作业",
            "局部验收范围与写路径边界分开",
        ):
            self.assertIn(requirement, compact)

    def test_current_documents_do_not_revive_outside_instruction_write_grants(self) -> None:
        for name, text in self.documents.items():
            with self.subTest(document=name):
                self.assertEqual(
                    instruction_write_grants(current_document_text(name, text)), [],
                    "current rules must not grant unscoped/outside-tests instruction writes or require retired write fields",
                )

    def test_write_grant_check_distinguishes_tests_local_outside_denial_and_oracle(self) -> None:
        self.assertEqual(compact_rule_text("`tests/**` **全部内容**"), "tests/**全部内容")
        permitted = (
            "必要合法本地 oracle 验证默认许可，无需逐题批准。",
            "此前 instruction 写例外已撤销，不生成 instruction_allowlist。",
            "不再要求 instruction_permission_basis=WORKC_DEFAULT。",
            "tests外 instruction 仅只读，不由作业员修改。",
            "instruction 不由协调者写。",
            "外部有权负责人变更 instruction 后重新独立推导并冻结。",
            "作业员修复 tests/instruction.md 并同步根报告。",
            "tests内 instruction 默认可修。",
            "允许修改 tests/output/instruction.md。",
            "首次 tests/instruction 写入前保全。",
            "tests-local instruction 可修改。",
            "instruction 位于 tests 内可修改。",
            "位于 tests 内的 instruction 由协调者写。",
            "tests/**中的正式 instruction 可修改。",
            "`tests/**` 内的正式 instruction 可修改。",
            "tests/instruction/extra.md实际目标在tests外，不沿链接改环境。",
            "tests/instruction/extra.md实际目标在tests外，仅记录移交。",
            "tests内instruction可修；tests外instruction不允许修改。",
            "tests 内 instruction 可修改且 tests 外 instruction 只读。",
            "tests/instruction.md可修改且根instruction.md不可修改。",
        )
        for text in permitted:
            with self.subTest(text=text):
                self.assertEqual(instruction_write_grants(text), [])
        forbidden = (
            "instruction 默认可修。",
            "instruction默认写许可来自统一合同。",
            "必要 instruction 修复按 WORKC_DEFAULT 默认许可。",
            "作业员修复 instruction 并同步报告。",
            "架构与授权：instruction_allowlist、instruction_permission_basis=WORKC_DEFAULT。",
            "tests外 instruction 默认可修。",
            "根 instruction.md 可修改。",
            "允许修改 environment/instruction.md。",
            "tests/instruction.md 链接指向 environment/instruction.md 可写入。",
            "作业员修复 tests/../instruction.md。",
            "允许修改 tests/output/../../instruction.md。",
            "instruction 路径批准、由作业员修改。",
            "instruction 由协调者写。",
            "instruction 不由作业员修改但由协调者写。",
            "instruction 不由作业员修改，instruction 默认可修。",
            "tests内instruction可修；tests外instruction也可修复。",
            "tests 内 instruction 可修改且 tests 外 instruction 可修改。",
            "tests/instruction.md可修改且根instruction.md也可修改。",
            "tests/instruction.md链接指向tests外instruction.md可修改。",
            "tests内instruction可修。\ninstruction默认可修。",
            "tests内instruction可修并且instruction默认可修。",
        )
        for text in forbidden:
            with self.subTest(text=text):
                self.assertTrue(instruction_write_grants(text))

    def test_history_filter_is_explicit_and_keeps_live_replacements(self) -> None:
        evaluations = (
            "tests外instruction只读。\n"
            "## 7. 2026-10-13 质检专用例外与开工准入维护记录\n"
            f"{CURRENT_HISTORY_NOTICE} tests内instruction可修；tests外instruction只读。\n"
            "instruction默认可修。\n"
            "## 8. 2026-10-13 解除逐题授权条件维护记录\n"
            f"{CURRENT_HISTORY_NOTICE} tests内instruction可修；tests外instruction只读。\n"
            "instruction_allowlist。\n"
            "## 2026-10-14 作业员角色与执行 SOP 维护记录\n"
            "instruction默认可修。\n"
            f"{CURRENT_HISTORY_NOTICE} tests内instruction可修；tests外instruction只读。\n"
            "## 9. 现行维护\n作业员修复tests/instruction.md。"
        )
        filtered = current_document_text("references/skill-evals.md", evaluations)
        self.assertIn(CURRENT_HISTORY_NOTICE, filtered)
        self.assertEqual(instruction_write_grants(filtered), [])
        for added in (
            "\ninstruction 默认可修。",
            "\n## 2026-10-15 新现行规则\ninstruction默认可修。",
        ):
            with self.subTest(added=added):
                self.assertTrue(instruction_write_grants(current_document_text(
                    "references/skill-evals.md", evaluations + added
                )))
        notice = evaluations.replace(
            f"{CURRENT_HISTORY_NOTICE} tests内instruction可修；tests外instruction只读。",
            f"{CURRENT_HISTORY_NOTICE} tests外instruction默认可修。",
        )
        self.assertTrue(instruction_write_grants(current_document_text(
            "references/skill-evals.md", notice
        )))
        # Unknown numbered sections and known records lacking a notice are live.
        for name, heading in (
            ("references/skill-evals.md", "7. 现行权限"),
            ("references/current-sop.md", "6. 现行权限"),
            ("references/skill-evals.md", "7. 2026-10-13 质检专用例外与开工准入维护记录"),
            ("references/skill-evals.md", "2026-10-14 作业员角色与执行 SOP 维护记录"),
            ("references/current-sop.md", "7. 历史维护的差异结论"),
        ):
            candidate = f"## {heading}\ninstruction默认可修。"
            with self.subTest(document=name, heading=heading):
                self.assertIn("instruction默认可修", current_document_text(name, candidate))
                self.assertTrue(instruction_write_grants(current_document_text(name, candidate)))
                if "现行权限" in heading:
                    # Even a notice cannot hide an unrecognized live heading.
                    candidate += f"\n{CURRENT_HISTORY_NOTICE} tests外instruction只读。"
                    self.assertTrue(instruction_write_grants(current_document_text(name, candidate)))
        sop_history = (
            "## 6. 2026-10-13 本地 QC 运行验收补充\n"
            f"{CURRENT_HISTORY_NOTICE} tests外instruction只读。\n"
            "instruction默认可修。\n"
            "## 7. 历史维护的差异结论\n"
            f"{CURRENT_HISTORY_NOTICE} tests外instruction只读。\n"
            "instruction_allowlist。\n"
        )
        self.assertEqual(instruction_write_grants(current_document_text(
            "references/current-sop.md", sop_history
        )), [])
        sop_live = sop_history + "## 8. 现行替代\ninstruction默认可修。"
        self.assertTrue(instruction_write_grants(current_document_text("references/current-sop.md", sop_live)))
        # Known receipt labels in any other document are not a hiding mechanism.
        self.assertTrue(instruction_write_grants(current_document_text("README.md", evaluations)))
        for name, headings in HISTORICAL_SECTIONS.items():
            for heading in headings:
                section = re.search(
                    rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
                    self.documents[name], re.MULTILINE | re.DOTALL,
                )
                with self.subTest(document=name, historical_heading=heading):
                    self.assertIsNotNone(section)
                    self.assertRegex(section[1], rf"(?m)^{re.escape(CURRENT_HISTORY_NOTICE)}")
        for heading in HISTORICAL_RECEIPT_HEADINGS:
            section = re.search(
                rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
                self.documents["references/skill-evals.md"], re.MULTILINE | re.DOTALL,
            )
            with self.subTest(receipt=heading):
                self.assertIsNotNone(section)
                self.assertRegex(section[1], rf"(?m)^{re.escape(CURRENT_HISTORY_NOTICE)}")
                self.assertIn("当时事实及测试结果", section[1])
                self.assertIn("不构成本次结果回执", section[1])

    def test_admission_distinguishes_history_and_future_run(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        for requirement in (
            "ADMITTED / NOT_ADMITTED / N/A", "historical_requirements",
            "ROUND_PREIMAGE", "future_run_plan", "只将实际依赖旧材料的项 NOT_ADMITTED",
            "不启动依赖缺口的循环", "修前不要求已有修后结果",
            "计划不能填 CURRENT_RUN=VERIFIED", "修后实际取得正式 CURRENT_RUN",
            "独立当前全题范围继续修验", "handoff 指标",
        ):
            self.assertIn(requirement, contract)
        for name in ("SKILL.md", "assets/qa_report.template.md", "references/routing-and-authority.md"):
            for field in ("admission_status", "future_run_plan"):
                with self.subTest(document=name, field=field):
                    self.assertIn(field, self.documents[name])

    def test_exception_eval_positive_and_negative_cases_exist(self) -> None:
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-Q01", "EVAL-Q02", "EVAL-Q03"):
            self.assertIn(identity, evaluations)
        for requirement in ("没有任何单独GT/oracle读取批准", "允许必要本地oracle验证", "不启动该返修", "修前当然没有修后CURRENT_RUN"):
            self.assertIn(requirement, evaluations)
        q02 = re.search(r"^### EVAL-Q02[^\n]*\n(.*?)(?=^### EVAL-Q03)", evaluations, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(q02)
        scenario = re.sub(r"\s+", "", q02[1])
        self.assertRegex(scenario, r"instruction/extra\.md[^。\n]*链接指向environment/setup\.sh")
        self.assertRegex(scenario, r"根instruction\.md在tests外只读[^。\n]*不修改")
        self.assertRegex(scenario, r"tests内正式instruction载体可由worker按实际范围修复")
        for requirement in ("写前基线", "双冻结", "STALE", "不写task", "不削弱有效义务救候选"):
            self.assertIn(requirement, scenario)
        self.assertRegex(scenario, r"不沿链接改环境|不得沿链接(?:修改|写入)环境")

    def test_retired_absolute_boundaries_not_reintroduced(self) -> None:
        retired = (
            "ground_truth.json和.pipeline/连离线交叉核查也禁读",
            "ground_truth.json与.pipeline/内容始终禁读",
            "ground_truth.json/.pipeline/始终不读",
            "QC文档要求的ground_truth/oracle或冻结路径操作不能导入WorkC",
            "不能导入例外，也不能把整个可执行质量流程丢弃",
            "外部禁读例外、多份报告或冻结路径修改不导入 WorkC",
        )
        for name, text in self.documents.items():
            for requirement in retired:
                with self.subTest(document=name, wording=requirement):
                    self.assertNotIn(requirement, text)

    def test_default_permissions_do_not_need_per_task_approval(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        for requirement in (
            "不再索要单独 GT/oracle 批准", "不再索要独立 oracle 执行批准",
            "不启动当前不存在的题包作业",
            "工具权限拒绝不能", "普通候选新 rollout",
        ):
            self.assertIn(requirement, contract)
        for name in ("SKILL.md", "README.md", "assets/qa_report.template.md"):
            with self.subTest(document=name):
                self.assertIn("默认许可", self.documents[name])
                self.assertIn("oracle", self.documents[name])

    def test_permission_basis_is_not_a_new_approval_field(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        field = "qc_permission_basis=WORKC_DEFAULT"
        self.assertIn(field, contract)
        self.assertIn(field, self.documents["assets/qa_report.template.md"])
        for name in ("SKILL.md", "assets/qa_report.template.md", "references/routing-and-authority.md"):
            with self.subTest(document=name):
                self.assertEqual(
                    instruction_write_grants(current_document_text(name, self.documents[name])), [],
                    "tests-local instruction is in actual scope, not a separate approval field or outside write grant",
                )
        self.assertNotIn("qc_authority_ref", contract)
        self.assertNotIn("instruction_authority_ref", contract)
        for name in ("SKILL.md", "README.md", "assets/qa_report.template.md", "references/unattended-mode.md", "references/routing-and-authority.md"):
            with self.subTest(document=name):
                self.assertNotIn("实际题包读取授权及适用条款存在后", self.documents[name])
                self.assertNotIn("instruction_authority_ref", self.documents[name])

    def test_full_technical_checklist_is_routed(self) -> None:
        for name in (
            "SKILL.md", "README.md", "references/unattended-mode.md",
            "references/runtime-acceptance.md", "references/verification-and-reporting.md",
            "assets/qa_report.template.md", "references/seal-rewardkit.md",
            "references/judge-chain.md",
        ):
            with self.subTest(document=name):
                self.assertIn("pre-delivery-qa-fusion.md", self.documents[name])
        checklist = self.documents["references/pre-delivery-qa-fusion.md"]
        for requirement in (
            "a31c7d0", "全部实际评分判据", "未修改项", "不以外部两遍 QC 是否采用为前提",
            "LOCAL_REPAIR", "READ_ONLY", "不另设权限等级", "不回滚旧权限或机械配额",
        ):
            self.assertIn(requirement, checklist)

    def test_full_audit_has_independent_recomputation_and_ownership(self) -> None:
        checklist = self.documents["references/pre-delivery-qa-fusion.md"]
        for requirement in (
            "独立参照值—实现/配置声称值—报告值", "调用被审函数再抄结果不算独立复算",
            "source→manifest", "runtime→result exact-once", "满分可达性",
            "mutation path", "backing state", "不能自证独立真值",
            "合法权威空集", "不证明动作完成", "基础设施失败",
        ):
            self.assertIn(requirement, checklist)

    def test_all_criteria_have_applicability_and_measured_evidence(self) -> None:
        checklist = self.documents["references/pre-delivery-qa-fusion.md"]
        for requirement in (
            "部分分和语义项", "正式尺度", "已实测/适用总数", "静态推演另列",
            "零已发现缺陷不等于漏审", "空集与顺序", "对象与字段身份",
            "锚点污染", "合法等价", "语义浅代理", "适用反例未测",
        ):
            self.assertIn(requirement, checklist)
        template = self.documents["assets/qa_report.template.md"]
        for requirement in (
            "独立复算与真实输入对拍", "独立参照值", "实现/配置声称值",
            "已实测/适用总数", "未验证原因", "变更依赖与证据新鲜度",
        ):
            self.assertIn(requirement, template)

    def test_real_input_and_dependency_revalidation_are_distinct(self) -> None:
        checklist = self.documents["references/pre-delivery-qa-fusion.md"]
        runtime = self.documents["references/runtime-acceptance.md"]
        self.assertIn("标准局部作业不新增全题外侧巡检或额外独立QC门", runtime)
        self.assertIn("本次作业适用清单", checklist)
        self.assertIn("CONSULT/READ_ONLY 仅完成获准静态部分", checklist)
        for requirement in (
            "合法正式导出的真实输入样本", "自产 fixture", "真实兼容性 UNVERIFIED",
            "不启动未经授权的新候选", "负向空集不强行非空",
            "按技术依赖标受影响证据STALE", "任何报告变更均核对应内容", "技术依赖未变可复用 FRESH 证据",
            "不空重跑 verifier", "不拼不兼容评分版本",
            "不机械每轮从 C1 全题重启",
        ):
            self.assertIn(requirement, checklist)
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-S01", "EVAL-S02", "EVAL-S03"):
            self.assertIn(identity, evaluations)

    def test_report_quality_and_history_are_separate_across_live_interfaces(self) -> None:
        for name in (
            "SKILL.md", "README.md", "assets/qa_report.template.md",
            "references/verification-and-reporting.md", "references/unattended-mode.md",
            "references/routing-and-authority.md", "references/runtime-acceptance.md",
            "references/evidence-preparation.md", "references/qc-exceptions-and-admission.md",
            "references/pre-delivery-qa-fusion.md", "references/legacy-claw-eval.md",
            "references/seal-rewardkit.md",
        ):
            text = current_document_text(name, self.documents[name])
            compact = re.sub(r"[\s`*]+", "", text)
            with self.subTest(document=name):
                self.assertIn("本轮报告质量", compact)
                self.assertRegex(compact, r"历史(?:失败)?A/B")
                if name != "references/verification-and-reporting.md":
                    self.assertIn("verification-and-reporting.md", text)

    def test_history_na_requires_object_discovery_not_report_self_claim(self) -> None:
        for name in (
            "SKILL.md", "assets/qa_report.template.md", "references/unattended-mode.md",
            "references/routing-and-authority.md", "references/verification-and-reporting.md",
        ):
            text = self.documents[name]
            with self.subTest(document=name):
                for state in ("APPLICABLE", "CONFIRMED_ABSENT", "UNDETERMINED"):
                    self.assertIn(state, text)
        contract = self.documents["references/verification-and-reporting.md"]
        for requirement in (
            "没有 always-failing 清单也不能 N/A", "报告自标 N/A", "未找到清单/原题",
            "均不能证明不存在", "历史 N/A 仅用于 CONFIRMED_ABSENT",
            "未查不能报 EXHAUSTED", "不删除历史来制造无对象",
        ):
            self.assertIn(requirement, contract)
        retired = (
            "报告QC无对象记N/A", "适用报告QC无对象N/A", "没有对象N/A，关键证据缺失",
            "| B16 | 无报告或无always-failing对象 | QC N/A",
            "| 报告归因QC结论 | 全部适用反馈行",
        )
        for name, text in self.documents.items():
            for wording in retired:
                with self.subTest(document=name, wording=wording):
                    self.assertNotIn(wording, current_document_text(name, text))

    def test_current_report_production_chain_and_missing_preimage_responsibility(self) -> None:
        contract = self.documents["references/verification-and-reporting.md"]
        for requirement in (
            "稳定 issue ID", "实际 diff与终态", "独立预期", "不虚构 Agent 历史行为",
            "未验证不标 FIXED+FRESH", "WorkC 本轮缺口", "不倒填 preimage",
            "不自动成为权威 ORIGINAL_TASK", "关键缺陷、修法或有效性主张自身无证",
            "质量 QC 也应 UNVERIFIED", "确证虚假/错误主张为 FAIL",
        ):
            self.assertIn(requirement, contract)
        template = self.documents["assets/qa_report.template.md"]
        quality_status = re.search(r"^.*\*\*本轮报告质量 QC\*\*.*?\{\{([^；\n]+)", template, re.MULTILINE)
        self.assertIsNotNone(quality_status)
        self.assertEqual(quality_status[1].split("/"), ["PASS", "FAIL", "UNVERIFIED", "NOT_RUN"])
        for requirement in ("本轮报告质量审核", "写前内容/真实diff及终态", "主动静态发现", "WorkC本轮缺口"):
            self.assertIn(requirement, template)

    def test_report_review_modes_preserve_scope_and_do_not_loop_on_receipts(self) -> None:
        contract = self.documents["references/verification-and-reporting.md"]
        for requirement in (
            "FULL_ACCEPTANCE 与 UNATTENDED", "局部标准作业默认自查", "不因此新增全题独立门",
            "未指定窄范围时识别并分别核", "RUN_ONLY 仅获授权报告写入时自查",
            "先完成作业员自查修验、实质报告与报告自查，再派独立非写入 QC", "不无限自指复审", "不空跑 verifier",
            "质量 QC PASS 只证明", "质量 PASS 不抹历史未证/失败",
        ):
            self.assertIn(requirement, contract)
        mode = self.documents["references/unattended-mode.md"]
        self.assertIn("本轮有报告写入时其质量QC独立核实通过", mode)
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-R01", "EVAL-R02", "EVAL-R03"):
            self.assertIn(identity, evaluations)

    def test_retrospective_registration_is_routed_before_delivery_review(self) -> None:
        for name in (
            "SKILL.md", "README.md", "assets/qa_report.template.md",
            "references/verification-and-reporting.md", "references/unattended-mode.md",
            "references/evidence-preparation.md", "references/pre-delivery-qa-fusion.md",
        ):
            with self.subTest(document=name):
                self.assertIn("回顾登记", self.documents[name])
        contract = self.documents["references/verification-and-reporting.md"]
        for requirement in (
            "交付前、首次派独立 QC 前", "返修后只核新增/受影响项", "漏登记不等于没有证据",
            "记忆、摘要或旧交接总结只作查找线索", "事后补登记", "事后找回证据",
            "不伪称当时已登记/写前保全", "不重复计 F/A", "登记齐全不等于归因、修法或外部 QC 已通过",
        ):
            self.assertIn(requirement, contract)
        mode = self.documents["references/unattended-mode.md"]
        step = mode.index("4. **独立质检**")
        self.assertLess(mode.index("派发前先完成回顾登记", step), mode.index("派独立不写题包 reviewer", step))

    def test_retrospective_registration_preserves_evidence_and_scope(self) -> None:
        contract = self.documents["references/verification-and-reporting.md"]
        for requirement in (
            "只有记忆、缺原内容或运行记录", "不永久卡未证", "不能用补表代替修复",
            "新 run 只证明对应当前行为", "不无界搜索会话/工作区", "不读秘密、隐藏答案或 .pipeline",
            "纯咨询不启动回顾取证", "不扩全题历史清算", "不写 QA、不运行",
            "RUN_ONLY 仅在报告写入获准时登记指定运行范围",
        ):
            self.assertIn(requirement, contract)
        evaluations = self.documents["references/skill-evals.md"]
        for identity in ("EVAL-H01", "EVAL-H02"):
            self.assertIn(identity, evaluations)

    def test_qc_can_verify_without_task_write_authority(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        for requirement in (
            "质检可执行核验，但题包不写", "非破坏地查询现有环境/版本",
            "parser/回归", "正式 verifier-only", "task 全路径不写",
            "cache、日志、字节码、临时文件、评分结果及子进程副作用",
            "路径别名、链接、挂载和重定向按实际目标判定",
            "只读最小允许输入挂载或等效强制只读沙箱", "task 外独立隔离工作区",
            "不生成/应用修复补丁", "根 QA 仍由协调者写",
            "command/mode/版本", "预期/实际", "freshness",
        ):
            self.assertIn(requirement, contract)
        for name in ("SKILL.md", "references/unattended-mode.md"):
            self.assertIn("#11-质检可执行核验但题包不写", self.documents[name])
        self.assertIn("实际核验与隔离", self.documents["references/unattended-mode.md"])

    def test_qc_execution_preserves_operation_limits_and_answer_isolation(self) -> None:
        contract = self.documents["references/qc-exceptions-and-admission.md"]
        for requirement in (
            "角色能力不替代作业授权", "默认静态 REPORT_QC", "CONSULT 不启动题包取证",
            "RUN_ONLY 只限指定模式", "局部不升级全题", "无安全入口则不执行",
            "-B", "不能单独证明副作用已被阻止", "不自行安装依赖",
            "修改系统/配置", "重启服务", "不放源代码副本",
            "移交不扩大协调者权限", "普通新候选", "外部 judge", "工具拒绝不绕过",
            "先独立义务和评分设计双冻结", "脱敏状态及可核引用",
            "不收隐藏原文、数值或可反推摘要", "不等于参与修复",
        ):
            self.assertIn(requirement, contract)
        for identity in ("EVAL-P01", "EVAL-P02", "EVAL-P03"):
            self.assertIn(identity, self.documents["references/skill-evals.md"])

    def test_live_qc_interfaces_do_not_reinstate_blanket_execution_ban(self) -> None:
        retired = (
            "reviewer 永不运行", "reviewer永不运行", "reviewer 不执行",
            "reviewer不执行", "reviewer 永不执行题包", "子 Agent 永远只读",
            "子代理仅做只读审核", "子代理只读且永不执行题包",
            "独立 reviewer 永远只读不执行", "不能自己运行题包",
            "子Agent只读不执行", "子代理题包只读不执行",
            "子 Agent 不导入或执行题包代码", "子 Agent 只读不运行题包代码",
        )
        for name, text in self.documents.items():
            for wording in retired:
                with self.subTest(document=name, wording=wording):
                    self.assertNotIn(wording, current_document_text(name, text))

    def test_worker_role_and_operational_sop_are_primary(self) -> None:
        skill = self.documents["SKILL.md"]
        self.assertLess(skill.index("## 0. 先认角色"), skill.index("## 1."))
        for requirement in (
            "主代理是作业员（协调者），不是独立质检员",
            "不是只给问题清单或审核意见", "不等质检替你发现全部问题",
            "不能代替独立质检或自己签 QC PASS", "references/execution-sop.md",
        ):
            self.assertIn(requirement, skill)
        for name in (
            "README.md", "assets/qa_report.template.md", "references/routing-and-authority.md",
            "references/unattended-mode.md", "references/qc-exceptions-and-admission.md",
            "references/verification-and-reporting.md", "references/pre-delivery-qa-fusion.md",
            "references/current-sop.md",
        ):
            with self.subTest(document=name):
                self.assertIn("execution-sop.md", self.documents[name])
        route = self.documents["references/routing-and-authority.md"]
        role = re.search(r"^\| qc_role \|([^\n]+)", route, re.MULTILINE)
        self.assertIsNotNone(role)
        self.assertNotIn("/ 协调者 /", role[1])

    def test_sop_has_ordered_actions_outputs_and_return_paths(self) -> None:
        sop = self.documents["references/execution-sop.md"]
        steps = (
            "## 1. 接单", "## 2. 定依据", "## 3. 主动发现", "## 4. 验证本轮",
            "## 5. 外侧检查", "## 6. 送交真正", "## 7. 核实反馈", "## 8. 通过或真实受阻",
        )
        positions = [sop.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for requirement in (
            "**产物**", "**转移**", "确认且在授权范围内的 tests 缺陷要实际修复",
            "不只登记、建议修改或等待 QC", "实际授权文件/diff/终态",
            "不改依据", "送检前", "当前版本", "qc-qa-report/SKILL.md",
            "未参与修复", "不写 task", "第3–5步", "第5步及第6步",
            "合法路径尚存就回第7步", "不以输出一份 FAIL 清单结束",
        ):
            self.assertIn(requirement, sop)

    def test_worker_loop_preserves_scope_and_real_independent_pass(self) -> None:
        sop = self.documents["references/execution-sop.md"]
        for requirement in (
            "标准模式不是免返修", "而非唯一允许闭环的模式", "不加全题独立门",
            "默认 FULL_ACCEPTANCE", "REPORT_QC", "RUN_ONLY", "CONSULT", "READ_ONLY",
            "不扫整个工作区", "冻结对象不改", "移交不等于已修",
            "GT/oracle 双冻结", ".pipeline/秘密禁区", "不为让候选满分放宽有效规则",
            "不能写 task", "不用内部质量 PASS 代外部条款通过", "实际要求的独立质检对当前版本通过",
            "作业员不能自己签它", "用户停止或显式预算耗尽", "没有默认8轮",
            "不空跑 verifier", "未变有效证据可复用", "不无限自指复审",
        ):
            self.assertIn(requirement, sop)
        for identity in ("EVAL-W01", "EVAL-W02", "EVAL-W03"):
            self.assertIn(identity, self.documents["references/skill-evals.md"])

    def test_history_uncertainty_does_not_automatically_gate_current_full_delivery(self) -> None:
        skill = self.documents["SKILL.md"]
        for requirement in (
            "历史未证不自动阻断当前交付", "历史认证是否为本次必需门",
            "FULL_ACCEPTANCE、无人值守、QA模板", "当前全题",
            "当前 tests 侧完整交付 PASS 或 UNATTENDED_COMPLETE",
            "明确要求的历史门仍未闭合时", "不声称历史/外部验收通过",
        ):
            self.assertIn(requirement, skill)
        sop = self.documents["references/execution-sop.md"]
        for requirement in (
            "历史 UNVERIFIED 不自动阻断当前交付", "不降成局部交付",
            "含历史验收的原请求未完成", "不因模板或历史状态自动增加",
        ):
            self.assertIn(requirement, sop)

    def test_history_exhaustion_stops_only_dependent_work_and_can_reopen(self) -> None:
        sop = self.documents["references/execution-sop.md"]
        for requirement in (
            "当前规则正确性与本轮修法", "历史修改对照依权威原task_path",
            "旧候选行为归因依相应旧轨迹/产物", "固定缺失主张/对象/材料",
            "来源/实际动作/结果", "必需性/影响及恢复责任",
            "没有新来源、权限或版本变化", "不每轮重查已穷尽来源",
            "包含不依赖旧材料的当前全题", "不能只留“旧候选失败 A/B：UNVERIFIED”",
        ):
            self.assertIn(requirement, sop)
        for identity in ("EVAL-G01", "EVAL-G02", "EVAL-G03"):
            self.assertIn(identity, self.documents["references/skill-evals.md"])

    def test_history_split_cannot_exempt_current_production_or_false_claims(self) -> None:
        skill = self.documents["SKILL.md"]
        for requirement in (
            "旧报告中的错误/未证结论须核实", "保留来源、纠正理由与未证范围",
            "不能删行或改成“本次未请求”逃避实际错误修法",
            "本轮漏保全/漏登记仍是作业员生产缺口", "不享历史灭失免责",
            "已审但缺证保留 UNVERIFIED", "只有确认无历史对象才 N/A",
            "不把未证改成 PASS",
        ):
            self.assertIn(requirement, skill)

    def test_current_full_history_gate_split_across_live_interfaces(self) -> None:
        cases = (
            ("SKILL.md", "### 历史未证不自动阻断当前交付", "历史合法查源仍须做", (
                r"继续当前全题.*修复、验证、报告和独立质检.*不存在本次历史必需门且当前全部必需项真实通过时，可报当前tests侧完整交付PASS或UNATTENDED_COMPLETE",
                r"明确要求的历史门仍未闭合时，不能报包含该历史验收的原请求全通过",
            )),
            ("README.md", "## 无人值守模式", "不再默认8轮", (
                r"非必需历史保留UNVERIFIED，当前FULLtests、当前报告及真实独立QC的自身必需门闭合后可PASS/UNATTENDED_COMPLETE，不静默降为LOCAL",
                r"明确历史门未闭合时不得称原请求全要求完成",
            )),
            ("assets/qa_report.template.md", "## 当前结论与本次范围", "- **历史门依据与当前交付结果（分别列）**", (
                r"明确历史验收请求/正式采用的适用条款/当前主张真实依赖旧失败或旧修改时才需相应旧证据",
                r"非必需历史UNVERIFIED不阻当前FULLtests\+当前报告\+真实独立QC自身必需门闭合后的PASS/UNATTENDED_COMPLETE，不降为LOCAL",
                r"明确历史门未闭合则不得称原请求全要求完成，不预填实际未取得的验证/QCPASS",
            )),
            ("assets/qa_report.template.md", "### 本次验收要求与证据矩阵", "| 要求 ID |", (
                r"正式来源/版本与采用依据（authority）.*必需性（required）/验证/通过条件.*实际依赖（dependency）/缺口影响与责任",
                r"历史门列请求或已采用且适用的条款/版本.*required=true/false及依据.*具体依赖主张、缺口限制的对象与责任，不传播无关阻塞",
            )),
            ("references/routing-and-authority.md", "## 2. 本次验收清单", "历史门以", (
                r"当前FULL_ACCEPTANCE/裸“无人值守”不自动采用全历史认证",
                r"无历史必需门且无无据沿用的旧主张时，当前全题技术、报告及独立QC全部实际通过即可当前交付/UNATTENDED_COMPLETE",
                r"有明确历史门仍限制原请求全范围认证",
            )),
            ("references/runtime-acceptance.md", "## 6. 收口与移交", "- 完整技术范围全部适用门有效", (
                r"无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题PASS/UNATTENDED_COMPLETE",
                r"确有必需历史门缺证仍阻包含该门的原请求全通过",
            )),
            ("references/verification-and-reporting.md", "#### 7.2.1 历史未证只限制实际依赖的结论", "- **无历史必需门**", (
                r"对象APPLICABLE/UNDETERMINED、历史缺证时保留相应UNVERIFIED.*不改成N/A/PASS",
                r"当前全题全部适用技术门、真实必需运行、报告质量和当前版本独立QC都已实际通过，即可报当前FULL_ACCEPTANCEPASS；无人值守其他本次必需项亦已闭合可报UNATTENDED_COMPLETE",
                r"不将完整当前范围降为局部workaround",
            )),
            ("references/verification-and-reporting.md", "#### 7.2.1 历史未证只限制实际依赖的结论", "- **门的来源**", (
                r"只有用户明确要求历史验收、正式已采用批次条款确实适用于该具体对象，或当前实际交付的实质主张依赖旧候选行为/失败原因或历史修改时，才将相应历史证据列为必需",
                r"模板栏目.*单独均不要求证明所有旧失败原因",
                r"已知外部硬门及真实采用分歧仍须核实，不能弱化、删行",
            )),
            ("references/verification-and-reporting.md", "#### 7.2.1 历史未证只限制实际依赖的结论", "- **有历史必需门**", (
                r"确不可恢复且没有有权方对具体对象、版本、条款和范围的可核正式替代接受记录时，只将实际依赖项列NOT_ADMITTED，历史仍UNVERIFIED",
                r"保留并继续独立当前全题修验.*该门属于原请求时仍阻其全范围认证/完成声明",
                r"移交或披露缺口不是该门通过",
            )),
            ("references/unattended-mode.md", "## 4. 成功与停止条件", "`UNATTENDED_COMPLETE` 只在", (
                r"非必需历史UNVERIFIED可与当前FULLtests交付PASS及UNATTENDED_COMPLETE并列，前提是当前tests、报告质量和真实独立QC的自身必需门实际闭合",
                r"明确历史验收请求、正式采用且适用的历史条款或真实依赖主张形成的门仍须闭合，未闭合不称原请求全要求完成，不删真门",
            )),
            ("references/execution-sop.md", "## 8. 通过或真实受阻收口", "本次 PASS 要同时满足", (
                r"本次无必需历史认证且当前全题修验、报告质量与独立质检均通过，可报当前tests侧完整交付PASS或UNATTENDED_COMPLETE",
                r"不降成局部交付.*若明确必需历史门仍缺证，当前全题可单列通过，但含历史验收的原请求未完成",
            )),
            ("references/pre-delivery-qa-fusion.md", "## 7. 边界与最终收口", "- tests 外相关允许发现直接写同根 QA", (
                r"不改外侧、不等待外部先修、不把全部外侧缺陷变成交付门；只有实际依赖的必需项限制对应结论",
                r"对象存在/未知/灭失不自证当前必需性",
                r"无当前历史必需门时，当前FULLtests可凭.*真实必需运行、当前报告和真实独立QC闭合自身门后PASS/UNATTENDED_COMPLETE，历史仍UNVERIFIED，不静默降为LOCAL",
                r"明确历史门保留来源/版本/对象及影响，未闭合则不称原请求全要求完成",
            )),
            ("references/current-sop.md", "## 8. 现行默认许可与开工准入（替代说明，不改写历史验证）", "- **依赖材料准入**", (
                r"对象存在/未知/灭失.*本身不产生历史门",
                r"非必需历史保持UNVERIFIED，当前FULLtests\+当前报告\+真实独立QC自身必需门闭合可PASS/UNATTENDED_COMPLETE，不静默降为LOCAL",
                r"明确历史门未闭合不称原请求全要求完成",
            )),
            ("references/evidence-preparation.md", "## 1. 不以一句证据不足结束：先建立取证计划", "历史材料缺口、旧 QA 主张纠错", (
                r"全题继续验收统一按.*verification-and-reporting\.md#721-历史未证只限制实际依赖的结论",
                r"只停实际依赖项，继续独立CURRENTFULLscope，不降为局部workaround，不自签历史替代接受",
            )),
            ("references/evidence-preparation.md", "## 4. 修改检查点、无人值守和收口", "无显式预算不默认8轮", (
                r"继续独立当前全题验收.*完成声明按同节分当前通过与原请求含历史门的全范围认证，不冒全历史通过",
            )),
            ("references/qc-exceptions-and-admission.md", "## 3. 材料不足前移为开工准入", "历史必需性、穷尽后的依赖隔离", (
                r"独立当前全题范围继续修验，不退成仅parser/局部workaround",
                r"无历史必需门且当前全部必需证据通过可当前交付/UNATTENDED_COMPLETE；有明确历史门仍阻原请求全范围认证，不自签替代接受",
            )),
            ("references/qc-exceptions-and-admission.md", "### 3.1 报告生产与质量接口", "FULL_ACCEPTANCE/UNATTENDED 有本轮报告写入", (
                r"FULL_ACCEPTANCE/UNATTENDED有本轮报告写入须未参与修复的不写题包reviewer独立质量审核，作为该报告/模式交付必需项",
                r"历史层的对象/状态/必需性及完成声明按.*verification-and-reporting\.md#72-先发现对象不能用报告自证不适用.*不自动阻当前全题/模式完成，不删真门",
            )),
            ("references/skill-evals.md", "### EVAL-G01：无历史硬门，当前全题通过不降局部", None, (
                r"未采用逐旧候选历史归因验收，也没有当前交付依赖的历史修法/失败原因主张.*历史对象APPLICABLE",
                r"当前全题正式义务、修改前内容、实际修法/验证、本轮报告及真实独立当前版本回执均充分且通过",
                r"历史对象存在不自动变必需门，保留历史UNVERIFIED",
                r"当前全题可独立报tests侧完整交付PASS及UNATTENDED_COMPLETE，不仅交局部补丁、不冒历史/平台/外部签收通过",
            )),
            ("references/skill-evals.md", "### EVAL-G02：明确历史验收仍缺证，不能偷删门", None, (
                r"历史门明确必需，旧行为UNVERIFIED/依赖NOT_ADMITTED",
                r"不报含历史的原请求全通过或UNATTENDED_COMPLETE.*当前全题可以单列PASS但不是整份历史交付PASS",
            )),
            ("references/local-runtime.md", "## 能力证据及限制", "真实题包按本次作业清单", (
                r"明确历史验收请求、适用正式采用条款或当前主张依赖才产生对应历史门",
                r"不阻独立当前范围（包括全题）修验/报告/独立QC；全部当前必需门闭合且无必需历史门可报当前全题PASS/UNATTENDED_COMPLETE",
                r"确有未闭合历史门仍阻包含该门的原请求全通过，不删门",
            )),
        )
        for name, heading, prefix in (
            ("references/legacy-claw-eval.md", "## 6. 报告QC与移交", "历史变化与本轮写入分开"),
            ("references/seal-rewardkit.md", "## 9. 指标、报告与本次范围收口", "保留历史与原反馈映射"),
            ("references/judge-chain.md", "## 5. 通过条件及验证范围", "复用 judge 链"),
        ):
            cases += ((name, heading, prefix, (
                r"无本次必需历史门且当前全部必需技术、报告及独立QC门通过，可报当前全题PASS/UNATTENDED_COMPLETE",
                r"确有必需历史门缺证仍阻包含该门的原请求全通过",
            )),)
        for name, heading, prefix, requirements in cases:
            text = current_document_text(name, self.documents[name])
            level = len(heading.split(" ", 1)[0])
            with self.subTest(document=name, section=heading, paragraph=prefix):
                section = re.search(
                    rf"^{re.escape(heading)}\n(.*?)(?=^#{{1,{level}}}\s|\Z)",
                    text, re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(section, "missing live history-gate section")
                paragraphs = [section[1]] if prefix is None else [
                    paragraph.strip() for paragraph in re.split(r"\n\s*\n|\n(?=- )", section[1])
                    if paragraph.strip().startswith(prefix)
                ]
                self.assertEqual(len(paragraphs), 1, "expected one specific live paragraph")
                compact = re.sub(r"[\s`*]+", "", paragraphs[0])
                for requirement in requirements:
                    with self.subTest(requirement=requirement):
                        self.assertRegex(compact, requirement)

    def test_all_tests_scope_eval_specs_cover_inside_outside_and_isolation(self) -> None:
        evaluations = current_document_text("references/skill-evals.md", self.documents["references/skill-evals.md"])
        cases = {
            "EVAL-T01": (
                "tests/test.sh", "tests/legacytests/judge.py", "tests/runner.py",
                "tests/helper.py", "tests/shim.py", "tests/instruction.md",
                "默认全部tests/**及同根qa_report.md", "而非等待额外审批",
                "tests外同名路径一律只读", "正式版本", "双冻结", "STALE",
                "不放宽有效义务救候选", "不追认历史", "QC不写task",
            ),
            "EVAL-T02": (
                "environment/instruction.md", "路径别名", "拒绝tests外与题包外逃逸写入",
                "普通tests内instruction可按正式依据及本次范围修", "sidecar",
                "所有角色禁读/依赖.pipeline", "worker不读GT、不收隐藏答案",
                "已接答案QC不重设计、不写task", "双冻结", "STALE",
            ),
            "EVAL-T03": (
                "LOCAL_REPAIR", "UNATTENDED+READ_ONLY", "RUN_ONLY",
                "仅实际局部范围", "不写不import/collect/执行", "不自动写tests或QA",
                "默认全部tests不覆盖显式局部/只读/禁运行/窄路径",
                "D FULL_ACCEPTANCE按当前题全部tests检查修复并完整验收",
                "附带反馈只是起始线索，不因有反馈改成LOCAL_REPAIR",
                "只有明示局部限制才裁剪", "局部验收范围不自动冻结其他tests写路径",
                "QC任何模式均不写task全路径", "运行副作用", "秘密", "GT答案隔离",
            ),
        }
        for identity, requirements in cases.items():
            section = re.search(
                rf"^### {identity}[^\n]*\n(.*?)(?=^#{{1,3}} |\Z)",
                evaluations, re.MULTILINE | re.DOTALL,
            )
            with self.subTest(evaluation=identity):
                self.assertIsNotNone(section)
                for requirement in requirements:
                    with self.subTest(requirement=requirement):
                        self.assertIn(requirement, section[1])
        self.assertIn("以下三项是现行合成行为规格，不是题包执行或真实验收证据", evaluations)
        self.assertIn("不声称逐字场景已实跑", evaluations)

    def test_live_scope_does_not_reintroduce_internal_frozen_subset(self) -> None:
        retired = (
            "instruction 即使位于 tests 内也不可写",
            "受保护 runner、tests/test.sh、legacy tests/judge.py、基础设施 shim/helper 不因位于 tests 内自动可改",
            "本请求即许可当前题非受保护 tests 侧修复",
            "任何instruction（含instruction.md、extra.md或tests内载体）均只读",
            "任何 instruction 只读移交、不请求批准、不修改",
            "全部 instruction 只读移交不变",
        )
        for name, text in self.documents.items():
            live = current_document_text(name, text)
            for wording in retired:
                with self.subTest(document=name, retired=wording):
                    self.assertNotIn(wording, live)

    def _live_rule_paragraph(self, name: str, heading: str | None, prefix: str) -> str:
        """Bind a claim to one live section and paragraph, never a file keyword pool."""
        text = current_document_text(name, self.documents[name])
        if heading is None:
            section = re.split(r"^##\s+", text, maxsplit=1, flags=re.MULTILINE)[0]
        else:
            level = len(heading.split(" ", 1)[0])
            match = re.search(
                rf"^{re.escape(heading)}\n(.*?)(?=^#{{1,{level}}}\s|\Z)",
                text, re.MULTILINE | re.DOTALL,
            )
            self.assertIsNotNone(match, f"missing live section: {name}: {heading}")
            section = match[1]
        paragraphs = [
            paragraph.strip() for paragraph in re.split(r"\n\s*\n|\n(?=- |\| )", section)
            if paragraph.strip().startswith(prefix)
        ]
        self.assertEqual(len(paragraphs), 1, f"expected one live rule: {name}: {prefix}")
        return compact_rule_text(paragraphs[0])

    def test_confirmed_internal_defects_require_repair_validation_and_same_root_qa(self) -> None:
        cases = (
            ("SKILL.md", "## 2. 先选本次作业，固定验收范围", "**问题处置（不是仅有写权限）**", (
                "tests内本次范围已确认的问题必须由作业员实际修复、完成适用合法验证",
                "把依据、实际变更及结果记入同根QA",
                "主动发现和独立QC反馈适用同一义务",
                "不得以只登记、建议修改、移交或等待QC代替修复",
                "内部可修的验证入口故障也应先修后验",
                "tests内确认缺陷仍未修、适用必需验证未闭合时，该范围不能PASS",
            )),
            ("references/execution-sop.md", None, "**内外处置总则**", (
                "tests内本次范围已确认的问题必须实际修复、完成适用合法验证",
                "将修法与结果记同根QA，不以只登记/建议/移交结案",
                "实际目标决定归属，内部可修的runner/配置故障也回修复流程",
                "不直接推成外部环境阻塞",
                "内部确认缺陷未修或必需验证未闭合不能该范围PASS",
            )),
            ("references/verification-and-reporting.md", "## 2. 状态、归因与证据范围", "**内外问题处置合同**", (
                "主动发现与独立QC反馈同样适用",
                "tests内本次范围已确认的问题必须由作业员实际修复、完成适用合法验证",
                "把依据/实际变更/结果记同根QA，不能只登记、建议或移交",
            )),
            ("references/execution-sop.md", "## 4. 验证本轮修法，失败继续修", "**转移**", (
                "tests内可修的runner/helper/配置/验证入口故障回第3步实际修复，再回本步验证",
                "不能只登记成环境移交", "不冒充候选错", "尚有合法路径就继续",
            )),
            ("references/execution-sop.md", "## 7. 核实反馈，作业员返修，再送检", "| tests 内可修的 runner/配置/验证入口错误 |", (
                "按tests缺陷实际修复、适用验证和QA，不只记录环境移交",
                "第3–5步，随后第6步复检",
            )),
            ("references/verification-and-reporting.md", "## 2. 状态、归因与证据范围", "- **tests 内验证入口/配置问题**", (
                "核实际落点，属于本次范围且可合法修复就实际修复、验证、记QA",
                "不能因runner/helper/依赖描述等文件类型而移交或标OUT_OF_SCOPE",
                "也不以“环境问题”跳过",
            )),
        )
        for name, heading, prefix, requirements in cases:
            with self.subTest(document=name, section=heading, paragraph=prefix):
                paragraph = self._live_rule_paragraph(name, heading, prefix)
                for requirement in requirements:
                    self.assertIn(requirement, paragraph)

    def test_external_confirmed_defects_go_directly_to_qa_and_gate_only_dependencies(self) -> None:
        cases = (
            ("SKILL.md", "## 2. 先选本次作业，固定验收范围", "**问题处置（不是仅有写权限）**", (
                "tests外除同根QA均不修改，发现的相关允许材料问题直接记入同根QA",
                "位置/版本、证据、影响及责任/移交状态",
                "不要求先修外侧才能交付，记录也不等于外侧已修",
                "外侧问题不自动新增通过门，只有实际影响本次必需判据时才限制对应结论",
                "外侧已按要求记录且无未闭合必需依赖时，不因外侧缺陷仍在而卡住当前tests交付",
            )),
            ("references/execution-sop.md", "## 5. 外侧检查、报告和回顾登记", "tests 外相关允许材料的错误直接", (
                "错误直接在同根QA记精确对象、版本/依据、实际观察、对评分/验收的影响、责任与移交",
                "外侧冻结对象不改，移交不等于已修",
                "不影响本次必需门的外侧真实缺陷或建议都不阻tests交付，不等待外侧修复",
                "通过所需的外部矛盾仍限制对应结论，写明所依赖的具体门",
                "不把所有外侧问题升级为门",
            )),
            ("references/execution-sop.md", "## 7. 核实反馈，作业员返修，再送检", "| tests 外相关允许材料错误 |", (
                "直接记同根QA的位置/证据/影响/责任，不改外侧",
                "无必需依赖不等外侧修好，有依赖仅限制对应结论",
                "继续其他独立可执行项",
            )),
            ("references/verification-and-reporting.md", "## 2. 状态、归因与证据范围", "- **tests 外冻结对象问题**", (
                "精确位置/版本、证据、影响、责任和移交，直接记同根QA，不修改外侧",
                "确实影响必需门时可阻塞对应整体结论，移交不是修复",
                "未影响必需门的外侧真实缺陷同样记录，但不等外部修好、不阻当前tests交付",
            )),
        )
        for name, heading, prefix, requirements in cases:
            with self.subTest(document=name, section=heading, paragraph=prefix):
                paragraph = self._live_rule_paragraph(name, heading, prefix)
                for requirement in requirements:
                    self.assertIn(requirement, paragraph)

    def test_disposition_duties_preserve_explicit_ceilings_and_real_failure_attribution(self) -> None:
        cases = (
            ("SKILL.md", "## 2. 先选本次作业，固定验收范围", "**问题处置（不是仅有写权限）**", (
                "疑点先核实，候选违反有效测试则保留规则",
                "明确只读、局部、指定运行等上限仍优先",
                "真有证据保全、权限或安全/执行条件阻止时，写具体动作、结果和影响",
                "继续其他可修范围，不用笼统“环境问题”跳过内部修复",
            )),
            ("references/execution-sop.md", None, "**内外处置总则**", (
                "明确只读/局部/指定运行等上限仍优先",
                "真实权限、保全或安全/执行阻止须有具体证据",
            )),
            ("references/execution-sop.md", "## 7. 核实反馈，作业员返修，再送检", "| 真实权限、证据保全或安全/执行条件阻止 |", (
                "记录具体动作/结果、阻止依据及受影响必需门",
                "不能靠只记阻塞跳过内部可修问题",
                "确无合法路径按第8步受阻收口",
            )),
            ("references/verification-and-reporting.md", "## 2. 状态、归因与证据范围", "**内外问题处置合同**", (
                "明确只读/局部/指定运行上限不变，疑点先核实，候选真错不改有效规则",
                "具体保全、权限、安全/执行阻止按实际影响记录",
                "不以笼统阻塞代替可执行修复",
            )),
            ("references/verification-and-reporting.md", "## 2. 状态、归因与证据范围", "- **候选真实失败、测试有效**", (
                "保留规则，记录有依据的不改与验证，不为候选提分放宽测试",
            )),
        )
        for name, heading, prefix, requirements in cases:
            with self.subTest(document=name, section=heading, paragraph=prefix):
                paragraph = self._live_rule_paragraph(name, heading, prefix)
                for requirement in requirements:
                    self.assertIn(requirement, paragraph)

    def test_problem_disposition_eval_specs_bind_prompts_to_required_behavior(self) -> None:
        evaluations = current_document_text(
            "references/skill-evals.md", self.documents["references/skill-evals.md"]
        )
        cases = {
            "EVAL-D01": (
                ("tests/output/parser.py", "tests/runner.py", "漏传必需 --evidence",
                 "实际目标均在 tests 内", "仅把两个 issue 写 QA"),
                ("必须由作业员实际修复", "不只列问题、写 QA、建议、等待或移交",
                 "tests 内坏掉的验证入口不是自动外部阻塞", "再修 parser 与 runner",
                 "执行适用合法正反例", "正式 verifier-only", "同根 QA",
                 "真实 diff/终态", "run/版本/freshness", "未跑不填 FIXED+FRESH",
                 "若变体修法实际需要未授权网络或确无合法隔离入口"),
            ),
            "EVAL-D02": (
                ("environment/service.json", "确为错误而不只是文档建议",
                 "变体 A", "不依赖该服务", "变体 B", "本次明确必需的真实判据依赖该服务"),
                ("错误直接记同根 QA", "精确路径/版本", "责任方与移交状态",
                 "不改外侧配置", "不自动成为 tests 交付阻塞", "无实际必需依赖",
                 "按实际必需依赖限制该判据", "具体门/依赖/阻止证据/恢复责任",
                 "继续其他独立当前范围修复", "不把所有工作一律 BLOCKED",
                 "移交不等于已修或该门通过", "不删真门冒整题 PASS"),
            ),
            "EVAL-D03": (
                ("静态只读核 tests，不产生文件", "用户明确禁止改该入口",
                 "不授权改 tests 或写 QA", "候选确实没交必需文件"),
                ("UNATTENDED+READ_ONLY", "不写 tests/QA、不 import/collect/执行",
                 "LOCAL_REPAIR", "明示禁止的 runner 不改", "局部不升级全题",
                 "RUN_ONLY", "不自动改 tests 或写 QA", "保留有效规则",
                 "不为候选提分改测试", "有据不改", "candidate_failure",
                 "grader_defect", "QC 不写 task", "不因义务新增写入/运行/外发权"),
            ),
        }
        for identity, (prompt_requirements, expected_requirements) in cases.items():
            with self.subTest(evaluation=identity):
                section = re.search(
                    rf"^### {identity}[^\n]*\n(.*?)(?=^#{{1,3}} |\Z)",
                    evaluations, re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(section, "missing live disposition evaluation")
                prompt, separator, expectation = section[1].partition("\n预期：")
                self.assertTrue(separator, "prompt and expected behavior must remain separate")
                self.assertRegex(prompt, r"(?m)^> ")
                for requirement in prompt_requirements:
                    with self.subTest(prompt_requirement=requirement):
                        self.assertIn(requirement, prompt)
                for requirement in expected_requirements:
                    with self.subTest(expected_requirement=requirement):
                        self.assertIn(requirement, expectation)
        introduction = re.search(
            r"^## 问题处置义务顺序评估\n(.*?)(?=^### )",
            evaluations, re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(introduction)
        self.assertIn("为合成行为规格，不是实际修复、运行或题包独立质检回执", introduction[1])
        self.assertIn("三个未参与编辑的独立上下文按顺序完成同类边界变体评估", introduction[1])
        self.assertIn("不声称逐字场景均已实跑", introduction[1])

    def test_live_routing_does_not_reduce_full_delivery_to_feedback_only(self) -> None:
        name = "references/routing-and-authority.md"
        heading = "## 4. 请求路由与完成条件"
        local = self._live_rule_paragraph(name, heading, "- 用户明确仅修具体反馈/具体规则或指定局部范围")
        self.assertIn("LOCAL_REPAIR", local)
        self.assertIn("其余未审范围不宣称PASS", local)
        full = self._live_rule_paragraph(name, heading, "- 要求整题 tests 交付/完整验收")
        for requirement in (
            "FULL_ACCEPTANCE", "附带反馈只是起始线索，不因有反馈改成LOCAL_REPAIR",
            "未明示局部的“修复tests”按当前题tests全范围检查修复",
            "全部规则", "正式verifier", "独立质量审核",
        ):
            self.assertIn(requirement, full)
        self.assertNotIn("无反馈且", full)

    def test_fenced_blocks_balanced(self) -> None:
        for name, text in self.documents.items():
            fences = re.findall(r"^```", text, re.MULTILINE)
            with self.subTest(document=name):
                self.assertEqual(len(fences) % 2, 0)


if __name__ == "__main__":
    unittest.main()
