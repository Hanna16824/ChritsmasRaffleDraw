names_to_import=[]
with open(file="names.txt",mode="r") as name_file:
    name_list = name_file.readlines()

    for i in range(len(name_list)):
        name_without = name_list[i].strip("\n")
        names_to_import.append(name_without)
