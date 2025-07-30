# 匯入 random 模組並以 r 作為別名
import random as r

# random.randrange
# 產生 0~9 之間的隨機整數
print(r.randrange(10))
# 產生 1~9 之間的隨機整數
print(r.randrange(1, 10))
# 產生 1~9 之間，間隔為2的隨機整數（即奇數）
print(r.randrange(1, 10, 2))

# random.randint
# 產生 1~10 之間的隨機整數
print(r.randint(1, 10))  # 包含10，與randrange不同
