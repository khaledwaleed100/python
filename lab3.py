import sqlite3


def setup_database():
    """Initializes the SQLite database and creates the employee table if it doesn't exist."""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            department TEXT,
            salary REAL,
            role TEXT,
            managed_department TEXT
        )
    ''')
    conn.commit()
    return conn


db_conn = setup_database()


class Employee:
    # Static list containing all employee objects [cite: 1588]
    all_employees = [] 

    def __init__(self, first_name, last_name, age, department, salary, role='Employee', managed_department=None):
        # Assign values to instance attributes [cite: 1592]
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.department = department
        self.salary = salary
        self.role = role
        
        # Insert the created object to the list [cite: 1593]
        Employee.all_employees.append(self)
        
        # Insert new record in table employee in database [cite: 1594]
        cursor = db_conn.cursor()
        cursor.execute('''
            INSERT INTO employee (first_name, last_name, age, department, salary, role, managed_department)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.first_name, self.last_name, self.age, self.department, self.salary, self.role, managed_department))
        
      
        self.db_id = cursor.lastrowid 
        db_conn.commit()

    def transfer(self, new_department):
        """Changes employee department and updates the database [cite: 1595, 1596, 1597]"""
        self.department = new_department
        cursor = db_conn.cursor()
        cursor.execute('''
            UPDATE employee SET department = ? WHERE id = ?
        ''', (self.department, self.db_id))
        db_conn.commit()
        print(f"\nSuccess: {self.first_name} transferred to {self.department}.")

    def fire(self):
        """Removes the employee from the shared list and deletes their record from the database [cite: 1598, 1599]"""
        if self in Employee.all_employees:
            Employee.all_employees.remove(self)
            
        cursor = db_conn.cursor()
        cursor.execute('''
            DELETE FROM employee WHERE id = ?
        ''', (self.db_id,))
        db_conn.commit()
        print(f"\nSuccess: {self.first_name} has been fired and removed from the database.")

    def show(self):
        """Prints all employee data [cite: 1600, 1601]"""
        print(f"Role: {self.role} | Name: {self.first_name} {self.last_name} | Age: {self.age} | "
              f"Dept: {self.department} | Salary: ${self.salary}")

    @staticmethod
    def List_employees():
        """Selects all employees from the database and prints their data [cite: 1602, 1603]"""
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM employee')
        records = cursor.fetchall()
        
        print("\n--- All Employees in Database ---")
        if not records:
            print("The database is currently empty.")
        else:
            for row in records:
              
                if row[6] == 'Manager':
                    print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Age: {row[3]} | "
                          f"Dept: {row[4]} | Salary: **Confidential** | Managed Dept: {row[7]}")
                else:
                    print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Age: {row[3]} | "
                          f"Dept: {row[4]} | Salary: ${row[5]}")
        print("---------------------------------")


class Manager(Employee):
    """Class manager inherits from class employee with an additional attribute [cite: 1604, 1605, 1606]"""
    def __init__(self, first_name, last_name, age, department, salary, managed_department):
        self.managed_department = managed_department
        
        super().__init__(first_name, last_name, age, department, salary, role='Manager', managed_department=managed_department)

    def show(self):
        """Prints all data except salary, printing 'confidential' instead [cite: 1608, 1609]"""
        print(f"Role: {self.role} | Name: {self.first_name} {self.last_name} | Age: {self.age} | "
              f"Dept: {self.department} | Salary: **Confidential** | Managed Dept: {self.managed_department}")



def run_app():
    while True:
      
        print("\n" + "="*35)
        print("   EMPLOYEE MANAGEMENT SYSTEM")
        print("="*35)
        print("  'add'   - Add new employee/manager")
        print("  'list'  - List all employees from DB")
        print("  'show'  - Show specific employee details")
        print("  'trans' - Transfer an employee")
        print("  'fire'  - Fire an employee")
        print("  'q'     - Exit the program")
        
        choice = input("\nEnter operation: ").strip().lower()
        
      
        if choice == 'q':
            print("Exiting application. Goodbye!")
            db_conn.close()
            break
            
        elif choice == 'add':
           
            emp_type = input("If manager press 'm' / if employee press 'e': ").strip().lower()
            if emp_type not in ['m', 'e']:
                print("Invalid role selection!")
                continue
                
            print("\nPlease insert data:")
            fname = input("Name (First):>> ")
            lname = input("Name (Last):>> ")
            age = int(input("Age:>> "))
            dept = input("Department:>> ")
            salary = float(input("Salary:>> "))
            
            if emp_type == 'm':
                m_dept = input("Managed Department:>> ")
                Manager(fname, lname, age, dept, salary, m_dept)
                print(f"Manager {fname} {lname} added successfully!")
            else:
                Employee(fname, lname, age, dept, salary)
                print(f"Employee {fname} {lname} added successfully!")
                
        elif choice == 'list':
            Employee.List_employees()
            
        elif choice == 'show':
            if not Employee.all_employees:
                print("No employees currently loaded in memory.")
                continue
            
            print("\nSelect an employee to show details:")
            for i, emp in enumerate(Employee.all_employees):
                print(f"[{i}] {emp.first_name} {emp.last_name}")
            
            try:
                idx = int(input("Index>> "))
                Employee.all_employees[idx].show()
            except (ValueError, IndexError):
                print("Invalid index selection.")

        elif choice == 'trans':
            if not Employee.all_employees:
                print("No employees currently loaded in memory.")
                continue
                
            print("\nSelect an employee to transfer:")
            for i, emp in enumerate(Employee.all_employees):
                print(f"[{i}] {emp.first_name} {emp.last_name} (Current Dept: {emp.department})")
                
            try:
                idx = int(input("Index>> "))
                target_emp = Employee.all_employees[idx]
                new_dept = input("New Department:>> ")
                target_emp.transfer(new_dept)
            except (ValueError, IndexError):
                print("Invalid index selection.")

        elif choice == 'fire':
            if not Employee.all_employees:
                print("No employees currently loaded in memory.")
                continue
                
            print("\nSelect an employee to fire:")
            for i, emp in enumerate(Employee.all_employees):
                print(f"[{i}] {emp.first_name} {emp.last_name}")
                
            try:
                idx = int(input("Index>> "))
                target_emp = Employee.all_employees[idx]
                target_emp.fire()
            except (ValueError, IndexError):
                print("Invalid index selection.")
                
        else:
            print("Invalid command. Please try again.")


if __name__ == '__main__':
    run_app()