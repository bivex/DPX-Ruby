import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class ChainOfResponsibilityRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_CHAIN_OF_RESPONSIBILITY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_app_init = any(m.name == "initialize" and "@app" in m.raw_body for m in cls.methods)
                has_call = any(m.name == "call" and ("@app.call" in m.raw_body or "status, headers, response" in m.raw_body or "@successor" in m.raw_body) for m in cls.methods)
                if has_app_init or has_call or "Middleware" in cls.name or "Chain" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_CHAIN_OF_RESPONSIBILITY",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements GoF Chain of Responsibility passing requests along a handler pipeline",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_CHAIN_OF_RESPONSIBILITY,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class CommandRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_COMMAND"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_job or (cls.superclass and "ApplicationJob" in cls.superclass) or any(m.name in ["perform", "execute"] for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_COMMAND",
                        weight=0.95,
                        description=f"Class '{cls.name}' encapsulates GoF Command pattern with executable invocation",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_COMMAND,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class InterpreterRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_INTERPRETER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_eval = any(m.name in ["evaluate", "interpret", "eval_expr"] for m in cls.methods)
                if has_eval or "Interpreter" in cls.name or "Expression" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_INTERPRETER",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Interpreter evaluating domain grammar/AST nodes",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_INTERPRETER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class IteratorRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_ITERATOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "Enumerable" in cls.mixins and any(m.name == "each" for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_ITERATOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements GoF Iterator via standard 'include Enumerable' and 'def each'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_ITERATOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class MediatorRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_MEDIATOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "Mediator" in cls.name or "Coordinator" in cls.name or any(m.name in ["notify", "coordinate"] and "sender" in m.params for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_MEDIATOR",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Mediator pattern coordinating colleague interactions",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_MEDIATOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class MementoRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_MEMENTO"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_memento = any(m.name in ["save_state", "restore_state", "create_memento", "restore"] for m in cls.methods)
                if has_memento or "Memento" in cls.name or "Snapshot" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_MEMENTO",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Memento capturing and restoring internal state snapshots",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_MEMENTO,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class ObserverRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_OBSERVER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        notif_pattern = re.compile(r'ActiveSupport::Notifications\.(?:subscribe|instrument)\b|\binclude\s+Observable\b|\badd_observer\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if notif_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_OBSERVER",
                        weight=0.95,
                        description=f"GoF Observer / PubSub event subscription or notification in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_OBSERVER,
                            target_name="ObserverPubSub",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class StateRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_STATE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        aasm_pattern = re.compile(r'include\s+AASM\b|\baasm\s+do\b|\bstate_machine\b')
        for file in model.files:
            for cls in file.classes:
                if aasm_pattern.search(cls.raw_body) or "State" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_STATE",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements GoF State pattern altering behavior based on lifecycle states",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_STATE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class StrategyRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_STRATEGY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        provisioner_pattern = re.compile(r'\b(?:vm\.provision|config\.vm\.provision)\s+["\']([a-zA-Z0-9_]+)["\']')
        for file in model.files:
            # 1. DSL Strategy pattern (Provisioner strategies)
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                m = provisioner_pattern.search(line)
                if m and not line.strip().startswith("#"):
                    strat_name = m.group(1)
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_DSL_STRATEGY",
                        weight=0.92,
                        description=f"Pluggable provisioner Strategy pattern '{strat_name}' in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_STRATEGY,
                            target_name=f"ProvisionerStrategy:{strat_name}",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
            # 2. Method block strategy injection
            for cls in file.classes:
                for m in cls.methods:
                    if "&block" in m.params or "&strategy" in m.params or "&handler" in m.params or "Strategy" in cls.name:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_STRATEGY",
                            weight=0.92,
                            description=f"Method '{cls.name}#{m.name}' injects interchangeable GoF Strategy algorithm via block/proc ({m.params})",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.GOF_STRATEGY,
                                target_name=f"{cls.name}#{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
        return detections


class TemplateMethodRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_TEMPLATE_METHOD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if "raise NotImplementedError" in m.raw_body or "raise 'Override in subclass'" in m.raw_body:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_TEMPLATE_METHOD",
                            weight=0.90,
                            description=f"Method '{cls.name}#{m.name}' defines GoF Template Method abstract hook for subclass overrides",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.GOF_TEMPLATE_METHOD,
                                target_name=f"{cls.name}#{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections


class VisitorRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_VISITOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_accept = any(m.name == "accept" and "visitor" in m.params for m in cls.methods)
                has_visit = any(m.name.startswith("visit_") or m.name == "visit" for m in cls.methods)
                if has_accept or has_visit or "Visitor" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_VISITOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements GoF Visitor pattern double dispatch on object structures",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_VISITOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections
