#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, jsonify, request
from Rule_engine_AST import db, Rule, Node, create_rule, evaluate_rule,combine_rules
import re


# In[3]:


app = Flask(__name__)  # Initialize the Flask app


# In[ ]:


# Sample rules
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Create individual rules
ast1 = create_rule(rule1)
ast2 = create_rule(rule2)

# Combine rules
combined_ast = combine_rules([rule1, rule2])

# Sample data for evaluation
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

# Evaluate rules
print("AST 1 Evaluation:", evaluate_rule(ast1, data))  # Should return True/False based on the data
print("AST 2 Evaluation:", evaluate_rule(ast2, data))  # Should return True/False based on the data
print("Combined AST Evaluation:", evaluate_rule(combined_ast, data))  # Should return True/False based on the combined logic

