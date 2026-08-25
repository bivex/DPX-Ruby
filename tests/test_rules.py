import pytest
from pattern_detector.domain.value_objects import PatternType
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.adapters.inbound.parsers.ruby_parser import RegexRubyParser
from pattern_detector.adapters.inbound.detectors.ruby_detector import RubyPatternDetector


COMPREHENSIVE_RUBY_CODE = """
module Auditable
  extend ActiveSupport::Concern
end

Point = Data.define(:x, :y)

# 1. GoF Creational
class VehicleFactory
  def create_car
    Car.new
  end
end

class GUIAbstractFactory
  def create_button
    raise NotImplementedError
  end
end

class QueryBuilder
  def with_limit(l)
    @limit = l
    self
  end
end

class Configuration
  include Singleton
end

# 2. GoF Structural
class StripeAdapter
  def charge(amount)
    true
  end
end

class RemoteControlBridge
  def initialize(driver)
    @driver = driver
  end
end

class MenuComposite
  def initialize
    @children = []
  end

  def add(child)
    @children << child
  end
end

class UserPresenter < SimpleDelegator
  def formatted_name
    name.upcase
  end
end

class CheckoutFacade
  def process_order
    true
  end
end

class FlyweightPool
  def self.get(key)
    @pool ||= {}
    @pool[key] ||= Object.new
  end
end

class VirtualProxy
  def method_missing(name, *args)
    puts "missing: #{name}"
  end
end

# 3. GoF Behavioral
class AuthMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    @app.call(env)
  end
end

class SendEmailCommand < ApplicationJob
  def perform(id)
    true
  end
end

class MathInterpreter
  def evaluate(context)
    42
  end
end

class CustomCollection
  include Enumerable

  def each(&block)
    [1, 2, 3].each(&block)
  end
end

class ChatMediator
  def notify(sender, event)
    puts "#{sender}: #{event}"
  end
end

class EditorMemento
  def save_state
    @state.dup
  end
end

class OrderState
  include AASM

  aasm do
    state :pending, initial: true
    state :paid
  end
end

class SortStrategy
  def sort_items(&block)
    items.sort(&block)
  end
end

class AbstractReport
  def generate
    header
    body
  end

  def header
    raise NotImplementedError
  end
end

class AstVisitor
  def visit_node(node)
    true
  end

  def accept(visitor)
    visitor.visit(self)
  end
end

# Security Hazards
class SecurityExploitsController < ApplicationController
  def search
    User.where("name = '#{params[:name]}'")
    eval(params[:ruby_code])
    params.permit!
    `ping #{params[:host]}`
    Marshal.load(params[:payload])
    redirect_to params[:url]
  end

  def show
    User.all.each do |user|
      puts user.posts.count
    end
  end
end
"""


def test_rule_evaluations():
    parser = RegexRubyParser()
    file_ast = parser.parse_file("app/models/test_patterns.rb", COMPREHENSIVE_RUBY_CODE)

    model = CodeModel()
    model.add_file(file_ast)

    detector = RubyPatternDetector()
    report = detector.detect(model)

    detected_types = {d.pattern_type for d in report.detections}

    # Idiomatic
    assert PatternType.ACTIVESUPPORT_CONCERN in detected_types
    assert PatternType.DATA_CLASS_DEFINE in detected_types

    # GoF Creational (5/5)
    assert PatternType.GOF_FACTORY_METHOD in detected_types
    assert PatternType.GOF_ABSTRACT_FACTORY in detected_types
    assert PatternType.GOF_BUILDER in detected_types
    assert PatternType.GOF_SINGLETON in detected_types
    assert PatternType.GOF_PROTOTYPE in detected_types

    # GoF Structural (7/7)
    assert PatternType.GOF_ADAPTER in detected_types
    assert PatternType.GOF_BRIDGE in detected_types
    assert PatternType.GOF_COMPOSITE in detected_types
    assert PatternType.GOF_DECORATOR in detected_types
    assert PatternType.GOF_FACADE in detected_types
    assert PatternType.GOF_FLYWEIGHT in detected_types
    assert PatternType.GOF_PROXY in detected_types

    # GoF Behavioral (11/11)
    assert PatternType.GOF_CHAIN_OF_RESPONSIBILITY in detected_types
    assert PatternType.GOF_COMMAND in detected_types
    assert PatternType.GOF_INTERPRETER in detected_types
    assert PatternType.GOF_ITERATOR in detected_types
    assert PatternType.GOF_MEDIATOR in detected_types
    assert PatternType.GOF_MEMENTO in detected_types
    assert PatternType.GOF_STATE in detected_types
    assert PatternType.GOF_STRATEGY in detected_types
    assert PatternType.GOF_TEMPLATE_METHOD in detected_types
    assert PatternType.GOF_VISITOR in detected_types

    # Security Hazards
    assert PatternType.SQL_INJECTION_HAZARD in detected_types
    assert PatternType.UNSAFE_EVAL_CODE_EXECUTION_HAZARD in detected_types
    assert PatternType.MASS_ASSIGNMENT_PERMIT_ALL_HAZARD in detected_types
    assert PatternType.COMMAND_INJECTION_HAZARD in detected_types
    assert PatternType.UNSAFE_DESERIALIZATION_HAZARD in detected_types
    assert PatternType.UNVALIDATED_REDIRECT_OPEN_HAZARD in detected_types
    assert PatternType.MISSING_RESPOND_TO_MISSING_HAZARD in detected_types
    assert PatternType.N_PLUS_ONE_QUERY_HAZARD in detected_types
