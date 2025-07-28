# 讓使用者輸入半徑，計算圓面積

radius = input("請輸入圓的半徑: ")  # 取得使用者輸入（字串）
radius = float(radius)  # 轉成浮點數
area = 3.14159 * (radius**2)  # 計算圓面積
print(f"半徑為 {radius} 的圓面積為 {area}")
