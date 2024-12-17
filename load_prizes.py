prizes_to_import=[]
with open(file="prizes.txt",mode="r") as prize_file:
    prize_list = prize_file.readlines()

    for i in range(len(prize_list)):
        name_without = prize_list[i].strip("\n")
        prizes_to_import.append(name_without)

