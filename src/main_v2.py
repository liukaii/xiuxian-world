import os
import sys
import json
import random
from datetime import datetime

# 璁剧疆UTF-8缂栫爜锛圵indows鍏煎锛?import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 娣诲姞褰撳墠鐩綍鍒拌矾寰?sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import GameConfig
from character import Character
from world import World

class Game:
    """娓告垙涓荤被"""
    
    def __init__(self):
        self.player = None
        self.world = None
        self.running = False
        self.mode = None  # 'player' 鎴?'god'
        self.player_id = None  # 鐜╁瑙掕壊鍚嶇О锛堢敤浜庡瓨妗ｏ級
        
        # 瀛樻。鐩綍
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
        self.world_save_dir = os.path.join(os.path.dirname(__file__), "..", "world_data")
        
        # 纭繚瀛樻。鐩綍瀛樺湪
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        if not os.path.exists(self.world_save_dir):
            os.makedirs(self.world_save_dir)
        
        # 鍔犺浇鎴栧垱寤轰笘鐣?        self._load_or_create_world()
    
    def _load_or_create_world(self):
        """鍔犺浇鎴栧垱寤轰笘鐣?""
        world_file = os.path.join(self.world_save_dir, "world.json")
        
        if os.path.exists(world_file):
            # 鍔犺浇鐜版湁涓栫晫
            with open(world_file, 'r', encoding='utf-8') as f:
                world_data = json.load(f)
            self.world = World()
            self.world.day = world_data.get('day', 1)
            self.world.year = world_data.get('year', 1)
            self.world.season = world_data.get('season', '鏄?)
            self.world.weather = world_data.get('weather', '鏅存湕')
            print("[绯荤粺] 宸插姞杞界幇鏈変笘鐣?)
        else:
            # 鍒涘缓鏂颁笘鐣?            self.world = World()
            print("[绯荤粺] 宸插垱寤烘柊涓栫晫")
    
    def _save_world(self):
        """淇濆瓨涓栫晫鐘舵€?""
        world_file = os.path.join(self.world_save_dir, "world.json")
        world_data = {
            'day': self.world.day,
            'year': self.world.year,
            'season': self.world.season,
            'weather': self.world.weather,
            'saved_at': datetime.now().isoformat()
        }
        with open(world_file, 'w', encoding='utf-8') as f:
            json.dump(world_data, f, ensure_ascii=False, indent=2)
    
    def clear_screen(self):
        """娓呭睆"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """鎵撳嵃娓告垙鏍囬"""
        title = """
鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?鈺?                                                              鈺?鈺?             鈿旓笍  淇?浠?涓?鐣? 鈿旓笍                              鈺?鈺?                                                              鈺?鈺?             Xiuxian World - A Cultivation Journey          鈺?鈺?                                                              鈺?鈺氣晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?"""
        print(title)
    
    def get_input(self, prompt: str = "") -> str:
        """鑾峰彇鐢ㄦ埛杈撳叆"""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def select_mode(self):
        """閫夋嫨娓告垙妯″紡"""
        self.clear_screen()
        self.print_title()
        
        print("\n銆愰€夋嫨妯″紡銆?)
        print("1. 馃幃 鐜╁妯″紡 - 鎵紨涓€鍚嶄慨澹慨浠?)
        print("2. 馃憗锔? 澶╅亾妯″紡 - 鏌ョ湅鎵€鏈変慨澹俊鎭?)
        print("3. 馃毆 閫€鍑?)
        print()
        
        choice = self.get_input("璇烽€夋嫨 (1-3): ")
        
        if choice == "1":
            self.mode = "player"
            self.player_mode_menu()
        elif choice == "2":
            self.mode = "god"
            self.god_mode()
        elif choice == "3":
            print("\n鎰熻阿娓哥帺锛岀閬撳弸浠欑紭娣卞帤锛?)
            return False
        
        return True
    
    def player_mode_menu(self):
        """鐜╁妯″紡鑿滃崟"""
        while True:
            self.clear_screen()
            self.print_title()
            
            print("\n銆愮帺瀹舵ā寮忋€?)
            print("1. 馃啎 鍒涘缓鏂拌鑹?)
            print("2. 馃搨 鍔犺浇宸叉湁瑙掕壊")
            print("3. 馃敊 杩斿洖")
            print()
            
            choice = self.get_input("璇烽€夋嫨 (1-3): ")
            
            if choice == "1":
                self.create_new_player()
                break
            elif choice == "2":
                if self.load_player():
                    break
            elif choice == "3":
                return
    
    def create_new_player(self):
        """鍒涘缓鏂扮帺瀹惰鑹?""
        self.clear_screen()
        self.print_title()
        
        print("\n銆愬垱寤鸿鑹层€慭n")
        print("姝ｅ湪涓轰綘鐢熸垚淇粰璧勮川...\n")
        
        self.player = Character(is_player=True)
        self.player_id = self.player.name
        
        print("鉁?浣犵殑淇粰涔嬭矾鍗冲皢寮€濮嬶紒\n")
        print(self.player.get_status())
        print("\n鐏垫牴鍝佽川鍐冲畾浜嗕綘鐨勪慨鐐奸€熷害锛?)
        print(f"  {self.player.spirit_root}")
        
        # 淇濆瓨鏂拌鑹?        self._save_player()
        
        input("\n鎸夊洖杞︾户缁?..")
        self.player_game_loop()
    
    def load_player(self):
        """鍔犺浇宸叉湁瑙掕壊"""
        # 鑾峰彇鎵€鏈夊瓨妗?        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                saves.append(filename[:-5])  # 鍘绘帀.json
        
        if not saves:
            print("\n娌℃湁鍙敤鐨勫瓨妗ｏ紒")
            input("鎸夊洖杞︾户缁?..")
            return False
        
        print("\n銆愰€夋嫨瑙掕壊銆?)
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save}")
        print(f"{len(saves)+1}. 杩斿洖")
        
        choice = self.get_input(f"\n璇烽€夋嫨 (1-{len(saves)+1}): ")
        
        try:
            idx = int(choice) - 1
            if idx == len(saves):
                return False
            if 0 <= idx < len(saves):
                self.player_id = saves[idx]
                self._load_player()
                return True
        except:
            pass
        
        print("鏃犳晥閫夋嫨锛?)
        input("鎸夊洖杞︾户缁?..")
        return False
    
    def _save_player(self):
        """淇濆瓨鐜╁鏁版嵁"""
        if not self.player:
            return
        
        save_data = {
            "name": self.player.name,
            "age": self.player.age,
            "realm_level": self.player.realm_level,
            "realm_progress": self.player.realm_progress,
            "hp": self.player.hp,
            "max_hp": self.player.max_hp,
            "mp": self.player.mp,
            "max_mp": self.player.max_mp,
            "spirit_root": {
                "quality": self.player.spirit_root.quality,
                "elements": self.player.spirit_root.elements
            },
            "comprehension": self.player.comprehension,
            "luck": self.player.luck,
            "perception": self.player.perception,
            "karma": self.player.karma,
            "destiny": self.player.destiny,
            "spirit_stones": self.player.spirit_stones,
            "items": self.player.items,
            "skills": self.player.skills,
            "saved_at": datetime.now().isoformat()
        }
        
        filename = f"{self.player_id}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    def _load_player(self):
        """鍔犺浇鐜╁鏁版嵁"""
        filename = f"{self.player_id}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.player = Character(is_player=True)
        self.player.name = data['name']
        self.player.age = data['age']
        self.player.realm_level = data['realm_level']
        self.player.realm_progress = data['realm_progress']
        self.player.hp = data['hp']
        self.player.max_hp = data['max_hp']
        self.player.mp = data['mp']
        self.player.max_mp = data['max_mp']
        self.player.comprehension = data['comprehension']
        self.player.luck = data['luck']
        self.player.perception = data['perception']
        self.player.karma = data['karma']
        self.player.destiny = data['destiny']
        self.player.spirit_stones = data['spirit_stones']
        self.player.items = data['items']
        self.player.skills = data['skills']
        
        # 鎭㈠鐏垫牴
        self.player.spirit_root.quality = data['spirit_root']['quality']
        self.player.spirit_root.elements = data['spirit_root']['elements']
        
        print(f"\n鉁?宸插姞杞借鑹诧細{self.player.name}")
        input("鎸夊洖杞︾户缁?..")
        self.player_game_loop()
    
    def player_game_loop(self):
        """鐜╁娓告垙涓诲惊鐜?""
        self.running = True
        
        while self.running and self.player and self.player.is_alive:
            self.clear_screen()
            self.print_title()
            
            # 鏄剧ず鐘舵€?            print(self.world.get_world_status())
            print(self.player.get_status())
            
            # 鏄剧ず鑿滃崟
            print("\n銆愯鍔ㄣ€?)
            print("1. 馃 淇偧锛堟彁鍗囦慨涓猴級")
            print("2. 馃椇锔? 鎺㈢储锛堥殢鏈洪伃閬囷級")
            print("3. 馃捈 鐗╁搧锛堟煡鐪嬭儗鍖咃級")
            print("4. 馃捑 淇濆瓨骞堕€€鍑?)
            print()
            
            choice = self.get_input("璇烽€夋嫨琛屽姩 (1-4): ")
            
            if choice == "1":
                self.action_cultivate()
            elif choice == "2":
                self.action_explore()
            elif choice == "3":
                self.action_inventory()
            elif choice == "4":
                self._save_player()
                self._save_world()
                print("\n鉁?娓告垙宸蹭繚瀛橈紒")
                input("鎸夊洖杞﹂€€鍑?..")
                self.running = False
            else:
                print("鏃犳晥閫夋嫨锛岃閲嶆柊杈撳叆")
                input("鎸夊洖杞︾户缁?..")
        
        # 娓告垙缁撴潫
        if self.player and not self.player.is_alive:
            self.game_over()
    
    def action_cultivate(self):
        """淇偧琛屽姩"""
        print("\n銆愪慨鐐笺€?)
        print("1. 淇偧1澶?)
        print("2. 淇偧10澶?)
        print("3. 淇偧30澶?)
        print("4. 淇偧100澶?)
        print("5. 杩斿洖")
        
        choice = self.get_input("閫夋嫨淇偧鏃堕暱: ")
        days_map = {"1": 1, "2": 10, "3": 30, "4": 100}
        
        if choice in days_map:
            days = days_map[choice]
            print(f"\n浣犲紑濮嬮棴鍏充慨鐐?..")
            
            # 鎵ц淇偧
            for _ in range(days):
                result = self.player.cultivate(1)
                self.world.advance_time(1)
                
                # 鏄剧ず閲嶈娑堟伅
                for msg in result["messages"]:
                    if "绐佺牬" in msg or "瀵垮厓鑰楀敖" in msg:
                        print(msg)
            
            print(f"\n鉁?淇偧瀹屾垚锛佸叡淇偧{days}澶?)
            print(f"   褰撳墠淇负杩涘害: {self.player.realm_progress:.1f}%")
            input("\n鎸夊洖杞︾户缁?..")
    
    def action_explore(self):
        """鎺㈢储琛屽姩"""
        print("\n銆愭帰绱笘鐣屻€?)
        print("浣犺笍涓婁簡鎺㈢储涔嬫梾...\n")
        
        # 鎺ㄨ繘鏃堕棿
        self.world.advance_time(random.randint(1, 7))
        
        # 鎺㈢储浜嬩欢
        result = self.world.explore(self.player)
        
        for msg in result["messages"]:
            print(msg)
        
        input("\n鎸夊洖杞︾户缁?..")
    
    def action_inventory(self):
        """鏌ョ湅鐗╁搧"""
        print("\n銆愮墿鍝佹爮銆?)
        print(f"鐏电煶: {self.player.spirit_stones}")
        print(f"\n鐗╁搧 ({len(self.player.items)}浠?:")
        
        if self.player.items:
            for i, item in enumerate(self.player.items, 1):
                print(f"  {i}. {item['name']} ({item['grade']}) - {item['effect']}")
        else:
            print("  (绌?")
        
        print(f"\n鍔熸硶 ({len(self.player.skills)}闂?:")
        if self.player.skills:
            for skill in self.player.skills:
                print(f"  - {skill}")
        else:
            print("  (鏈涔?")
        
        input("\n鎸夊洖杞︾户缁?..")
    
    def game_over(self):
        """娓告垙缁撴潫"""
        self.clear_screen()
        print("""
鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?鈺?                                                              鈺?鈺?                   馃拃  閬?娑?韬?姝? 馃拃                        鈺?鈺?                                                              鈺?鈺氣晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?""")
        print(f"\n{self.player.name} 鍦?{self.player.age:.1f} 宀佹椂瀵垮厓鑰楀敖...")
        print(f"鏈€缁堝鐣? {self.player.get_realm_name()}")
        print(f"淇粰澶╂暟: {self.world.day} 澶?)
        print("\n淇粰涔嬭矾婕极锛屾潵鐢熷啀缁粰缂?..")
        
        input("\n鎸夊洖杞﹁繑鍥?..")
    
    def god_mode(self):
        """澶╅亾妯″紡锛堜笂甯濊瑙掞級"""
        self.clear_screen()
        self.print_title()
        
        print("\n銆愬ぉ閬撴ā寮?- 涓婂笣瑙嗚銆慭n")
        print(self.world.get_world_status())
        
        print("\n銆愭墍鏈変慨澹俊鎭€?)
        print("-" * 60)
        
        # 鏄剧ずAI淇＋
        alive_cultivators = [c for c in self.world.world_cultivators if c.is_alive]
        print(f"\nAI淇＋ ({len(alive_cultivators)}浜哄瓨娲?:")
        for i, cultivator in enumerate(alive_cultivators[:10], 1):
            print(f"{i}. {cultivator.name:<10} | {cultivator.get_realm_name():<8} | "
                  f"{cultivator.age:.1f}宀?| 鎴樺姏:{cultivator.get_power()}")
        
        if len(alive_cultivators) > 10:
            print(f"... 杩樻湁 {len(alive_cultivators)-10} 浜?)
        
        # 鏄剧ず鐜╁瀛樻。
        print(f"\n銆愮帺瀹跺瓨妗ｃ€?)
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                saves.append(filename[:-5])
        
        if saves:
            for save in saves:
                print(f"  - {save}")
        else:
            print("  (鏃犵帺瀹跺瓨妗?")
        
        print("\n銆愯繎鏈熶笘鐣屼簨浠躲€?)
        recent_events = self.world.get_recent_events(5)
        if recent_events:
            for event in recent_events:
                print(f"  - {event}")
        else:
            print("  鏆傛棤浜嬩欢")
        
        input("\n鎸夊洖杞﹁繑鍥?..")
    
    def run(self):
        """杩愯娓告垙"""
        while True:
            if not self.select_mode():
                break


def main():
    """涓诲嚱鏁?""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
