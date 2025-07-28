score = input("請輸入分數: ")  # 取得使用者輸入（字串）
score = float(score)  # 轉成浮點數
if score >= 90:
    print("你的成績是 A")
elif score >= 80:
    print("你的成績是 B")
elif score >= 70:
    print("你的成績是 C")
elif score >= 60:
    print("你的成績是 D")
elif score < 60:
    print("你的成績是 F")
elif score < 0 or score > 100:
    print("輸入錯誤，請輸入 0 到 100 的分數")
