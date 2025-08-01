# LIST
print([])  # 這是空的list
print([1, 2, 3])  # 這是包含三個整數的list
print(["a", "b", "c"])  # 這是包含三個字串的list
print(1, 2, 3, ["a", "b", "c"])  # 這是同時輸出三個整數和一個列表
print([1, "a", 3.14, True])  # 這是包含不同類型元素的列表

# 元素的索引從0開始
# 這是CRUD的R
L = [1, 2, 3, "a", "b", "c"]
print(L[0])  # 1
print(L[1])  # 2
print(L[2])  # 3
print(L[3])  # a

# 切片(跟range用法相同)
L = [1, 2, 3, "a", "b", "c"]
print(L[::2])  # [1, 3, 'b']，每隔一個取一個元素
print(L[1:4])  # [2, 3, 'a']，從索引1到3
print(L[1:4:2])  # [2, 'a']，從索引1到3，每隔一個取一個

print(len(L))  # 輸出列表的長度

# list走訪元素
L = [1, 2, 3, "a", "b", "c"]
for i in range(0, len(L), 2):
    print(L[i])  # 每隔一個輸出一次元素

for i in L:
    print(i)  # 依次輸出列表中的每個元素

# list修改元素
L = [1, 2, 3, "a", "b", "c"]
L[0] = 100
L[1] = 200
print(L)  # [100, 200, 3, 'a', 'b', 'c']

# 傳值呼叫
a = 1
b = a
b = 2
print(a, b)  # 1, 2，a沒有被改變，b被改變為2

# 傳址呼叫
a = [1, 2, 3]
b = a
b[0] = 100
print(a, b)  # [100, 2, 3], [100, 2, 3]，a和b指向同一個列表

a = [1, 2, 3]
b = a.copy()  # 使用copy方法創建a的副本
b[0] = 100
print(a, b)  # [1, 2, 3], [100, 2, 3]，a沒有被改變，b是a的副本

# list的append
L = [1, 2, 3]
L.append(4)  # 在列表末尾添加元素
print(L)  # [1, 2, 3, 4]

# list的移除元素
# 1. 使用remove方法移除指定元素
L = [1, 2, 3, 4, 1]
L.remove(1)
print(L)  # [2, 3, 4, 1]，只移除由左至右第一個1
# 如果要移除所有的1，可以使用循環
L = [1, 2, 3, 4, 1]
for i in range(0, len(L)):
    if L[i] == 1:
        L.remove(1)  # 移除所有的1

# 2. 使用pop方法移除指定索引的元素
L = [1, 2, 3, 4, 1]
L.pop(0)  # 移除索引0的元素
print(L)  # [2, 3, 4, 1]，移除第一個

L.pop()  # 移除最後一個元素
print(L)  # [2, 3, 4]，移除最後一個
