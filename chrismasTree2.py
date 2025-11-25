import os
import time
import random

colors = [
    "\033[30m","\033[31m","\033[32m","\033[33m","\033[34m","\033[35m"
]


lyrics = [
    "Jingle bells, jingle bells",
    "Jingle all the way",
    "Oh what fun it is to ride",
    "In a one-horse open sleigh",
    "Hey! Jingle bells...",
    "Jingle all the way...",
    "Merry Christmas!",
    "Happy New Year!",
    "To: Tech Lead",
    "From: Python"
]

n=10
def draw_Chrismas(tick):
    char_budget = tick
    for i in range(n):
        spaces = " "*(n-1-i)
        print(spaces,end="")
        for _ in range(2*i+1):
            color = random.choice(colors)
            print(color + "*" + "\033[0m",end="")

        padding_right = " " * (n-i + 5)
        print(padding_right,end="")


        if i < len(lyrics):
            line = lyrics[i]
            line_len = len(line)

            if char_budget >= line_len:
                # Trường hợp 1: Ngân sách dư dả -> In hết dòng này
                print("\033[32m" + line + "\033[0m", end="")
                char_budget -= line_len # Trừ đi số chữ đã in để tính cho dòng sau
            elif char_budget > 0:
                # Trường hợp 2: Ngân sách còn ít -> In dang dở
                print("\033[32m" + line[:char_budget] + "\033[0m", end="")
                char_budget = 0 # Xài hết vốn rồi
            else:
                # Trường hợp 3: Hết ngân sách -> Không in gì cả
                pass
        
        # In ra phần chuỗi đã được "cắt"
  



        print()

    for i in range(2):
        print(" "*(n-2) + "\033[32m||\033[0m")


def clear():
    os.system('cls' if os.name=='nt' else 'clear')
def main():
    tick=0
    while True:
        clear()
        draw_Chrismas(tick)
        tick+=1
        time.sleep(0.2)

if __name__ == "__main__":
    main()