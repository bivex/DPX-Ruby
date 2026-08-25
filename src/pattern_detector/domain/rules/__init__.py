from typing import List
from .base import Rule
from .idiomatic_rules import (
    ActiveSupportConcernRule,
    PatternMatchingCaseInRule,
    DataClassDefineRule,
    RefinementScopedExtensionRule,
    SorbetRbsTypeSignatureRule,
    EndlessMethodDefinitionRule,
)
from .enterprise_rules import (
    ServiceObjectInteractorRule,
    PolicyObjectAuthorizationRule,
    FormObjectValidationRule,
    DryMonadTransactionRule,
    QueryObjectScopeRule,
    DecoratorPresenterRule,
)
from .metaprogramming_rules import (
    DynamicMethodDefinitionRule,
    DynamicDispatchSendRule,
    ModulePrependInterceptionRule,
    ConstantLookupResolutionRule,
)
from .creational_rules import (
    FactoryMethodRule,
    AbstractFactoryRule,
    BuilderRule,
    PrototypeRule,
    SingletonRule,
)
from .structural_rules import (
    AdapterRule,
    BridgeRule,
    CompositeRule,
    DecoratorRule,
    FacadeRule,
    FlyweightRule,
    ProxyRule,
)
from .behavioral_rules import (
    ChainOfResponsibilityRule,
    CommandRule,
    InterpreterRule,
    IteratorRule,
    MediatorRule,
    MementoRule,
    ObserverRule,
    StateRule,
    StrategyRule,
    TemplateMethodRule,
    VisitorRule,
)
from .security_rules import (
    SqlInjectionHazardRule,
    UnsafeEvalCodeExecutionHazardRule,
    MassAssignmentPermitAllHazardRule,
    CommandInjectionHazardRule,
    UnsafeDeserializationHazardRule,
    UnvalidatedRedirectOpenHazardRule,
    MissingRespondToMissingHazardRule,
    DestructiveMonkeyPatchingHazardRule,
    NPlusOneQueryHazardRule,
)
from .solid_principles_rules import (
    GodModelMonolithicSrpRule,
    FatControllerSrpRule,
    LeakyActiveRecordCouplingRule,
)


def get_default_rules() -> List[Rule]:
    return [
        # Idiomatic (6)
        ActiveSupportConcernRule(),
        PatternMatchingCaseInRule(),
        DataClassDefineRule(),
        RefinementScopedExtensionRule(),
        SorbetRbsTypeSignatureRule(),
        EndlessMethodDefinitionRule(),
        # Enterprise & Rails (6)
        ServiceObjectInteractorRule(),
        PolicyObjectAuthorizationRule(),
        FormObjectValidationRule(),
        DryMonadTransactionRule(),
        QueryObjectScopeRule(),
        DecoratorPresenterRule(),
        # Metaprogramming (4)
        DynamicMethodDefinitionRule(),
        DynamicDispatchSendRule(),
        ModulePrependInterceptionRule(),
        ConstantLookupResolutionRule(),
        # ALL 23 GANG OF FOUR (GoF) PATTERNS:
        # GoF Creational (5)
        FactoryMethodRule(),
        AbstractFactoryRule(),
        BuilderRule(),
        PrototypeRule(),
        SingletonRule(),
        # GoF Structural (7)
        AdapterRule(),
        BridgeRule(),
        CompositeRule(),
        DecoratorRule(),
        FacadeRule(),
        FlyweightRule(),
        ProxyRule(),
        # GoF Behavioral (11)
        ChainOfResponsibilityRule(),
        CommandRule(),
        InterpreterRule(),
        IteratorRule(),
        MediatorRule(),
        MementoRule(),
        ObserverRule(),
        StateRule(),
        StrategyRule(),
        TemplateMethodRule(),
        VisitorRule(),
        # Security Hazards (9)
        SqlInjectionHazardRule(),
        UnsafeEvalCodeExecutionHazardRule(),
        MassAssignmentPermitAllHazardRule(),
        CommandInjectionHazardRule(),
        UnsafeDeserializationHazardRule(),
        UnvalidatedRedirectOpenHazardRule(),
        MissingRespondToMissingHazardRule(),
        DestructiveMonkeyPatchingHazardRule(),
        NPlusOneQueryHazardRule(),
        # SOLID Principles (3)
        GodModelMonolithicSrpRule(),
        FatControllerSrpRule(),
        LeakyActiveRecordCouplingRule(),
    ]
