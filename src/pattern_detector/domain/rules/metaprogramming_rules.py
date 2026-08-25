import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class DynamicMethodDefinitionRule(Rule):
    @property
    def name(self) -> str:
        return "DYNAMIC_METHOD_DEFINITION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        def_pattern = re.compile(r'\bdefine_method\s*\(\s*(?::[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)\s*\)|\bclass_eval\s*do\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if def_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="METAPROGRAMMING_DYNAMIC_METHOD",
                        weight=0.92,
                        description=f"Metaprogramming dynamic method definition in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DYNAMIC_METHOD_DEFINITION,
                            target_name="define_method",
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DynamicDispatchSendRule(Rule):
    @property
    def name(self) -> str:
        return "DYNAMIC_DISPATCH_SEND"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        send_pattern = re.compile(r'\b(?:send|public_send|__send__)\s*\(\s*(?:[a-zA-Z0-9_:@]+)')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if send_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="METAPROGRAMMING_DYNAMIC_DISPATCH",
                        weight=0.90,
                        description=f"Dynamic message dispatch at runtime via send/public_send in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DYNAMIC_DISPATCH_SEND,
                            target_name="DynamicDispatch",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class ModulePrependInterceptionRule(Rule):
    @property
    def name(self) -> str:
        return "MODULE_PREPEND_INTERCEPTION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        prepend_pattern = re.compile(r'^\s*prepend\s+([A-Z][a-zA-Z0-9_:]*)', re.MULTILINE)
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                m = prepend_pattern.match(line)
                if m and not line.strip().startswith("#"):
                    mod_name = m.group(1)
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="METAPROGRAMMING_MODULE_PREPEND",
                        weight=0.95,
                        description=f"Module#prepend places '{mod_name}' before class in ancestor lookup chain for method wrapping",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.MODULE_PREPEND_INTERCEPTION,
                            target_name=mod_name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class ConstantLookupResolutionRule(Rule):
    @property
    def name(self) -> str:
        return "CONSTANT_LOOKUP_RESOLUTION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        const_pattern = re.compile(r'\bconst_get\s*\(\s*[^)]+\)|\bconstantize\b')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if const_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="METAPROGRAMMING_CONSTANT_LOOKUP",
                        weight=0.90,
                        description=f"Dynamic constant reflection lookup in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CONSTANT_LOOKUP_RESOLUTION,
                            target_name="const_get",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
