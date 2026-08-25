import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class StrategyProcBlockInjectionRule(Rule):
    @property
    def name(self) -> str:
        return "STRATEGY_PROC_BLOCK_INJECTION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if "&block" in m.params or "&strategy" in m.params or "&handler" in m.params:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_STRATEGY_BLOCK",
                            weight=0.92,
                            description=f"Method '{cls.name}#{m.name}' injects interchangeable Strategy algorithm via block/proc ({m.params})",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.STRATEGY_PROC_BLOCK_INJECTION,
                                target_name=f"{cls.name}#{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
        return detections


class CommandActiveJobRule(Rule):
    @property
    def name(self) -> str:
        return "COMMAND_ACTIVE_JOB"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_job or (cls.superclass and "ApplicationJob" in cls.superclass) or any(m.name == "perform" for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_COMMAND_ACTIVE_JOB",
                        weight=0.95,
                        description=f"Class '{cls.name}' encapsulates background Command pattern execution (ActiveJob / Sidekiq)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.COMMAND_ACTIVE_JOB,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class ObserverActiveSupportNotificationsRule(Rule):
    @property
    def name(self) -> str:
        return "OBSERVER_ACTIVESUPPORT_NOTIFICATIONS"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        notif_pattern = re.compile(r'ActiveSupport::Notifications\.(?:subscribe|instrument)\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if notif_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_OBSERVER_NOTIFICATIONS",
                        weight=0.95,
                        description=f"ActiveSupport::Notifications instrumentation / subscription in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.OBSERVER_ACTIVESUPPORT_NOTIFICATIONS,
                            target_name="ActiveSupport::Notifications",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class StateMachineAasmRule(Rule):
    @property
    def name(self) -> str:
        return "STATE_MACHINE_AASM"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        aasm_pattern = re.compile(r'include\s+AASM\b|\baasm\s+do\b|\bstate_machine\b')
        for file in model.files:
            for cls in file.classes:
                if aasm_pattern.search(cls.raw_body):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_STATE_MACHINE",
                        weight=0.95,
                        description=f"Class '{cls.name}' defines explicit State Machine transitions with guard conditions (AASM)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.STATE_MACHINE_AASM,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class TemplateMethodAbstractHookRule(Rule):
    @property
    def name(self) -> str:
        return "TEMPLATE_METHOD_ABSTRACT_HOOK"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if "raise NotImplementedError" in m.raw_body or "raise 'Override in subclass'" in m.raw_body:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_TEMPLATE_METHOD_HOOK",
                            weight=0.90,
                            description=f"Method '{cls.name}#{m.name}' defines abstract hook for subclass customization (Template Method)",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.TEMPLATE_METHOD_ABSTRACT_HOOK,
                                target_name=f"{cls.name}#{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections


class ChainOfResponsibilityMiddlewareRule(Rule):
    @property
    def name(self) -> str:
        return "CHAIN_OF_RESPONSIBILITY_MIDDLEWARE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_app_init = any(m.name == "initialize" and "@app" in m.raw_body for m in cls.methods)
                has_call = any(m.name == "call" and ("@app.call" in m.raw_body or "status, headers, response" in m.raw_body) for m in cls.methods)
                if has_app_init or has_call:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_CHAIN_MIDDLEWARE",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements Rack Middleware participating in Chain of Responsibility pipeline",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections
