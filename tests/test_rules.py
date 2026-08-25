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

class PostPolicy < ApplicationPolicy
  def update?
    user.admin?
  end
end

class UserPresenter < SimpleDelegator
  def formatted_name
    name.upcase
  end
end

class PaymentGateway
  def charge(amount)
    Stripe::Charge.create(amount: amount)
  end
end

class OrderWorkflow
  include AASM

  aasm do
    state :pending, initial: true
    state :paid
  end

  def execute(&strategy)
    strategy.call
  end
end

class ProcessEmailJob < ApplicationJob
  def perform(user_id)
    UserMailer.welcome(user_id).deliver_later
  end
end

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

class DynamicWrapper
  def method_missing(name, *args)
    puts "missing: #{name}"
  end
end
"""


def test_rule_evaluations():
    parser = RegexRubyParser()
    file_ast = parser.parse_file("app/controllers/security_exploits_controller.rb", COMPREHENSIVE_RUBY_CODE)

    model = CodeModel()
    model.add_file(file_ast)

    detector = RubyPatternDetector()
    report = detector.detect(model)

    detected_types = {d.pattern_type for d in report.detections}

    # Idiomatic
    assert PatternType.ACTIVESUPPORT_CONCERN in detected_types
    assert PatternType.DATA_CLASS_DEFINE in detected_types

    # Enterprise & Clean Rails
    assert PatternType.POLICY_OBJECT_AUTHORIZATION in detected_types
    assert PatternType.DECORATOR_PRESENTER in detected_types

    # Structural & Behavioral
    assert PatternType.GATEWAY_ADAPTER_WRAPPER in detected_types
    assert PatternType.SIMPLE_DELEGATOR_DECORATOR in detected_types
    assert PatternType.STATE_MACHINE_AASM in detected_types
    assert PatternType.STRATEGY_PROC_BLOCK_INJECTION in detected_types
    assert PatternType.COMMAND_ACTIVE_JOB in detected_types

    # Security Hazards
    assert PatternType.SQL_INJECTION_HAZARD in detected_types
    assert PatternType.UNSAFE_EVAL_CODE_EXECUTION_HAZARD in detected_types
    assert PatternType.MASS_ASSIGNMENT_PERMIT_ALL_HAZARD in detected_types
    assert PatternType.COMMAND_INJECTION_HAZARD in detected_types
    assert PatternType.UNSAFE_DESERIALIZATION_HAZARD in detected_types
    assert PatternType.UNVALIDATED_REDIRECT_OPEN_HAZARD in detected_types
    assert PatternType.MISSING_RESPOND_TO_MISSING_HAZARD in detected_types
    assert PatternType.N_PLUS_ONE_QUERY_HAZARD in detected_types
