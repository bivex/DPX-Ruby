from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class SimpleDelegatorDecoratorRule(Rule):
    @property
    def name(self) -> str:
        return "SIMPLE_DELEGATOR_DECORATOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.superclass and ("SimpleDelegator" in cls.superclass or "Delegator" in cls.superclass or "DelegateClass" in cls.superclass):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_SIMPLE_DELEGATOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Decorator pattern delegating unhandled calls via '{cls.superclass}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SIMPLE_DELEGATOR_DECORATOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class GatewayAdapterWrapperRule(Rule):
    @property
    def name(self) -> str:
        return "GATEWAY_ADAPTER_WRAPPER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.name.endswith("Gateway") or cls.name.endswith("Adapter") or cls.name.endswith("Client"):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_GATEWAY_ADAPTER",
                        weight=0.92,
                        description=f"Class '{cls.name}' acts as Adapter adapting external API protocol to domain interfaces",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GATEWAY_ADAPTER_WRAPPER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class FacadeSubsystemEntrypointRule(Rule):
    @property
    def name(self) -> str:
        return "FACADE_SUBSYSTEM_ENTRYPOINT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.name.endswith("Facade"):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_FACADE",
                        weight=0.92,
                        description=f"Class '{cls.name}' provides unified Facade entrypoint coordinating subsystem components",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FACADE_SUBSYSTEM_ENTRYPOINT,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class ProxyMethodMissingDelegateRule(Rule):
    @property
    def name(self) -> str:
        return "PROXY_METHOD_MISSING_DELEGATE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_mm = any(m.name == "method_missing" for m in cls.methods)
                if has_mm and "def method_missing" in cls.raw_body:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_PROXY_METHOD_MISSING",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements dynamic Proxy intercepting messages via method_missing",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PROXY_METHOD_MISSING_DELEGATE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
