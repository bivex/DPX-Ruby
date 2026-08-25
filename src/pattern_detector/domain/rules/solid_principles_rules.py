import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class GodModelMonolithicSrpRule(Rule):
    @property
    def name(self) -> str:
        return "GOD_MODEL_MONOLITHIC_SRP"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                is_ar = cls.superclass and "ApplicationRecord" in cls.superclass or "ActiveRecord::Base" in (cls.superclass or "")
                if is_ar and (cls.lines_count >= 150 or len(cls.associations) >= 8 or len(cls.methods) >= 15):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="SOLID_SRP_GOD_MODEL",
                        weight=0.85,
                        description=f"Model '{cls.name}' defines {len(cls.methods)} methods, {len(cls.associations)} associations, {cls.lines_count} lines (SRP Violation); extract Concerns, Service Objects, and Query Objects",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOD_MODEL_MONOLITHIC_SRP,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.85),
                            evidence=[ev],
                        )
                    )
        return detections


class FatControllerSrpRule(Rule):
    @property
    def name(self) -> str:
        return "FAT_CONTROLLER_SRP"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                is_controller = cls.superclass and "ApplicationController" in cls.superclass or "ActionController::Base" in (cls.superclass or "")
                if is_controller:
                    for m in cls.methods:
                        if m.lines_count >= 25:
                            loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                            ev = EvidenceItem(
                                rule_name="SOLID_SRP_FAT_CONTROLLER",
                                weight=0.85,
                                description=f"Controller action '{cls.name}#{m.name}' has {m.lines_count} lines (>25 lines), mixing HTTP handling with business logic; extract to Service / Interactor Object",
                                location=loc,
                            )
                            detections.append(
                                Detection(
                                    pattern_type=PatternType.FAT_CONTROLLER_SRP,
                                    target_name=f"{cls.name}#{m.name}",
                                    location=loc,
                                    confidence=Confidence(0.85),
                                    evidence=[ev],
                                )
                            )
        return detections


class LeakyActiveRecordCouplingRule(Rule):
    @property
    def name(self) -> str:
        return "LEAKY_ACTIVE_RECORD_COUPLING"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        raw_query_pattern = re.compile(r'\b(?:User|Order|Product|Account|Invoice)\.(?:where|find_by|create|update|destroy_all)\b')
        for file in model.files:
            if "views/" in file.file_path or "helpers/" in file.file_path:
                for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                    if raw_query_pattern.search(line) and not line.strip().startswith("#"):
                        loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                        ev = EvidenceItem(
                            rule_name="SOLID_LEAKY_DATABASE_COUPLING",
                            weight=0.88,
                            description=f"Direct ActiveRecord query executed in view/helper layer violating Separation of Concerns: '{line.strip()}'",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.LEAKY_ACTIVE_RECORD_COUPLING,
                                target_name="ViewDatabaseCoupling",
                                location=loc,
                                confidence=Confidence(0.88),
                                evidence=[ev],
                            )
                        )
        return detections
