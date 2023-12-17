# Senior Project Management System Proposal
### Introduction
The Senior Project Management System is designed to facilitate the administrative process involved in managing senior projects at our institution. This system engages three types of users: Students, Faculty, and Admin. Each user type has specific roles and responsibilities within the system.

## User Roles
### 1. Student
**Actions**
- Create Project: Students can create a new project and become the lead.
- Send Member Requests: Students can send requests to other students to become members of their project.
- Send Advisor Requests: Students can send requests to faculty members to become the advisor of their project.
- See Pending Requests: Students can view pending requests to join their projects.
```python
class Student:
    def create_project(self, title):
        pass

    def send_member_request(self, project_id, to_be_member):
        pass

    def send_advisor_request(self, project_id, to_be_advisor):
        pass

    def see_pending_requests(self, project_id):
        pass
```

### 2. Faculty
**Actions**
- View Projects: Faculty members can view the projects available for supervision.
- Accept/Reject Member Requests: Faculty members can accept or reject requests from students to become members of a project.
- Accept/Reject Advisor Requests: Faculty members can accept or reject requests from students to become advisors of a project.

### 3. Admin
**Actions**
- Manage Users: Admins can add, modify, or delete user accounts.
- View Project Status: Admins can view the status of all projects in the system.
- Generate Reports: Admins can generate reports on project and user statistics.