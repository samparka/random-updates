import random
answer = random.randint(1, 100)
counter = 0
while True:
    counter += 1
    num = int(input("输入一个数字："))
    if num > answer:
        print("大了")
    elif num < answer:
        print("小了")
    elif num == answer:
        print("对了")
        break
print("一共猜了%d次" % (counter))
if counter > 7:
    print("你真是个哈儿猜了%d次"% (counter))

