from database import Database, Table
import random

class Person:
    def __init__(self, person_id, first_name, last_name):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"Welcome, {self.first_name} {self.last_name}"


class Admin(Person):
    def __init__(self, person_id, first_name, last_name):
        super().__init__(person_id, first_name, last_name)

    def __str__(self):
        return f"Admin: {super().__str__()}"
    
    def insert_person(self):
        while True:
            try:
                person_id = int(input("Input ID (7-digit integer): "))
                if not (1000000 <= person_id <= 9999999):
                    raise ValueError("ID must be a 7-digit integer.")
                
                first = input("Input first name: ").capitalize()
                if not first.isalpha():
                    raise ValueError("First name must be a string.")
                
                last = input("Input last name: ").capitalize()
                if not last.isalpha():
                    raise ValueError("Last name must be a string.")
                
                type = input("Input type (student or faculty): ").lower()
                if type not in ('student', 'faculty'):
                    raise ValueError("Type must be 'student' or 'faculty'.")
                
                data = {'ID': person_id, 'first': first, 'last': last, 'type': type}
                person_table.insert(data)
                
                print("Person inserted successfully!")
                break
            except ValueError as e:
                print(f"Invalid input: {e}")


class Student(Person):
    def __init__(self, person_id, first_name, last_name):
        super().__init__(person_id, first_name, last_name)

    def __str__(self):
        return f"Student: {super().__str__()}"

    def create_project(self, title):
        project_id = len(project_table.table_data) + 1
        members = ['None', 'None']
        advisor = 'None'
        status = "Created"
        data = {'ProjectID': project_id, 'Title': title, 'Lead': self.person_id, 'Member1': members[0],
                'Member2': members[1], 'Advisor': advisor, 'Status': status, 'Evaluate': "lead|member|member|advisor|faculty|faculty|faculty"}
        project_table.insert(data)
        print(f'Project with title: {title} created, ProjectID: {project_id}')

    def view_request(self):
        while True:
            if invitation_table.filter(lambda row: row['ID'] == self.person_id) is None:
                print("No invitations were dispatched.")
                return 'student'

            request_info = invitation_table.filter(lambda row: row['ID'] == self.person_id)
            for row in request_info.table_data:
                print(f"ProjectID: {row['ProjectID']}, Title: {row['Title']} have invited you to be a member")

            while True:
                accept = input("Do you want to accept member request? (y/n): ").lower()
                if accept in ('y', 'n'):
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if accept == "y" and len(request_info.table_data) >= 1:
                while True:
                    project_id = str(input("Which project id do you want to join?: "))
                    if project_id in [row['ProjectID'] for row in request_info.table_data]:
                        break
                    else:
                        print("Invalid project ID. Please enter a valid project ID.")

                project_info = project_table.filter(lambda row: row['ProjectID'] == project_id).table_data[0]
                if invitation_table.filter(lambda row: row['ID'] == self.person_id and row['ProjectID'] != project_id) != None:
                    reject_table = invitation_table.filter(lambda row: row['ID'] == self.person_id and row['ProjectID'] != project_id)
                else:
                    reject_table = 0

                if project_info['Member1'] == "Invited" or project_info['Member1'] == "Reject":
                    update_data = {'Member1': self.person_id}
                    Project.update_project(update_data, project_id)
                    if reject_table != 0:
                        for project_row in reject_table.table_data:
                            Project.update_project({'Member1': 'Reject'}, project_row['ProjectID'])
                elif project_info['Member2'] == "Invited" or project_info['Member2'] == "Reject":
                    update_data = {'Member2': self.person_id}
                    Project.update_project(update_data, project_id)
                    if reject_table != 0:
                        for project_row in reject_table.table_data:
                            Project.update_project({'Member2': 'Reject'}, project_row['ProjectID'])
                
                # Check if both members have accepted before deleting other invitations
                student_ids_table = [row['ID'] for row in person_table.select(['ID']).table_data]
                if project_info['Member1'] in student_ids_table and project_info['Member2'] in student_ids_table:
                    invitation_table.delete(lambda row: row['ProjectID'] == project_id and row['type'] == 'member')
                
                # Update the role in login_table
                login_table.update({'role': 'member'}, {'ID': self.person_id})

                invitation_table.delete(lambda row: row['ID'] == self.person_id)
                return 'member'

            elif accept == "n" and invitation_table.filter(lambda row: row['ID'] == self.person_id) != None:
                project_id = [row['ProjectID'] for row in invitation_table.filter(lambda row: row['ID'] == self.person_id).table_data]
                for id in project_id:
                    project = project_table.filter(lambda row: row['ProjectID'] == id).table_data[0]
                    if project['Member1'] == "Invited" or project['Member1'] == "Reject":
                        update_data = {'Member1': 'Reject'}
                        Project.update_project(update_data, id)
                    elif project['Member2'] == "Invited" or project['Member2'] == "Reject":
                        update_data = {'Member2': 'Reject'}
                        Project.update_project(update_data, id)
                
                invitation_table.delete(lambda row: row['ID'] == self.person_id)
                return 'student'
            break


class Lead(Person):
    def __init__(self, person_id, first_name, last_name, project_id, title):
        super().__init__(person_id, first_name, last_name)
        self.project_id = project_id
        self.title = title

    def __str__(self):
        return f"Lead: {super().__str__()}"
    
    def update(self, column, data):
        update_data = {column: data}
        Project.update_project(update_data, self.project_id)

    def invite_member(self):
        while True:
            student_id = input('Invite member ID: ')
            student_data = person_table.filter(lambda row: row['ID'] == student_id and row['type'] == 'student')

            if student_id is not None:
                if student_data:
                    student_data = student_data.table_data[0]
                    data = {'ID': student_id, 'type': 'member', 'ProjectID': self.project_id, 'Title': self.title, 'Lead': self.person_id}
                    invitation_table.insert(data)
                    print(f"Invitation sent to {student_data['first']} {student_data['last']}, ID {student_id}")
                    if project_info['Member1'] == "None":
                        Project.update_project({'Member1': 'Invited'}, self.project_id)
                    elif project_info['Member2'] == "None":
                        Project.update_project({'Member2': 'Invited'}, self.project_id)
                    break
                else:
                    print(f"Student with ID {student_id} not found.\n"
                            "Please try again.")

    def invite_advisor(self):
        while True:
            advisor_id = input('Invite advisor ID: ')
            advisor_data = person_table.filter(lambda row: row['ID'] == advisor_id and row['type'] == 'faculty')

            if advisor_id is not None:
                if advisor_data:
                    advisor_data = advisor_data.table_data[0]
                    data = {'ID': advisor_id, 'type': 'advisor', 'ProjectID': self.project_id, 'Title': self.title, 'Lead': self.person_id}
                    invitation_table.insert(data)
                    print(f"Invitation sent to {advisor_data['first']} {advisor_data['last']}, ID {advisor_id}")
                    project_table.update({'Advisor': 'Invited'}, {'ProjectID': self.project_id})
                    break
                else:
                    print(f"Advisor with ID {advisor_id} not found or is not a faculty member.\n"
                            "Please try again.")
                    
                student_ids_table = [row['ID'] for row in person_table.select(['ID']).table_data]
                if project_info['Advisor'] in student_ids_table:
                    invitation_table.delete(lambda row: row['ProjectID'] == self.project_id)


class Member(Person):
    def __init__(self, person_id, first_name, last_name, project_id, title):
        super().__init__(person_id, first_name, last_name)
        self.project_id = project_id
        self.title = title

    def __str__(self):
        return f"Member: {super().__str__()}"


class Faculty(Person):
    def __init__(self, person_id, first_name, last_name):
        super().__init__(person_id, first_name, last_name)

    def __str__(self):
        return f"Faculty: {super().__str__()}"
    
    def view_request(self):
        while True:
            if invitation_table.filter(lambda row: row['ID'] == self.person_id and row['type'] == 'advisor') is None:
                print("No invitations were dispatched.")
                return 'faculty'

            request_info = invitation_table.filter(lambda row: row['ID'] == self.person_id and row['type'] == 'advisor')
            for row in request_info.table_data:
                print(f"ProjectID: {row['ProjectID']}, Title: {row['Title']} have invited you to be an advisor")

            while True:
                accept = input("Do you want to accept member request? (y/n): ").lower()
                if accept in ('y', 'n'):
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if accept == "y" and len(request_info.table_data) >= 1:
                while True:
                    project_id = str(input("Which project id do you want to join?: "))
                    if project_id in [row['ProjectID'] for row in request_info.table_data]:
                        break
                    else:
                        print("Invalid project ID. Please enter a valid project ID.")

                project_info = project_table.filter(lambda row: row['ProjectID'] == project_id).table_data[0]
                if invitation_table.filter(lambda row: row['ID'] == self.person_id and row['ProjectID'] != project_id) != None:
                    reject_table = invitation_table.filter(lambda row: row['ID'] == self.person_id and row['ProjectID'] != project_id)
                else:
                    reject_table = 0

                if project_info['Advisor'] == "Invited" or project_info['Advisor'] == "Reject":
                    update_data = {'Advisor': self.person_id}
                    Project.update_project(update_data, project_id)
                    Project.update_project({'Status': 'Accepted'}, project_id)
                    if reject_table != 0:
                        for project_row in reject_table.table_data:
                            Project.update_project({'Advisor': 'Reject'}, project_row['ProjectID'])
                
                # Check if both members have accepted before deleting other invitations
                student_ids_table = [row['ID'] for row in person_table.select(['ID']).table_data]
                if project_info['Advisor'] in student_ids_table:
                    invitation_table.delete(lambda row: row['ProjectID'] == project_id and row['type'] == 'advisor')
                
                # Update the role in login_table
                login_table.update({'role': 'advisor'}, {'ID': self.person_id})

                invitation_table.delete(lambda row: row['ID'] == self.person_id)
                return 'advisor'

            elif accept == "n" and invitation_table.filter(lambda row: row['ID'] == self.person_id) != None:
                project_id = [row['ProjectID'] for row in invitation_table.filter(lambda row: row['ID'] == self.person_id).table_data]
                for id in project_id:
                    project = project_table.filter(lambda row: row['ProjectID'] == id).table_data[0]
                    if project['Advisor'] == "Invited" or project['Advisor'] == "Reject":
                        update_data = {'Advisor': 'Reject'}
                        Project.update_project(update_data, id)
                
                invitation_table.delete(lambda row: row['ID'] == self.person_id)
                return 'faculty'
            break

    def evaluate(self):
        while True:
            if invitation_table.filter(lambda row: row['ID'] == self.person_id) is None:
                print("No projects available for evaluation.")
                return None

            request_info = invitation_table.filter(lambda row: row['ID'] == self.person_id)
            for row in request_info.table_data:
                print(f"ProjectID: {row['ProjectID']}, Title: {row['Title']} is available for evaluation")

            while True:
                project_id = str(input("Which project id do you want to evaluate?: "))
                if project_id in [row['ProjectID'] for row in request_info.table_data]:
                    break
                else:
                    print("Invalid project ID. Please enter a valid project ID.")
            Project.evaluate_project(project_id, self.person_id)
            invitation_table.delete(lambda row: row['ID'] == self.person_id)
            print("Evaluate Complete.")
            break

class Advisor(Person):
    def __init__(self, person_id, first_name, last_name, project_id, title):
        super().__init__(person_id, first_name, last_name)
        self.project_id = project_id
        self.title = title

    def __str__(self):
        return f"Advisor: {super().__str__()}"

    def update(self, column, data):
        update_data = {column : data}
        Project.update_project(update_data, self.project_id)

    def invite_faculty(self):
        faculty_ids_table = [row['ID'] for row in (person_table.filter(lambda row: row['type'] == 'faculty' and row['ID'] != self.person_id)).select(['ID']).table_data]
        random_faculty = random.sample(faculty_ids_table, 3)
        for faculty_id in random_faculty:
            faculty_data = person_table.filter(lambda row: row['ID'] == faculty_id and row['type'] == 'faculty').table_data[0]
            data = {'ID': faculty_id, 'type': 'faculty', 'ProjectID': self.project_id, 'Title': self.title, 'Lead': self.person_id}
            invitation_table.insert(data)
            print(f"Invitation sent to {faculty_data['first']} {faculty_data['last']}, ID {faculty_id}")

    def evaluate(self):
        while True:
            if invitation_table.filter(lambda row: row['ID'] == self.person_id) is None:
                print("No projects available for evaluation.")
                return None

            request_info = invitation_table.filter(lambda row: row['ID'] == self.person_id)
            for row in request_info.table_data:
                print(f"ProjectID: {row['ProjectID']}, Title: {row['Title']} is available for evaluation")

            while True:
                project_id = str(input("Which project id do you want to evaluate?: "))
                if project_id in [row['ProjectID'] for row in request_info.table_data]:
                    break
                else:
                    print("Invalid project ID. Please enter a valid project ID.")
            Project.evaluate_project(project_id, self.person_id)
            print("Evaluate Complete.")
            break

class Project:
    def __init__(self, project_id, title, lead, members, advisor, status):
        self.project_id = project_id
        self.title = title
        self.lead = lead
        self.members = members
        self.advisor = advisor
        self.status = status

    def __str__(self):
        return f"ProjectID: {self.project_id}, Title: {self.title}, Lead: {self.lead}, " \
               f"Members: {self.members}, Advisor: {self.advisor}, Status: {self.status}"

    @staticmethod
    def update_project(data, project_id):
        update_filter = {'ProjectID': project_id}
        project_table.update(data, update_filter)

    @staticmethod
    def evaluate_project(project_id, person_id):
        project_score_list = project_table.filter(lambda row: row['ProjectID'] == 'project_id').table_data[0]
        project_score_list = project_score_list['Evaluate'].split("|")
        project_info = project_table.filter(lambda row: row['ProjectID'] == project_id).table_data[0]

        if project_info['Status'] != 'Evaluation':
            print("Project is not in the evaluation phase.")
            return
        
        person_info = person_table.filter(lambda row: row['ID'] == person_id).table_data[0]
        score = str(input("Enter score out of 100: "))

        if person_id == project_info['Lead']:
            project_score_list[0] = score
        elif person_id == project_info['Member1']:
            project_score_list[1] = score
        elif person_id == project_info['Member2']:
            project_score_list[2] = score
        elif person_id == project_info['Advisor']:
            project_score_list[3] = score
        else:
            for i in range(4, 7):
                if project_score_list[i] == 'faculty':
                    project_score_list[i] = score
                    break
        project_score_list = "|".join(project_score_list)
        Project.update_project({'Evaluate': project_score_list}, project_id)
        
        if not all(role in project_score_list for role in ['lead', 'member', 'advisor', 'faculty']):
            total_score = Project.calculate_project_score(project_id)
            Project.update_project({'Evaluate': total_score}, project_id)
            Project.update_project({'Status': 'Evaluated'}, project_id)

    @staticmethod
    def calculate_project_score(project_id):
        project_info = project_table.filter(lambda row: row['ProjectID'] == project_id).table_data[0]
        project_score_list = project_info['Evaluate']

        if None in project_score_list:
            print("Cannot calculate total score as not all slots are scored.")
            return None

        lead_score = project_score_list[0] * 0.05
        member1_score = project_score_list[1] * 0.05
        member2_score = project_score_list[2] * 0.05
        advisor_score = project_score_list[3] * 0.25
        faculty1_score = project_score_list[4] * 0.2
        faculty2_score = project_score_list[5] * 0.2
        faculty3_score = project_score_list[6] * 0.2

        total_score = lead_score + member1_score + member2_score + advisor_score + faculty1_score + faculty2_score + faculty3_score

        return total_score

####################################################################################################

db = Database()
db = db.import_csv('persons.csv')
db = db.import_csv('login.csv')
db = db.import_csv('project.csv')
db = db.import_csv('invitation.csv')

person_table = db.table("persons")
login_table = db.table("login")
project_table = db.table("project")
invitation_table = db.table("invitation")

def login():
    for _ in range(3):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if not isinstance(username, str):
            print("Username must be a string. Please try again.")
            continue
        if not (password.isdigit() and len(password) == 4):
            print("Password must be a 4-digit integer. Please try again.")
            continue
        for login_row in login_table.table_data:
            if login_row['username'] == username and login_row['password'] == password:
                person_id = login_row['ID']
                person_role = login_row['role']
                return person_id, person_role

        print("Incorrect username or password. Please try again.")
    print("Exceeded maximum attempts. Exiting program.")
    return None, None


def exit():
    db.write(person_table)
    db.write(project_table)
    db.write(login_table)
    db.write(invitation_table)

person_id, person_role = login()


while True:
    if person_id is not None:
        person_info = person_table.filter(lambda row: row['ID'] == person_id).table_data[0]

    if person_role == 'admin':
        admin = Admin(person_info['ID'], person_info['first'], person_info['last'])
        print(f'{admin}\n'
              f'1. Insert Person \n'
              f'2. Change Password \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            print("Insert Person")
            admin.insert_person()
        elif choice == 2:
            id = int(input("Input ID you want to update: "))
            new_password = int(input("Input updated password: "))
            login_table.update({'password': new_password}, {'ID': id})
        elif choice == 0:
            exit()
            break

    elif person_role == 'student':
        student = Student(person_info['ID'], person_info['first'], person_info['last'])

        print(f'{student}\n'
              f'1. Create Project \n'
              f'2. View Invitation \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            create_project_choice = input("Do you want to create a project? (y/n): ").lower()
            if create_project_choice == "y":
                project_title = input("Enter the title of the project: ")
                student.create_project(project_title)
                login_table.update({'role': 'lead'},{'ID': person_info['ID']})

                if invitation_table.filter(lambda row: row['ID'] == person_id) != None:
                    project_id = [row['ProjectID'] for row in invitation_table.filter(lambda row: row['ID'] == person_id).table_data]
                    update_data = {'Member1': person_id}
                    Project.update_project(update_data, project_id)
                    for id in project_id:
                        project_table.update({'Member1': 'Reject'}, {'ProjectID': id})
                    
                    for row in invitation_table.table_data:
                        invitation_table.delete(lambda row: row['ID'] == person_id)

            person_role = 'lead'
        elif choice == 2:
            person_role = student.view_request()
        elif choice == 0:
            exit()
            break

    elif person_role == 'lead':
        project_info = project_table.filter(lambda row: row['Lead'] == person_id).table_data[0]
        lead = Lead(person_id, person_info['first'], person_info['last'], project_info['ProjectID'],
                    project_info['Title'])
        print(f'{lead}\n'
              f'1. Invite Member \n'
              f'2. Invite Advisor \n'
              f'3. Update Project \n'
              f'4. Evaluate Project as Lead \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            lead.invite_member()
        elif choice == 2:
            student_ids_table = [row['ID'] for row in person_table.select(['ID']).table_data]
            if project_info['Member1'] not in student_ids_table and project_info['Member2'] not in student_ids_table:
                print("Before inviting an advisor, the project should have 2 members")
            else:
                lead.invite_advisor()
        elif choice == 3:
            column = input('What do you want to update (title/status): ').lower()
            if column == 'title':
                title = input('New Title: ')
                lead.update('Title', title)
            elif column == 'status':
                if project_info['Status'] == 'Accepted':
                    review_project_choice = input("Do you like to submit the project for review? (y/n): ").lower()
                    if review_project_choice == "y":
                        lead.update('Status', 'Reviewing') 
                elif project_info['Status'] == 'Approved':
                    review_project_choice = input("Do you like to submit the project for evaluation? (y/n): ").lower()
                    if review_project_choice == "y":
                        lead.update('Status', 'Evaluate Request')
        elif choice == 4:
            Project.evaluate_project(project_info['ProjectID'], person_id)
        elif choice == 0:
            exit()
            break

    elif person_role == 'member':
        project_info = project_table.filter(lambda row: row['Member1'] == person_id or row['Member2'] == person_id).table_data[0]
        member = Member(person_info['ID'], person_info['first'], person_info['last'], project_info['ProjectID'],
                    project_info['Title'])
        print(f'{member}\n'
              f'1. View Project \n'
              f'2. Evaluate Project as Member \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            print(f"ProjectID: {project_info['ProjectID']}, Title: {project_info['Title']}, Status: {project_info['Status']}, Evaluate: {project_info['Evaluate']}")
        elif choice == 2:
            Project.evaluate_project(project_info['ProjectID'], person_id)
        elif choice == 0:
            exit()
            break

    elif person_role == 'faculty':
        faculty = Faculty(person_info['ID'], person_info['first'], person_info['last'])
        print(f'{faculty}\n'
              f'1. View Invitation \n'
              f'2. Evaluate Project as Faculty \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            faculty.view_request()
        elif choice == 2:
            faculty.evaluate()
        elif choice == 0:
            exit()
            break

    elif person_role == 'advisor':
        project_info = project_table.filter(lambda row: row['Advisor'] == person_id).table_data[0]
        advisor = Advisor(person_info['ID'], person_info['first'], person_info['last'], project_info['ProjectID'],
                    project_info['Title'])
        print(f'{advisor}\n'
              f'1. Review Project \n'
              f'2. Evaluate Project as Advisor \n'
              f'3. Evaluate Project as Faculty \n'
              f'0. Exit')
        choice = int(input('choice: '))
        if choice == 1:
            print(f"ProjectID: {project_info['ProjectID']}, Title: {project_info['Title']}, Status: {project_info['Status']}, Evaluate: {project_info['Evaluate']}")
            if project_info['Status'] == 'Reviewing':
                review_project_choice = input("Do you want to approve the project? (y/n): ").lower()
                if review_project_choice == "y":
                    advisor.update('Status', 'Approved')   
            elif project_info['Status'] == 'Evaluate Request':
                review_project_choice = input("Sent Project to evaluation? (y/n): ").lower()
                if review_project_choice == "y":
                    advisor.update('Status', 'Evaluation')
                    advisor.invite_faculty()
        elif choice == 2:
            Project.evaluate_project(project_info['ProjectID'], person_id)
        elif choice == 3:
            advisor.evaluate()
        elif choice == 0:
            exit()
            break
