
name = input("Enter the student's name: ")
score = float(input("Enter the test score (0–100): "))


if score >= 90:
    grade = "A"
    status = "Pass"
elif score >= 80:
    grade = "B"
    status = "Pass"
elif score >= 70:
    grade = "C"
    status = "Pass"
elif score >= 60:
    grade = "D"
    status = "Pass"
else:
    grade = "F"
    status = "Fail"

print("\nStudent Name:", name)
print("Score:", score)
print("Grade:", grade)
print("Status:", status)
