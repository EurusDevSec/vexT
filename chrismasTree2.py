import os
import time
import random

# --- CẤU HÌNH (CONFIG) ---
n = 12  # Cây cao hơn xíu cho đẹp
width = 40 # Bầu trời rộng hơn

# Palette màu
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[97m"
GREY = "\033[90m"
RESET = "\033[0m"

colors = [RED, GREEN, YELLOW, BLUE, PURPLE, CYAN]

# Danh sách vật trang trí (Lá nhiều hơn quả châu)
# Tỷ lệ: 70% là lá (*), 30% là quả châu (o, @, O)
ornaments = ['*'] * 7 + ['o', '@', 'O']

lyrics = [
    "Jingle bells, jingle bells",
    "Jingle all the way",
    "Oh what fun it is to ride",
    "In a one-horse open sleigh",
    "Hey! Jingle bells...",
    "Jingle all the way...",
    "Merry Christmas!",
    "Happy New Year!",
    "To: who Read this",
    "From: EurusDevSec (Hoàng)"
]

snow_buffer = [" " * width for _ in range(n + 3)] # Buffer dài hơn để bao cả phần gốc

def update_snow():
    """Logic tạo tuyết rơi (Queue)"""
    snow_buffer.pop()
    new_row = ""
    for _ in range(width):
        # 15% khả năng có tuyết rơi
        rand = random.random()
        if rand < 0.05: new_row += "." 
        elif rand < 0.1: new_row += "+" # Thêm bông tuyết hình dấu cộng cho đa dạng
        else: new_row += " "
    snow_buffer.insert(0, new_row)

def draw_Christmas(tick):
    char_budget = tick 

    # --- 1. VẼ TÁN CÂY ---
    for i in range(n):
        # Lớp tuyết nền bên trái
        padding_len = n - 1 - i
        print(GREY + snow_buffer[i][:padding_len] + RESET, end="")
        
        # LOGIC VẼ CÂY & TRANG TRÍ
        if i == 0:
            # Đỉnh cây: Luôn là ngôi sao vàng to
            print(YELLOW + "★" + RESET, end="") 
        else:
            # Thân cây: Vẽ từng ký tự
            for _ in range(2 * i + 1):
                # Chọn ngẫu nhiên vật trang trí (lá hoặc quả)
                char = random.choice(ornaments)
                color = random.choice(colors)
                
                # Nếu là lá (*) thì ưu tiên màu xanh cho giống cây thật
                if char == '*':
                    if random.random() < 0.7: color = GREEN # 70% lá màu xanh
                
                print(color + char + RESET, end="")
        
        # Lớp tuyết nền bên phải
        padding_right_len = n - i + 5
        snow_right = snow_buffer[i][padding_len : padding_len + padding_right_len]
        print(GREY + snow_right + RESET, end="")

        # LOGIC CHỮ CHẠY (Giữ nguyên logic Happy Path)
        if i < len(lyrics):
            line = lyrics[i]
            if char_budget >= len(line):
                print(GREEN + line + RESET, end="")
                char_budget -= len(line)
            elif char_budget > 0:
                print(GREEN + line[:char_budget] + RESET, end="")
                char_budget = 0
            
        print() # Xuống dòng

    # --- 2. VẼ THÂN CÂY & MẶT ĐẤT ---
    # Thân cây
    for i in range(2):
        print(GREY + snow_buffer[n+i][:n-2] + RESET, end="") # Tuyết bao quanh thân
        print(YELLOW + "|||" + RESET, end="")
        print(GREY + snow_buffer[n+i][n+1:n+10] + RESET) # Tuyết bên phải thân

    # Mặt đất (Footer)
    ground_snow = snow_buffer[n+2][:n-4]
    print(GREY + ground_snow + WHITE + "~^~^~^~^~^~^~^~" + RESET) 


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    tick = 0
    try:
        while True:
            clear()
            update_snow()
            draw_Christmas(tick)
            tick += 1
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\033[31mGiáng sinh vui vẻ nhé!\033[0m")

if __name__ == "__main__":
    main()