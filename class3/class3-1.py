# open()
# r - read，讀取模式，檔案必須存在
# w - write，寫入模式，檔案不存在則建立，存在則清空
# a - append，附加模式，檔案不存在則建立，存在則在檔案末尾新增內容
# r+ - read and write，讀取與寫入模式，檔案必須存在
# w+ - write and read，寫入與讀取模式，檔案不存在則建立，存在則清空
# a+ - append and read，附加與讀取模式，檔案不存在則建立，存在則在檔案末尾新增內容

f = open("class3-1.txt", "r", encoding="utf-8")  # 開啟檔案，若不存在則建立
content = f.read()
print(content)
f.close()
##################################################################################
with open("class3-1.txt", "r", encoding="utf-8") as f:  # 使用 with 語句自動關閉檔案
    content = f.read()
    print(content)
# 這裡是使用 with 語句的好處，檔案會自動關閉
