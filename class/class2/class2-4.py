import random

# 設定初始範圍
low = 0
high = 100
answer = random.randint(low, high)

while True:
    guess = int(input(f"請輸入{low}~{high}的整數:"))
    if guess < low or guess > high:
        print("你輸入的數字不在範圍內，請再試一次")
        continue
    if guess == answer:
        print("恭喜猜中!")
        break
    elif guess > answer:
        print("再小一點")
        # 更新上限
        if guess < high:
            high = guess
    else:
        print("再大一點")
        # 更新下限
        if guess > low:
            low = guess
