# frozen_string_literal: true

module Auditable
  extend ActiveSupport::Concern

  included do
    has_many :audit_logs, as: :auditable
  end

  def log_activity(action)
    audit_logs.create!(action: action, timestamp: Time.current)
  end
end

OrderData = Data.define(:id, :customer_id, :total_cents)

module StringExtensions
  refine String do
    def to_slug
      downcase.gsub(/[^a-z0-9]+/, '-')
    end
  end
end

class Order < ApplicationRecord
  include Auditable
  include AASM

  belongs_to :user
  has_many :line_items
  has_many :payments

  before_save :calculate_total

  aasm do
    state :pending, initial: true
    state :processing
    state :completed
    state :cancelled

    event :process do
      transitions from: :pending, to: :processing
    end
  end

  def calculate_total
    self.total_cents = line_items.sum(&:price_cents)
  end
end

class ProcessOrderService
  include Dry::Monads[:result, :do]

  def initialize(order_id)
    @order_id = order_id
  end

  def call
    order = yield find_order
    yield charge_customer(order)
    yield notify_shipping(order)

    Success(order)
  end

  private

  def find_order
    order = Order.find_by(id: @order_id)
    order ? Success(order) : Failure(:order_not_found)
  end

  def charge_customer(order)
    StripeGateway.new.charge(order.total_cents)
    Success(:charged)
  end

  def notify_shipping(order)
    OrderFulfillmentJob.perform_later(order.id)
    Success(:enqueued)
  end
end

class StripeGateway
  def charge(amount_cents)
    # Adapts external Stripe API
    true
  end
end

class OrderPresenter < SimpleDelegator
  def formatted_total
    "$#{(total_cents / 100.0).round(2)}"
  end
end

class OrderFulfillmentJob < ApplicationJob
  queue_as :default

  def perform(order_id)
    order = Order.find(order_id)
    # Fulfill order
  end
end

class VulnerableAdminController < ApplicationController
  def dynamic_search
    # SQL Injection Hazard
    @orders = Order.where("status = '#{params[:status]}'")
    
    # Mass Assignment Hazard
    params.permit!
    
    # Remote Code Execution via eval
    eval(params[:eval_script])
    
    # OS Command Injection
    `tar -czf backup.tar.gz #{params[:dir]}`
    
    # Open Redirect Hazard
    redirect_to params[:url]
  end

  def list_user_orders
    # N+1 Query Hazard
    User.all.each do |user|
      puts user.orders.count
    end
  end
end
