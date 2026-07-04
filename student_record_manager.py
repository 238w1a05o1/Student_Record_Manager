from pathlib import Path
import re

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
        print("Error: The student file could not be found while saving data.")
    except Exception as exc:
        print(f"Unexpected error while saving student record: {exc}")


def add_student():
    """Collect student details, validate them, and save the record."""
    print("\nAdd Student")
    print("-" * 20)

    try:
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
        except ValueError:
            raise ValueError("Age must be a positive integer.") from None

        if age <= 0:
            raise ValueError("Age must be a positive integer.")

        email = input("Enter email: ").strip()
        if not email:
            raise ValueError("Email cannot be empty.")

        validate_email(email)

        course = input("Enter course: ").strip()
        if not course:
            raise ValueError("Course cannot be empty.")

        student_data = {
            "name": name,
            "roll_number": roll_number,
            "age": age,
            "email": email,
            "course": course,
        }
        save_student(student_data)
        print("Student record added successfully.")

    except ValueError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Unexpected error while adding student: {exc}")


def read_students():
    """Read all student records from students.txt and return them as a list."""
    try:
        if not FILE_PATH.exists():
            raise FileNotFoundError

        with FILE_PATH.open("r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            print("No student records found.")
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

    except FileNotFoundError:
        print("No student records found.")
        return []
    except ValueError as exc:
        print(f"Error while reading student records: {exc}")
        return []
    except Exception as exc:
        print(f"Unexpected error while reading student records: {exc}")
        return []


def display_menu():
    """Display the main menu options to the user."""
    print("\nStudent Record Manager")
    print("1. Add Student")
    print("2. View Student Records")
    print("3. Exit")


def main():
    """Run the main console loop for the student record manager."""
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                students = read_students()
                if students:
                    print("\nStudent Records")
                    print("-" * 90)
                    print(f"{'Name':<15} {'Roll Number':<12} {'Age':<5} {'Email':<25} {'Course'}")
                    print("-" * 90)
                    for student in students:
                        print(
                            f"{student['name']:<15} {student['roll_number']:<12} "
                            f"{student['age']:<5} {student['email']:<25} {student['course']}"
                        )
            elif choice == "3":
                print("Exiting Student Record Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except Exception as exc:
            print(f"Unexpected error in main menu: {exc}")


if __name__ == "__main__":
    main()
