# 💎 DPX-Ruby Analysis Report

- **Target Path**: `benchmarks/ecommerce_platform.rb`
- **Scanned Files**: `5`
- **Execution Time**: `0.0058s`
- **Total Detections**: `33`

## 📊 Category Breakdown

| Category | Detections |
|---|:---:|
| `ruby_idiomatic` | 11 |
| `metaprogramming` | 8 |
| `security_hazards` | 6 |
| `enterprise_rails` | 3 |
| `gof_structural` | 2 |
| `gof_behavioral` | 2 |
| `gof_creational` | 1 |

## 🔍 Findings & Detections

| # | Category | Pattern Type | Target | Confidence | Location | Summary |
|---|---|---|---|:---:|---|---|
| 1 | `ruby_idiomatic` | `activesupport_concern` | `Auditable` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:2` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 2 | `ruby_idiomatic` | `activesupport_concern` | `Devise` | **95%** [VERY_HIGH] | `helpers.rb:2` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 3 | `ruby_idiomatic` | `activesupport_concern` | `Controllers` | **95%** [VERY_HIGH] | `helpers.rb:4` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 4 | `ruby_idiomatic` | `activesupport_concern` | `Helpers` | **95%** [VERY_HIGH] | `helpers.rb:6` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 5 | `ruby_idiomatic` | `activesupport_concern` | `Devise` | **95%** [VERY_HIGH] | `authenticatable.rb:5` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 6 | `ruby_idiomatic` | `activesupport_concern` | `Models` | **95%** [VERY_HIGH] | `authenticatable.rb:7` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 7 | `ruby_idiomatic` | `activesupport_concern` | `Authenticatable` | **95%** [VERY_HIGH] | `authenticatable.rb:55` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 8 | `ruby_idiomatic` | `activesupport_concern` | `ActiveSupport` | **95%** [VERY_HIGH] | `concern.rb:3` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 9 | `ruby_idiomatic` | `activesupport_concern` | `Concern` | **95%** [VERY_HIGH] | `concern.rb:124` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 10 | `ruby_idiomatic` | `data_class_define` | `OrderData` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:15` | Immutable value object declaration using Ruby 3.2+ Data.define. |
| 11 | `ruby_idiomatic` | `refinement_scoped_extension` | `String` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:18` | Lexically scoped monkey-patching avoiding global namespace collision. |
| 12 | `enterprise_rails` | `service_object_interactor` | `ProcessOrderService` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:50` | Encapsulated business workflow following Single Responsibility Principle with standard call method. |
| 13 | `enterprise_rails` | `dry_monad_transaction` | `DryMonads` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:52` | Railway-oriented programming using Dry::Monads Result (Success/Failure) and Do notation. |
| 14 | `enterprise_rails` | `decorator_presenter` | `OrderPresenter` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:90` | View logic isolation wrapping models in presenter decorators (Draper / SimpleDelegator). |
| 15 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:177` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 16 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:180` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 17 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:230` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 18 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `authenticatable.rb:194` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 19 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `authenticatable.rb:215` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 20 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:149` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 21 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:162` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 22 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:225` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 23 | `gof_creational` | `gof_prototype` | `dup/clone` | **90%** [VERY_HIGH] | `authenticatable.rb:107` | Creational pattern creating new objects by cloning prototypical instances via dup, clone, or initialize_copy. |
| 24 | `gof_structural` | `gof_adapter` | `StripeGateway` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:83` | Structural pattern converting the interface of a class into another interface expected by clients. |
| 25 | `gof_structural` | `gof_decorator` | `OrderPresenter` | **92%** [VERY_HIGH] | `ecommerce_platform.rb:90` | Structural pattern dynamically attaching additional responsibilities to an object via SimpleDelegator or module wrapping. |
| 26 | `gof_behavioral` | `gof_command` | `OrderFulfillmentJob` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:96` | Behavioral pattern encapsulating a request as a standalone object with execution methods (ActiveJob, Sidekiq, Interactor). |
| 27 | `gof_behavioral` | `gof_state` | `Order` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:24` | Behavioral pattern allowing an object to alter its behavior when its internal state changes (AASM, state_machine). |
| 28 | `security_hazards` | `sql_injection_hazard` | `SQLInjection` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:109` | Unsanitized raw string interpolation inside SQL queries (where, find_by_sql, order). |
| 29 | `security_hazards` | `unsafe_eval_code_execution_hazard` | `eval` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:115` | Remote code execution vulnerability evaluating untrusted user input via eval or instance_eval. |
| 30 | `security_hazards` | `mass_assignment_permit_all_hazard` | `params.permit!` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:112` | Bypassing Strong Parameters with params.permit! exposing internal attributes to tampering. |
| 31 | `security_hazards` | `command_injection_hazard` | `CommandInjection` | **95%** [VERY_HIGH] | `ecommerce_platform.rb:118` | Executing unsanitized shell commands via backticks, system(), or Open3. |
| 32 | `security_hazards` | `unvalidated_redirect_open_hazard` | `OpenRedirect` | **90%** [VERY_HIGH] | `ecommerce_platform.rb:121` | Open redirect vulnerability redirecting directly to user-supplied params[:url]. |
| 33 | `security_hazards` | `n_plus_one_query_hazard` | `VulnerableAdminController#list_user_orders` | **88%** [VERY_HIGH] | `ecommerce_platform.rb:123` | Iterating over collections accessing association properties without includes/eager_load. |
