import time
import os
import random



HEIGHT=10


COLORS=[
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
]

# bau troi 
WIDTH = 20
snow_buffer = [" " * WIDTH for _ in range(HEIGHT + 3)]
print(snow_buffer)

def update_snow():
    snow_buffer.pop()

    new_row = ""
    for _ in range(WIDTH):
        if random.random() <0.1:
            new_row+="."
        else:
            new_row+=" "
    snow_buffer.insert(0,new_row)

def clear():
    os.system("cls" if os.name == "nt" else "clear")



def draw_tree():
    
    for i in range(HEIGHT):
        padding = HEIGHT - 1  -i
        snow_layer = snow_buffer[i][:padding] 
        print("\033[90m" + snow_layer + "\033[0m", end  ="" )
        # print(" " * padding , end = "")
        for _ in range(2 * i + 1):
            color = random.choice(COLORS)
            print(color +  "*"  + "\033[0m", end = "")
        print()



    #  than cay 
    for i  in range(2):
        if i ==1:
            print(" " * (HEIGHT -2)  + "\033[32m||\033[0m" + "🎁" + " " * 3 + "☃️")
        else:
            print(" " * (HEIGHT -2 ) + "\033[32m||\033[0m")



def main():
    try:
        while True:

            clear()
            update_snow()
            draw_tree()
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\033[34mMerryChrismas 🎁")

if __name__ == "__main__":
    main()

