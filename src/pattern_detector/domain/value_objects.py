from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PatternCategory(str, Enum):
    RUBY_IDIOMATIC = "ruby_idiomatic"
    ENTERPRISE_RAILS = "enterprise_rails"
    METAPROGRAMMING = "metaprogramming"
    GOF_CREATIONAL = "gof_creational"
    GOF_STRUCTURAL = "gof_structural"
    GOF_BEHAVIORAL = "gof_behavioral"
    SECURITY_HAZARDS = "security_hazards"
    SOLID_PRINCIPLES = "solid_principles"


class PatternType(str, Enum):
    # Ruby Idiomatic & Ruby 3.x
    ACTIVESUPPORT_CONCERN = "activesupport_concern"
    PATTERN_MATCHING_CASE_IN = "pattern_matching_case_in"
    DATA_CLASS_DEFINE = "data_class_define"
    REFINEMENT_SCOPED_EXTENSION = "refinement_scoped_extension"
    SORBET_RBS_TYPE_SIGNATURE = "sorbet_rbs_type_signature"
    ENDLESS_METHOD_DEFINITION = "endless_method_definition"

    # Enterprise & Clean Rails
    SERVICE_OBJECT_INTERACTOR = "service_object_interactor"
    POLICY_OBJECT_AUTHORIZATION = "policy_object_authorization"
    FORM_OBJECT_VALIDATION = "form_object_validation"
    DRY_MONAD_TRANSACTION = "dry_monad_transaction"
    QUERY_OBJECT_SCOPE = "query_object_scope"
    DECORATOR_PRESENTER = "decorator_presenter"

    # Metaprogramming & Dynamic Dispatch
    DYNAMIC_METHOD_DEFINITION = "dynamic_method_definition"
    DYNAMIC_DISPATCH_SEND = "dynamic_dispatch_send"
    MODULE_PREPEND_INTERCEPTION = "module_prepend_interception"
    CONSTANT_LOOKUP_RESOLUTION = "constant_lookup_resolution"

    # --- ALL 23 GANG OF FOUR (GoF) PATTERNS ---

    # GoF Creational (5/5)
    GOF_FACTORY_METHOD = "gof_factory_method"
    GOF_ABSTRACT_FACTORY = "gof_abstract_factory"
    GOF_BUILDER = "gof_builder"
    GOF_PROTOTYPE = "gof_prototype"
    GOF_SINGLETON = "gof_singleton"

    # GoF Structural (7/7)
    GOF_ADAPTER = "gof_adapter"
    GOF_BRIDGE = "gof_bridge"
    GOF_COMPOSITE = "gof_composite"
    GOF_DECORATOR = "gof_decorator"
    GOF_FACADE = "gof_facade"
    GOF_FLYWEIGHT = "gof_flyweight"
    GOF_PROXY = "gof_proxy"

    # GoF Behavioral (11/11)
    GOF_CHAIN_OF_RESPONSIBILITY = "gof_chain_of_responsibility"
    GOF_COMMAND = "gof_command"
    GOF_INTERPRETER = "gof_interpreter"
    GOF_ITERATOR = "gof_iterator"
    GOF_MEDIATOR = "gof_mediator"
    GOF_MEMENTO = "gof_memento"
    GOF_OBSERVER = "gof_observer"
    GOF_STATE = "gof_state"
    GOF_STRATEGY = "gof_strategy"
    GOF_TEMPLATE_METHOD = "gof_template_method"
    GOF_VISITOR = "gof_visitor"

    # Security & Architectural Hazards
    SQL_INJECTION_HAZARD = "sql_injection_hazard"
    UNSAFE_EVAL_CODE_EXECUTION_HAZARD = "unsafe_eval_code_execution_hazard"
    MASS_ASSIGNMENT_PERMIT_ALL_HAZARD = "mass_assignment_permit_all_hazard"
    COMMAND_INJECTION_HAZARD = "command_injection_hazard"
    UNSAFE_DESERIALIZATION_HAZARD = "unsafe_deserialization_hazard"
    UNVALIDATED_REDIRECT_OPEN_HAZARD = "unvalidated_redirect_open_hazard"
    MISSING_RESPOND_TO_MISSING_HAZARD = "missing_respond_to_missing_hazard"
    DESTRUCTIVE_MONKEY_PATCHING_HAZARD = "destructive_monkey_patching_hazard"
    N_PLUS_ONE_QUERY_HAZARD = "n_plus_one_query_hazard"

    # SOLID Principles in Ruby
    GOD_MODEL_MONOLITHIC_SRP = "god_model_monolithic_srp"
    FAT_CONTROLLER_SRP = "fat_controller_srp"
    LEAKY_ACTIVE_RECORD_COUPLING = "leaky_active_record_coupling"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class SourceLocation:
    file_path: str
    line_number: int
    column_number: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}:{self.column_number}"


@dataclass(frozen=True)
class EvidenceItem:
    rule_name: str
    weight: float
    description: str
    location: Optional[SourceLocation] = None


@dataclass
class Confidence:
    value: float  # 0.0 to 1.0

    @property
    def level(self) -> ConfidenceLevel:
        if self.value >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.value >= 0.70:
            return ConfidenceLevel.HIGH
        if self.value >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def percentage(self) -> int:
        return int(round(self.value * 100))
