
gradeArray = []

gradeArray.append(5.5)
gradeArray.append(3.2)
gradeArray.append(-2.7)

print(gradeArray)

print(gradeArray[1])

gradeArray[1] = 255.5
print(gradeArray[1])

# ==========================
numGrades = int(input("How many grades do you have?: "))

gradeArray = []
for i in range(0, numGrades, 1):
    grade = float(input("Enter the Grade: "))    
    gradeArray.append(grade);

for i in range(0, numGrades, 1):
    print("Your ", i+1, "grades are ", gradeArray[i])

print("thanks for playing...")
