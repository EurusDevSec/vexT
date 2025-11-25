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


lyrics=[
    "I don't want a lot for Christmas",
    "There is just one thing I need",
    "I don't care about the presents underneath the Christmas tree",
    "I just want you for my own",
    "More than you could ever know",
    "Make my wish come true",
    "All I want for Christmas is you"
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



def draw_tree(tick):

    budget = tick //2

    for i in range(HEIGHT):

        #SNOW LEFT

        left_padding = HEIGHT - 1  -i
        snow_layer = snow_buffer[i][:left_padding] 
        print("\033[90m" + snow_layer + "\033[0m", end  ="" )

        # print(" " * padding , end = "")
        #CHRISTMAS TREE

        for _ in range(2 * i + 1):
            color = random.choice(COLORS)
            print(color +  "*"  + "\033[0m", end = "")
        right_padding=(HEIGHT -i) + 5

        # SNOW RIGHT (NEW)
        snow_layer_right=snow_buffer[i][left_padding:left_padding+right_padding]
        print("\033[90m" + snow_layer_right + "\033[0m", end = "")


        # DRAW TEXT
        if i < len(lyrics):
            text = lyrics[i]

            if budget > 0:
                print("\033[32m" + text[:budget] + "\033[0m", end = "")
        print()



    #  body tree 
    for i  in range(2):
        if i ==1:
            print(" " * (HEIGHT -2)  + "\033[32m||\033[0m" + "🎁" + " " * 3 + "☃️")
        else:
            print(" " * (HEIGHT -2 ) + "\033[32m||\033[0m")
    # ground


def main():
    tick=0 # clock
    try:
        while True:

            clear()
            update_snow()
            draw_tree(tick)
            tick+=1
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\033[34mMerryChrismas 🎁")

if __name__ == "__main__":
    main()

