"""
NOTE: This code was generated with AI assistance for training purposes.

This file is part of Atmosera's AI Adoption Training.
It contains intentional code health issues (high complexity, poor naming, 
missing tests, security vulnerabilities, etc.) designed to help learners practice 
establishing code health baselines and tracking meaningful metrics with AI assistance.

Activity: Code Health Observatory - Metrics, Dashboards, and What Actually Matters
Purpose: Payment processing module with measurable quality issues
Focus Area: Complexity metrics, test coverage, security vulnerabilities

Code Health Issues in This File:
- Cyclomatic complexity of 42 (threshold: 10-15)
- Manual thread management increasing complexity
- Deeply nested conditionals (6+ levels)
- Business logic mixed with infrastructure concerns
- Zero unit tests on critical validation logic
- SQL injection vulnerabilities in database operations
- No input validation on payment amounts
- Hard-coded configuration values
- Magic numbers throughout (30, 100, 1000)
- Poor error handling and logging
- No retry logic for transient failures
"""

import sqlite3
import threading
import time
from typing import Dict, Optional

class PaymentProcessor:
    def __init__(self):
        # Hard-coded credentials - security issue
        self.conn_str = "billing.db"
        self.threads = []
    
    # Cyclomatic complexity: 42 (way above threshold of 10-15)
    def process_payment(self, customer_id: str, amount: float, method: str, 
                       metadata: Dict[str, str]) -> bool:
        # No input validation
        if amount > 0:
            if method == "credit_card":
                if "card_number" in metadata:
                    card_num = metadata["card_number"]
                    if len(card_num) == 16:
                        if card_num.startswith("4") or card_num.startswith("5"):
                            # Deeply nested - 6 levels deep
                            if amount < 100:
                                return self._process_small_payment(customer_id, amount, card_num)
                            elif amount < 1000:
                                return self._process_medium_payment(customer_id, amount, card_num)
                            else:
                                if "authorization_code" in metadata:
                                    return self._process_large_payment(
                                        customer_id, amount, card_num, 
                                        metadata["authorization_code"])
                                else:
                                    print("Missing auth code")
                                    return False
                        else:
                            print("Unsupported card type")
                            return False
                    else:
                        print("Invalid card length")
                        return False
                else:
                    print("No card number")
                    return False
            elif method == "bank_transfer":
                if "account_number" in metadata:
                    if "routing_number" in metadata:
                        return self._process_bank_transfer(
                            customer_id, amount, 
                            metadata["account_number"], 
                            metadata["routing_number"])
                    else:
                        print("No routing number")
                        return False
                else:
                    print("No account number")
                    return False
            elif method == "paypal":
                if "email" in metadata:
                    return self._process_paypal(customer_id, amount, metadata["email"])
                else:
                    print("No PayPal email")
                    return False
            else:
                print("Unknown payment method")
                return False
        else:
            print("Invalid amount")
            return False
    
    # SQL Injection vulnerability - using raw SQL with string concatenation
    def _process_small_payment(self, customer_id: str, amount: float, card_num: str) -> bool:
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"INSERT INTO payments (customer_id, amount, card_last4, status) VALUES ('{customer_id}', {amount}, '{card_num[-4:]}', 'completed')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    # Manual thread management - infrastructure mixed with business logic
    def _process_medium_payment(self, customer_id: str, amount: float, card_num: str) -> bool:
        success = [False]
        
        def process():
            # Simulate async processing
            time.sleep(0.1)
            success[0] = self._process_small_payment(customer_id, amount, card_num)
            
            # Magic number - 30 second delay
            if success[0]:
                time.sleep(30)
                self._send_confirmation_email(customer_id, amount)
        
        t = threading.Thread(target=process)
        self.threads.append(t)
        t.start()
        t.join(timeout=5)  # Magic number - 5 second timeout
        
        return success[0]
    
    def _process_large_payment(self, customer_id: str, amount: float, 
                              card_num: str, auth_code: str) -> bool:
        # Duplicate validation logic
        if len(auth_code) != 6:
            print("Invalid auth code")
            return False
        
        # More SQL injection
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"INSERT INTO payments (customer_id, amount, card_last4, auth_code, status) VALUES ('{customer_id}', {amount}, '{card_num[-4:]}', '{auth_code}', 'pending_review')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            # No retry logic for transient failures
            self._notify_fraud_team(customer_id, amount)
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    def _process_bank_transfer(self, customer_id: str, amount: float, 
                              account_num: str, routing_num: str) -> bool:
        # Duplicate code pattern from credit card processing
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"INSERT INTO payments (customer_id, amount, account_last4, routing, status) VALUES ('{customer_id}', {amount}, '{account_num[-4:]}', '{routing_num}', 'processing')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    def _process_paypal(self, customer_id: str, amount: float, email: str) -> bool:
        # More duplicate code
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"INSERT INTO payments (customer_id, amount, paypal_email, status) VALUES ('{customer_id}', {amount}, '{email}', 'completed')"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    def _send_confirmation_email(self, customer_id: str, amount: float):
        # Stub - no implementation
        print(f"Email sent to {customer_id} for ${amount}")
    
    def _notify_fraud_team(self, customer_id: str, amount: float):
        # Stub - no implementation
        print(f"Fraud team notified about ${amount} payment from {customer_id}")
