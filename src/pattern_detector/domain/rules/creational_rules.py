import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class FactoryMethodRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_FACTORY_METHOD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        fb_pattern = re.compile(r'FactoryBot\.define\b|\bfactory\s+:[a-zA-Z0-9_]+\s+do\b')
        for file in model.files:
            # 1. FactoryBot definition
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if fb_pattern.search(line):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_FACTORY_BOT",
                        weight=0.92,
                        description=f"Factory Method / FactoryBot definition for object creation: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_FACTORY_METHOD,
                            target_name="FactoryBot",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
            # 2. Factory class / method
            for cls in file.classes:
                if cls.name.endswith("Factory") or any(m.name.startswith("create_") or m.name.startswith("build_") for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_FACTORY_METHOD",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Factory Method pattern constructing concrete object instances",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_FACTORY_METHOD,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class AbstractFactoryRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_ABSTRACT_FACTORY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "AbstractFactory" in cls.name or (cls.name.endswith("Factory") and any("NotImplementedError" in m.raw_body for m in cls.methods)):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_ABSTRACT_FACTORY",
                        weight=0.92,
                        description=f"Class '{cls.name}' defines Abstract Factory interface producing families of related domain products",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_ABSTRACT_FACTORY,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class BuilderRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_BUILDER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        builder_dsl_pattern = re.compile(r'\b(?:Vagrant\.configure|config\.vm\.define)\b')
        for file in model.files:
            # 1. DSL Builder pattern (Vagrantfile / Infrastructure)
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if builder_dsl_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_DSL_BUILDER",
                        weight=0.92,
                        description=f"Configuration Builder DSL in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_BUILDER,
                            target_name="VagrantBuilder",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
            # 2. Class Builder pattern
            for cls in file.classes:
                if "Builder" in cls.name or any(m.name.startswith("with_") or m.name.startswith("set_") for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_FLUENT_BUILDER",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements GoF Builder pattern with fluent stepwise configuration",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_BUILDER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class PrototypeRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_PROTOTYPE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        proto_pattern = re.compile(r'\.(?:dup|clone|deep_dup)\b|\bdef\s+initialize_copy\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if proto_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_PROTOTYPE",
                        weight=0.90,
                        description=f"GoF Prototype pattern cloning prototype instance in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_PROTOTYPE,
                            target_name="dup/clone",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class SingletonRule(Rule):
    @property
    def name(self) -> str:
        return "GOF_SINGLETON"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if "Singleton" in cls.mixins or any(m.name == "instance" and m.is_class_method for m in cls.methods):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_SINGLETON",
                        weight=0.92,
                        description=f"Class '{cls.name}' enforces GoF Singleton pattern via 'include Singleton' or global instance accessor",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOF_SINGLETON,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections
