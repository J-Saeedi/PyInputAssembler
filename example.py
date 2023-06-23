from time import sleep
input1 = 3.1  # @@var1@@
input2 = 4.12  # @@var2@@
save_to = "result1.txt"  # @@var3@@


def calc(input1, input2):
    result = input1**2 + input2**2
    with open(save_to, 'w') as f:
        f.write(str(result))


calc(input1, input2)
sleep(10)
