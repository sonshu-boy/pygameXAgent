"""
這是多行註解
這些註解不會被執行
# 選取個別程式可個別執行
"""

# 這是單行註解
# 單行註解可以用 ctrl + / 快速添加或刪除

# 基本型態
print(1)  # 輸出整數 (int)
# -1, 9
print(1.0)  # 輸出浮點數 (float)
print(1.234)  # 輸出浮點數 (float)
print("apple")  # 輸出字串 (str)
# "dwsadaw" '1'
print(True)  # 輸出布林值 True (bool)
print(False)  # 輸出布林值 False (bool)

# 變數(功能是把右邊的值存到左邊的變數中)
a = 1  # a 是整數 (int)
print(a)  # 輸出變數 a 的值
a = "apple"  # a 變成字串 (str) (直接覆蓋)
print(a)  # 輸出變數 a 的值

# 運算式子
print((2 + 3) * 4)  # 括號，輸出 20
print(2**3)  # 次方，輸出 8
print(6 * 3)  # 乘法，輸出 18
print(6 / 3)  # 除法，輸出 2.0
print(7 // 3)  # 整除，輸出 2
print(7 % 3)  # 取餘數，輸出 1
print(2 + 3)  # 加法，輸出 5
print(5 - 2)  # 減法，輸出 3

# 運算符號優先順序
# 1. () 括號
# 2. ** 次方
# 3. *、/、//、% 乘、除、整除、取餘數
# 4. +、- 加、減

# 字串運算
print("Hello, " + "world!")  # 字串連接，輸出 "Hello, world!"
print("Python" * 3)  # 字串重複，輸出 "PythonPythonPython"

# 字串格式化
name = "Alice"
age = 30
# 錯誤寫法
print(
    "My name is " + name + " and I am " + age + " years old."
)  # 這會報錯，因為 age 是整數
# 正確寫法
print(f"My name is {name} and I am {age} years old.")  # 使用 f-string 格式化字串

# 型態轉換
# int(x): 轉成整數
print(int(3.7))  # 3
print(int("8"))  # 8

# float(x): 轉成浮點數
print(float(5))  # 5.0
print(float("2.3"))  # 2.3

# str(x): 轉成字串
print(str(123))  # "123"
print(str(4.56))  # "4.56"
print(str(True))  # "True"

# bool(x): 轉成布林值
print(bool(0))  # False
print(bool(1))  # True
print(bool(""))  # False
print(bool("abc"))  # True

# len 格式
s = "hello"
print(len(s))  # 輸出字串長度，結果為 5

# type 格式
print(type(s))  # 輸出變數 s 的型態，結果為 <class 'str'>
print(type(123))  # 輸出整數的型態，結果為 <class 'int'>
print(type(3.14))  # 輸出浮點數的型態，結果為 <class 'float'>
print(type(True))  # 輸出布林值的型態，結果為 <class 'bool'>
