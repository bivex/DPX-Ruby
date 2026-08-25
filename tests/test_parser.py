import pytest
from pattern_detector.adapters.inbound.parsers.ruby_parser import RegexRubyParser


SAMPLE_RUBY_CODE = """
module Taggable
  extend ActiveSupport::Concern

  included do
    has_many :tags
  end

  def add_tag(tag_name)
    tags.create(name: tag_name)
  end
end

class User < ApplicationRecord
  include Taggable
  include Singleton

  has_many :posts
  has_many :comments
  before_save :normalize_email

  def full_name
    "#{first_name} #{last_name}"
  end

  def self.active_users
    where(active: true)
  end
end

class CreateUserService
  def initialize(params)
    @params = params
  end

  def call
    User.create!(@params)
  end
end
"""


def test_regex_ruby_parser():
    parser = RegexRubyParser()
    file_ast = parser.parse_file("app/models/user.rb", SAMPLE_RUBY_CODE)

    # Modules
    assert len(file_ast.modules) == 1
    mod = file_ast.modules[0]
    assert mod.name == "Taggable"
    assert mod.is_concern is True
    assert len(mod.methods) == 1
    assert mod.methods[0].name == "add_tag"

    # Classes
    assert len(file_ast.classes) == 2
    user_cls = file_ast.classes[0]
    assert user_cls.name == "User"
    assert user_cls.superclass == "ApplicationRecord"
    assert "Taggable" in user_cls.mixins
    assert "Singleton" in user_cls.mixins
    assert "posts" in user_cls.associations
    assert "comments" in user_cls.associations
    assert "normalize_email" in user_cls.callbacks
    assert len(user_cls.methods) == 2

    fn_names = [m.name for m in user_cls.methods]
    assert "full_name" in fn_names
    assert "active_users" in fn_names

    # Service class
    service_cls = file_ast.classes[1]
    assert service_cls.name == "CreateUserService"
    assert service_cls.is_service is True
