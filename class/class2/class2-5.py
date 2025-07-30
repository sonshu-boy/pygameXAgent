"""
# 設定提示檔案(/)
F1 > Prompt > 設定提示檔案 > 新增檔案 > 輸入指令名稱
"""

# 字典(dict)
# {"a": 1} ----> "a"為key，1為value

# 取得dict的key
d = {"a": 1, "b": 2, "c": 3}
print(d.keys())
for key in d.keys():
    print(key)

# 取得dict的value
d = {"a": 1, "b": 2, "c": 3}
print(d.values())
for value in d.values():
    print(value)

# 取得dict的key-value
d = {"a": 1, "b": 2, "c": 3}
print(d.items())
for key, value in d.items():
    print(key, value)

# 新增/修改dict的key-value
d["d"] = 4  # 新增
d["a"] = 5  # 修改
print(d)

# 刪除dict的key-value
print(d.pop("a"))  # 刪除key為"a"的項目，並返回其value
print(d.pop("e", "不存在"))  # 刪除key為"e"的項目，並返回其value，若不存在則返回"不存在"

# 檢查dict是否有某個key
print("a" in d)  # True
print("e" in d)  # False

# 比較複雜的dict
d = {"a": [1, 2, 3], "b": {"c": 4, "d": 5}}
print(d["a"])  # [1, 2, 3]
print(d["a"][0])  # 1
print(d["b"])  # {"c": 4, "d": 5}
print(d["b"]["c"])  # 4


# 成績登記系統
grades = {
    "小明": {"國文": [85, 80, 90], "數學": [90, 85, 95], "英文": [88, 82, 90]},
    "小華": {"國文": [78, 85, 80], "數學": [82, 88, 90], "英文": [80, 90, 85]},
    "小美": {"國文": [92, 85, 88], "數學": [95, 90, 92], "英文": [90, 85, 88]},
}

# 取得小明的數學成績
print(grades["小明"]["數學"])
# 取得小美第一次的國文成績
print(grades["小美"]["國文"][0])
# 取得小華第二次的國文成績
print(grades["小華"]["國文"][1])

for student, subjects in grades.items():
    chinese = subjects["國文"]
    avg = sum(chinese) / len(chinese)  # 計算每位學生國文成績的平均值
    print(
        f"{student} 的國文平均成績是 {avg:.2f}"
    )  # 輸出每位學生的國文平均成績至小數點後兩位
