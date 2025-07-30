# SORT

# 預設的排序是從小到大
L = [5, 2, 9, 1, 5, 6]
L.sort()
print(L)
# 如果要從大到小排序，可以使用 reverse=True 參數
L.sort(reverse=True)
print(L)

"""
鼠標放在指令上可以看到說明
"""


# 算術指定運算子
a = 1
a += 2  # 相當於 a = a + 2
print(a)  # 輸出 3

a -= 1  # 相當於 a = a - 1
print(a)  # 輸出 2

a *= 3  # 相當於 a = a * 3
print(a)  # 輸出 6

a /= 2  # 相當於 a = a / 2
print(a)  # 輸出 3.0

a //= 2  # 相當於 a = a // 2
print(a)  # 輸出 1.0

a %= 2  # 相當於 a = a % 2
print(a)  # 輸出 1.0

a **= 3  # 相當於 a = a ** 3
print(a)  # 輸出 1.0

# 優先順序
# 1. () 括號
# 2. ** 次方
# 3. *、/、//、% 乘、除、整除、取餘數
# 4. +、- 加、減
# 5. 比較運算子
# 6. not
# 7. and
# 8. or
# 9. 算術指定運算子


# WHILE
# 條件為 True 時，會一直執行，反之則結束
i = 0
while i < 5:
    print(i)
    i += 1

# break可強制結束迴圈
i = 0
while i < 5:
    print(i)

    for j in range(5):
        print(j)

    if i == 3:
        break  # 強制結束迴圈，跳出外層的 while 迴圈
    i += 1

for i in range(5):
    print(i)
    if i == 3:
        break
