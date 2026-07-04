# Student Record Manager

A simple Python console application for managing student records.

## Features

- Add a new student with name, roll number, age, email, and course
- Validate input fields and email format
- Save records to a text file named `students.txt`
- View all saved student records in a tabular format
- Continue running until the user chooses to exit

## Requirements

- Python 3.x

## How to Run

1. Open a terminal in this folder.
2. Run the program:

```bash
python student_record_manager.py
```

## File Structure

- `student_record_manager.py` - Main program
- `students.txt` - Saved student records

## Menu Options

1. Add Student
2. View Student Records
3. Exit

## Notes

- The program validates that:
  - Name and course are not empty
  - Age is a positive integer
  - Email uses a valid format
- Invalid input shows an appropriate error message.
