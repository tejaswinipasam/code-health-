"""
NOTE: This code was generated with AI assistance for training purposes.

This file is part of Atmosera's AI Adoption Training.
It contains intentional code health issues (security vulnerabilities, missing tests,
poor error handling, etc.) designed to help learners practice establishing code health 
baselines and identifying critical issues with AI assistance.

Activity: Code Health Observatory - Metrics, Dashboards, and What Actually Matters
Purpose: Data access layer with critical security vulnerabilities
Focus Area: Security vulnerabilities, SQL injection risks, missing tests

Code Health Issues in This File:
- Multiple SQL injection vulnerabilities (raw SQL with string concatenation)
- No parameterized queries
- Hard-coded database credentials
- Zero unit tests for data access logic
- No connection pooling or resource management
- Missing error handling for database failures
- No logging of database operations
- Direct exposure of database exceptions
- No transaction management
- Missing validation on all inputs
- Code duplication across CRUD operations
"""

import sqlite3
from typing import Dict, List, Optional

class InvoiceDAO:
    def __init__(self):
        # Hard-coded credentials - security issue
        self.conn_str = "billing.db"
    
    # SQL Injection vulnerability - no parameterized query
    def get_invoice(self, invoice_id: str) -> Optional[Dict]:
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"SELECT * FROM invoices WHERE invoice_id = '{invoice_id}'"
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row:
                invoice = {
                    "invoice_id": row[0],
                    "customer_id": row[1],
                    "amount": row[2],
                    "status": row[3],
                    "created_date": row[4]
                }
                conn.close()
                return invoice
            
            conn.close()
        except Exception as ex:
            # Poor error handling - exposing internal details
            raise Exception(f"Database error: {ex}")
        
        return None
    
    # More SQL injection vulnerabilities
    def get_invoices_by_customer(self, customer_id: str) -> List[Dict]:
        invoices = []
        
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"SELECT * FROM invoices WHERE customer_id = '{customer_id}' ORDER BY created_date DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                invoice = {
                    "invoice_id": row[0],
                    "customer_id": row[1],
                    "amount": row[2],
                    "status": row[3],
                    "created_date": row[4]
                }
                invoices.append(invoice)
            
            conn.close()
        except Exception as ex:
            raise Exception(f"Database error: {ex}")
        
        return invoices
    
    # No input validation
    def create_invoice(self, customer_id: str, amount: float, status: str) -> bool:
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"INSERT INTO invoices (customer_id, amount, status, created_date) VALUES ('{customer_id}', {amount}, '{status}', datetime('now'))"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    # Duplicate code pattern
    def update_invoice_status(self, invoice_id: str, new_status: str) -> bool:
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"UPDATE invoices SET status = '{new_status}' WHERE invoice_id = '{invoice_id}'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    # No transaction management for financial operations
    def delete_invoice(self, invoice_id: str) -> bool:
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: SQL Injection vulnerability
            sql = f"DELETE FROM invoices WHERE invoice_id = '{invoice_id}'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    # Complex query with multiple vulnerabilities
    def search_invoices(self, customer_name: str, status: str, 
                       min_amount: float, max_amount: float) -> List[Dict]:
        invoices = []
        
        try:
            conn = sqlite3.connect(self.conn_str)
            cursor = conn.cursor()
            
            # CRITICAL: Multiple SQL Injection vulnerabilities
            sql = f"""SELECT i.*, c.name FROM invoices i 
                     JOIN customers c ON i.customer_id = c.customer_id 
                     WHERE c.name LIKE '%{customer_name}%' 
                     AND i.status = '{status}' 
                     AND i.amount >= {min_amount} 
                     AND i.amount <= {max_amount}"""
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                invoice = {
                    "invoice_id": row[0],
                    "customer_id": row[1],
                    "customer_name": row[5],
                    "amount": row[2],
                    "status": row[3]
                }
                invoices.append(invoice)
            
            conn.close()
        except Exception as ex:
            raise Exception(f"Database error: {ex}")
        
        return invoices
