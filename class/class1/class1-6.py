num = int(input("1~9中輸入一個數字："))
if num < 1 or num > 9:
    print("請輸入1~9之間的數字")
else:
    for i in range(1, num + 1):
        print(str(i) * i)
