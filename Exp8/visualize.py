import csv
import matplotlib.pyplot as plt

names = []
scores = []

with open("students.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        names.append(row["name"])
        scores.append(int(row["score"]))

plt.figure(figsize=(10, 6))
bars = plt.bar(names, scores)

plt.title("Big Data Marks of Students")
plt.xlabel("Student Name")
plt.ylabel("Marks")
plt.ylim(0, 100)
plt.grid(axis="y", linestyle="--", alpha=0.4)

for bar, score in zip(bars, scores):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(score),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("student_marks.png", dpi=300)
print("Chart saved as student_marks.png")
plt.show()
