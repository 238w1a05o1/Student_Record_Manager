from pathlib import Path
import argparse
import re
import tkinter as tk
from tkinter import ttk, messagebox

FILE_PATH = Path(__file__).resolve().parent / "students.txt"
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email):
    """Validate an email address using a regular expression."""
    if not isinstance(email, str):
        raise ValueError("Email must be a string.")

    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email format. Please enter a valid email address.")

    return True


def save_student(student_data):
    """Save a student record to students.txt in comma-separated format."""
    try:
        with FILE_PATH.open("a", encoding="utf-8") as file:
            record = (
                f"{student_data['name']},{student_data['roll_number']},"
                f"{student_data['age']},{student_data['email']},{student_data['course']}\n"
            )
            file.write(record)
    except FileNotFoundError:
        raise FileNotFoundError("The student file could not be found while saving data.") from None
    except Exception as exc:
        raise RuntimeError(f"Unexpected error while saving student record: {exc}") from exc


def read_students():
    """Read all student records from students.txt and return them as a list."""
    try:
        if not FILE_PATH.exists():
            return []

        with FILE_PATH.open("r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            return []

        students = []
        for line in lines:
            name, roll_number, age, email, course = line.split(",", 4)
            students.append(
                {
                    "name": name,
                    "roll_number": roll_number,
                    "age": int(age),
                    "email": email,
                    "course": course,
                }
            )
        return students

    except ValueError as exc:
        raise ValueError(f"Error while reading student records: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Unexpected error while reading student records: {exc}") from exc


class StudentPortalApp(tk.Tk):
    """A simple portal-style GUI for managing student records."""

    def __init__(self):
        super().__init__()
        self.title("Student Portal")
        self.geometry("940x620")
        self.minsize(860, 560)
        self.configure(bg="#f4f7fb")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Portal.TFrame", background="#f4f7fb")
        style.configure("Sidebar.TFrame", background="#1f3a5f")
        style.configure("Sidebar.TButton", background="#1f3a5f", foreground="white", padding=8)
        style.map("Sidebar.TButton", background=[("active", "#2f4f7f")])

        self._build_layout()
        self.views = {}
        self._build_dashboard_view()
        self._build_form_view()
        self._build_records_view()
        self.show_view("dashboard")

    def _build_layout(self):
        header = ttk.Frame(self, padding=(24, 20, 24, 10), style="Portal.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Student Portal",
            font=("Segoe UI", 22, "bold"),
            foreground="#12324a",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="Manage student details through a simple portal dashboard.",
            font=("Segoe UI", 10),
            foreground="#4d6472",
        ).pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self, style="Portal.TFrame")
        body.pack(fill="both", expand=True)

        sidebar = ttk.Frame(body, padding=(16, 16, 16, 16), style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y")

        ttk.Label(sidebar, text="Navigation", font=("Segoe UI", 12, "bold"), foreground="white").pack(anchor="w", pady=(0, 10))

        self.nav_buttons = {}
        for name, label in (("dashboard", "Dashboard"), ("form", "Add Student"), ("records", "View Records")):
            button = ttk.Button(
                sidebar,
                text=label,
                command=lambda view=name: self.show_view(view),
                style="Sidebar.TButton",
            )
            button.pack(fill="x", pady=4)
            self.nav_buttons[name] = button

        self.content = ttk.Frame(body, padding=(20, 10, 20, 20), style="Portal.TFrame")
        self.content.pack(side="left", fill="both", expand=True)

    def _build_dashboard_view(self):
        frame = ttk.Frame(self.content, style="Portal.TFrame")
        self.views["dashboard"] = frame

        ttk.Label(frame, text="Welcome to the student portal", font=("Segoe UI", 16, "bold"), foreground="#12324a").pack(anchor="w")
        ttk.Label(frame, text="Use the navigation to add a student or review the current records.", font=("Segoe UI", 10), foreground="#4d6472").pack(anchor="w", pady=(6, 16))

        card = ttk.Frame(frame, padding=16, style="Portal.TFrame")
        card.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text="Portal overview", font=("Segoe UI", 12, "bold"), foreground="#12324a").pack(anchor="w")
        self.dashboard_count = tk.StringVar(value="Total students: 0")
        ttk.Label(card, textvariable=self.dashboard_count, font=("Segoe UI", 11)).pack(anchor="w", pady=(8, 0))

        actions = ttk.Frame(frame, style="Portal.TFrame")
        actions.pack(fill="x", pady=(8, 0))
        ttk.Button(actions, text="Add a Student", command=lambda: self.show_view("form")).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Open Records", command=lambda: self.show_view("records")).pack(side="left")

    def _build_form_view(self):
        frame = ttk.Frame(self.content, style="Portal.TFrame")
        self.views["form"] = frame

        ttk.Label(frame, text="Add Student", font=("Segoe UI", 16, "bold"), foreground="#12324a").pack(anchor="w")
        ttk.Label(frame, text="Fill in the student details below.", font=("Segoe UI", 10), foreground="#4d6472").pack(anchor="w", pady=(6, 12))

        fields = ttk.Frame(frame, style="Portal.TFrame")
        fields.pack(fill="x")

        self.form_entries = {}
        for label_text, key in (("Name", "name"), ("Roll Number", "roll_number"), ("Age", "age"), ("Email", "email"), ("Course", "course")):
            row = ttk.Frame(fields, style="Portal.TFrame")
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=label_text, width=14, anchor="w").pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.form_entries[key] = entry

        buttons = ttk.Frame(frame, style="Portal.TFrame")
        buttons.pack(fill="x", pady=(16, 0))
        ttk.Button(buttons, text="Save Student", command=self.save_student_from_form).pack(side="left")
        ttk.Button(buttons, text="Clear", command=self.clear_form).pack(side="left", padx=(8, 0))

    def _build_records_view(self):
        frame = ttk.Frame(self.content, style="Portal.TFrame")
        self.views["records"] = frame

        ttk.Label(frame, text="Student Records", font=("Segoe UI", 16, "bold"), foreground="#12324a").pack(anchor="w")
        ttk.Label(frame, text="A list of all saved student records.", font=("Segoe UI", 10), foreground="#4d6472").pack(anchor="w", pady=(6, 12))

        columns = ("name", "roll_number", "age", "email", "course")
        self.records_tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        self.records_tree.heading("name", text="Name")
        self.records_tree.heading("roll_number", text="Roll Number")
        self.records_tree.heading("age", text="Age")
        self.records_tree.heading("email", text="Email")
        self.records_tree.heading("course", text="Course")

        self.records_tree.column("name", width=140, anchor="w")
        self.records_tree.column("roll_number", width=100, anchor="w")
        self.records_tree.column("age", width=60, anchor="center")
        self.records_tree.column("email", width=220, anchor="w")
        self.records_tree.column("course", width=180, anchor="w")
        self.records_tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.records_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.records_tree.configure(yscrollcommand=scrollbar.set)

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()
        self.views[view_name].pack(fill="both", expand=True)
        if view_name == "dashboard":
            self.refresh_dashboard()
        elif view_name == "records":
            self.refresh_records()

    def refresh_dashboard(self):
        students = read_students()
        self.dashboard_count.set(f"Total students: {len(students)}")

    def refresh_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        students = read_students()
        for student in students:
            self.records_tree.insert(
                "",
                "end",
                values=(
                    student["name"],
                    student["roll_number"],
                    student["age"],
                    student["email"],
                    student["course"],
                ),
            )

    def clear_form(self):
        for entry in self.form_entries.values():
            entry.delete(0, tk.END)

    def save_student_from_form(self):
        try:
            student_data = {}
            student_data["name"] = self.form_entries["name"].get().strip()
            student_data["roll_number"] = self.form_entries["roll_number"].get().strip()
            student_data["age"] = self.form_entries["age"].get().strip()
            student_data["email"] = self.form_entries["email"].get().strip()
            student_data["course"] = self.form_entries["course"].get().strip()

            if not student_data["name"]:
                raise ValueError("Name cannot be empty.")
            if not student_data["roll_number"]:
                raise ValueError("Roll number cannot be empty.")
            if not student_data["age"]:
                raise ValueError("Age cannot be empty.")
            if not student_data["email"]:
                raise ValueError("Email cannot be empty.")
            if not student_data["course"]:
                raise ValueError("Course cannot be empty.")

            age = int(student_data["age"])
            if age <= 0:
                raise ValueError("Age must be a positive integer.")
            student_data["age"] = age
            validate_email(student_data["email"])
            save_student(student_data)
            self.clear_form()
            self.refresh_records()
            self.refresh_dashboard()
            self.show_view("records")
            messagebox.showinfo("Success", "Student record added successfully.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))


def run_console_mode():
    """Run the original console-based menu."""
    while True:
        print("\nStudent Record Manager")
        print("1. Add Student")
        print("2. View Student Records")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                print("\nAdd Student")
                print("-" * 20)
                name = input("Enter student name: ").strip()
                if not name:
                    raise ValueError("Name cannot be empty.")

                roll_number = input("Enter roll number: ").strip()
                if not roll_number:
                    raise ValueError("Roll number cannot be empty.")

                age_input = input("Enter age: ").strip()
                if not age_input:
                    raise ValueError("Age cannot be empty.")

                try:
                    age = int(age_input)
                except ValueError as exc:
                    raise ValueError("Age must be a positive integer.") from exc

                if age <= 0:
                    raise ValueError("Age must be a positive integer.")

                email = input("Enter email: ").strip()
                if not email:
                    raise ValueError("Email cannot be empty.")
                validate_email(email)

                course = input("Enter course: ").strip()
                if not course:
                    raise ValueError("Course cannot be empty.")

                save_student({"name": name, "roll_number": roll_number, "age": age, "email": email, "course": course})
                print("Student record added successfully.")
            elif choice == "2":
                students = read_students()
                if students:
                    print("\nStudent Records")
                    print("-" * 90)
                    print(f"{'Name':<15} {'Roll Number':<12} {'Age':<5} {'Email':<25} {'Course'}")
                    print("-" * 90)
                    for student in students:
                        print(f"{student['name']:<15} {student['roll_number']:<12} {student['age']:<5} {student['email']:<25} {student['course']}")
                else:
                    print("No student records found.")
            elif choice == "3":
                print("Exiting Student Record Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Student Record Manager")
    parser.add_argument("--console", action="store_true", help="Run the original console interface")
    args = parser.parse_args()

    if args.console:
        run_console_mode()
    else:
        app = StudentPortalApp()
        app.mainloop()


if __name__ == "__main__":
    main()
