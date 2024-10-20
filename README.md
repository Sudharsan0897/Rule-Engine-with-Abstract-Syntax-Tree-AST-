# Rule-Engine-with-Abstract-Syntax-Tree
### Overview
The Rule Engine is a web application designed to evaluate user eligibility based on various attributes such as age, department, income, and experience. Utilizing Abstract Syntax Trees (AST), the engine dynamically creates, combines, and modifies conditional rules. This application features a simple user interface, a RESTful API for interaction, and a backend powered by a SQL database for data storage.

### Objective
The primary objective of this project is to provide a robust and flexible rule evaluation system that allows users to define complex rules in a natural language format. The application supports the creation of individual rules, the combination of rules into a comprehensive evaluation criteria, and the evaluation of these rules against user data.

### Features
Dynamic Rule Creation: Users can create rules using a straightforward string format that describes conditions.
Rule Combination: The engine can combine multiple rules into a single evaluation criteria using logical operators.
Real-Time Evaluation: The rules can be evaluated against user data to determine eligibility.
Database Integration: A MySQL database is used to store rules and their metadata, ensuring persistence and easy retrieval.
Error Handling: The application includes mechanisms for handling invalid rule strings and data formats.
Architecture
The application follows a 3-tier architecture comprising:

#### Presentation Layer: A simple user interface for rule creation and evaluation.
API Layer: RESTful APIs to handle rule management (create, delete, evaluate) and interaction with the frontend.
Data Layer: SQL database for storing rules and metadata.
Data Structure
The core data structure for the AST is defined as follows:

#### Node Class: Represents each node in the AST with the following attributes:
node_type: Indicates if the node is an "operator" (AND/OR) or an "operand" (conditions).
left: Reference to the left child node.
right: Reference to the right child node.
value: Optional value for operand nodes (e.g., comparison values).
API Endpoints

1. Create Rule
POST /api/rules

### Creates a new rule in the database.

#### Request Body:
`{
    "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))"
}`

2. Delete Rule
DELETE /api/rules/<rule_id>
Deletes a specified rule from the database.

3. Evaluate Rules
POST /api/rules/evaluate
Evaluates the combined rules against user data.

#### Request Body:
`{
    "user_data": {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
}`
Sample Rules
Rule 1:
`((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)`

Rule 2:
`((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)`

### Setup Instructions
Clone the Repository:
git clone <github.com/Sudharsan0897>

#### Install Dependencies:
pip install -r requirements.txt

#### Configure Database:
Update the database URI in the code to connect to your MySQL database.

#### Run Migrations: Ensure the database schema is created.
with app.app_context():
    db.create_all()
    
#### Start the Application:
python main.py

### Conclusion
The Rule Engine application serves as a powerful tool for dynamically evaluating user eligibility based on complex, user-defined rules. By leveraging Abstract Syntax Trees (AST), it allows for intuitive rule creation and evaluation, making it suitable for various applications where eligibility criteria need to be established.

The project's architecture separates concerns into three distinct layers—presentation, API, and data—ensuring a clean and maintainable codebase. With features such as dynamic rule management, real-time evaluation, and robust error handling, the Rule Engine is designed to be both flexible and reliable.

This application provides a strong foundation for future enhancements, including user-defined functions and more sophisticated validation mechanisms. By continuing to expand its capabilities, the Rule Engine can adapt to increasingly complex business requirements and offer users a powerful solution for decision-making processes.

