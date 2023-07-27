import random
import os
import csv
import time
from termcolor import colored

def get_main_directory():
    return os.path.dirname(os.path.abspath(__file__))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_profiles_file_path():
    return os.path.join(get_main_directory(), "profiles.csv")

def get_high_scores_file_path():
    return os.path.join(get_main_directory(), "gamedata.csv")

def check_dot(number):
    return number % 5 == 0

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def display_profiles():
    filename = get_profiles_file_path()
    profiles = []

    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                profiles = list(reader)
    except IOError:
        print(colored("ข้อผิดพลาด: ไม่สามารถอ่านไฟล์ข้อมูลผู้ใช้ได้..", "red"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print("โปรไฟล์ที่มีอยู่ในตอนนี้:")
    found = False
    if profiles:
        print(colored("ชื่อผู้ใช้งาน", "cyan"))
        for i, profile in enumerate(profiles, start=1):
            found = True
            print(f"{i}) {profile[0]}")
    if found == True:
        print("0) สร้างบัญชีใหม่")

def create_profile(name):
    filename = get_profiles_file_path()
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name])
    except IOError:
        print(colored("ข้อผิดพลาด: ไม่สามารถสร้าง โปรไฟล์ใหม่ได้", "red"))

def remove_profile(name):
    filename = get_profiles_file_path()
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
        print(colored("ข้อผิดพลาด: ไม่สามารถลบโปรไฟล์ได้", "red"))

def login_or_signin():
    display_profiles()

    if os.path.isfile(get_profiles_file_path()):
        choice = input(colored("\nพิมพ์ตัวเลขเพื่อเข้าสู่โปรไฟล์ของคุณ หรือพิมพ์เลข '0' เพื่อสร้างโปรไฟล์ใหม่: ", "yellow"))
        profiles_count = sum(1 for _ in open(get_profiles_file_path()))

        if choice.isdigit() and int(choice) in range(1, profiles_count + 1):
            try:
                with open(get_profiles_file_path(), 'r') as file:
                    reader = csv.reader(file)
                    profiles = list(reader)
                    return profiles[int(choice) - 1][0]
            except (IOError, csv.Error):
                print(colored("ข้อผิดพลาด: อ่านโปรไฟล์ไม่ได้", "red"))

    print(colored("คุณยังไม่เคยสร้างโปรไฟล์เลย", "red"))
    while True:
        name = input(colored("กรูราป้อนชื่อของคุณที่นี่: ", "yellow")).strip()
        if len(name) == 0:
            print(f"ชื่อเว้นว่างไม่ได้..")
        else:
            break
    create_profile(name)
    return name

def confirm_removal(name):
    confirm = input(colored(f"แน่ใจที่จะลบโปรไฟล์ '{name}' ใหม (Y/N): ", "yellow"))
    return confirm.lower() == 'y'

def remove_profile_prompt():
    profiles = []
    if os.path.isfile(get_profiles_file_path()):
        try:
            with open(get_profiles_file_path(), 'r') as file:
                reader = csv.reader(file)
                profiles = list(reader)
        except (IOError, csv.Error):
            print(colored("ข้อผิดพลาด: อ่านโปรไฟล์ไม่ได้..", "red"))

    if profiles:
        display_profiles()
        choice = input(colored("\nป้อนตัวเลขของชื่อที่คุณต้องการจะลบ โปรไฟล์ ", "yellow"))

        if choice.isdigit() and int(choice) in range(1, len(profiles) + 1):
            profile_name = profiles[int(choice) - 1][0]
            if confirm_removal(profile_name):
                remove_profile(profile_name)
                print(colored(f"โปรไฟล์ '{profile_name}' ถูกลบแล้ว", "green"))
                input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))
            else:
                print(colored("การลบโปรไฟล์ ถูกยกเลิก", "yellow"))
                input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))
        else:
            print(colored("อ่านข้อมูลที่ป้อนไม่ได้ การลบโปรไฟล์ ถูกยกเลิก", "red"))
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))
    else:
        print(colored("ไม่มีโปรไฟล์ให้ลบ..?", "red"))
        input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))

def play_game(difficulty, player_name):
    clear_console()
    debug = True
    print(f"กรุณารอตัวเลขลับสุ่ม..")
    time.sleep(0.2)
    secret_number = random.randint(1, 100)

    if difficulty == '1':
        while not check_dot(secret_number / 5):
            secret_number = random.randint(1, 100)
    elif difficulty == '2':
        while not check_dot(secret_number / 2):
            secret_number = random.randint(1, 100)
    elif difficulty == '3':
        while not is_prime(secret_number):
            secret_number = random.randint(1, 100)

    attempts = 0
    max_attempts = 0
    additional_feature = ''

    if difficulty == '1':
        max_attempts = 10
        additional_feature = "ตัวช่วย: ตัวเลขลับสามารถ หารด้วย 5 ลงตัว"
    elif difficulty == '2':
        max_attempts = 7
        additional_feature = "ตัวช่วย: ตัวเลขลับสามารถ หารด้วย 2 ลงตัว"
    elif difficulty == '3':
        max_attempts = 5
        additional_feature = "ตัวช่วย: ตัวเลขลับเป็น จำนวนเฉพาะ"

    difficulty_array = [colored('ง่าย', 'green'), colored('ปานกลาง', 'yellow'), colored('ยาก', 'red')]
    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print("กรุณาเดาตัวเลขลับ")
    print(f"ระดับความยาก: {difficulty_array[int(difficulty) - 1]}")
    print(additional_feature)

    while attempts < max_attempts:
        user_guess = input("ลองเดาตัวเลขสิ: ")
        attempts += 1

        if user_guess == 'show' and debug == True:
            print(f"ตัวเลขคือ: {colored(secret_number, 'green')}")
            continue

        try:
            user_guess = int(user_guess)
        except ValueError:
            print(colored("ข้อผิดพลาด: จำนวนไม่เป็นตัวเลข", "red"))
            continue

        if user_guess == secret_number:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print(colored("ยินดีด้วย! คุณทายตัวเลขลับถูกต้อง!", "green"))
            print("ความพยายามที่เหลือ: ", colored(max_attempts - attempts, "yellow"))
            save_player_data(player_name, attempts, difficulty)
            return attempts
        elif user_guess < secret_number:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("กรุณาเดาตัวเลขลับ")
            print("ระดับความยาก:", difficulty_array[int(difficulty) - 1])
            print(additional_feature)
            print(f'ตัวเลขลับ {colored("สูงกว่า", "red")} {colored(user_guess, "blue")}')
        else:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("กรุณาเดาตัวเลขลับ")
            print("ระดับความยาก:", colored(difficulty_array[int(difficulty) - 1], "green"))
            print(additional_feature)
            print(f'ตัวเลขลับ {colored("น้อยกว่า", "red")} {colored(user_guess, "blue")}')

        if user_guess > 100 or user_guess < 1:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("กรุณาเดาตัวเลขลับ")
            print(f"ระดับความยาก: {difficulty_array[int(difficulty) - 1]}")
            print(additional_feature)
            print("ตัวเลขต้องอยู่ใน 1-100")
            attempts -= 1

        print("ความพยายามที่เหลือ:", colored(max_attempts - attempts, "yellow"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(colored("เกมจบแล้ว! ความพยายามคงเหลือหมดแล้ว", "red"))
    print("ตัวเลขลับก็คือ ", colored(secret_number, "blue"))
    return 0

def update_high_score(player_name, score, difficulty):
    filename = get_high_scores_file_path()
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Score', 'Difficulty'])
            writer.writerow([player_name, score, difficulty])
    except (IOError, csv.Error):
        print(colored("ข้อผิดพลาด: แก้ไขข้อมูลโปรไฟล์ไม่ได้", "red"))

def show_high_score(difficulty):
    filename = get_high_scores_file_path()
    high_scores = []

    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                high_scores = list(reader)
    except IOError:
        print(colored("ข้อผิดพลาด: อ่านข้อมูลคะแนนไม่ได้", "red"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(f"คะแนนสูงสุดของโหมด {difficulty}:")
    if high_scores:
        print(colored("ชื่อ  |  คะแนน", "cyan"))
        for score in high_scores:
            if score[2] == difficulty:
                print(f"{score[0]}  |  {score[1]}")
    else:
        print(colored("ยังไม่มีคะแนนในโหมดนี้", "yellow"))

def save_player_data(player_name, score, difficulty):
    filename = get_high_scores_file_path()
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Score', 'Difficulty'])
            writer.writerow([player_name, score, difficulty])
    except (IOError, csv.Error):
        print(colored("ข้อผิดพลาด: บันทึกข้อมูลไม่ได้.", "red"))

def main_menu(player_name="nonPlayer"):
    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("          ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(f"คุณอยู่ในบัญชี: {player_name}")
    print("\nเลือกตัวเลือกของคุณ:")
    print(colored("1. เล่นเกม", "green"))
    print(colored("2. ดูคะแนนสูงสุด", "yellow"))
    print(colored("3. ออกเกม", "red"))
    choice = input("\nใส่ตัวเลือกของคุณ (1-3): ")
    return choice

def start_game():
    player_name = login_or_signin()

    while True:
        choice = main_menu(player_name)

        if choice == '1':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("เลือกระดับความยาก:")
            print(colored("1. ง่าย", "green"))
            print(colored("2. ปานกลาง", "yellow"))
            print(colored("3. ยาก", "red"))
            difficulty = input("\nตัวเลือกของคุณ (1-3): ")
            score = play_game(difficulty, player_name)
            if score > 0:
                update_high_score(player_name, score, difficulty)
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))
        elif choice == '2':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("คะแนนสูงสุดของ:")
            print(colored("1. โหมดง่าย", "green"))
            print(colored("2. โหมดปานกลาง", "yellow"))
            print(colored("3. โหมดยาก", "red"))
            difficulty = input("\nใส่โหมดที่ต้องการดูคะแนน (1-3): ")
            show_high_score(difficulty)
            input(colored("\nกด Enter เพื่อดำเนินการต่อ...", "cyan"))
        elif choice == '3':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           ยินดีต้อนรับสู่ เกมทายตัวเลข", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("ขอบคุณที่เข้ามาเล่นนะ Bye Bye!")
            break
        elif choice == '4':
            remove_profile_prompt()

try:
    start_game()
except KeyboardInterrupt:
    clear_console()
    print("เกมถูกปิดโดยกด 'Ctrl + C'")
