consolation_prize_to_import=[]
with open(file="consolation_prize.txt",mode="r") as consolation_prize_file:
    consolation_prize_list = consolation_prize_file.readlines()

    for i in range(len(consolation_prize_list)):
        name_without = consolation_prize_list[i].strip("\n")
        consolation_prize_to_import.append(name_without)
