import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class ServiceObjectInteractorRule(Rule):
    @property
    def name(self) -> str:
        return "SERVICE_OBJECT_INTERACTOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_service:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_SERVICE_OBJECT",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements Service / Interactor Object encapsulating single business operation",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SERVICE_OBJECT_INTERACTOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class PolicyObjectAuthorizationRule(Rule):
    @property
    def name(self) -> str:
        return "POLICY_OBJECT_AUTHORIZATION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_policy:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_POLICY_OBJECT",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements Policy Object for fine-grained authorization (Pundit / ActionPolicy)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.POLICY_OBJECT_AUTHORIZATION,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class FormObjectValidationRule(Rule):
    @property
    def name(self) -> str:
        return "FORM_OBJECT_VALIDATION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_form or "ActiveModel::Attributes" in cls.mixins:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_FORM_OBJECT",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Form Object separating input validation from database models",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FORM_OBJECT_VALIDATION,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DryMonadTransactionRule(Rule):
    @property
    def name(self) -> str:
        return "DRY_MONAD_TRANSACTION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        dry_pattern = re.compile(r'include\s+Dry::Monads\[|include\s+Dry::Transaction|Dry::Matcher\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if dry_pattern.search(line):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_DRY_MONAD",
                        weight=0.95,
                        description=f"Railway-oriented programming with Dry::Monads in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DRY_MONAD_TRANSACTION,
                            target_name="DryMonads",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class QueryObjectScopeRule(Rule):
    @property
    def name(self) -> str:
        return "QUERY_OBJECT_SCOPE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_query:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_QUERY_OBJECT",
                        weight=0.92,
                        description=f"Class '{cls.name}' encapsulates complex relational ActiveRecord queries",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.QUERY_OBJECT_SCOPE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DecoratorPresenterRule(Rule):
    @property
    def name(self) -> str:
        return "DECORATOR_PRESENTER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.name.endswith("Presenter") or cls.name.endswith("Decorator") or (cls.superclass and "Draper::Decorator" in cls.superclass):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="ENTERPRISE_PRESENTER_DECORATOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' isolates presentation logic from model objects",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DECORATOR_PRESENTER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections
