# 💎 DPX-Ruby Analysis Report

- **Target Path**: `benchmarks/real_world/helpers.rb`
- **Scanned Files**: `4`
- **Execution Time**: `0.0044s`
- **Total Detections**: `17`

## 📊 Category Breakdown

| Category | Detections |
|---|:---:|
| `ruby_idiomatic` | 8 |
| `metaprogramming` | 8 |
| `creational` | 1 |

## 🔍 Findings & Detections

| # | Category | Pattern Type | Target | Confidence | Location | Summary |
|---|---|---|---|:---:|---|---|
| 1 | `ruby_idiomatic` | `activesupport_concern` | `Devise` | **95%** [VERY_HIGH] | `helpers.rb:2` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 2 | `ruby_idiomatic` | `activesupport_concern` | `Controllers` | **95%** [VERY_HIGH] | `helpers.rb:4` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 3 | `ruby_idiomatic` | `activesupport_concern` | `Helpers` | **95%** [VERY_HIGH] | `helpers.rb:6` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 4 | `ruby_idiomatic` | `activesupport_concern` | `Devise` | **95%** [VERY_HIGH] | `authenticatable.rb:5` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 5 | `ruby_idiomatic` | `activesupport_concern` | `Models` | **95%** [VERY_HIGH] | `authenticatable.rb:7` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 6 | `ruby_idiomatic` | `activesupport_concern` | `Authenticatable` | **95%** [VERY_HIGH] | `authenticatable.rb:55` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 7 | `ruby_idiomatic` | `activesupport_concern` | `ActiveSupport` | **95%** [VERY_HIGH] | `concern.rb:3` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 8 | `ruby_idiomatic` | `activesupport_concern` | `Concern` | **95%** [VERY_HIGH] | `concern.rb:124` | Modular Rails mixin pattern with automated dependency resolution and class_methods blocks. |
| 9 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:177` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 10 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:180` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 11 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `helpers.rb:230` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 12 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `authenticatable.rb:194` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 13 | `metaprogramming` | `dynamic_dispatch_send` | `DynamicDispatch` | **90%** [VERY_HIGH] | `authenticatable.rb:215` | Metaprogramming dynamic message dispatch at runtime via send or public_send. |
| 14 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:149` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 15 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:162` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 16 | `metaprogramming` | `constant_lookup_resolution` | `const_get` | **90%** [VERY_HIGH] | `concern.rb:225` | Dynamic constant reflection resolving class types at runtime via const_get. |
| 17 | `creational` | `prototype_dup_clone` | `dup/clone` | **90%** [VERY_HIGH] | `authenticatable.rb:107` | Prototype pattern creating object duplicates via dup or clone. |
