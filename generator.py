#!/usr/bin/env python
# generates sequences of items randomly and imports into txt file
import random
import copy

group_prefs = ["Adams", "Cabot", "Currier", "Dunster", "Eliot", "Kirkland", "Leverett", "Lowell", 
    "Mather", "Pfoho", "Quincy", "Winthrop"]
house_mapping = {"Adams": 1, "Cabot": 2, "Currier": 3, "Dunster": 4, "Eliot": 5, "Kirkland": 6, "Leverett": 7, "Lowell": 8, 
    "Mather": 9, "Pfoho": 10, "Quincy": 11, "Winthrop": 12}

def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    
    # parser.add_argument('samples', metavar='N', type=int, nargs='+', 
    #     help='total number of samples to be generated for students that wish to switch')

    # parser.parse_args

    f = open("input2.txt", "w")
    groups = 400
    f.write(str(groups) + "\n")
    # for each iteration, copy from the original and write to the file according to the spec
    for group in range(groups):
        temp_groups = copy.deepcopy(group_prefs)
        f.write(str(group) + " ")
        f.write(str(random.randint(1,8)) + " ")
        f.write(temp_groups.pop(random.randint(0, 11)) + " ")

        while len(temp_groups) > 0:
            f.write(str(house_mapping[temp_groups.pop(random.randint(0, len(temp_groups)-1))]) + " ")

        f.write("\n")
    f.close()

if __name__ == "__main__":
    main()