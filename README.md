# Final project for 2023's 219114/115 Programming I

## Project Structure

### Files

1. `project_manage.py`: Contains the main execution code for the project.
2. `database.py`: Defines the `Database` class for handling data storage and retrieval.
3. csv files: `persons.csv`, `login.csv`, `project.csv`, `invitation.csv` - CSV files for storing person, login, project, and invitation data.

### Classes

- `Person`: Represents a person with common attributes like `person_id`, `first_name`, and `last_name`.
- `Admin`: Inherits from `Person` and includes admin-specific functionality.
- `Student`: Inherits from `Person` and includes student-specific functionality.
- `Lead`, `Member`, `Faculty`, `Advisor`: Inherited classes from `Person` with specific roles and functionalities.
- `Project`: Represents a project with methods for updating and evaluating projects.

## Compilation and Execution

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Run the code using a Python interpreter: `python main.py`

## Roles and Actions

| Role     | Action                                | Classes             | Methods                              | Completion (%) |
|----------|---------------------------------------|---------------------|--------------------------------------|-----------------|
| Admin    | Insert a new person                   | `Admin`             | `insert_person`                      | 100             |
| Admin    | Change password for a person          | `login_table`       | `update`                             | 100             |
| Student  | Create a new project                  | `Student`           | `create_project`                     | 100             |
| Student  | View project invitations              | `Student`           | `view_request`                       | 100             |
| Student  | Receive notifications for requests   | `Student`           | `view_request` + Notification feature| 70              |
| Lead     | Invite members to the project         | `Lead`              | `invite_member`                      | 100             |
| Lead     | Invite an advisor to the project      | `Lead`              | `invite_advisor`                     | 100             |
| Lead     | Update project information            | `Lead`              | `update`                             | 90             |
| Lead     | Evaluate the project as the lead       | `Project`           | `evaluate_project`                   | 70             |
| Member   | View project details                  | `Member`            | `__str__` + `Project.__str__`        | 100             |
| Member   | Evaluate the project as a member      | `Project`           | `evaluate_project`                   | 70             |
| Faculty  | View invitations to be an advisor     | `Faculty`           | `view_request`                      | 100             |
| Faculty  | Evaluate projects as faculty          | `Faculty`           | `evaluate`                           | 70             |
| Advisor  | Review projects                       | `Advisor`           | `__str__` + `Project.__str__`        | 100             |
| Advisor  | Evaluate projects as an advisor       | `Advisor`           | `evaluate` + `invite_faculty`        | 70             |


## Missing Features and Bugs

- **Missing Features:**
  - Handling project submission for review.
  - Handling project submission for evaluation.
  - Notification for pending requests and evaluation requests.
- **Bugs:**
  - Some input might cause errors.
  - Cannot handle data type mismatches in the table during the evaluation step.