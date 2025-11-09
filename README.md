Everything done till now:
1. Installed Postgresql - psql, pgadmin
2. Installed Fast API and uvicorn
3. Git Setup done
4. PostgreSQL setup done
5. PyJWT 
6. Passlib


### **Week One - Completed**
* Set up the FastAPI backend with basic API routes for transaction creation and retrieval.
* Configured PostgreSQL and created a fraud_detection_db with tables for users and transactions.
* Implemented SQLAlchemy ORM to map database models (User, Transaction) to the database.
* Added a POST /transactions/ route to create new transactions and a GET /transactions/ route to retrieve all transactions.
* Configured Git for version control and pushed the initial commit to the GitHub repository.

### **Week Two - In Progress**
#### JWT Authentication:
* Added user registration and login routes to issue JWT tokens after successful user credentials validation.
* Implemented password hashing using bcrypt via Passlib before storing passwords securely in the database.

#### Role-Based Access Control (RBAC):
* Introduced roles (admin, fraud analyst, user) in the User model to manage access permissions.
* Secured routes like /fraud_alert/ to ensure only admins can access them, with a 403 Forbidden response for non-admin users.

#### User Model Updates:
* Added role column in the User model to manage user roles and their access levels in the system.

#### Testing:
* Verified user registration, login, JWT token issuance, and role-based route access using Swagger UI and Postman.