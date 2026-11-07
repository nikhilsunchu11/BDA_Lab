
import re
import csv

records = {}

with open("students_raw.txt", "r") as file:
    for line in file:
        row_match = re.search(r"\b(S\d{3})\s+column=([^,]+),.*?value=(.*)", line)
        if not row_match:
            continue

        student_id, column, value = row_match.groups()
        student = records.setdefault(student_id, {})

        if column == "info:name":
            student["name"] = value.strip()
        elif column == "info:department":
            student["department"] = value.strip()
        elif column == "info:semester":
            student["semester"] = value.strip()
        elif column == "marks:subject":
            student["subject"] = value.strip()
        elif column == "marks:score":
            student["score"] = value.strip()

fields = [
    "student_id", "name", "department",
    "semester", "subject", "score"
]

with open("students.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for student_id in sorted(records):
        student = records[student_id]
        writer.writerow({
            "student_id": student_id,
            **student
        })

print("Created students.csv")
print("Students exported:", len(records))
