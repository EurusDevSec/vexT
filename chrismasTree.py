# import os
# import random
# import time

# tree = [
#     "        * ",
#     "       *** ",
#     "      ***** ",
#     "     ******* ",
#     "       ||| "

# ]

# colors = [
#     "\033[31m",
#     "\033[32m",
#     "\033[33m",
#     "\033[34m"
# ]

# def draw_frame():
#     for line in tree:
#         for char in line:
#             if char == "*":
#                 color = random.choice(colors)
#                 print(color + "*" + "\033[0m",end="")
#             else:
#                 print(" ",end="")
#         print()

# def main():
#     while True:
#         os.system('cls' if os.name=='nt' else 'clear')
#         draw_frame()
#         time.sleep(0.5)

# if __name__ == "__main__":
#     main()
import os
import random
import time

n=10

colors=[
    "\033[31m", "\033[32m", "\033[33m","\033[34m", "\033[35m"
]


def draw_frame_dynamic():
    for i in range(n):
        spaces=n-1-i
        print(" " * spaces,end="")
        numStars=2*i+1

        for _ in range(numStars):
            color=random.choice(colors)
            print(color + "*" + "\033[0m", end="")

        print()
    
    for _ in range(2):
        print(" " * (n-2) + "\033[33m|||\033[0m")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        draw_frame_dynamic()
        time.sleep(0.5)

if __name__ == "__main__":
    
    main()