"""
NOTE: This code was generated with AI assistance for training purposes.

This file is part of Atmosera's AI Adoption Training.
It contains intentional code health issues (zero test coverage, missing validation,
poor error handling, etc.) designed to help learners practice establishing code health 
baselines and identifying critical testing gaps with AI assistance.

Activity: Code Health Observatory - Metrics, Dashboards, and What Actually Matters
Purpose: Customer service layer with critical testing gaps
Focus Area: Test coverage gaps, missing validation, error handling

Code Health Issues in This File:
- Zero unit tests on critical validation logic (0% coverage)
- No input validation on customer data
- Missing error handling for null/invalid inputs
- No validation of email format
- No validation of phone number format
- No boundary checks on age/credit limits
- Direct exposure of internal exceptions
- No logging of customer operations
- Magic numbers for credit limits (5000, 10000)
- Duplicate validation logic across methods
- No data sanitization before storage
- Missing business rule validations
"""

from datetime import datetime
from typing import Dict, Optional
from invoice_dao import InvoiceDAO
import re

class CustomerServlet:
    def __init__(self):
        self.invoice_dao = InvoiceDAO()
        self.customers = {}
    
    # CRITICAL: Zero tests on this validation logic
    def create_customer(self, customer_id: str, name: str, email: str, 
                       phone: str, age: int, credit_limit: float) -> bool:
        # No input validation at all
        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "phone": phone,
            "age": age,
            "credit_limit": credit_limit,
            "status": "active",
            "created_date": datetime.now()
        }
        
        self.customers[customer_id] = customer
        return True
    
    # No validation of email format
    def update_email(self, customer_id: str, new_email: str) -> bool:
        if customer_id in self.customers:
            self.customers[customer_id]["email"] = new_email
            return True
        return False
    
    # No boundary checks on credit limit
    def update_credit_limit(self, customer_id: str, new_limit: float) -> bool:
        if customer_id in self.customers:
            # Magic numbers - what's the business rule?
            if new_limit > 0:
                self.customers[customer_id]["credit_limit"] = new_limit
                return True
        return False
    
    # CRITICAL: Complex business logic with zero tests
    def approve_credit_increase(self, customer_id: str, requested_increase: float) -> bool:
        if customer_id not in self.customers:
            return False
        
        customer = self.customers[customer_id]
        current_limit = customer["credit_limit"]
        age = customer["age"]
        
        # Complex business rules with no tests
        if age < 18:
            return False  # Minors cannot get credit increases
        
        if requested_increase > 5000:
            # Large increases require manual approval
            return False
        
        if current_limit + requested_increase > 10000:
            # Total limit cannot exceed $10,000
            return False
        
        # Check payment history
        invoices = self.invoice_dao.get_invoices_by_customer(customer_id)
        late_payments = 0
        for invoice in invoices:
            if invoice["status"] == "late":
                late_payments += 1
        
        if late_payments > 2:
            # Too many late payments
            return False
        
        # Approve the increase
        customer["credit_limit"] = current_limit + requested_increase
        return True
    
    # Missing validation on phone format
    def update_phone(self, customer_id: str, new_phone: str) -> bool:
        if customer_id in self.customers:
            self.customers[customer_id]["phone"] = new_phone
            return True
        return False
    
    # No error handling for missing customer
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        return self.customers.get(customer_id)  # Will return None if customer doesn't exist
    
    # CRITICAL: Account closure logic with zero tests
    def close_account(self, customer_id: str, reason: str) -> bool:
        if customer_id not in self.customers:
            return False
        
        customer = self.customers[customer_id]
        
        # Check for outstanding invoices
        invoices = self.invoice_dao.get_invoices_by_customer(customer_id)
        total_outstanding = 0
        
        for invoice in invoices:
            status = invoice["status"]
            if status == "pending" or status == "late":
                total_outstanding += invoice["amount"]
        
        if total_outstanding > 0:
            # Cannot close account with outstanding balance
            return False
        
        # Close the account
        customer["status"] = "closed"
        customer["closed_date"] = datetime.now()
        customer["close_reason"] = reason
        
        return True
    
    # Duplicate validation logic - should be extracted
    def validate_customer_data(self, name: str, email: str, phone: str, age: int) -> bool:
        if not name or len(name) == 0:
            return False
        
        if not email or len(email) == 0:
            return False
        
        if not phone or len(phone) == 0:
            return False
        
        if age < 0 or age > 150:
            return False
        
        return True
    
    # No tests for this calculation logic
    def calculate_available_credit(self, customer_id: str) -> float:
        if customer_id not in self.customers:
            return 0
        
        customer = self.customers[customer_id]
        credit_limit = customer["credit_limit"]
        
        invoices = self.invoice_dao.get_invoices_by_customer(customer_id)
        total_used = 0
        
        for invoice in invoices:
            status = invoice["status"]
            if status != "paid" and status != "cancelled":
                total_used += invoice["amount"]
        
        return credit_limit - total_used
