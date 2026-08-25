# 💎 DPX-Ruby Analysis Report

- **Target Path**: `benchmarks/ecommerce_platform.rb`
- **Scanned Files**: `1`
- **Execution Time**: `0.0012s`
- **Total Detections**: `16`

## 📊 Category Breakdown

| Category | Detections |
|---|:---:|
| `security_hazards` | 6 |
| `ruby_idiomatic` | 3 |
| `enterprise_rails` | 3 |
| `structural` | 2 |
| `behavioral` | 2 |

## 🔍 Findings & Detections

| # | Category | Pattern Type | Target | Confidence | Location | Summary |
|---|---|---|---|:---:|---|---|
| 1 | `ruby_idiomatic` | `activesupport_concern` | `Auditable` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:2` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 2 | `ruby_idiomatic` | `data_class_define` | `OrderData` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:15` | Immutable value object declaration using Ruby 3.2+ Data.define. |
| 3 | `ruby_idiomatic` | `refinement_scoped_extension` | `String` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:18` | Lexically scoped monkey-patching avoiding global namespace collision. |
| 4 | `enterprise_rails` | `service_object_interactor` | `ProcessOrderService` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:50` | Encapsulated business workflow following Single Responsibility Principle with standard call method. |
| 5 | `enterprise_rails` | `dry_monad_transaction` | `DryMonads` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:52` | Railway-oriented programming using Dry::Monads Result (Success/Failure) and Do notation. |
| 6 | `enterprise_rails` | `decorator_presenter` | `OrderPresenter` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:90` | View logic isolation wrapping models in presenter decorators (Draper / SimpleDelegator). |
| 7 | `structural` | `simple_delegator_decorator` | `OrderPresenter` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:90` | Decorator pattern forwarding unhandled messages to wrapped component via SimpleDelegator. |
| 8 | `structural` | `gateway_adapter_wrapper` | `StripeGateway` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:83` | Adapter pattern adapting external third-party API payloads to domain interfaces. |
| 9 | `behavioral` | `command_active_job` | `OrderFulfillmentJob` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:96` | Command pattern encapsulating asynchronous job execution and background workflows. |
| 10 | `behavioral` | `state_machine_aasm` | `Order` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:24` | State machine pattern enforcing verified state transitions and guards. |
| 11 | `security_hazards` | `sql_injection_hazard` | `SQLInjection` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:109` | Unsanitized raw string interpolation inside SQL queries (where, find_by_sql, order). |
| 12 | `security_hazards` | `unsafe_eval_code_execution_hazard` | `eval` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:115` | Remote code execution vulnerability evaluating untrusted user input via eval or instance_eval. |
| 13 | `security_hazards` | `mass_assignment_permit_all_hazard` | `params.permit!` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:112` | Bypassing Strong Parameters with params.permit! exposing internal attributes to tampering. |
| 14 | `security_hazards` | `command_injection_hazard` | `CommandInjection` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:118` | Executing unsanitized shell commands via backticks, system(), or Open3. |
| 15 | `security_hazards` | `unvalidated_redirect_open_hazard` | `OpenRedirect` | **90%** [VERY_HIGH] | `ecommerce_platform.rb:121` | Open redirect vulnerability redirecting directly to user-supplied params[:url]. |
| 16 | `security_hazards` | `n_plus_one_query_hazard` | `VulnerableAdminController#list_user_orders` | **88%** [VERY_HIGH] | `ecommerce_platform.rb:123` | Iterating over collections accessing association properties without includes/eager_load. |
