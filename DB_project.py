import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import mysql.connector


# ------ Rigiter Page ------
class RegistrationPage:
    def __init__(self, master):
        self.master = master
        master.title("Registration")

        # Create entry widgets for user information
        self.name_label = tk.Label(master, text="Username:")
        self.name_entry = tk.Entry(master)
        self.name_label.pack()
        self.name_entry.pack()

        self.id_label = tk.Label(master, text="student/teacher ID:")
        self.id_entry = tk.Entry(master)
        self.id_label.pack()
        self.id_entry.pack()

        self.user_type_label = tk.Label(master, text="User Type:")
        self.user_type_var = tk.StringVar()
        self.user_type_var.set("Student")
        self.user_type_menu = tk.OptionMenu(master, self.user_type_var, "Student", "Teacher")
        self.user_type_label.pack()
        self.user_type_menu.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_entry = tk.Entry(master, show="*")
        self.password_label.pack()
        self.password_entry.pack()

        # Create button for registration
        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack()

        # Create a connection to the database
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        self.c = self.conn.cursor()


    def register(self):
        """Save user information to database"""
        name = self.name_entry.get()
        id = self.id_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        try:
            self.c.execute("INSERT INTO users (name, id, password, user_type) VALUES (%s, %s, %s, %s);", (name, id, password, user_type))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error","Failed to register user.")
            return
        # Check that all fields are filled
        if not name or not id or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

# ------ Login Page --------
class LoginPage:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        # Create entry widgets for username and password
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        # Create login and registration buttons
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(master, text="Register", command=self.open_registration_page)
        self.register_button.pack()

        # Create a database connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        self.c = self.conn.cursor()

    def login(self):
        """Authenticate user and grant access"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        try: 
            # Create a database connection
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
            self.c = self.conn.cursor()
            # Check if user exists in database
            self.c.execute("SELECT * FROM users WHERE name = %s AND password = %s ", (username, password))
            user = self.c.fetchone()

            if user:
                # Check the user type
                user_type = user[3]
                if user_type == "Student":
                    # Grant access to the CourseSelectionApp
                    messagebox.showinfo("Success", "Login successful!")
                    self.master.destroy()
                    root = tk.Tk()
                    app = CourseSelectionApp(root, user[1], user[0])
                    root.mainloop()
                elif user_type == "Teacher":
                    # Grant access to the TeacherPage
                    messagebox.showinfo("Success", "Login successful!")
                    self.master.destroy()
                    root = tk.Tk()
                    teacher_page = TeacherPage(root, username)
                    #teacher_page.grid(row=0, column=0)
                    root.mainloop()
                else:
                    messagebox.showerror("Error", "Invalid username or password.")
                    self.register_button.config(fg='red')
            else:
                messagebox.showinfo("No Database", "There Is No Data Base")
                self.register_button.config(fg='red')
        except:
            messagebox.showinfo("No User Yet", "Ther is no User Register Please")
            self.register_button.config(fg='red')

    def open_registration_page(self):
        """Open the registration page"""
        root = tk.Tk()
        registration_page = RegistrationPage(root)
        root.mainloop()

    def __del__(self):
        """Close database connection"""
        self.conn.close()

# ------ Teacher Page ------
class TeacherPage:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Course Selection App - Teacher Page")

        # Create a database connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        self.cursor = self.conn.cursor()

        # Define labels
        self.label1 = tk.Label(master, text="Your courses:")
        self.label2 = tk.Label(master, text="Select a course to view students:")

        # Define listboxes
        self.courses = tk.Listbox(master)
        self.students = tk.Listbox(master)

        # Define buttons
        self.add_button = tk.Button(master, text="Add", command=self.add_course)
        self.remove_button = tk.Button(master, text="Remove", command=self.remove_course)
        self.view_button = tk.Button(master, text="View Students", command=self.view_students)
        self.delete_button = tk.Button(master, text="Delete Student", command=self.delete_student)
        self.enter_grade_button = tk.Button(master, text="Enter Grade", command=self.enter_grade)
        self.logout_button = tk.Button(master, text="Logout", command=self.logout)

        # Define layout
        self.label1.grid(row=0, column=0, sticky="w")
        self.label2.grid(row=0, column=1, sticky="w")
        self.courses.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.students.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.add_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.remove_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.view_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.delete_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.enter_grade_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.logout_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Populate courses listbox
        self.cursor.execute("SELECT name FROM courses WHERE teacher = %s", (self.username,))
        courses = self.cursor.fetchall()
        for course in courses:
            self.courses.insert(tk.END, course[0])

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        app = LoginPage(root)
        root.mainloop()

    def add_course(self):
        """Add a new course"""
        course_name = tk.simpledialog.askstring("Add Course", "Enter the name of the new course:")
        if course_name:
            self.cursor.execute("INSERT INTO courses (name, teacher) VALUES (%s, %s)", (course_name, self.username))
            self.conn.commit()
            self.courses.insert(tk.END, course_name)

    def remove_course(self):
        """Remove selected course"""
        selected = self.courses.curselection()
        if selected:
            course_name = self.courses.get(selected[0])
            self.cursor.execute("DELETE FROM courses WHERE name = %s AND teacher = %s", (course_name, self.username))
            self.conn.commit()
            self.courses.delete(selected[0])

    def view_students(self):
        """View students in all courses taught by the teacher"""
        global selected
        selected = self.courses.curselection()
        if selected:
            course_name = self.courses.get(selected[0])
            self.students.delete(0, tk.END)
            self.cursor.execute("SELECT id FROM courses WHERE name = %s AND teacher = %s", (course_name, self.username))
            course_id = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT name FROM users INNER JOIN course_selection ON users.id = course_selection.student_id WHERE course_selection.course_id = %s",(course_id,))
            student_names = self.cursor.fetchall()
            for student_name in student_names:
                self.students.insert(tk.END, student_name[0])
        else:
            messagebox.showerror("Error", "Please select a course")

    def delete_student(self):
        """Delete selected student from selected course"""
        selected_course = self.courses.curselection()
        selected_student = self.students.curselection()
        if selected_student:
            student_name = self.students.get(selected_student[0])
            self.cursor.execute("SELECT id FROM users WHERE name = %s", (student_name,))
            student_id = self.cursor.fetchone()
            if student_id is not None:
                student_id = student_id[0]
                if selected_course:
                    course_name = self.courses.get(selected_course[0])
                    self.cursor.execute("SELECT id FROM courses WHERE name = %s AND teacher = %s", (course_name, self.username))
                    course_id = self.cursor.fetchone()
                    if course_id is not None:
                        course_id = course_id[0]
                        self.cursor.execute("DELETE FROM course_selection WHERE course_id = %s AND student_id = %s", (course_id, student_id))
                        self.conn.commit()
                        self.students.delete(selected_student[0])
                        messagebox.showinfo("Delete Student", "Student deleted successfully")
                    else:
                        messagebox.showerror("Error Happened", "Course not found !")
                else:
                    self.cursor.execute("DELETE FROM course_selection WHERE student_id = %s", (student_id,))
                    self.conn.commit()
                    self.students.delete(selected_student[0])
                    messagebox.showinfo("Delete Student", "Student deleted successfully")
            else:
                messagebox.showerror("Error Happened", "Student not found !")
        else:
            messagebox.showerror("Error Happened", "Please select a student")

    def enter_grade(self):
        """Enter grade for selected student in selected course"""
        selected_student = self.students.curselection()
        if selected_student:
            course_name = self.courses.get(selected[0])
            student_name = self.students.get(selected_student[0])
            grade = tk.simpledialog.askinteger("Enter Grade", f"Enter grade for {student_name} :")
            if grade is not None:
                self.cursor.execute("UPDATE course_selection SET grade = %s WHERE course_id = (SELECT id FROM courses WHERE name = %s AND teacher = %s) AND student_id = (SELECT id FROM users WHERE name = %s)", (grade, course_name, self.username, student_name))
                self.conn.commit()
                print("Grade entered successfully!")
        else:
            messagebox.showerror("Error Happened", "Please select a student")

# ------ Student Page ------
class CourseSelectionApp:
    def __init__(self, master, id, name):
        self.master = master
        self.student_id = id
        self.username = name
        master.title("Course Selection App")

        # Define labels
        self.label1 = tk.Label(master, text="Select your courses:")
        self.label2 = tk.Label(master, text="Selected courses:")

        # Define listboxes
        self.available_courses = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.selected_courses = tk.Listbox(master, selectmode=tk.MULTIPLE)

        # Define buttons
        self.add_button = tk.Button(master, text="Add", command=self.add_course)
        self.remove_button = tk.Button(master, text="Remove", command=self.remove_course)
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_courses)
        self.grade_button = tk.Button(master, text="View Grades", command=self.view_grades)
        self.logout_button = tk.Button(master, text="Logout", command=self.logout)

        # Define layout
        self.label1.grid(row=0, column=0, sticky="w")
        self.label2.grid(row=0, column=1, sticky="w")
        self.available_courses.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.selected_courses.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.add_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.remove_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.submit_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.grade_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.logout_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        try:
            # Load courses from database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
            c = conn.cursor()
            c.execute("SELECT * FROM courses")
            courses = c.fetchall()

            # Insert courses into available_courses listbox
            for course in courses:
                self.available_courses.insert(tk.END, course[1])
            conn.close()
        except mysql.connector.Error as error:
            print("Failed to connect to MySQL database: {}".format(error))

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        app = LoginPage(root)
        root.mainloop()

    def add_course(self):
        """Add selected course to selected_courses listbox"""
        selected = self.available_courses.curselection()
        for i in selected:
            self.selected_courses.insert(tk.END, self.available_courses.get(i))

    def remove_course(self):
        """Remove selected course from selected_courses listbox"""
        self.selected_courses.delete(tk.ACTIVE)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ali@1382",
            database="user_db"
        )
        c = conn.cursor()
        selected_courses = self.selected_courses.get(0, tk.END)
        for course in selected_courses:
            c.execute("SELECT id FROM courses WHERE name=%s", (course,))
            result = c.fetchone()
            if result is not None:
                course_id = result[0]
                c.execute("DELETE FROM course_selection WHERE course_id = %s AND student_id = %s", (course_id, self.student_id))
                conn.commit()
        conn.close()

    def submit_courses(self):
        """Submit selected courses"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
            c = conn.cursor()
            selected_courses = self.selected_courses.get(0, tk.END)

            for course in selected_courses:
                c.execute("SELECT id FROM courses WHERE name=%s", (course,))
                result = c.fetchone()
                if result is not None:
                    course_id = result[0]
                    c.execute("INSERT INTO course_selection (course_id, student_id, grade) VALUES (%s, %s, %s)", (course_id, self.student_id, 0))
                else:
                    print(f"The course '{course}' does not exist.")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            print("Ok")
        except mysql.connector.Error as error:
            print("Failed to connect to MySQL database: {}".format(error))

    def view_grades(self):
        """View the grades of the selected student"""
        selected = self.selected_courses.curselection()
        if selected:
            course_name = self.selected_courses.get(selected[0])
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ali@1382",
                database="user_db"
            )
            c = conn.cursor()
            c.execute("SELECT grade FROM course_selection WHERE course_id IN (SELECT id FROM courses WHERE name=%s) AND student_id=%s", (course_name, self.student_id))
            result = c.fetchone()
            if result is not None:
                grade = result[0]
                messagebox.showinfo("Grade", f"Your grade for {course_name} is {grade}")
            else:
                messagebox.showinfo("Grade", f"You have not yet received a grade for {course_name}.")
            conn.close()
        else:
            messagebox.showinfo("Grade", "Please select a course to view grades.")

    

# ------ Main code ---------

root = tk.Tk()
app = LoginPage(root)
root.mainloop()