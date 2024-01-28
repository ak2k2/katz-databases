import json
import os
import tempfile
import unittest

from orm import *


class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        # Create a temporary db file
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".json")
        self.conn = Connection(self.db_path)

        # Initialize with mock data
        with open(self.db_path, "w") as f:
            json.dump({"students": {}, "courses": {}, "registrations": []}, f)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_add_student(self):
        with self.conn as database:
            students = database["students"]
            add_student("Jane Doe", students)
            self.assertTrue(
                any(student["name"] == "Jane Doe" for student in students.values())
            )

    def test_remove_student(self):
        with self.conn as database:
            students = database["students"]
            add_student("John Doe", students)
            student_id = next(iter(students.keys()))
            remove_student(student_id, students, database["registrations"])
            self.assertNotIn(student_id, students)

    def test_add_course(self):
        with self.conn as database:
            courses = database["courses"]
            add_course("Math 101", 101, "Prof. Smith", 30, courses)
            self.assertTrue(
                any(course["name"] == "Math 101" for course in courses.values())
            )

    def test_remove_course(self):
        with self.conn as database:
            courses = database["courses"]
            add_course("Math 101", 101, "Prof. Smith", 30, courses)
            course_id = next(iter(courses.keys()))
            remove_course(course_id, courses, database["registrations"])
            self.assertNotIn(course_id, courses)

    def test_add_registration(self):
        with self.conn as database:
            add_student("John Doe", database["students"])
            add_course("Math 101", 101, "Prof. Smith", 30, database["courses"])
            student_id = next(iter(database["students"].keys()))
            course_id = next(iter(database["courses"].keys()))
            add_registration(
                student_id,
                course_id,
                database["registrations"],
                database["students"],
                database["courses"],
            )
            self.assertTrue(
                any(
                    reg["student_id"] == student_id and reg["course_id"] == course_id
                    for reg in database["registrations"]
                )
            )

    def test_remove_registration(self):
        with self.conn as database:
            add_student("John Doe", database["students"])
            add_course("Math 101", 101, "Prof. Smith", 30, database["courses"])
            student_id = next(iter(database["students"].keys()))
            course_id = next(iter(database["courses"].keys()))
            add_registration(
                student_id,
                course_id,
                database["registrations"],
                database["students"],
                database["courses"],
            )
            remove_registration(student_id, course_id, database["registrations"])
            self.assertFalse(
                any(
                    reg["student_id"] == student_id and reg["course_id"] == course_id
                    for reg in database["registrations"]
                )
            )

    def test_view_functions(self):
        with self.conn as database:
            add_student("John Doe", database["students"])
            add_course("Math 101", 101, "Prof. Smith", 30, database["courses"])
            student_id = next(iter(database["students"].keys()))
            course_id = next(iter(database["courses"].keys()))
            add_registration(
                student_id,
                course_id,
                database["registrations"],
                database["students"],
                database["courses"],
            )

            student_view = get_student(student_id, database["students"])
            self.assertEqual(student_view["name"], "John Doe")

            course_view = get_course(course_id, database["courses"])
            self.assertEqual(course_view["name"], "Math 101")

            courses_for_student = get_courses_for_student(
                student_id, database["registrations"]
            )
            self.assertIn(course_id, courses_for_student)

            students_for_course = get_students_for_course(
                course_id, database["registrations"]
            )
            self.assertIn(student_id, students_for_course)


if __name__ == "__main__":
    unittest.main()
