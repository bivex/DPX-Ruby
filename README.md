# 💎 DPX-Ruby: Architectural Pattern & Static Analysis Engine for Ruby 3.x & Ruby on Rails

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-green.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
[![Patterns: 42 Rules](https://img.shields.io/badge/Patterns-42%20Rules-red.svg)](#-supported-patterns--hazard-catalog)

**DPX-Ruby** is a high-performance static analysis and architectural pattern detection engine for **Ruby 3.x, Ruby on Rails, and Dry-RB** codebases (`.rb`, `.rake`, `.erb`).

Built with **Hexagonal Clean Architecture (DDD)**, DPX-Ruby detects Metaprogramming patterns, ActiveSupport Concerns, Service/Interactor Objects, Dry-Monads transactions, GoF patterns in dynamic object models, and critical security/architectural hazards (SQL Injection, Remote Code Execution, Mass Assignment, Unsafe Deserialization, Destructive Monkey-Patching, God Models).

---

## 🏛️ Architecture & Design Philosophy

DPX-Ruby follows Domain-Driven Design and Ports & Adapters (Hexagonal) architecture:

```
src/pattern_detector/
├── domain/                      # Core domain entities & invariants (Zero external dependencies)
│   ├── code_model.py            # AST/Code Model (RubyClass, RubyModule, RubyMethod, RubyFile)
│   ├── detection.py             # Detection & DetectionReport aggregates
│   ├── pattern.py               # 42 Pattern catalog definitions & weights
│   ├── value_objects.py         # Confidence, SourceLocation, PatternCategory, PatternType
│   └── rules/                   # 42 Pattern Detection Rules
│       ├── idiomatic_rules.py   # ActiveSupport Concerns, Pattern Matching (case in), Data.define, Refinements
│       ├── enterprise_rules.py  # Service Objects / Interactors, Form Objects, Policy Objects, Dry-Monads
│       ├── metaprogramming_rules.py # Dynamic Dispatch (send/define_method), Module Prepend/Include, const_get
│       ├── creational_rules.py  # Factory Girl / FactoryBot, Builder Pattern, Singleton, Prototype (dup/clone)
│       ├── structural_rules.py  # SimpleDelegator Decorator, Gateway Adapter, Presenter, Facade
│       ├── behavioral_rules.py  # Strategy (Block / Proc), Command (Jobs / Interactors), Observer (PubSub), State Machines
│       ├── security_rules.py    # SQL Injection, Unsafe eval / send, Mass Assignment permit!, Unsafe YAML/Marshal
│       └── solid_principles_rules.py # God Model SRP, Fat Controller, Leaky ActiveRecord Scopes
├── ports/                       # Interfaces defining domain boundaries
│   ├── inbound/                 # ParserPort, PatternDetectorPort
│   └── outbound/                # ExporterPort (HTML, JSON, Markdown, SARIF)
├── adapters/                    # Concrete technology implementations
│   ├── inbound/
│   │   ├── parsers/             # RegexRubyParser (Single-pass Ruby parser)
│   │   ├── detectors/           # RubyPatternDetector engine
│   │   └── cli/                 # Typer & Rich interactive CLI
│   └── outbound/
│       └── exporters/           # Interactive HTML HUD, SARIF v2.1.0, JSON, Markdown
└── application/
    └── scan_service.py          # Orchestration service
```

---

## 🔍 Supported Patterns & Hazard Catalog (42 Rules)

| Category | Pattern Type | Target / Construct | Default Weight | Description |
|---|---|---|:---:|---|
| **Ruby Idiomatic** | `activesupport_concern` | `extend ActiveSupport::Concern` | 95% | Modular Rails mixin with dependency resolution and class_methods blocks |
| | `pattern_matching_case_in` | `case val; in { a: }` | 92% | Modern Ruby 3.x structural deconstruction and pattern matching |
| | `data_class_define` | `Data.define(:x, :y)` | 95% | Immutable value object using Ruby 3.2+ Data class |
| | `refinement_scoped_extension` | `refine String do ...` | 92% | Lexically scoped monkey-patching avoiding global namespace pollution |
| | `sorbet_rbs_type_signature` | `sig { params(...).returns(...) }` | 90% | Static type annotation via Sorbet sig or RBS typing |
| | `endless_method_definition` | `def double(x) = x * 2` | 90% | Modern Ruby 3.x concise one-liner method syntax |
| **Enterprise & Clean Rails** | `service_object_interactor` | `class CreateUser; def call` | 95% | Encapsulated business workflow following Single Responsibility Principle |
| | `policy_object_authorization` | `class PostPolicy < ApplicationPolicy` | 95% | Granular access control following Pundit / ActionPolicy conventions |
| | `form_object_validation` | `include ActiveModel::Model` | 92% | Decoupled form handling and validation separating input from models |
| | `dry_monad_transaction` | `Dry::Monads[:result, :do]` | 95% | Railway-oriented programming with explicit Success/Failure monads |
| | `query_object_scope` | `class RecentUsersQuery` | 92% | Dedicated query object isolating complex ActiveRecord relational logic |
| | `decorator_presenter` | `class UserPresenter < SimpleDelegator`| 92% | View logic isolation wrapping models in presenter decorators |
| **Metaprogramming & Reflection**| `dynamic_method_definition` | `define_method(:...)` | 92% | Runtime method generation synthesizing repetitive behaviors |
| | `dynamic_dispatch_send` | `send(action, *args)` | 90% | Metaprogramming dynamic message dispatch at runtime |
| | `module_prepend_interception` | `prepend AroundAdvice` | 95% | Method wrapper interception placing module ahead of class in ancestor chain |
| | `constant_lookup_resolution` | `const_get(class_name)` | 90% | Dynamic constant reflection resolving class types at runtime |
| **GoF Creational** | `factory_object_factory_bot` | `FactoryBot.define` | 92% | Factory pattern stamping out test fixtures or complex domain objects |
| | `fluent_builder_dsl` | `class QueryBuilder; def where` | 90% | Builder pattern providing fluent method chaining for complex object construction |
| | `singleton_module_include` | `include Singleton` | 92% | Enforcing single global runtime instance via Ruby standard Singleton |
| | `prototype_dup_clone` | `dup / clone deep copy` | 90% | Prototype pattern cloning prototype objects |
| **GoF Structural** | `simple_delegator_decorator` | `class Decorator < SimpleDelegator`| 92% | Decorator pattern forwarding unhandled messages to wrapped component |
| | `gateway_adapter_wrapper` | `class StripeGateway; def charge` | 92% | Adapter pattern adapting third-party API payloads to domain interfaces |
| | `facade_subsystem_entrypoint`| `class BillingFacade; def checkout` | 92% | Facade pattern coordinating payments, invoices, and email subsystems |
| | `proxy_method_missing_delegate`| `def method_missing; @target.send` | 90% | Proxy pattern lazily intercepting and forwarding messages to target |
| **GoF Behavioral** | `strategy_proc_block_injection`| `def compute(&strategy)` | 92% | Strategy pattern injecting interchangeable algorithms via blocks/procs |
| | `command_active_job` | `class ProcessPaymentJob < ApplicationJob`| 95% | Command pattern encapsulating asynchronous job execution |
| | `observer_activesupport_notifications`| `ActiveSupport::Notifications.subscribe`| 95% | Observer / PubSub pattern decoupling event producers and listeners |
| | `state_machine_aasm` | `include AASM; aasm do` | 95% | State machine pattern enforcing verified state transitions |
| | `template_method_abstract_hook`| `def process; pre; step; post; end`| 90% | Template Method defining algorithm skeleton with subclass hooks |
| | `chain_of_responsibility_middleware`| `def call(env); @app.call(env)` | 95% | Rack middleware pipeline processing HTTP requests sequentially |
| **Security & Architectural Hazards**| `sql_injection_hazard` | `where("name = '#{params[:name]}'")` | 95% | Unsanitized raw string interpolation inside SQL queries risking SQLi |
| | `unsafe_eval_code_execution_hazard`| `eval(params[:code])` | 95% | Remote code execution vulnerability evaluating untrusted user input |
| | `mass_assignment_permit_all_hazard`| `params.permit!` | 95% | Bypassing Strong Parameters exposing internal model attributes to tampering |
| | `command_injection_hazard` | `` `rm #{file}` `` / `system(...)` | 95% | OS command injection executing unsanitized shell commands |
| | `unsafe_deserialization_hazard` | `Marshal.load` / `YAML.load` | 95% | Remote code execution via unsafe object deserialization |
| | `unvalidated_redirect_open_hazard`| `redirect_to params[:url]` | 90% | Open redirect vulnerability redirecting to external malicious URLs |
| | `missing_respond_to_missing_hazard`| `method_missing` without `respond_to_missing?`| 92% | Overriding method_missing without respond_to_missing? breaking reflection |
| | `destructive_monkey_patching_hazard`| Reopening `String` / `Array` | 90% | Global monkey-patching core Ruby classes causing silent runtime conflicts |
| | `n_plus_one_query_hazard` | Association query in iteration | 88% | Potential N+1 database queries due to missing includes/eager_load |
| **SOLID Principles in Ruby** | `god_model_monolithic_srp` | Model > 300 lines / > 15 associations | 85% | Monolithic ActiveRecord model violating Single Responsibility Principle |
| | `fat_controller_srp` | Controller action > 30 lines | 85% | Fat controller action containing business logic; extract to Service Object |
| | `leaky_active_record_coupling`| Raw SQL queries in views/controllers| 88% | Direct database coupling violating Separation of Concerns |

---

## ⚡ Installation & CLI Usage

```bash
# Clone repository
git clone https://github.com/bivex/DPX-Ruby.git
cd DPX-Ruby

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 🚀 Running Analysis

```bash
# 1. Quick scan on Ruby/Rails codebases
dpx-ruby scan app/

# 2. Export Full Interactive HTML HUD + SARIF + JSON + Markdown
dpx-ruby scan app/ \
    -H reports/dpx_ruby_hud.html \
    -J reports/dpx_ruby_findings.json \
    -M reports/dpx_ruby_report.md \
    -S reports/dpx_ruby_report.sarif

# 3. View 42 supported pattern catalog
dpx-ruby catalog
```

---

## 🌐 The DPX Multi-Language Static Analysis Family (31 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 2 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 3 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 4 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 5 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 6 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 7 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 8 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 9 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 10 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 11 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 12 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 13 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 14 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 15 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 16 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 17 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 18 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 19 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 20 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 21 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 22 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 23 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 24 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | **Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security** |
| 25 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 26 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 27 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 28 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 29 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 30 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 31 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

## 📄 License

MIT License © 2026 Bivex
