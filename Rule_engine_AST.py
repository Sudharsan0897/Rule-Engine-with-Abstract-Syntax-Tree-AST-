#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, jsonify, request, render_template
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import Counter


# In[2]:


app = Flask(__name__)  # Initialize the Flask app


# In[3]:


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:13209988!@localhost:3306/rules_db'


# In[4]:


db = SQLAlchemy(app)


# In[5]:


# # Define the Rule model with additional fields and functionality
class Rule(db.Model):
    __tablename__ = 'rules'  # Explicit table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    rule_string = db.Column(db.String(255), nullable=False)  # Rule string with length limit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when rule is created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp when rule is updated


# In[6]:


def __repr__(self):
    return f'<Rule {self.rule_string}>'


# In[7]:


with app.app_context():
    db.create_all()  # This will create the 'rules' table in the database


# # Defining the Node Class

# In[8]:


class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.node_type == "operand":
            return f"Operand(value={self.value})"
        elif self.node_type == "operator":
            return f"Operator(value={self.value}, left={self.left}, right={self.right})"
        return "Node()"

    def __repr__(self):
        return self.__str__()


# # Create the `create_rule` function

# In[8]:


def create_rule(rule_string):
    # Remove spaces and define regex patterns
    rule_string = rule_string.replace(" ", "")
    operand_pattern = r"(\w+)([<>]=?|=)(\d+|'[\w\s]+')"
    
    # Tokenize the input string
    tokens = []
    index = 0

    while index < len(rule_string):
        match = re.match(operand_pattern, rule_string[index:])
        if match:
            tokens.append(('operand', match.group(0)))
            index += len(match.group(0))
        elif rule_string.startswith(('AND', 'OR'), index):
            tokens.append(('operator', rule_string[index:index + 3]))
            index += 3
        elif rule_string[index] in '()':
            tokens.append(('parenthesis', rule_string[index]))
            index += 1
        else:
            index += 1  # Skip unrecognized characters

    # Build the AST from tokens
    def parse(tokens):
        current_node, last_operator = None, None
        
        for token_type, token_value in tokens:
            if token_type == 'parenthesis':
                if token_value == '(':
                    sub_node, sub_index = parse(tokens)
                    current_node = sub_node if current_node is None else Node("operator", left=current_node, right=sub_node, value=last_operator)
                continue  # Handle closing parenthesis implicitly
            elif token_type == 'operand':
                node = Node("operand", value=token_value)
                current_node = node if current_node is None else Node("operator", left=current_node, right=node, value=last_operator)
            elif token_type == 'operator':
                last_operator = token_value

        return current_node

    return parse(tokens)


# # Create the `evaluate_rule` function

# In[9]:


def evaluate_rule(node, data):
    def get_value(value):
        """Convert the right operand to the correct type."""
        if value.startswith("'") and value.endswith("'"):
            return value.strip("'")  # Return string without quotes
        return int(value)  # Convert to int for numerical comparison

    if node.node_type == "operand":
        # Parse operand condition (e.g., age > 30)
        match = re.match(r"(\w+)([<>]=?|=)(\d+|'[\w\s]+')", node.value)
        if not match:
            return False  # If parsing fails, return False

        left, operator, right = match.groups()
        left_value = data.get(left)

        if left_value is None:
            return False  # If left_value is not present in data, return False

        # Ensure left_value is treated as int if it should be
        if isinstance(left_value, str) and left_value.isdigit():
            left_value = int(left_value)

        right_value = get_value(right)  # Convert right_value using helper function

        # Comparison logic
        comparisons = {
            '=': lambda a, b: a == b,
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
        }

        return comparisons[operator](left_value, right_value)

    elif node.node_type == "operator":
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        return left_result and right_result if node.value == "AND" else left_result or right_result

    return False


# # Create the `combine_rules` function

# In[10]:


def combine_rules(rules):
    combined_nodes = [create_rule(rule) for rule in rules]

    if not combined_nodes:
        return None

    # Create a combined AST using OR as the operator
    root = Node("operator", left=combined_nodes[0], right=combined_nodes[1], value="OR")
    return root


# In[ ]:


# Define the API endpoint for evaluating rules
@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate_api():
    data = request.json
    user_data = data.get('user_data')
    rule_strings = [rule.rule_string for rule in Rule.query.all()]
    combined_ast = combine_rules(rule_strings)
    is_eligible = evaluate_rule(combined_ast, user_data)
    return jsonify({'is_eligible': is_eligible})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

