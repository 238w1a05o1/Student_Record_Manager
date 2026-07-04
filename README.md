# Student Record Manager

A simple Python application for managing student records through a lightweight portal-style desktop interface.

## Features

- Add student records with name, roll number, age, email, and course
- Validate required fields and email format
- Save records to a plain text file named `students.txt`
- View all saved students in a table-style records panel
- Navigate between a dashboard, add-student form, and records view

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

## How to Run

1. Open a terminal in the project folder.
2. Start the portal UI:

```bash
python student_record_manager.py
```

3. Use the original console version instead:

```bash
python student_record_manager.py --console
```

## File Structure

- `student_record_manager.py` - Main application script
- `students.txt` - Saved student records
- `README.md` - Project documentation

## Validation Rules

The application checks that:
- Name and course are not empty
- Roll number is provided
- Age is a positive integer
- Email follows a valid format

If any input is invalid, the app shows an error message and asks for corrected information.
