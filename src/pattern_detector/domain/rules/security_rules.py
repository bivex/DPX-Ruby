import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class SqlInjectionHazardRule(Rule):
    @property
    def name(self) -> str:
        return "SQL_INJECTION_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        sqli_pattern = re.compile(
            r'\b(?:where|find_by_sql|order|select|having|joins|pluck)\s*\(\s*["\'].*?#\{params\[.+?\].*?["\']'
        )
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if sqli_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_SQL_INJECTION",
                        weight=0.95,
                        description=f"Raw user input interpolated inside ActiveRecord SQL fragment risking SQL Injection: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SQL_INJECTION_HAZARD,
                            target_name="SQLInjection",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class UnsafeEvalCodeExecutionHazardRule(Rule):
    @property
    def name(self) -> str:
        return "UNSAFE_EVAL_CODE_EXECUTION_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        eval_pattern = re.compile(r'\b(?:eval|class_eval|instance_eval|module_eval)\s*\(\s*(?:params\[|request\.|cookies\[|[a-z_]+\))')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if eval_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_UNSAFE_EVAL",
                        weight=0.95,
                        description=f"Direct evaluation of dynamic input via eval / instance_eval risking Remote Code Execution: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.UNSAFE_EVAL_CODE_EXECUTION_HAZARD,
                            target_name="eval",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class MassAssignmentPermitAllHazardRule(Rule):
    @property
    def name(self) -> str:
        return "MASS_ASSIGNMENT_PERMIT_ALL_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        permit_all_pattern = re.compile(r'\bparams(?:\.[a-zA-Z0-9_]+|\[:[a-zA-Z0-9_]+\])?\.permit!')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if permit_all_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_MASS_ASSIGNMENT_PERMIT_ALL",
                        weight=0.95,
                        description=f"Strong Parameters bypassed via 'params.permit!' exposing model attributes to mass-assignment attacks: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.MASS_ASSIGNMENT_PERMIT_ALL_HAZARD,
                            target_name="params.permit!",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class CommandInjectionHazardRule(Rule):
    @property
    def name(self) -> str:
        return "COMMAND_INJECTION_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        cmd_pattern = re.compile(r'`.*?#\{params\[.+?\].*?`|\b(?:system|exec|Open3\.popen3|IO\.popen)\s*\(\s*["\'].*?#\{params\[.+?\].*?["\']')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if cmd_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_COMMAND_INJECTION",
                        weight=0.95,
                        description=f"User parameters interpolated directly into OS shell command execution: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.COMMAND_INJECTION_HAZARD,
                            target_name="CommandInjection",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class UnsafeDeserializationHazardRule(Rule):
    @property
    def name(self) -> str:
        return "UNSAFE_DESERIALIZATION_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        deser_pattern = re.compile(r'\bMarshal\.load\s*\(|\bYAML\.load\s*\((?!.*safe_load)')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if deser_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_UNSAFE_DESERIALIZATION",
                        weight=0.95,
                        description=f"Unsafe deserialization via Marshal.load or legacy YAML.load risking Object Injection / RCE: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.UNSAFE_DESERIALIZATION_HAZARD,
                            target_name="Marshal.load",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class UnvalidatedRedirectOpenHazardRule(Rule):
    @property
    def name(self) -> str:
        return "UNVALIDATED_REDIRECT_OPEN_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        redir_pattern = re.compile(r'\bredirect_to\s+params\[:(?:url|redirect_to|next|target|return_to)\]')
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if redir_pattern.search(line) and not line.strip().startswith("#"):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_OPEN_REDIRECT",
                        weight=0.90,
                        description=f"Unvalidated open redirect to user-controlled parameter in line: '{line.strip()}'",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.UNVALIDATED_REDIRECT_OPEN_HAZARD,
                            target_name="OpenRedirect",
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class MissingRespondToMissingHazardRule(Rule):
    @property
    def name(self) -> str:
        return "MISSING_RESPOND_TO_MISSING_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_mm = any(m.name == "method_missing" for m in cls.methods)
                has_rtm = any(m.name == "respond_to_missing?" for m in cls.methods)
                if has_mm and not has_rtm:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="HAZARD_MISSING_RESPOND_TO_MISSING",
                        weight=0.92,
                        description=f"Class '{cls.name}' defines method_missing without respond_to_missing?, breaking respond_to? introspection",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.MISSING_RESPOND_TO_MISSING_HAZARD,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class DestructiveMonkeyPatchingHazardRule(Rule):
    @property
    def name(self) -> str:
        return "DESTRUCTIVE_MONKEY_PATCHING_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        core_classes = {"String", "Array", "Hash", "Integer", "Numeric", "Object", "Kernel", "Symbol"}
        for file in model.files:
            for cls in file.classes:
                if cls.name in core_classes and not cls.superclass and "refine" not in file.raw_content:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="HAZARD_GLOBAL_MONKEY_PATCH",
                        weight=0.90,
                        description=f"Global monkey-patching core Ruby class '{cls.name}' without Refinements causes namespace collisions",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DESTRUCTIVE_MONKEY_PATCHING_HAZARD,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class NPlusOneQueryHazardRule(Rule):
    @property
    def name(self) -> str:
        return "N_PLUS_ONE_QUERY_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if ".each do |" in m.raw_body and any(assoc in m.raw_body for assoc in [".posts", ".comments", ".user", ".orders", ".items", ".profile"]):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="HAZARD_N_PLUS_ONE_QUERY",
                            weight=0.88,
                            description=f"Potential N+1 database query in method '{cls.name}#{m.name}' iterating over records without eager loading (includes/preload)",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.N_PLUS_ONE_QUERY_HAZARD,
                                target_name=f"{cls.name}#{m.name}",
                                location=loc,
                                confidence=Confidence(0.88),
                                evidence=[ev],
                            )
                        )
        return detections
