import sqlite3
import openpyxl
from reportlab.pdfgen import canvas


conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, dob TEXT, gender TEXT, class TEXT, contact TEXT, address TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, subject TEXT, salary REAL, contact TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, duration TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, date TEXT, status TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, subject TEXT, marks INTEGER)")
conn.commit()


def export_excel():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Students"
    sheet.append(["ID", "Name", "DOB", "Gender", "Class", "Contact", "Address"])
    cursor.execute("SELECT * FROM Students")
    for row in cursor.fetchall():
        sheet.append(row)
    workbook.save("students_report.xlsx")
    print("Excel report generated: students_report.xlsx")


def export_pdf():
    c = canvas.Canvas("students_report.pdf")
    c.drawString(100, 800, "Students Report")
    y = 700
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        c.drawString(50, y, str(row))
        y -= 20
    c.save()
    print("PDF report generated: students_report.pdf")


def add_student():
    name = input("Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    gender = input("Gender: ")
    clas = input("Class: ")
    contact = input("Contact: ")
    address = input("Address: ")
    cursor.execute("INSERT INTO students (name,dob,gender,class,contact,address) VALUES (?,?,?,?,?,?)", (name,dob,gender,clas,contact,address))
    conn.commit()
    print("Student added successfully!")

def view_students():
    cursor.execute("SELECT * FROM Students")
    for row in cursor.fetchall():
        print(row)

def update_students():
    student_id = input("ENter Student ID to update: ")
    name = input("New Name: ")
    dob = input("New Dob: ")
    gender = input("New class: ")
    clas = input("New Class: ")
    contact = input("New Contact: ")
    address = input("New Address: ")
    cursor.execute("UPDATE students SET name=?, dob=?, gender=?, class=?, contact=?, address=? where id=?",(name,dob,gender,clas,contact,address,student_id))
    conn.commit()
    print("Student updated successfully!")


def delete_student():
    student_id = input("Enter student ID to delete: ")
    cursor.execute("DELETE FROM students where id=?", (student_id,))
    conn.commit()
    print("Student deleted successfully!")


while True:
    print("\n=========== School Management System ========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete student")
    print("5. Export Excel Report")
    print("6. Export PDF Report")
    print("0. Exit")
    choice = input("Enter choice: ")
    if choice == '1': add_student()
    elif choice == '2': view_students()
    elif choice == '3': update_students()
    elif choice == '4': delete_student()
    elif choice == '5': export_excel()
    elif choice == '6': export_pdf()
    elif choice == '0': break
    else: print("Invalid choice")