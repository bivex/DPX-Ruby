from dataclasses import dataclass
from typing import Dict
from .value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternMetadata:
    pattern_type: PatternType
    name: str
    category: PatternCategory
    description: str
    default_weight: float


PATTERN_CATALOG: Dict[PatternType, PatternMetadata] = {
    # Ruby Idiomatic & Ruby 3.x
    PatternType.ACTIVESUPPORT_CONCERN: PatternMetadata(
        pattern_type=PatternType.ACTIVESUPPORT_CONCERN,
        name="ActiveSupport Concern",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Modular Rails mixin pattern with automated dependency resolution and class_methods blocks.",
        default_weight=0.95,
    ),
    PatternType.PATTERN_MATCHING_CASE_IN: PatternMetadata(
        pattern_type=PatternType.PATTERN_MATCHING_CASE_IN,
        name="Pattern Matching (case in)",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Modern Ruby 3.x structural deconstruction and pattern matching syntax.",
        default_weight=0.92,
    ),
    PatternType.DATA_CLASS_DEFINE: PatternMetadata(
        pattern_type=PatternType.DATA_CLASS_DEFINE,
        name="Data Class Define",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Immutable value object declaration using Ruby 3.2+ Data.define.",
        default_weight=0.95,
    ),
    PatternType.REFINEMENT_SCOPED_EXTENSION: PatternMetadata(
        pattern_type=PatternType.REFINEMENT_SCOPED_EXTENSION,
        name="Refinement Scoped Extension",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Lexically scoped monkey-patching avoiding global namespace collision.",
        default_weight=0.92,
    ),
    PatternType.SORBET_RBS_TYPE_SIGNATURE: PatternMetadata(
        pattern_type=PatternType.SORBET_RBS_TYPE_SIGNATURE,
        name="Sorbet / RBS Type Signature",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Static type annotation via Sorbet sig block or RBS type definitions.",
        default_weight=0.90,
    ),
    PatternType.ENDLESS_METHOD_DEFINITION: PatternMetadata(
        pattern_type=PatternType.ENDLESS_METHOD_DEFINITION,
        name="Endless Method Definition",
        category=PatternCategory.RUBY_IDIOMATIC,
        description="Modern Ruby 3.x concise one-liner method definition (def method(x) = expr).",
        default_weight=0.90,
    ),

    # Enterprise & Clean Rails
    PatternType.SERVICE_OBJECT_INTERACTOR: PatternMetadata(
        pattern_type=PatternType.SERVICE_OBJECT_INTERACTOR,
        name="Service Object / Interactor",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="Encapsulated business workflow following Single Responsibility Principle with standard call method.",
        default_weight=0.95,
    ),
    PatternType.POLICY_OBJECT_AUTHORIZATION: PatternMetadata(
        pattern_type=PatternType.POLICY_OBJECT_AUTHORIZATION,
        name="Policy Object Authorization",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="Granular access control policy object following Pundit or ActionPolicy conventions.",
        default_weight=0.95,
    ),
    PatternType.FORM_OBJECT_VALIDATION: PatternMetadata(
        pattern_type=PatternType.FORM_OBJECT_VALIDATION,
        name="Form Object Validation",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="Decoupled form handling and validation separating user input handling from database models.",
        default_weight=0.92,
    ),
    PatternType.DRY_MONAD_TRANSACTION: PatternMetadata(
        pattern_type=PatternType.DRY_MONAD_TRANSACTION,
        name="Dry-Monad Railway Transaction",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="Railway-oriented programming using Dry::Monads Result (Success/Failure) and Do notation.",
        default_weight=0.95,
    ),
    PatternType.QUERY_OBJECT_SCOPE: PatternMetadata(
        pattern_type=PatternType.QUERY_OBJECT_SCOPE,
        name="Query Object Scope",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="Dedicated query object isolating complex ActiveRecord relational composition logic.",
        default_weight=0.92,
    ),
    PatternType.DECORATOR_PRESENTER: PatternMetadata(
        pattern_type=PatternType.DECORATOR_PRESENTER,
        name="Decorator Presenter",
        category=PatternCategory.ENTERPRISE_RAILS,
        description="View logic isolation wrapping models in presenter decorators (Draper / SimpleDelegator).",
        default_weight=0.92,
    ),

    # Metaprogramming & Dynamic Dispatch
    PatternType.DYNAMIC_METHOD_DEFINITION: PatternMetadata(
        pattern_type=PatternType.DYNAMIC_METHOD_DEFINITION,
        name="Dynamic Method Definition",
        category=PatternCategory.METAPROGRAMMING,
        description="Runtime metaprogramming method generation via define_method or class_eval.",
        default_weight=0.92,
    ),
    PatternType.DYNAMIC_DISPATCH_SEND: PatternMetadata(
        pattern_type=PatternType.DYNAMIC_DISPATCH_SEND,
        name="Dynamic Dispatch (send/public_send)",
        category=PatternCategory.METAPROGRAMMING,
        description="Metaprogramming dynamic message dispatch at runtime via send or public_send.",
        default_weight=0.90,
    ),
    PatternType.MODULE_PREPEND_INTERCEPTION: PatternMetadata(
        pattern_type=PatternType.MODULE_PREPEND_INTERCEPTION,
        name="Module Prepend Interception",
        category=PatternCategory.METAPROGRAMMING,
        description="Method wrapper interception placing module ahead of target class in ancestor lookup chain.",
        default_weight=0.95,
    ),
    PatternType.CONSTANT_LOOKUP_RESOLUTION: PatternMetadata(
        pattern_type=PatternType.CONSTANT_LOOKUP_RESOLUTION,
        name="Constant Lookup Resolution",
        category=PatternCategory.METAPROGRAMMING,
        description="Dynamic constant reflection resolving class types at runtime via const_get.",
        default_weight=0.90,
    ),

    # GoF Creational
    PatternType.FACTORY_OBJECT_FACTORY_BOT: PatternMetadata(
        pattern_type=PatternType.FACTORY_OBJECT_FACTORY_BOT,
        name="Factory Object (FactoryBot)",
        category=PatternCategory.CREATIONAL,
        description="Factory pattern stamping out test fixtures or complex domain models.",
        default_weight=0.92,
    ),
    PatternType.FLUENT_BUILDER_DSL: PatternMetadata(
        pattern_type=PatternType.FLUENT_BUILDER_DSL,
        name="Fluent Builder DSL",
        category=PatternCategory.CREATIONAL,
        description="Builder pattern providing fluent method chaining for stepwise complex object configuration.",
        default_weight=0.90,
    ),
    PatternType.SINGLETON_MODULE_INCLUDE: PatternMetadata(
        pattern_type=PatternType.SINGLETON_MODULE_INCLUDE,
        name="Singleton Module Include",
        category=PatternCategory.CREATIONAL,
        description="Enforcing single global runtime instance via Ruby standard Singleton module.",
        default_weight=0.92,
    ),
    PatternType.PROTOTYPE_DUP_CLONE: PatternMetadata(
        pattern_type=PatternType.PROTOTYPE_DUP_CLONE,
        name="Prototype (dup/clone)",
        category=PatternCategory.CREATIONAL,
        description="Prototype pattern creating object duplicates via dup or clone.",
        default_weight=0.90,
    ),

    # GoF Structural
    PatternType.SIMPLE_DELEGATOR_DECORATOR: PatternMetadata(
        pattern_type=PatternType.SIMPLE_DELEGATOR_DECORATOR,
        name="SimpleDelegator Decorator",
        category=PatternCategory.STRUCTURAL,
        description="Decorator pattern forwarding unhandled messages to wrapped component via SimpleDelegator.",
        default_weight=0.92,
    ),
    PatternType.GATEWAY_ADAPTER_WRAPPER: PatternMetadata(
        pattern_type=PatternType.GATEWAY_ADAPTER_WRAPPER,
        name="Gateway Adapter Wrapper",
        category=PatternCategory.STRUCTURAL,
        description="Adapter pattern adapting external third-party API payloads to domain interfaces.",
        default_weight=0.92,
    ),
    PatternType.FACADE_SUBSYSTEM_ENTRYPOINT: PatternMetadata(
        pattern_type=PatternType.FACADE_SUBSYSTEM_ENTRYPOINT,
        name="Facade Subsystem Entrypoint",
        category=PatternCategory.STRUCTURAL,
        description="Facade pattern coordinating multiple internal subsystems behind a unified API.",
        default_weight=0.92,
    ),
    PatternType.PROXY_METHOD_MISSING_DELEGATE: PatternMetadata(
        pattern_type=PatternType.PROXY_METHOD_MISSING_DELEGATE,
        name="Proxy Method Missing Delegate",
        category=PatternCategory.STRUCTURAL,
        description="Proxy pattern lazily intercepting and forwarding messages to target objects.",
        default_weight=0.90,
    ),

    # GoF Behavioral
    PatternType.STRATEGY_PROC_BLOCK_INJECTION: PatternMetadata(
        pattern_type=PatternType.STRATEGY_PROC_BLOCK_INJECTION,
        name="Strategy Proc/Block Injection",
        category=PatternCategory.BEHAVIORAL,
        description="Strategy pattern injecting interchangeable algorithms via blocks, lambdas, or procs.",
        default_weight=0.92,
    ),
    PatternType.COMMAND_ACTIVE_JOB: PatternMetadata(
        pattern_type=PatternType.COMMAND_ACTIVE_JOB,
        name="Command ActiveJob",
        category=PatternCategory.BEHAVIORAL,
        description="Command pattern encapsulating asynchronous job execution and background workflows.",
        default_weight=0.95,
    ),
    PatternType.OBSERVER_ACTIVESUPPORT_NOTIFICATIONS: PatternMetadata(
        pattern_type=PatternType.OBSERVER_ACTIVESUPPORT_NOTIFICATIONS,
        name="Observer (ActiveSupport::Notifications)",
        category=PatternCategory.BEHAVIORAL,
        description="Observer / PubSub pattern decoupling event producers from subscribers via ActiveSupport instrumentation.",
        default_weight=0.95,
    ),
    PatternType.STATE_MACHINE_AASM: PatternMetadata(
        pattern_type=PatternType.STATE_MACHINE_AASM,
        name="State Machine (AASM)",
        category=PatternCategory.BEHAVIORAL,
        description="State machine pattern enforcing verified state transitions and guards.",
        default_weight=0.95,
    ),
    PatternType.TEMPLATE_METHOD_ABSTRACT_HOOK: PatternMetadata(
        pattern_type=PatternType.TEMPLATE_METHOD_ABSTRACT_HOOK,
        name="Template Method Abstract Hook",
        category=PatternCategory.BEHAVIORAL,
        description="Template Method defining overall algorithm skeleton with subclass hook customizations.",
        default_weight=0.90,
    ),
    PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE: PatternMetadata(
        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
        name="Chain of Responsibility Middleware",
        category=PatternCategory.BEHAVIORAL,
        description="Rack middleware pipeline processing HTTP requests sequentially in a chain.",
        default_weight=0.95,
    ),

    # Security & Architectural Hazards
    PatternType.SQL_INJECTION_HAZARD: PatternMetadata(
        pattern_type=PatternType.SQL_INJECTION_HAZARD,
        name="SQL Injection Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Unsanitized raw string interpolation inside SQL queries (where, find_by_sql, order).",
        default_weight=0.95,
    ),
    PatternType.UNSAFE_EVAL_CODE_EXECUTION_HAZARD: PatternMetadata(
        pattern_type=PatternType.UNSAFE_EVAL_CODE_EXECUTION_HAZARD,
        name="Unsafe eval Code Execution Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Remote code execution vulnerability evaluating untrusted user input via eval or instance_eval.",
        default_weight=0.95,
    ),
    PatternType.MASS_ASSIGNMENT_PERMIT_ALL_HAZARD: PatternMetadata(
        pattern_type=PatternType.MASS_ASSIGNMENT_PERMIT_ALL_HAZARD,
        name="Mass Assignment (permit!) Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Bypassing Strong Parameters with params.permit! exposing internal attributes to tampering.",
        default_weight=0.95,
    ),
    PatternType.COMMAND_INJECTION_HAZARD: PatternMetadata(
        pattern_type=PatternType.COMMAND_INJECTION_HAZARD,
        name="OS Command Injection Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Executing unsanitized shell commands via backticks, system(), or Open3.",
        default_weight=0.95,
    ),
    PatternType.UNSAFE_DESERIALIZATION_HAZARD: PatternMetadata(
        pattern_type=PatternType.UNSAFE_DESERIALIZATION_HAZARD,
        name="Unsafe Deserialization Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Remote code execution via Marshal.load or unsafe YAML.load on untrusted data.",
        default_weight=0.95,
    ),
    PatternType.UNVALIDATED_REDIRECT_OPEN_HAZARD: PatternMetadata(
        pattern_type=PatternType.UNVALIDATED_REDIRECT_OPEN_HAZARD,
        name="Unvalidated Open Redirect Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Open redirect vulnerability redirecting directly to user-supplied params[:url].",
        default_weight=0.90,
    ),
    PatternType.MISSING_RESPOND_TO_MISSING_HAZARD: PatternMetadata(
        pattern_type=PatternType.MISSING_RESPOND_TO_MISSING_HAZARD,
        name="Missing respond_to_missing? Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Overriding method_missing without respond_to_missing? breaking respond_to? reflection.",
        default_weight=0.92,
    ),
    PatternType.DESTRUCTIVE_MONKEY_PATCHING_HAZARD: PatternMetadata(
        pattern_type=PatternType.DESTRUCTIVE_MONKEY_PATCHING_HAZARD,
        name="Destructive Core Monkey-Patching Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Global monkey-patching core Ruby classes (String, Array, Hash) causing silent runtime conflicts.",
        default_weight=0.90,
    ),
    PatternType.N_PLUS_ONE_QUERY_HAZARD: PatternMetadata(
        pattern_type=PatternType.N_PLUS_ONE_QUERY_HAZARD,
        name="N+1 Query Association Hazard",
        category=PatternCategory.SECURITY_HAZARDS,
        description="Iterating over collections accessing association properties without includes/eager_load.",
        default_weight=0.88,
    ),

    # SOLID Principles in Ruby
    PatternType.GOD_MODEL_MONOLITHIC_SRP: PatternMetadata(
        pattern_type=PatternType.GOD_MODEL_MONOLITHIC_SRP,
        name="God Model (SRP Violation)",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Monolithic ActiveRecord model declaring excessive associations or lines (>300 lines).",
        default_weight=0.85,
    ),
    PatternType.FAT_CONTROLLER_SRP: PatternMetadata(
        pattern_type=PatternType.FAT_CONTROLLER_SRP,
        name="Fat Controller (SRP Violation)",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Controller action containing substantial business logic (>30 lines); extract to Service Object.",
        default_weight=0.85,
    ),
    PatternType.LEAKY_ACTIVE_RECORD_COUPLING: PatternMetadata(
        pattern_type=PatternType.LEAKY_ACTIVE_RECORD_COUPLING,
        name="Leaky Database Coupling",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Direct raw SQL or ActiveRecord mutation executed directly in views or helpers.",
        default_weight=0.88,
    ),
}
