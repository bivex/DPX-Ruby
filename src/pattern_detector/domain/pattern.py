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

    # --- ALL 23 GANG OF FOUR (GoF) PATTERNS ---

    # 1. GoF Creational (5/5)
    PatternType.GOF_FACTORY_METHOD: PatternMetadata(
        pattern_type=PatternType.GOF_FACTORY_METHOD,
        name="GoF Factory Method",
        category=PatternCategory.GOF_CREATIONAL,
        description="Creational pattern providing a dedicated creation method or FactoryBot definition for object instantiation.",
        default_weight=0.92,
    ),
    PatternType.GOF_ABSTRACT_FACTORY: PatternMetadata(
        pattern_type=PatternType.GOF_ABSTRACT_FACTORY,
        name="GoF Abstract Factory",
        category=PatternCategory.GOF_CREATIONAL,
        description="Creational pattern producing families of related or dependent objects without specifying concrete classes.",
        default_weight=0.92,
    ),
    PatternType.GOF_BUILDER: PatternMetadata(
        pattern_type=PatternType.GOF_BUILDER,
        name="GoF Builder",
        category=PatternCategory.GOF_CREATIONAL,
        description="Creational pattern separating complex object construction from its representation using fluent method chaining.",
        default_weight=0.90,
    ),
    PatternType.GOF_PROTOTYPE: PatternMetadata(
        pattern_type=PatternType.GOF_PROTOTYPE,
        name="GoF Prototype",
        category=PatternCategory.GOF_CREATIONAL,
        description="Creational pattern creating new objects by cloning prototypical instances via dup, clone, or initialize_copy.",
        default_weight=0.90,
    ),
    PatternType.GOF_SINGLETON: PatternMetadata(
        pattern_type=PatternType.GOF_SINGLETON,
        name="GoF Singleton",
        category=PatternCategory.GOF_CREATIONAL,
        description="Creational pattern ensuring a class has only one global instance via 'include Singleton' or class instance memoization.",
        default_weight=0.92,
    ),

    # 2. GoF Structural (7/7)
    PatternType.GOF_ADAPTER: PatternMetadata(
        pattern_type=PatternType.GOF_ADAPTER,
        name="GoF Adapter",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern converting the interface of a class into another interface expected by clients.",
        default_weight=0.92,
    ),
    PatternType.GOF_BRIDGE: PatternMetadata(
        pattern_type=PatternType.GOF_BRIDGE,
        name="GoF Bridge",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern decoupling an abstraction from its implementation so that the two can vary independently.",
        default_weight=0.90,
    ),
    PatternType.GOF_COMPOSITE: PatternMetadata(
        pattern_type=PatternType.GOF_COMPOSITE,
        name="GoF Composite",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern composing objects into tree structures to represent part-whole hierarchies with a uniform interface.",
        default_weight=0.92,
    ),
    PatternType.GOF_DECORATOR: PatternMetadata(
        pattern_type=PatternType.GOF_DECORATOR,
        name="GoF Decorator",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern dynamically attaching additional responsibilities to an object via SimpleDelegator or module wrapping.",
        default_weight=0.92,
    ),
    PatternType.GOF_FACADE: PatternMetadata(
        pattern_type=PatternType.GOF_FACADE,
        name="GoF Facade",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern providing a unified high-level interface to a set of interfaces in a subsystem.",
        default_weight=0.92,
    ),
    PatternType.GOF_FLYWEIGHT: PatternMetadata(
        pattern_type=PatternType.GOF_FLYWEIGHT,
        name="GoF Flyweight",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern using sharing to support large numbers of fine-grained objects efficiently (symbol/string interning, memoized pools).",
        default_weight=0.90,
    ),
    PatternType.GOF_PROXY: PatternMetadata(
        pattern_type=PatternType.GOF_PROXY,
        name="GoF Proxy",
        category=PatternCategory.GOF_STRUCTURAL,
        description="Structural pattern providing a surrogate or placeholder for another object to control access to it (virtual proxy, method_missing).",
        default_weight=0.90,
    ),

    # 3. GoF Behavioral (11/11)
    PatternType.GOF_CHAIN_OF_RESPONSIBILITY: PatternMetadata(
        pattern_type=PatternType.GOF_CHAIN_OF_RESPONSIBILITY,
        name="GoF Chain of Responsibility",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern passing requests along a chain of handlers/middleware until one handles it.",
        default_weight=0.95,
    ),
    PatternType.GOF_COMMAND: PatternMetadata(
        pattern_type=PatternType.GOF_COMMAND,
        name="GoF Command",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern encapsulating a request as a standalone object with execution methods (ActiveJob, Sidekiq, Interactor).",
        default_weight=0.95,
    ),
    PatternType.GOF_INTERPRETER: PatternMetadata(
        pattern_type=PatternType.GOF_INTERPRETER,
        name="GoF Interpreter",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern defining a representation for grammar along with an interpreter to evaluate expressions (AST/DSL evaluation).",
        default_weight=0.90,
    ),
    PatternType.GOF_ITERATOR: PatternMetadata(
        pattern_type=PatternType.GOF_ITERATOR,
        name="GoF Iterator",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern providing a way to access elements of an aggregate object sequentially via 'include Enumerable' and 'each'.",
        default_weight=0.92,
    ),
    PatternType.GOF_MEDIATOR: PatternMetadata(
        pattern_type=PatternType.GOF_MEDIATOR,
        name="GoF Mediator",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern defining an object that encapsulates how a set of objects interact, preventing direct coupling.",
        default_weight=0.90,
    ),
    PatternType.GOF_MEMENTO: PatternMetadata(
        pattern_type=PatternType.GOF_MEMENTO,
        name="GoF Memento",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern capturing and externalizing an object's internal state so it can be restored later without violating encapsulation.",
        default_weight=0.90,
    ),
    PatternType.GOF_OBSERVER: PatternMetadata(
        pattern_type=PatternType.GOF_OBSERVER,
        name="GoF Observer",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern defining a 1-to-N dependency where state changes automatically notify dependents (ActiveSupport::Notifications, Observable).",
        default_weight=0.95,
    ),
    PatternType.GOF_STATE: PatternMetadata(
        pattern_type=PatternType.GOF_STATE,
        name="GoF State",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern allowing an object to alter its behavior when its internal state changes (AASM, state_machine).",
        default_weight=0.95,
    ),
    PatternType.GOF_STRATEGY: PatternMetadata(
        pattern_type=PatternType.GOF_STRATEGY,
        name="GoF Strategy",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern defining a family of interchangeable algorithms and making them interchangeable at runtime via blocks/procs.",
        default_weight=0.92,
    ),
    PatternType.GOF_TEMPLATE_METHOD: PatternMetadata(
        pattern_type=PatternType.GOF_TEMPLATE_METHOD,
        name="GoF Template Method",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern defining the skeleton of an algorithm in an operation, deferring some steps to subclasses via hook methods.",
        default_weight=0.90,
    ),
    PatternType.GOF_VISITOR: PatternMetadata(
        pattern_type=PatternType.GOF_VISITOR,
        name="GoF Visitor",
        category=PatternCategory.GOF_BEHAVIORAL,
        description="Behavioral pattern representing an operation to be performed on the elements of an object structure using double dispatch (accept / visit).",
        default_weight=0.92,
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
        description="Overriding method_missing without respond_to_missing? breaking respond_to? introspection.",
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
