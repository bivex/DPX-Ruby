import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class FactoryObjectFactoryBotRule(Rule):
    @property
    def name(self) -> str:
        return "FACTORY_OBJECT_FACTORY_BOT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        fb_pattern = re.compile(r'FactoryBot\.define\b|\bfactory\s+:[a-zA-Z0-9_]+\s+do\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if fb_pattern.search(line):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_FACTORY_BOT",
                        weight=0.92,
                        description=f"FactoryBot definition stamping out domain fixture objects in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FACTORY_OBJECT_FACTORY_BOT,
                            target_name="FactoryBot",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class FluentBuilderDslRule(Rule):
    @property
    def name(self) -> str:
        return "FLUENT_BUILDER_DSL"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "Builder" in cls.name or any(m.name.startswith("with_") for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_FLUENT_BUILDER",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements Fluent Builder DSL with method chaining",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FLUENT_BUILDER_DSL,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class SingletonModuleIncludeRule(Rule):
    @property
    def name(self) -> str:
        return "SINGLETON_MODULE_INCLUDE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "Singleton" in cls.mixins:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_SINGLETON",
                        weight=0.92,
                        description=f"Class '{cls.name}' enforces Singleton instance constraint via standard 'include Singleton'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SINGLETON_MODULE_INCLUDE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class PrototypeDupCloneRule(Rule):
    @property
    def name(self) -> str:
        return "PROTOTYPE_DUP_CLONE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        proto_pattern = re.compile(r'\.(?:dup|clone|deep_dup)\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if proto_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_PROTOTYPE_DUP",
                        weight=0.90,
                        description=f"Prototype pattern duplicating object instance in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PROTOTYPE_DUP_CLONE,
                            target_name="dup/clone",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
