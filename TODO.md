# Senior Project Management System Proposal

## Introduction
The Senior Project Management System is designed to facilitate the administrative process involved in managing senior projects at our institution. This system engages three types of users: Students, Faculty, and Admin. Each user type has specific roles and responsibilities within the system.

## User Roles

### 1. Admin
**Class Purpose:**
- The `Admin` class represents an administrative user responsible for managing user accounts in the system.

**Class Responsibilities:**
- Inserting new users into the system with proper validation for ID, name, and user type.
- Managing the system's user database by adding, modifying, or deleting user accounts.

**Class Methods:**
```python
class Admin:
   def insert_person(self):  # Inserts a new person into the system with proper validation for user input.
       pass
```

### 2. Student
**Class Purpose:**
- The `Student` class represents a student user in the system.

**Class Responsibilities:**
- Creating a new project as a lead.
- Viewing and managing pending requests.

**Class Methods:**
```python
class Student:
   def create_project(self, title):  # Creates a new project and becomes the lead.
       pass

   def view_request(self):  # Views and manages pending requests for the student's project.
       pass
```


### 3. Lead
**Class Purpose:**
- The `Lead` class represents a student who is the lead of a project.

**Class Responsibilities:**
- Inviting members and advisors to join the project.
- Updating project details.

**Class Methods:**
```python
class Lead:
   def invite_member(self):  # Invites a student to join the project as a member.
       pass

   def invite_advisor(self):  # Invites a faculty member to join the project as an advisor.
       pass

   def update(self, column, data):  # Updates project details such as title or status.
       pass
```

### 4. Member
**Class Purpose:**
- The `Member` class represents a student who is a member of a project.

**Class Responsibilities:**
- Viewing project details.
- Evaluating projects as a member.

**Class Methods:**
```python
class Advisor:
   def view_project(self):  # Views details of the project the member is part of.
       pass

   def evaluate_project(self):  # Reviews a project as a member.
       pass

   def update(self, column, data):  # Updates project status.
       pass
```

### 5. Faculty
**Class Purpose:**
- The `Faculty` class represents a faculty user in the system.

**Class Responsibilities:**
- Viewing and managing invitations.
- Evaluating projects as a faculty member.

**Class Methods:**
```python
class Faculty:
   def view_request(self):  # Views and manages invitations for faculty.
       pass

   def evaluate_project(self):  # Evaluates a project as a faculty member.
       pass
```

### 6. Advisor
**Class Purpose:**
- The `Advisor` class represents a faculty member who is an advisor for a project.

**Class Responsibilities:**
- Reviewing and evaluating projects.

**Class Methods:**
```python
class Advisor:
   def review_project(self):  # Reviews a project as an advisor.
       pass

   def evaluate_project(self):  # Reviews a project as an advisor.
       pass

   def update(self, column, data):  # Updates project status.
       pass
```