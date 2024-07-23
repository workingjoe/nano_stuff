# - from youtube Paul McWhorter channel -- intro to Python

# note that x and y are STRINGS 
# x = input("Please Enter First number: ")
# y = input("Please Enter 2nd number: ")
# note that x and y are NUMERIC
x = int(float(input("Please Enter First number: ")))
y = int(float(input("Please Enter 2nd number: ")))

z = x + y
print("x + y = ",z)

if (x>0):
    print("Your number is POSITIVE")
    print("Thanks for playing")

if (x<0):
    print("Your number is NEGATIVE")
    print("Hope that you intended it that way")

for i in range(1,11,1):
    print(i)

print("That's all folks")

