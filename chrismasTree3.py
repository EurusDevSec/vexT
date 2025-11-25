import os
import time
import random



HEIGHT = 10
COLORS = [
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m"
]

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def draw_tree():
    
    for i in range(HEIGHT):
        padding = " " * (HEIGHT -1-i)
        print(padding,end="")
        for _ in range(2*i+1):
            color = random.choice(COLORS)
            print(color + "*" + "\033[0m",end="")
        print()    
    for _ in range(2):
        print( " " * (HEIGHT-3) + "\033[32m ||| \033[0m")

def main():
    try:
        while True:

            clear()
            draw_tree()

            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\n\033[33mMerryChrismas!!🎁\033[0m")
if __name__=="__main__":
    main()