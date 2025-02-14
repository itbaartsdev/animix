import requests
import json
from datetime import datetime
from colorama import init, Fore, Style
import base64
import os
import time

init()  # Inisialisasi colorama

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def key_bot():
    api = "https://raw.githubusercontent.com/itbaartsdev/base_nft/refs/heads/main/my.json"
    try:
        response = requests.get(api)
        response.raise_for_status()
        try:
            data = response.json()
            header = data['header']
            print('\033[96m' + header + '\033[0m')
        except json.JSONDecodeError:
            print('\033[96m' + response.text + '\033[0m')
    except requests.RequestException as e:
        print('\033[96m' + f"Failed to load header: {e}" + '\033[0m')

class AnimixBot:
    def __init__(self, query):
        self.base_url = "https://pro-api.animix.tech/public"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://tele-game.animix.tech",
            "referer": "https://tele-game.animix.tech/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors", 
            "sec-fetch-site": "same-site",
            "tg-init-data": query,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_user_info(self):
        """Mendapatkan informasi user"""
        endpoint = "/user/info"
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers
        )
        return response.json()

    def claim_bonus(self):
        """Mengklaim bonus DNA gacha"""
        endpoint = "/pet/dna/gacha/bonus"
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers
        )
        return response.json()

    def daily_checkin(self):
        """Melakukan daily check-in"""
        endpoint = "/quest/check"
        payload = {"quest_code": "CHECK_IN"}
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def do_quest(self, quest_code):
        """Melakukan quest dengan kode tertentu"""
        endpoint = "/quest/check"
        payload = {"quest_code": quest_code}
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def get_quest_list(self):
        """Mendapatkan daftar quest yang tersedia"""
        endpoint = "/quest/list"
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers
        )
        return response.json()

    def print_user_info(self, data):
        """Mencetak informasi user dengan format yang rapi"""
        result = data['result']
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[USER INFORMATION]")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"User ID       : {result['telegram_id']}")
        print(f"Username      : @{result['telegram_username']}")
        print(f"Nama Lengkap  : {result['full_name']}")
        print(f"Level         : {result['level']}")
        print(f"Token         : {result['token']}")
        print(f"God Power     : {result['god_power']}")

    def print_bonus_info(self, data):
        """Mencetak informasi bonus dengan format yang rapi"""
        result = data['result']
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[BONUS INFORMATION]")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"Season ID     : {result['season_id']}")
        print(f"DNA ID        : {result['dna_id']}")
        print(f"God Power     : {result['god_power_bonus']}")
        print(f"Progress      : {result['current_step']}/{result['total_step']}")
        
        status_gp = "[CLAIMED]" if result['is_claimed_god_power'] else "[NOT CLAIMED]"
        status_dna = "[CLAIMED]" if result['is_claimed_dna'] else "[NOT CLAIMED]"
        print(f"GP Status     : {status_gp}")
        print(f"DNA Status    : {status_dna}")

    def print_checkin_info(self, data):
        """Mencetak informasi check-in dengan format yang rapi"""
        result = data['result']
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[DAILY CHECK-IN]")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        status = "[SUCCESS]" if result['status'] else "[FAILED]"
        print(f"Status        : {status}")
        
        if result['token'] > 0:
            pass 
                        
        if result['other_rewards']:
            print(f"\n{Fore.GREEN}[ADDITIONAL REWARDS]{Style.RESET_ALL}")
            for reward in result['other_rewards']:
                print(f"|-- {reward['name']}: +{reward['amount']}")

    def print_quest_info(self, data, quest_name):
        """Mencetak informasi quest dengan format yang rapi"""
        result = data['result']
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[{quest_name}]")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        status = "[SUCCESS]" if result['status'] else "[FAILED]"
        print(f"Status        : {status}")
        
        if result['token'] > 0:
            print(f"Token         : +{result['token']}")
            
        if result['other_rewards']:
            print(f"\n{Fore.GREEN}[ADDITIONAL REWARDS]{Style.RESET_ALL}")
            for reward in result['other_rewards']:
                print(f"|-- {reward['name']}: +{reward['amount']}")

    def print_quest_list(self, data):
        """Mencetak daftar quest dengan format yang rapi"""
        if not isinstance(data, dict) or 'result' not in data:
            print(f"{Fore.RED}[ERROR] Format data quest tidak valid{Style.RESET_ALL}")
            return
        
        result = data['result']
        if 'quests' not in result:
            print(f"{Fore.RED}[ERROR] Tidak ada data quest{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[QUEST LIST]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}")
        
        for quest in result['quests']:
            status = f"{Fore.GREEN}[COMPLETED]" if quest['status'] else f"{Fore.RED}[AVAILABLE]"
            print(f"\n{status} {quest['title']}{Style.RESET_ALL}")
            
            # Tampilkan rewards jika ada
            if quest.get('rewards'):
                print(f"{Fore.CYAN}[REWARDS]{Style.RESET_ALL}")
                for reward in quest['rewards']:
                    print(f"|-- {reward.get('name', 'Unknown')}: {reward.get('amount', 0)}")
                
            # Tampilkan token jika ada
            if quest.get('token', 0) > 0:
                print(f"|-- Token: {quest['token']}")
            
            # Tampilkan link jika ada
            if quest.get('link'):
                print(f"|-- Link: {quest['link']}")
            
            # Tampilkan platform jika ada
            if quest.get('platform'):
                print(f"|-- Platform: {quest['platform']}")

    def mix_pet(self, dad_id, mom_id):
        """Melakukan mix pet"""
        endpoint = "/pet/mix"
        payload = {
            "dad_id": dad_id,
            "mom_id": mom_id
        }
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def print_mix_result(self, data):
        """Mencetak hasil mix pet"""
        if data.get('error_code') is not None:
            print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL}")
            print(f"Message: {data.get('message', 'Unknown error')}")
            return
        
        result = data.get('result')
        if not result:
            print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL}")
            print("No result data received")
            return
        
        pet = result['pet']
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[MIX PET RESULT]{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}{pet['name']} - {pet['class']}{Style.RESET_ALL}")
        print(f"|-- HP     : {pet['hp']}")
        print(f"|-- Damage : {pet['damage']}")
        print(f"|-- Speed  : {pet['speed']}")
        print(f"|-- Star   : {'⭐' * int(pet['star'])}")
        
        if 'dna' in result:
            print(f"\n{Fore.YELLOW}[AVAILABLE DNA]{Style.RESET_ALL}")
            for dna in result['dna']:
                can_mom = "[Can Mom]" if dna['can_mom'] else "[Can't Mom]"
                print(f"\n{dna['name']} - {dna['class']} ({can_mom})")
                print(f"|-- Amount : {dna['amount']}")
                print(f"|-- Star   : {'⭐' * int(dna['star'])}")

    def get_pet_list(self):
        """Mendapatkan daftar pet yang tersedia"""
        user_info = self.get_user_info()
        return user_info['result']['welcome_pets']

    def print_pet_list(self, pets):
        """Mencetak daftar pet dengan format yang rapi"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[AVAILABLE PETS]{Style.RESET_ALL}")
        
        for pet in pets:
            print(f"\n{Fore.GREEN}{pet['name']} - Class {pet['class']}{Style.RESET_ALL}")
            print(f"|-- Pet ID  : {pet['pet_id']}")
            print(f"|-- HP      : {pet['hp']}")
            print(f"|-- Damage  : {pet['damage']}")
            print(f"|-- Speed   : {pet['speed']}")
            print(f"|-- Star    : {'⭐' * int(pet['star'])}")

    def do_gacha(self, amount):
        """Melakukan gacha DNA"""
        endpoint = "/pet/dna/gacha"
        payload = {"amount": amount}
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def get_gacha_bonus(self):
        """Mendapatkan informasi bonus gacha"""
        endpoint = "/pet/dna/gacha/bonus"
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers
        )
        return response.json()

    def print_gacha_result(self, data):
        """Mencetak hasil gacha"""
        if data.get('error_code') is not None:
            print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL}")
            print(f"Message: {data.get('message', 'Unknown error')}")
            return
            
        result = data.get('result')
        if not result:
            print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL}")
            print("No result data received")
            return
            
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}[GACHA RESULT]{Style.RESET_ALL}")
        print(f"God Power: {result['god_power']}")
        
        print(f"\n{Fore.GREEN}[DNA OBTAINED]{Style.RESET_ALL}")
        for dna in result['dna']:
            stars = '⭐' * int(dna['star'])
            can_mom = "[Can Mom]" if dna['can_mom'] else "[Can't Mom]"
            print(f"\n{dna['name']} - {dna['class']} {stars}")
            print(f"|-- Star    : {dna['star']}")
            print(f"|-- Status  : {can_mom}")

    def get_achievement_list(self):
        """Mengambil daftar achievement"""
        try:
            response = requests.get(
                f"{self.base_url}/achievement/list",
                headers=self.headers
            )
            return response.json()
        except Exception as e:
            print(f"\n{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            return None

    def claim_achievement(self, quest_id):
        """Klaim achievement"""
        try:
            payload = {
                "quest_id": quest_id
            }
            response = requests.post(
                f"{self.base_url}/achievement/claim",
                headers=self.headers,
                json=payload
            )
            return response.json()
        except Exception as e:
            print(f"\n{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            return None

    def get_mission_list(self):
        """Get available missions"""
        endpoint = "/mission/list"
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers
        )
        return response.json()

    def enter_mission(self, mission_id, pet_joined):
        """Enter mission with previously used pets"""
        try:
            if not isinstance(pet_joined, list) or len(pet_joined) != 3:
                print(f"{Fore.RED}[ERROR] Data pet tidak valid{Style.RESET_ALL}")
                return False
            
            # Pastikan setiap pet memiliki pet_id
            pet_ids = []
            for pet in pet_joined:
                if isinstance(pet, dict) and 'pet_id' in pet:
                    pet_ids.append(pet['pet_id'])
                else:
                    print(f"{Fore.RED}[ERROR] Format data pet tidak valid{Style.RESET_ALL}")
                    return False
            
            payload = {
                "mission_id": str(mission_id),  # Konversi ke string
                "pet_1_id": str(pet_ids[0]),    # Konversi ke string
                "pet_2_id": str(pet_ids[1]),    # Konversi ke string
                "pet_3_id": str(pet_ids[2])     # Konversi ke string
            }
            
            response = self.session.post(
                f"{self.base_url}/mission/enter",
                json=payload
            )
            
            data = response.json()
            
            # Cek pesan error spesifik
            if 'error_code' in data:
                error_msg = data.get('message', 'Unknown error')
                print(f"{Fore.YELLOW}[INFO] {error_msg}{Style.RESET_ALL}")
                return False
            
            if data and 'result' in data:
                result = data['result']
                print(f"{Fore.GREEN}[SUCCESS] Berhasil memasuki misi!{Style.RESET_ALL}")
                print(f"Mission ID: {result['mission_id']}")
                print(f"Waktu mulai: {datetime.fromtimestamp(result['mission_time'])}")
                print(f"Waktu selesai: {datetime.fromtimestamp(result['end_time'])}")
                return True
            else:
                print(f"{Fore.RED}[ERROR] Gagal memasuki misi{Style.RESET_ALL}")
                if 'message' in data:
                    print(f"Pesan: {data['message']}")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            return False

    def claim_mission(self, mission_id):
        """Claim mission rewards"""
        try:
            payload = {"mission_id": mission_id}
            response = self.session.post(
                f"{self.base_url}/mission/claim",
                json=payload
            )
            
            if not response.ok:
                print(f"{Fore.RED}[ERROR] Failed to claim mission! Status code: {response.status_code}{Style.RESET_ALL}")
                return False
            
            data = response.json()
            
            if not data or not isinstance(data, dict):
                print(f"{Fore.RED}[ERROR] Invalid response data{Style.RESET_ALL}")
                return False
            
            result = data.get('result')
            if not result or not isinstance(result, dict):
                error_msg = data.get('message', 'Unknown error')
                print(f"{Fore.RED}[ERROR] {error_msg}{Style.RESET_ALL}")
                return False
            
            if result.get('status'):
                print(f"{Fore.GREEN}[SUCCESS] Mission claimed successfully!{Style.RESET_ALL}")
                
                # Display token reward
                token = result.get('token', 0)
                if token > 0:
                    print(f"Token received: {token}")
                
                # Display other rewards safely
                other_rewards = result.get('other_rewards', [])
                if other_rewards and isinstance(other_rewards, list):
                    print("\nAdditional rewards:")
                    for reward in other_rewards:
                        if isinstance(reward, dict):
                            reward_name = reward.get('name', 'Unknown')
                            reward_amount = reward.get('amount', 0)
                            reward_id = reward.get('id', 'N/A')
                            
                            # Map reward IDs to names if name is not provided
                            if reward_name == 'Unknown':
                                reward_name = {
                                    0: 'TOKEN',
                                    1: 'GOD_POWER',
                                    1001: 'Earth DNA',
                                    2001: 'Wind DNA',
                                    3001: 'Water DNA'
                                }.get(reward_id, 'Unknown')
                            
                            print(f"- {reward_name}: {reward_amount}")
                return True
            else:
                print(f"{Fore.RED}[ERROR] Failed to claim mission!{Style.RESET_ALL}")
                if data.get('message'):
                    print(f"Message: {data['message']}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            return False

    def check_and_claim_missions(self):
        """Check and claim completed missions"""
        try:
            # Get mission list
            response = self.session.get(f"{self.base_url}/mission/list")
            if not response.ok:
                print(f"{Fore.RED}[ERROR] Failed to get mission list{Style.RESET_ALL}")
                return
            
            data = response.json()
            if not data or 'result' not in data:
                print(f"{Fore.RED}[ERROR] Invalid mission data{Style.RESET_ALL}")
                return
            
            missions = data['result']
            if not missions:
                print("No missions available")
                return
            
            print(f"\n{Fore.CYAN}[CHECKING MISSIONS]{Style.RESET_ALL}\n")
            
            current_time = int(time.time())
            
            for mission in missions:
                if not isinstance(mission, dict):
                    continue
                
                mission_id = mission.get('mission_id')
                end_time = mission.get('end_time', 0)
                pet_joined = mission.get('pet_joined', [])
                
                # Check if mission is completed (end time has passed)
                if current_time >= end_time:
                    print(f"\nClaiming mission {mission_id}...")
                    
                    # Store pet IDs before claiming
                    pet_ids = []
                    if len(pet_joined) == 3:
                        for pet in pet_joined:
                            if isinstance(pet, dict) and 'pet_id' in pet:
                                pet_ids.append(str(pet['pet_id']))
                    
                    # Claim mission rewards
                    claim_payload = {"mission_id": str(mission_id)}
                    claim_response = self.session.post(
                        f"{self.base_url}/mission/claim",
                        json=claim_payload
                    )
                    
                    if claim_response.ok:
                        claim_data = claim_response.json()
                        if claim_data.get('result', {}).get('status'):
                            print(f"{Fore.GREEN}[SUCCESS] Mission {mission_id} claimed!{Style.RESET_ALL}")
                            
                            # Re-enter mission with stored pet IDs
                            if len(pet_ids) == 3:
                                enter_payload = {
                                    "mission_id": str(mission_id),
                                    "pet_1_id": pet_ids[0],
                                    "pet_2_id": pet_ids[1],
                                    "pet_3_id": pet_ids[2]
                                }
                                
                                print(f"Re-entering mission {mission_id} with previous pets...")
                                enter_response = self.session.post(
                                    f"{self.base_url}/mission/enter",
                                    json=enter_payload
                                )
                                
                                if enter_response.ok:
                                    enter_data = enter_response.json()
                                    if enter_data.get('result'):
                                        print(f"{Fore.GREEN}[SUCCESS] Re-entered mission {mission_id}{Style.RESET_ALL}")
                                    else:
                                        error_msg = enter_data.get('message', 'Unknown error')
                                        print(f"{Fore.RED}[ERROR] Failed to re-enter mission: {error_msg}{Style.RESET_ALL}")
                                else:
                                    print(f"{Fore.RED}[ERROR] Failed to re-enter mission: Network error{Style.RESET_ALL}")
                            
                            time.sleep(1)  # Delay between missions
                        else:
                            print(f"{Fore.YELLOW}[INFO] Mission {mission_id} not ready to claim{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[ERROR] Failed to claim mission {mission_id}{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

def print_status(message, status_type="info"):
    """Menampilkan pesan status dengan warna yang sesuai"""
    colors = {
        "success": Fore.GREEN,
        "error": Fore.RED,
        "info": Fore.YELLOW,
        "process": Fore.CYAN
    }
    color = colors.get(status_type, Fore.WHITE)
    print(f"{color}{message}{Style.RESET_ALL}")

def countdown_timer(seconds):
    """Display countdown timer dengan tampilan yang lebih menarik"""
    try:
        while seconds:
            minutes, secs = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            timer = f'{hours:02d}:{minutes:02d}:{secs:02d}'
            print(f"\r{Fore.CYAN}[{Fore.YELLOW}⏳ Next Check{Fore.CYAN}] {Fore.WHITE}{timer}", end='')
            time.sleep(1)
            seconds -= 1
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Countdown interrupted by user{Style.RESET_ALL}")
        raise KeyboardInterrupt

def auto_quest_and_mission(bot):
    """Run auto quest, mission, and achievement checker"""
    while True:
        try:
            queries = load_queries()
            if not queries:
                print(f"{Fore.RED}[ERROR] No valid queries found in query.txt. Exiting...{Style.RESET_ALL}")
                return

            while True:
                clear_screen()
                key_bot()  # Menggunakan key_bot() alih-alih print_banner()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n{Fore.CYAN}Starting check at: {current_time}{Style.RESET_ALL}")
                
                # Process each account
                for query in queries:
                    bot = AnimixBot(query)
                    
                    # Get user info
                    user_info = bot.get_user_info()
                    if user_info.get('result'):
                        print(f"\n{Fore.CYAN}{'='*50}")
                        print(f"{Fore.YELLOW}Processing account: @{user_info['result']['telegram_username']}{Style.RESET_ALL}")
                        
                        # Run auto achievement
                        print(f"\n{Fore.CYAN}[CHECKING ACHIEVEMENTS]{Style.RESET_ALL}")
                        try:
                            achievements = bot.get_achievement_list()
                            if isinstance(achievements, dict) and achievements.get('result'):
                                for achievement in achievements['result']:
                                    if isinstance(achievement, dict) and achievement.get('can_claim'):
                                        print(f"\nClaiming achievement: {achievement.get('title', 'Unknown')}")
                                        claim_result = bot.claim_achievement(achievement['achievement_id'])
                                        if isinstance(claim_result, dict) and claim_result.get('result'):
                                            print(f"{Fore.GREEN}[SUCCESS] Achievement claimed!{Style.RESET_ALL}")
                                            rewards = claim_result['result'].get('rewards', [])
                                            for reward in rewards:
                                                if isinstance(reward, dict):
                                                    print(f"- {reward.get('name', 'Unknown')}: +{reward.get('amount', 0)}")
                                        time.sleep(1)
                        except Exception as e:
                            print(f"{Fore.RED}[ERROR] Achievement check failed: {str(e)}{Style.RESET_ALL}")
                        
                        # Run auto quest
                        print(f"\n{Fore.CYAN}[CHECKING QUESTS]{Style.RESET_ALL}")
                        quest_list = bot.get_quest_list()
                        bot.print_quest_list(quest_list)
                        
                        # Get dan tampilkan bonus
                        bonus = bot.claim_bonus()
                        bot.print_bonus_info(bonus)
                        
                        # Run available quests
                        if isinstance(quest_list, dict) and quest_list.get('result'):
                            available_quests = [
                                quest for quest in quest_list['result']['quests']
                                if not quest['status'] and not quest['is_disabled']
                            ]
                            
                            for quest in available_quests:
                                quest_result = bot.do_quest(quest['quest_code'])
                                bot.print_quest_info(quest_result, quest['title'])
                                time.sleep(1)
                        
                        # Run auto mission
                        print(f"\n{Fore.CYAN}[CHECKING MISSIONS]{Style.RESET_ALL}")
                        bot.check_and_claim_missions()
                        
                    time.sleep(2)
                
                print(f"\n{Fore.CYAN}{'='*50}")
                print(f"{Fore.YELLOW}[WAITING FOR NEXT CHECK]{Style.RESET_ALL}")
                countdown_timer(3600)
                print()
                
        except Exception as e:
            print(f"\n{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Restarting in 5 seconds...{Style.RESET_ALL}")
            time.sleep(5)
            continue
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Bot stopped by user{Style.RESET_ALL}")
            return

def load_queries():
    """Load multiple queries from query.txt file"""
    queries = []
    try:
        with open('query.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    queries.append(line)
        return queries
    except FileNotFoundError:
        print(f"\n{Fore.RED}[ERROR] query.txt file not found!{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Failed to load queries: {str(e)}{Style.RESET_ALL}")
        return []

def main():
    try:
        print(f"\n{Fore.CYAN}Starting Auto Quest, Mission & Achievement...{Style.RESET_ALL}")
        auto_quest_and_mission(None)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Bot stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
