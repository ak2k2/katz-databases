import json

import pandas as pd


class Connection:
    def __init__(self, database_name: str) -> None:
        self.database_name = database_name
        self.database = None

    @staticmethod
    def read_database(database_name: str) -> dict:
        try:
            with open(database_name, "r") as f:
                data = json.load(f)
                # Convert keys to integers
                data["students"] = {int(k): v for k, v in data["students"].items()}
                data["courses"] = {int(k): v for k, v in data["courses"].items()}
                # No need to convert registration IDs as they should already be integers
                return data
        except FileNotFoundError:
            print(f"Database file {database_name} not found. Creating a new one.")
            create_mock_database(database_name)
            return Connection.read_database(database_name)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {database_name}.")
            return {}

    def __enter__(self) -> dict:
        self.database = self.read_database(self.database_name)
        return self.database

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        with open(self.database_name, "w") as f:
            json.dump(self.database, f, indent=4)


def create_mock_database(database_name: str) -> None:
    with open(database_name, "w") as f:
        data = {"students": {}, "courses": {}, "registrations": []}
        json.dump(data, f, indent=4)


def json_view(table: dict) -> None:
    print(json.dumps(table, indent=2))


def table_view(table: dict) -> None:
    df = pd.DataFrame.from_dict(table, orient="index")
    print(df)


def add_student(name: str, students: dict) -> None:
    student_id = max(students.keys(), default=0) + 1
    students[student_id] = {"name": name}


def add_course(
    name: str, course_number: int, instructor: str, num_seats: int, courses: dict
) -> None:
    course_id = max(courses.keys(), default=0) + 1
    courses[course_id] = {
        "name": name,
        "course_number": course_number,
        "instructor": instructor,
        "num_seats": num_seats,
    }


def add_registration(
    student_id: int, course_id: int, registrations: list, students: dict, courses: dict
) -> None:
    if student_id in students and course_id in courses:
        registrations.append({"student_id": student_id, "course_id": course_id})
    else:
        print("Invalid student or course ID.")


def remove_student(student_id: int, students: dict, registrations: list) -> None:
    if student_id in students:
        del students[student_id]
        registrations[:] = [
            reg for reg in registrations if reg["student_id"] != student_id
        ]
    else:
        print(f"Student ID {student_id} not found.")


def remove_course(course_id: int, courses: dict, registrations: list) -> None:
    if course_id in courses:
        del courses[course_id]
        registrations[:] = [
            reg for reg in registrations if reg["course_id"] != course_id
        ]
    else:
        print(f"Course ID {course_id} not found.")


def remove_registration(student_id: int, course_id: int, registrations: list) -> None:
    registrations[:] = [
        reg
        for reg in registrations
        if not (reg["student_id"] == student_id and reg["course_id"] == course_id)
    ]


def get_student(student_id: int, students: dict) -> dict:
    return students.get(student_id, {})


def get_course(course_id: int, courses: dict) -> dict:
    return courses.get(course_id, {})


def get_courses_for_student(student_id: int, registrations: list) -> list:
    return [
        reg["course_id"] for reg in registrations if reg["student_id"] == student_id
    ]


def get_students_for_course(course_id: int, registrations: list) -> list:
    return [reg["student_id"] for reg in registrations if reg["course_id"] == course_id]


import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Interact with the student database")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # View command
    view_parser = subparsers.add_parser(
        "view", help="View students, courses, or registrations"
    )
    view_parser.add_argument(
        "type",
        choices=["students", "courses", "registrations"],
        help="Type of data to view",
    )

    # Add student command
    add_student_parser = subparsers.add_parser("add_student", help="Add a student")
    add_student_parser.add_argument("name", help="Name of the student")

    # Add course command
    add_course_parser = subparsers.add_parser("add_course", help="Add a course")
    add_course_parser.add_argument("name", help="Name of the course")
    add_course_parser.add_argument("course_number", type=int, help="Course number")
    add_course_parser.add_argument("instructor", help="Instructor name")
    add_course_parser.add_argument("num_seats", type=int, help="Number of seats")

    # Add registration command
    add_registration_parser = subparsers.add_parser(
        "add_registration", help="Add a registration"
    )
    add_registration_parser.add_argument("student_id", type=int, help="Student ID")
    add_registration_parser.add_argument("course_id", type=int, help="Course ID")

    # Remove student command
    remove_student_parser = subparsers.add_parser(
        "remove_student", help="Remove a student"
    )
    remove_student_parser.add_argument(
        "student_id", type=int, help="Student ID to remove"
    )

    # Remove course command
    remove_course_parser = subparsers.add_parser(
        "remove_course", help="Remove a course"
    )
    remove_course_parser.add_argument("course_id", type=int, help="Course ID to remove")

    # Remove registration command
    remove_registration_parser = subparsers.add_parser(
        "remove_registration", help="Remove a registration"
    )
    remove_registration_parser.add_argument("student_id", type=int, help="Student ID")
    remove_registration_parser.add_argument("course_id", type=int, help="Course ID")

    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize the connection and database
    conn = Connection("data/database.json")
    with conn as database:
        students, courses, registrations = (
            database["students"],
            database["courses"],
            database["registrations"],
        )

        if args.command == "view":
            if args.type == "students":
                json_view(students)
            elif args.type == "courses":
                json_view(courses)
            elif args.type == "registrations":
                json_view(registrations)
        elif args.command == "add_student":
            add_student(args.name, students)
            print(f"Added student: {args.name}")
        elif args.command == "add_course":
            add_course(
                args.name, args.course_number, args.instructor, args.num_seats, courses
            )
            print(f"Added course: {args.name}")
        elif args.command == "add_registration":
            add_registration(
                args.student_id, args.course_id, registrations, students, courses
            )
            print(
                f"Added registration for student ID {args.student_id} to course ID {args.course_id}"
            )
        elif args.command == "remove_student":
            remove_student(args.student_id, students, registrations)
            print(f"Removed student ID {args.student_id}")
        elif args.command == "remove_course":
            remove_course(args.course_id, courses, registrations)
            print(f"Removed course ID {args.course_id}")
        elif args.command == "remove_registration":
            remove_registration(args.student_id, args.course_id, registrations)
            print(
                f"Removed registration for student ID {args.student_id} from course ID {args.course_id}"
            )
        else:
            print("Unknown command. Use -h for help.")
            sys.exit(1)


if __name__ == "__main__":
    main()
