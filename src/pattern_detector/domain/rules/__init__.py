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
    FactoryObjectFactoryBotRule,
    FluentBuilderDslRule,
    SingletonModuleIncludeRule,
    PrototypeDupCloneRule,
)
from .structural_rules import (
    SimpleDelegatorDecoratorRule,
    GatewayAdapterWrapperRule,
    FacadeSubsystemEntrypointRule,
    ProxyMethodMissingDelegateRule,
)
from .behavioral_rules import (
    StrategyProcBlockInjectionRule,
    CommandActiveJobRule,
    ObserverActiveSupportNotificationsRule,
    StateMachineAasmRule,
    TemplateMethodAbstractHookRule,
    ChainOfResponsibilityMiddlewareRule,
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
        # Idiomatic
        ActiveSupportConcernRule(),
        PatternMatchingCaseInRule(),
        DataClassDefineRule(),
        RefinementScopedExtensionRule(),
        SorbetRbsTypeSignatureRule(),
        EndlessMethodDefinitionRule(),
        # Enterprise & Rails
        ServiceObjectInteractorRule(),
        PolicyObjectAuthorizationRule(),
        FormObjectValidationRule(),
        DryMonadTransactionRule(),
        QueryObjectScopeRule(),
        DecoratorPresenterRule(),
        # Metaprogramming
        DynamicMethodDefinitionRule(),
        DynamicDispatchSendRule(),
        ModulePrependInterceptionRule(),
        ConstantLookupResolutionRule(),
        # Creational
        FactoryObjectFactoryBotRule(),
        FluentBuilderDslRule(),
        SingletonModuleIncludeRule(),
        PrototypeDupCloneRule(),
        # Structural
        SimpleDelegatorDecoratorRule(),
        GatewayAdapterWrapperRule(),
        FacadeSubsystemEntrypointRule(),
        ProxyMethodMissingDelegateRule(),
        # Behavioral
        StrategyProcBlockInjectionRule(),
        CommandActiveJobRule(),
        ObserverActiveSupportNotificationsRule(),
        StateMachineAasmRule(),
        TemplateMethodAbstractHookRule(),
        ChainOfResponsibilityMiddlewareRule(),
        # Security Hazards
        SqlInjectionHazardRule(),
        UnsafeEvalCodeExecutionHazardRule(),
        MassAssignmentPermitAllHazardRule(),
        CommandInjectionHazardRule(),
        UnsafeDeserializationHazardRule(),
        UnvalidatedRedirectOpenHazardRule(),
        MissingRespondToMissingHazardRule(),
        DestructiveMonkeyPatchingHazardRule(),
        NPlusOneQueryHazardRule(),
        # SOLID Principles
        GodModelMonolithicSrpRule(),
        FatControllerSrpRule(),
        LeakyActiveRecordCouplingRule(),
    ]
