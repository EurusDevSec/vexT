import time
import os
import random
import pygame


HEIGHT=10


COLORS=[
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
]


lyrics=[
  "(Intro)",
  "I don't want a lot for Christmas",
  "There is just one thing I need",
  "I don't care about the presents underneath the Christmas tree",
  "I just want you for my own",
  "More than you could ever know",
  "Make my wish come true",
  "All I want for Christmas is you, yeah.",
  "",
  "(Verse 1)",
  "I don't want a lot for Christmas",
  "There is just one thing I need, and I",
  "Don't care about the presents underneath the Christmas tree",
  "I don't need to hang my stocking there upon the fireplace",
  "Santa Claus won't make me happy with a toy on Christmas Day",
  "",
  "(Chorus)",
  "I just want you for my own",
  "More than you could ever know",
  "Make my wish come true",
  "All I want for Christmas is you",
  "You, baby",
  "",
  "(Verse 2)",
  "Oh, I won't ask for much this Christmas",
  "I won't even wish for snow, and I",
  "I just wanna keep on waiting underneath the mistletoe",
  "I won't make a list and send it to the North Pole for Saint Nick",
  "I won't even stay awake to hear those magic reindeer click",
  "",
  "(Chorus)",
  "'Cause I just want you here tonight",
  "Holding on to me so tight",
  "What more can I do?",
  "Oh, baby, all I want for Christmas is you",
  "You, baby",
  "",
  "(Bridge)",
  "Oh, all the lights are shining so brightly everywhere",
  "And the sound of children's laughter fills the air",
  "And everyone is singing",
  "I hear those sleigh bells ringing",
  "Santa, won't you bring me the one I really need?",
  "Won't you please bring my baby to me?",
  "",
  "(Verse 3)",
  "Oh, I don't want a lot for Christmas",
  "This is all I'm asking for",
  "I just wanna see my baby standing right outside my door",
  "",
  "(Chorus)",
  "Oh, I just want you for my own",
  "More than you could ever know",
  "Make my wish come true",
  "Oh, baby, all I want for Christmas is you",
  "You, baby",
  "",
  "(Outro)",
  "All I want for Christmas is you, baby",
  "All I want for Christmas is you, baby",
  "All I want for Christmas is you, baby",
  "All I want for Christmas is you, baby"
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

#CLEAR SCREEN
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
        if i ==0:
            print("\033[33m✯", end = "")
        else: 
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
            budget-=len(text)
        print()



    #  body tree 
    for i  in range(2):
        if i ==1:
            print(" " * (HEIGHT -2)  + "\033[32m||\033[0m" + "🎁" + " " * 3 + "☃️")
        else:
            print(" " * (HEIGHT -2 ) + "\033[32m||\033[0m")
    # ground

def init_music():
    pygame.mixer.init()
    code_path = os.path.dirname(os.path.abspath(__file__))
    song_path = os.path.join(code_path,"res","christmas_song.mp3")
    print(song_path)
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1) # loop forever
    except:
        print("Chua co file nhac 'christmas_song.mp3!' ")


def main():
    tick=0 # clock
    init_music()
    try:
        while True:

            clear()
            update_snow()
            draw_tree(tick)
            tick+=1
            time.sleep(0.08)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        print("\033[34mMerryChrismas 🎁")

if __name__ == "__main__":
    main()

