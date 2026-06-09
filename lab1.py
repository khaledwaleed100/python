
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
print(last_name + " " + first_name)

n = int(input("Enter an integer n: "))
n_str = str(n)
result = n + int(n_str * 2) + int(n_str * 3)
print("Expected Result:", result)


print(""" /\/\/\/\/\/\//\/\/\/\/\/\/\//\/
""")


pi = 3.14159265359
r = 6
volume = (4/3) * pi * (r ** 3)
print("Volume of the sphere:", volume)


base = float(input("Enter the base of the triangle: "))
height = float(input("Enter the height of the triangle: "))
area = 0.5 * base * height
print("Area of the triangle:", area)


for i in range(1, 6):
    print("*" * i)
for i in range(4, 0, -1):
    print("*" * i)


word = input("Enter a word to reverse: ")
print(word[::-1])


for i in range(7):
    if i == 3 or i == 6:
        continue
    print(i, end=" ")
print() 

a, b = 0, 1
while a <= 50:
    print(a, end=" ")
    a, b = b, a + b
print() 


text = input("Enter a string: ")
letters = 0
digits = 0
for char in text:
    if char.isalpha():
        letters += 1
    elif char.isdigit():
        digits += 1
print("Letters:", letters)
print("Digits:", digits)