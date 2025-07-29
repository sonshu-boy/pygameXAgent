fruits = {"蘋果": 25, "香蕉": 20, "橘子": 30}


while True:
    print("\n=== 水果店價格查詢系統 ===\n")
    print("目前水果價格：")
    for name, price in fruits.items():
        print(f"{name}: {price}元")
    print("\n1. 新增水果價格 (Add fruit price)")
    print("2. 修改水果價格 (Modify fruit price)")
    print("3. 刪除水果 (Delete fruit)")
    print("4. 離開系統 (Exit system)")
    choice = input("請選擇功能 (1-4): ")
    print("==========================")
    if choice == "1":
        fruit = input("請輸入要新增的水果名稱: ")
        if fruit in fruits:
            print(f"{fruit} 已存在，請使用修改功能。")
        else:
            price = input(f"請輸入{fruit}的價格: ")
            is_number = True
            if price:
                for c in price:
                    if c < "0" or c > "9":
                        is_number = False
                        break
            else:
                is_number = False
            if is_number:
                fruits[fruit] = int(price)
                print(f"{fruit}已新增，價格 {price}元")
            else:
                print("價格輸入錯誤，請輸入數字。")
    elif choice == "2":
        fruit = input("請輸入要修改的水果名稱: ")
        if fruit in fruits:
            price = input(f"請輸入{fruit}的新價格: ")
            is_number = True
            if price:
                for c in price:
                    if c < "0" or c > "9":
                        is_number = False
                        break
            else:
                is_number = False
            if is_number:
                fruits[fruit] = int(price)
                print(f"{fruit}價格已修改為 {price}元")
            else:
                print("價格輸入錯誤，請輸入數字。")
        else:
            print(f"{fruit} 不存在，請先新增。")
    elif choice == "3":
        fruit = input("請輸入要刪除的水果名稱: ")
        if fruit in fruits:
            fruits.pop(fruit)
            print(f"{fruit}已刪除")
        else:
            print(f"{fruit} 不存在。")
    elif choice == "4":
        print("感謝使用水果店價格查詢系統！")
        break
    else:
        print("請輸入1-4之間的數字。")
    print("==========================")
