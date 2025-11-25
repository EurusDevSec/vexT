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
   
    for i in range(n):
        spaces = " "*(n-1-i)
        print(spaces,end="")
        for _ in range(2*i+1):
            color = random.choice(colors)
            print(color + "*" + "\033[0m",end="")

            padding_right = " " * (n-i + 5)
            print(padding_right,end="")


            if i < len(lyrics):
                current_line=lyrics[i]
                hien_thi = max(0, (tick - i * 5) // 2)
            
            # In ra phần chuỗi đã được "cắt"
            print("\033[32m" + current_line[:hien_thi] + "\033[0m", end="")



        print()

    for i in range(2):
        print(" "*(n-2) + "\033[32m||\033[0m")


def clear():
    os.system('cls' if os.name=='nt' else 'clear')
def main():
    while True:
        clear()
        draw_Chrismas()
        time.sleep(0.5)

if __name__ == "__main__":
    main()