import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class ActiveSupportConcernRule(Rule):
    @property
    def name(self) -> str:
        return "ACTIVESUPPORT_CONCERN"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for mod in file.modules:
                if mod.is_concern or "extend ActiveSupport::Concern" in mod.raw_body:
                    loc = SourceLocation(file_path=file.file_path, line_number=mod.line_number)
                    ev = EvidenceItem(
                        rule_name="RUBY_ACTIVESUPPORT_CONCERN",
                        weight=0.95,
                        description=f"Module '{mod.name}' implements ActiveSupport::Concern mixin with dependency resolution",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ACTIVESUPPORT_CONCERN,
                            target_name=mod.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class PatternMatchingCaseInRule(Rule):
    @property
    def name(self) -> str:
        return "PATTERN_MATCHING_CASE_IN"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        in_pattern = re.compile(r'^\s*in\s+(?:\{|\[|[A-Z][a-zA-Z0-9_]*|\^[a-z_])', re.MULTILINE)
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if in_pattern.match(line) and "case" in file.raw_content:
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="RUBY_PATTERN_MATCHING_CASE_IN",
                        weight=0.92,
                        description=f"Ruby 3.x pattern matching 'in' clause in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PATTERN_MATCHING_CASE_IN,
                            target_name="PatternMatching",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DataClassDefineRule(Rule):
    @property
    def name(self) -> str:
        return "DATA_CLASS_DEFINE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        data_pattern = re.compile(r'([A-Z][a-zA-Z0-9_:]*)\s*=\s*Data\.define\((.*?)\)')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                m = data_pattern.search(line)
                if m:
                    data_name = m.group(1)
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="RUBY_DATA_CLASS_DEFINE",
                        weight=0.95,
                        description=f"Ruby 3.2+ Data.define immutable value object: '{data_name}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DATA_CLASS_DEFINE,
                            target_name=data_name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class RefinementScopedExtensionRule(Rule):
    @property
    def name(self) -> str:
        return "REFINEMENT_SCOPED_EXTENSION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        refine_pattern = re.compile(r'\brefine\s+([A-Z][a-zA-Z0-9_:]*)\s+do\b|\busing\s+([A-Z][a-zA-Z0-9_:]*)\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                m = refine_pattern.search(line)
                if m and not line.strip().startswith("#"):
                    target = m.group(1) or m.group(2)
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="RUBY_REFINEMENT_SCOPED_EXTENSION",
                        weight=0.92,
                        description=f"Lexically scoped monkey-patch refinement on '{target}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.REFINEMENT_SCOPED_EXTENSION,
                            target_name=target,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class SorbetRbsTypeSignatureRule(Rule):
    @property
    def name(self) -> str:
        return "SORBET_RBS_TYPE_SIGNATURE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        sig_pattern = re.compile(r'^\s*sig\s*\{(?:(?:\.params|\.returns|\.void).+?)\}', re.MULTILINE)
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if sig_pattern.match(line) or "extend T::Sig" in line:
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="RUBY_SORBET_TYPE_SIGNATURE",
                        weight=0.90,
                        description=f"Static type annotation signature in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SORBET_RBS_TYPE_SIGNATURE,
                            target_name="SorbetSig",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class EndlessMethodDefinitionRule(Rule):
    @property
    def name(self) -> str:
        return "ENDLESS_METHOD_DEFINITION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        endless_pattern = re.compile(r'^\s*def\s+([a-zA-Z0-9_]+(?:\([^\)]*\))?)\s*=\s*(.+)$')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                m = endless_pattern.match(line)
                if m and not line.strip().startswith("#"):
                    fn_name = m.group(1)
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="RUBY_ENDLESS_METHOD",
                        weight=0.90,
                        description=f"Ruby 3.x endless method definition: 'def {fn_name} = ...'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ENDLESS_METHOD_DEFINITION,
                            target_name=fn_name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
