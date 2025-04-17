import csv
import random
from faker import Faker

fake = Faker()
used_ids = set()


def generate_id():
    while True:
        unique_id = f"M{random.randint(10000, 99999)}"
        if unique_id not in used_ids:
            used_ids.add(unique_id)
            return unique_id


def generate_csv(file_path, num_rows=10):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        for _ in range(num_rows):
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            unique_id = generate_id()
            writer.writerow([full_name, first_name, unique_id])


if __name__ == "__main__":
    output_file_students = "data/students.csv"
    output_file_volunteers = "data/volunteers.csv"
    generate_csv(output_file_students, num_rows=500)
    generate_csv(output_file_volunteers, num_rows=500)
