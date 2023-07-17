import random 
import os 
import csv 
from termcolor import colored 

def clear_console(): 
    os.system('cls' if os.name == 'nt' else 'clear') 
  
def main_menu(player_name="nonPlayer"): 
    clear_console() 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("          ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
    print(colored("______________________________________________________", "cyan")) 
    print(f"คุณเข้าสู่ระบบด้วยชื่อ: {player_name}") 
    print("\nเลือกตัวเลือก:") 
    print(colored("1. เล่นเกม", "green")) 
    print(colored("2. คะแนนสูงสุด", "green")) 
    print(colored("3. ออกจากเกม", "green")) 
    choice = input("\nเลือกตัวเลือกของคุณ (1-3): ") 
    return choice 
  
def display_profiles(): 
    filename = "profiles.csv" 
    profiles = [] 
  
    try: 
        if os.path.isfile(filename): 
            with open(filename, 'r') as file: 
                reader = csv.reader(file) 
                profiles = list(reader) 
    except IOError: 
        print(colored("ผิดพลาด: ไม่สามารถอ่านไฟล์โปรไฟล์ได้", "red")) 
  
    clear_console() 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
    print(colored("______________________________________________________", "cyan")) 
    print("โปรไฟล์ที่มีอยู่:") 
  
    if profiles: 
        print(colored("ชื่อ", "cyan")) 
        for i, profile in enumerate(profiles, start=1): 
            print(f"{i}) {profile[0]}") 
  
    print("0) เข้าสู่ระบบด้วยโปรไฟล์ใหม่") 
  
def create_profile(name): 
    filename = "profiles.csv" 
    try: 
        with open(filename, 'a', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerow([name]) 
    except IOError: 
        print(colored("ผิดพลาด: ไม่สามารถสร้างโปรไฟล์ได้", "red")) 
  
def remove_profile(name): 
    filename = "profiles.csv" 
    profiles = [] 
  
    try: 
        if os.path.isfile(filename): 
            with open(filename, 'r') as file: 
                reader = csv.reader(file) 
                profiles = list(reader) 
  
        for profile in profiles: 
            if profile[0] == name: 
                profiles.remove(profile) 
  
        with open(filename, 'w', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerows(profiles) 
    except (IOError, csv.Error): 
        print(colored("ผิดพลาด: ไม่สามารถลบโปรไฟล์ได้", "red")) 
  
def login_or_signin(): 
    display_profiles() 
  
    if os.path.isfile("profiles.csv"): 
        choice = input(colored("\nป้อนหมายเลขของโปรไฟล์หรือ '0' เพื่อเข้าสู่ระบบด้วยโปรไฟล์ใหม่: ", "yellow")) 
        profiles_count = sum(1 for _ in open("profiles.csv")) 
  
        if choice.isdigit() and int(choice) in range(1, profiles_count + 1): 
            try: 
                with open("profiles.csv", 'r') as file: 
                    reader = csv.reader(file) 
                    profiles = list(reader) 
                    return profiles[int(choice) - 1][0] 
            except (IOError, csv.Error): 
                print(colored("ผิดพลาด: ไม่สามารถอ่านไฟล์โปรไฟล์ได้", "red")) 
  
    print(colored("คุณยังไม่มีโปรไฟล์ กรุณาเข้าสู่ระบบด้วยโปรไฟล์ใหม่", "red")) 
    name = input(colored("ป้อนชื่อของคุณ: ", "yellow")) 
    create_profile(name) 
    return name 
  
def confirm_removal(name): 
    confirm = input(colored(f"คุณแน่ใจว่าต้องการลบโปรไฟล์ '{name}'? (Y/N): ", "yellow")) 
    return confirm.lower() == 'y' 
  
def remove_profile_prompt(): 
    profiles = [] 
    if os.path.isfile("profiles.csv"): 
        try: 
            with open("profiles.csv", 'r') as file: 
                reader = csv.reader(file) 
                profiles = list(reader) 
        except (IOError, csv.Error): 
            print(colored("ผิดพลาด: ไม่สามารถอ่านไฟล์โปรไฟล์ได้", "red")) 
  
    if profiles: 
        display_profiles() 
        choice = input(colored("\nป้อนหมายเลขของโปรไฟล์ที่คุณต้องการลบ: ", "yellow")) 
  
        if choice.isdigit() and int(choice) in range(1, len(profiles) + 1): 
            profile_name = profiles[int(choice) - 1][0] 
            if confirm_removal(profile_name): 
                remove_profile(profile_name) 
                print(colored(f"ลบโปรไฟล์ '{profile_name}' สำเร็จ", "green")) 
                input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
            else: 
                print(colored("ยกเลิกการลบโปรไฟล์", "yellow")) 
                input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
        else: 
            print(colored("ป้อนข้อมูลไม่ถูกต้อง ยกเลิกการลบโปรไฟล์", "red")) 
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
    else: 
        print(colored("ไม่มีโปรไฟล์ในระบบ ยกเลิกการลบโปรไฟล์", "red")) 
        input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
  
def play_game(difficulty, player_name): 
    secret_number = random.randint(1, 100) 
    attempts = 0 
    max_attempts = 0 
    additional_feature = '' 
  
    if difficulty == '1': 
        max_attempts = 10 
        additional_feature = "เพิ่มเติม: ปิดปรับปรุง!" 
    elif difficulty == '2': 
        max_attempts = 7 
        additional_feature = "เพิ่มเติม: ปิดปรับปรุง!" 
    elif difficulty == '3': 
        max_attempts = 5 
        additional_feature = "เพิ่มเติม: ปิดปรับปรุง!" 
  
    clear_console() 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
    print(colored("______________________________________________________", "cyan")) 
    print("พยากรณ์ตัวเลขลับ") 
    print("ความยาก:", colored(difficulty, "green")) 
    print(additional_feature) 
  
    while attempts < max_attempts: 
        user_guess = input("ทายตัวเลข: ") 
        attempts += 1 
        if user_guess == 'show': 
            print(f"ตัวเลขลับคือ: {secret_number}") 
            continue 
        try: 
            user_guess = int(user_guess) 
        except ValueError: 
            print(colored("ผิดพลาด: ป้อนข้อมูลไม่ถูกต้อง โปรดป้อนตัวเลข", "red")) 
            attempts -= 1 
            continue 
  
        if user_guess == secret_number: 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("ยินดีด้วย! คุณทายตัวเลขลับได้ถูกต้อง", "green")) 
            print("จำนวนครั้งที่เหลือ:", colored(max_attempts - attempts, "yellow")) 
            save_player_data(player_name, attempts, difficulty) 
            return attempts 
        elif user_guess < secret_number: 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("พยากรณ์ตัวเลขลับ") 
            print("ความยาก:", colored(difficulty, "green")) 
            print(additional_feature) 
            print(colored("ตัวเลขลับมากกว่า", "red")) 
        else: 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("พยากรณ์ตัวเลขลับ") 
            print("ความยาก:", colored(difficulty, "green")) 
            print(additional_feature) 
            print(colored("ตัวเลขลับน้อยกว่า", "red")) 
  
        if user_guess > 100 or user_guess < 1: 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("พยากรณ์ตัวเลขลับ") 
            print("ความยาก:", colored(difficulty, "green")) 
            print(additional_feature) 
            print("ตัวเลขควรอยู่ระหว่าง 1 ถึง 100 เท่านั้น ลองอีกครั้ง") 
            attempts -= 1 
  
        print("จำนวนครั้งที่เหลือ:", colored(max_attempts - attempts, "yellow")) 
  
    clear_console() 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("เกมจบลงแล้ว! คุณใช้จำนวนครั้งที่มีได้หมดแล้ว", "red")) 
    print("ตัวเลขลับคือ:", colored(secret_number, "blue")) 
    return 0 
  
def update_high_score(player_name, score, difficulty): 
    filename = "gamedata.csv" 
    file_exists = os.path.isfile(filename) 
  
    try: 
        with open(filename, 'a', newline='') as file: 
            writer = csv.writer(file) 
            if not file_exists: 
                writer.writerow(['Name', 'Score', 'Difficulty']) 
            writer.writerow([player_name, score, difficulty]) 
    except (IOError, csv.Error): 
        print(colored("ผิดพลาด: ไม่สามารถอัปเดตคะแนนสูงสุดได้", "red")) 
  
def show_high_score(difficulty): 
    filename = "gamedata.csv" 
    high_scores = [] 
  
    try: 
        if os.path.isfile(filename): 
            with open(filename, 'r') as file: 
                reader = csv.reader(file) 
                high_scores = list(reader) 
    except IOError: 
        print(colored("ผิดพลาด: ไม่สามารถอ่านไฟล์คะแนนสูงสุดได้", "red")) 
  
    clear_console() 
    print(colored("______________________________________________________", "cyan")) 
    print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
    print(colored("______________________________________________________", "cyan")) 
    print(f"คะแนนสูงสุดสำหรับความยาก {difficulty}:") 
    if high_scores: 
        print(colored("ชื่อ  |  คะแนน", "cyan")) 
        for score in high_scores: 
            if score[2] == difficulty: 
                print(f"{score[0]}  |  {score[1]}") 
    else: 
        print(colored("ไม่มีคะแนนสูงสุดที่ใช้ได้", "yellow")) 
  
def save_player_data(player_name, score, difficulty): 
    filename = "gamedata.csv" 
    file_exists = os.path.isfile(filename) 
  
    try: 
        with open(filename, 'a', newline='') as file: 
            writer = csv.writer(file) 
            if not file_exists: 
                writer.writerow(['Name', 'Score', 'Difficulty']) 
            writer.writerow([player_name, score, difficulty]) 
    except (IOError, csv.Error): 
        print(colored("ผิดพลาด: ไม่สามารถบันทึกข้อมูลผู้เล่นได้", "red")) 
  
def start_game(): 
    player_name = login_or_signin() 
  
    while True: 
        choice = main_menu(player_name) 
  
        if choice == '1': 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("เลือกระดับความยาก:") 
            print(colored("1. ง่าย", "green")) 
            print(colored("2. ปานกลาง", "yellow")) 
            print(colored("3. ยาก", "red")) 
            difficulty = input("\nเลือกตัวเลือกของคุณ (1-3): ") 
            score = play_game(difficulty, player_name) 
            if score > 0: 
                update_high_score(player_name, score, difficulty) 
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
        elif choice == '2': 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("คะแนนสูงสุด:") 
            print(colored("1. ง่าย", "green")) 
            print(colored("2. ปานกลาง", "yellow")) 
            print(colored("3. ยาก", "red")) 
            difficulty = input("\nป้อนระดับความยากเพื่อดูคะแนนสูงสุด (1-3): ") 
            show_high_score(difficulty) 
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan")) 
        elif choice == '3': 
            clear_console() 
            print(colored("______________________________________________________", "cyan")) 
            print(colored("           ยินดีต้อนรับสู่เกมทายตัวเลข!", "yellow")) 
            print(colored("______________________________________________________", "cyan")) 
            print("ขอบคุณที่เล่น เดี๋ยวพบกันอีกนะ!") 
            break 
        elif choice == '4': 
            remove_profile_prompt() 
  
start_game()
  
