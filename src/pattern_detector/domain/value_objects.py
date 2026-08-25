from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PatternCategory(str, Enum):
    RUBY_IDIOMATIC = "ruby_idiomatic"
    ENTERPRISE_RAILS = "enterprise_rails"
    METAPROGRAMMING = "metaprogramming"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
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

    # GoF Creational
    FACTORY_OBJECT_FACTORY_BOT = "factory_object_factory_bot"
    FLUENT_BUILDER_DSL = "fluent_builder_dsl"
    SINGLETON_MODULE_INCLUDE = "singleton_module_include"
    PROTOTYPE_DUP_CLONE = "prototype_dup_clone"

    # GoF Structural
    SIMPLE_DELEGATOR_DECORATOR = "simple_delegator_decorator"
    GATEWAY_ADAPTER_WRAPPER = "gateway_adapter_wrapper"
    FACADE_SUBSYSTEM_ENTRYPOINT = "facade_subsystem_entrypoint"
    PROXY_METHOD_MISSING_DELEGATE = "proxy_method_missing_delegate"

    # GoF Behavioral
    STRATEGY_PROC_BLOCK_INJECTION = "strategy_proc_block_injection"
    COMMAND_ACTIVE_JOB = "command_active_job"
    OBSERVER_ACTIVESUPPORT_NOTIFICATIONS = "observer_activesupport_notifications"
    STATE_MACHINE_AASM = "state_machine_aasm"
    TEMPLATE_METHOD_ABSTRACT_HOOK = "template_method_abstract_hook"
    CHAIN_OF_RESPONSIBILITY_MIDDLEWARE = "chain_of_responsibility_middleware"

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
