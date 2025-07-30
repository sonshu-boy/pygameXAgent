# 購物小幫手 Shopping Assistant

shopping_list = []

while True:
    # 顯示清單
    print("\n🛒 目前購物清單：")
    if not shopping_list:
        print("（清單是空的）")
    else:
        idx = 0
        while idx < len(shopping_list):
            print(f"{idx}: {shopping_list[idx]}")
            idx += 1
    print("-" * 20)

    print("請選擇動作：")
    print("1️⃣ 新增東西 (append)")
    print("2️⃣ 修改東西 (replace by index)")
    print("3️⃣ 刪除東西 (remove by name / pop by index)")
    print("4️⃣ 離開程式 (exit)")
    choice = input("輸入選項編號 (1/2/3/4): ")

    if choice == "1":
        item = input("請輸入要新增的東西：")
        shopping_list.append(item)
        print(f"已新增「{item}」到清單。")
    elif choice == "2":
        if not shopping_list:
            print("清單是空的，無法修改。")
        else:
            idx_str = input("請輸入要修改的項目編號：")
            is_num = True
            for ch in idx_str:
                if ch < "0" or ch > "9":
                    is_num = False
            if is_num and idx_str != "":
                idx = int(idx_str)
                if 0 <= idx < len(shopping_list):
                    new_item = input("請輸入新的內容：")
                    print(f"將「{shopping_list[idx]}」改為「{new_item}」。")
                    shopping_list[idx] = new_item
                else:
                    print("編號超出範圍。")
            else:
                print("請輸入正確的數字編號。")
    elif choice == "3":
        if not shopping_list:
            print("清單是空的，無法刪除。")
        else:
            print("選擇刪除方式：")
            print("a. 用名稱刪除（remove）")
            print("b. 用位置刪除（pop）")
            sub_choice = input("輸入 a 或 b：")
            if sub_choice == "a":
                name = input("請輸入要刪除的名稱：")
                found = False
                i = 0
                while i < len(shopping_list):
                    if shopping_list[i] == name:
                        shopping_list.remove(name)
                        print(f"已刪除「{name}」。")
                        found = True
                        break
                    i += 1
                if not found:
                    print("清單中沒有這個項目。")
            elif sub_choice == "b":
                idx_str = input("請輸入要刪除的項目編號：")
                is_num = True
                for ch in idx_str:
                    if ch < "0" or ch > "9":
                        is_num = False
                if is_num and idx_str != "":
                    idx = int(idx_str)
                    if 0 <= idx < len(shopping_list):
                        removed = shopping_list[idx]
                        shopping_list.pop(idx)
                        print(f"已刪除「{removed}」。")
                    else:
                        print("編號超出範圍。")
                else:
                    print("請輸入正確的數字編號。")
            else:
                print("請輸入 a 或 b。")
    elif choice == "4":
        print("👋 掰掰，回家囉！")
        break
    else:
        print("請輸入 1、2、3 或 4。")
