import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class AdapterRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_ADAPTER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.name.endswith("Gateway") or cls.name.endswith("Adapter") or cls.name.endswith("Client"):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_ADAPTER",
                        weight=0.92,
                        description=f"Class '{cls.name}' acts as GoF Adapter adapting external protocol to internal domain expectations",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_ADAPTER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class BridgeRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_BRIDGE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                # Bridge: class taking renderer/driver/implementation object in initialize and delegating
                has_impl_param = any(
                    m.name == "initialize" and any(k in m.params for k in ["renderer", "driver", "backend", "implementor", "engine"])
                    for m in cls.methods
                )
                if has_impl_param or "Bridge" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_BRIDGE",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Bridge pattern decoupling abstraction from implementation backend",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_BRIDGE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class CompositeRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_COMPOSITE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_children = any(
                    m.name in ["add", "remove", "add_child", "children", "nodes"]
                    for m in cls.methods
                ) and ("@children" in cls.raw_body or "@nodes" in cls.raw_body or "Composite" in cls.name)
                if has_children:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_COMPOSITE",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements GoF Composite pattern managing recursive part-whole hierarchies",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_COMPOSITE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DecoratorRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_DECORATOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.superclass and ("SimpleDelegator" in cls.superclass or "Delegator" in cls.superclass or "DelegateClass" in cls.superclass or "Draper::Decorator" in cls.superclass):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_DECORATOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements GoF Decorator pattern augmenting target objects dynamically",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_DECORATOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class FacadeRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_FACADE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.name.endswith("Facade"):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_FACADE",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements GoF Facade pattern coordinating subsystems via a single API",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_FACADE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class FlyweightRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_FLYWEIGHT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        flyweight_pattern = re.compile(r'@@[a-zA-Z0-9_]*cache\s*\|\|=\s*\{\}|@[a-zA-Z0-9_]*pool\s*(?:\[.+?\])?\s*\|\|=|Concurrent::Map\.new\b|\bFlyweight\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if flyweight_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_FLYWEIGHT",
                        weight=0.90,
                        description=f"GoF Flyweight pattern sharing fine-grained instances via object pool/cache in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_FLYWEIGHT,
                            target_name="FlyweightPool",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class ProxyRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_PROXY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_mm = any(m.name == "method_missing" for m in cls.methods)
                if has_mm or "Proxy" in cls.name:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_PROXY",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Proxy pattern intercepting access to underlying subject",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_PROXY,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
