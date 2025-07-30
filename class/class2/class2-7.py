# try expect
try:
    n = int(input("請輸入一個數字: "))
except:
    print("輸入錯誤，請輸入數字。")


# 函數定義
def hello():
    print("Hello, World!")


for i in range(10):
    hello()


# 帶參數的函數
def hello(name):
    print(f"Hello, {name}!")


hello("Alice")
hello("Bob")
hello("Charlie")
for i in range(10):
    hello(i)  # 這裡i會被當作參數傳入


# 帶回傳值的函數
def add(a, b):
    return a + b  # 回傳兩個數字的和


print(add(3, 5))  # 這裡會印出8
print(add("hello", " world"))  # 這裡會印出"hello world"

sum = add(3, 5)
print(sum)  # 這裡會印出8


# 有多個回傳的函數
def add_and_sub(a, b):
    return a + b, a - b  # 回傳兩個值


sum, sub = add_and_sub(3, 5)
print(f"和: {sum}, 差: {sub}")  # 這裡會印出"和: 8, 差: -2"


# 預設參數
# 使用預設參數時需放在最後面
def hello(name, message="Hello"):
    print(f"{message}, {name}!")


hello("Alice")  # 這裡會使用預設值，印出"Hello, Alice!"
hello("Bob", "Hi")  # 這裡會使用傳入的值，印出"Hi, Bob!"


# 建議傳入參數型態
def add(a: int, b: int) -> int:  # 將鼠標放在函數名稱上可以看到提示
    return a + b


print(add(3, 5))  # 這裡會印出8
print(add("hello", " world"))  # 這裡會印出"hello world"


# def區域變數與全域變數(互不影響)

# 1.
length = 5  # 全域變數


def calculate_square_area():
    area = length**2  # area是區域變數
    print("面積是:", area)


calculate_square_area()  # 這裡會印出"面積是: 25"

# 2.
length = 5  # 全域變數


def calculate_square_area():
    area = length**2  # area是區域變數
    print("面積是:", area)


length = 10  # 修改全域變數
calculate_square_area()  # 這裡會印出"面積是: 100"

# 3.
length = 5  # 全域變數
area = 100  # 全域變數


def calculate_square_area():
    area = length**2  # area是區域變數


calculate_square_area()
print("面積是:", area)  # 這裡會印出"面積是: 100"

# 4.(於函數內修改全域變數)
length = 5  # 全域變數
area = 100  # 全域變數


def calculate_square_area():
    area = length**2  # area是區域變數
    return area  # 回傳區域變數


area = calculate_square_area()  # 將回傳值賦值給全域變數area
print("面積是:", area)  # 這裡會印出"面積是: 25"

# 4-1.(於函數內修改全域變數)
length = 5  # 全域變數
area = 100  # 全域變數


def calculate_square_area():
    global area  # 使用global關鍵字修改全域變數
    area = length**2


calculate_square_area()
print("面積是:", area)  # 這裡會印出"面積是: 25"


def hello(name: str):
    # 函數傳入參數都是區域變數
    """
    指令說明區\n

    這是一個打招呼的函數\n
    參數:\n
    name: str - 姓名\n

    回傳: None\n

    範例: hello("Alice")
    """
    print(f"Hello, {name}!")
