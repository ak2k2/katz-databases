# CLI Reference for Student Database Management

## Commands Overview

The CLI supports various operations for managing students, courses, and registrations within the database. Each command is followed by specific arguments and options to perform the desired action.

### `view`
Displays data from the database.
- **Arguments**:
  - `type`: Type of data to view (`students`, `courses`, `registrations`).

### `add_student`
Adds a new student to the database.
- **Arguments**:
  - `name`: Name of the student to add.

### `add_course`
Adds a new course to the database.
- **Arguments**:
  - `name`: Name of the course.
  - `course_number`: Course number.
  - `instructor`: Name of the instructor.
  - `num_seats`: Number of available seats in the course.

### `add_registration`
Creates a registration linking a student to a course.
- **Arguments**:
  - `student_id`: ID of the student to register.
  - `course_id`: ID of the course for registration.

### `remove_student`
Removes a student from the database.
- **Arguments**:
  - `student_id`: ID of the student to remove.

### `remove_course`
Removes a course from the database.
- **Arguments**:
  - `course_id`: ID of the course to remove.

### `remove_registration`
Removes a registration between a student and a course.
- **Arguments**:
  - `student_id`: ID of the student in the registration to remove.
  - `course_id`: ID of the course in the registration to remove.

## Usage Examples

- **View Students**: 
  ```
  view students
  ```
- **View Courses**: 
  ```
  view courses
  ```
- **View Registrations**: 
  ```
  view registrations
  ```
- **Add a Student**: 
  ```
  add_student "Jane Doe"
  ```
- **Add a Course**: 
  ```
  add_course "Calculus" 101 "Prof. Smith" 30
  ```
- **Register a Student to a Course**: 
  ```
  add_registration 1 2
  ```
- **Remove a Student**: 
  ```
  remove_student 1
  ```
- **Remove a Course**: 
  ```
  remove_course 2
  ```
- **Remove a Registration**: 
  ```
  remove_registration 1 2
  ```

Each command manipulates the underlying JSON database, immediately reflecting changes. Ensure correct usage of IDs and existing data when adding or removing entities to maintain database integrity.