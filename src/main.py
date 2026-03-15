import os
import sys
import json
import random
from datetime import datetime

# 娣诲姞褰撳墠鐩綍鍒拌矾寰?sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import GameConfig, game_state
from character import Character
from world import World

class Game:
    """娓告垙涓荤被"""
    
    def __init__(self):
        self.player = None
        self.world = None
        self.running = False
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
        
        # 纭繚瀛樻。鐩綍瀛樺湪
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def clear_screen(self):
        """娓呭睆"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """鎵撳嵃娓告垙鏍囬"""
        title = """
鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?鈺?                                                              鈺?鈺?    鈿旓笍  淇?浠?涓?鐣? 鈿旓笍                                        鈺?鈺?                                                              鈺?鈺?    Xiuxian World - A Cultivation Journey                   鈺?鈺?                                                              鈺?鈺氣晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?"""
        print(title)
    
    def print_menu(self):
        """鎵撳嵃涓昏彍鍗?""
        print("\n銆愪富鑿滃崟銆?)
        print("1. 馃幃 寮€濮嬫柊娓告垙")
        print("2. 馃捑 璇诲彇瀛樻。")
        print("3. 馃摉 娓告垙璇存槑")
        print("4. 馃毆 閫€鍑烘父鎴?)
        print()
    
    def get_input(self, prompt: str = "") -> str:
        """鑾峰彇鐢ㄦ埛杈撳叆"""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def create_character(self) -> Character:
        """鍒涘缓瑙掕壊"""
        self.clear_screen()
        self.print_title()
        
        print("\n銆愬垱寤鸿鑹层€慭n")
        print("姝ｅ湪涓轰綘鐢熸垚淇粰璧勮川...\n")
        
        player = Character(is_player=True)
        
        print("鉁?浣犵殑淇粰涔嬭矾鍗冲皢寮€濮嬶紒\n")
        print(player.get_status())
        print("\n鐏垫牴鍝佽川鍐冲畾浜嗕綘鐨勪慨鐐奸€熷害锛?)
        print(f"  {player.spirit_root}")
        
        input("\n鎸夊洖杞︾户缁?..")
        return player
    
    def game_loop(self):
        """娓告垙涓诲惊鐜?""
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
            print("4. 馃摐 浜嬩欢锛堜笘鐣屽姩鎬侊級")
            print("5. 馃捑 瀛樻。")
            print("6. 馃毆 閫€鍑?)
            print()
            
            choice = self.get_input("璇烽€夋嫨琛屽姩 (1-6): ")
            
            if choice == "1":
                self.action_cultivate()
            elif choice == "2":
                self.action_explore()
            elif choice == "3":
                self.action_inventory()
            elif choice == "4":
                self.action_events()
            elif choice == "5":
                self.action_save()
            elif choice == "6":
                self.action_exit()
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
            print(f"   褰撳墠淇负杩涘害: {self.player.realm_progress}%")
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
    
    def action_events(self):
        """鏌ョ湅浜嬩欢"""
        print("\n銆愪笘鐣屼簨浠躲€?)
        
        recent_events = self.world.get_recent_events(10)
        if recent_events:
            for event in recent_events:
                print(f"  鈥?{event}")
        else:
            print("  杩戞湡娌℃湁閲嶅ぇ浜嬩欢")
        
        input("\n鎸夊洖杞︾户缁?..")
    
    def action_save(self):
        """瀛樻。"""
        print("\n銆愪繚瀛樻父鎴忋€?)
        
        save_data = {
            "player": {
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
                "skills": self.player.skills
            },
            "world": self.world.save(),
            "saved_at": datetime.now().isoformat()
        }
        
        filename = f"save_{self.player.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"鉁?娓告垙宸蹭繚瀛? {filename}")
        input("\n鎸夊洖杞︾户缁?..")
    
    def action_exit(self):
        """閫€鍑烘父鎴?""
        print("\n纭畾瑕侀€€鍑哄悧锛熸湭淇濆瓨鐨勮繘搴﹀皢涓㈠け銆?)
        print("1. 淇濆瓨骞堕€€鍑?)
        print("2. 鐩存帴閫€鍑?)
        print("3. 鍙栨秷")
        
        choice = self.get_input("閫夋嫨: ")
        
        if choice == "1":
            self.action_save()
            self.running = False
        elif choice == "2":
            self.running = False
    
    def game_over(self):
        """娓告垙缁撴潫"""
        self.clear_screen()
        print("""
鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?鈺?                                                              鈺?鈺?                   馃拃  閬?娑?韬?姝? 馃拃                        鈺?鈺?                                                              鈺?鈺氣晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?""")
        print(f"\n{self.player.name} 鍦?{self.player.age} 宀佹椂瀵垮厓鑰楀敖...")
        print(f"鏈€缁堝鐣? {self.player.get_realm_name()}")
        print(f"淇粰澶╂暟: {self.world.day} 澶?)
        print("\n淇粰涔嬭矾婕极锛屾潵鐢熷啀缁粰缂?..")
        
        input("\n鎸夊洖杞﹁繑鍥炰富鑿滃崟...")
    
    def show_help(self):
        """鏄剧ず娓告垙璇存槑"""
        self.clear_screen()
        self.print_title()
        
        help_text = """
銆愭父鎴忚鏄庛€?
馃幃 娓告垙鐩爣:
   鍦ㄨ繖涓慨浠欎笘鐣屼腑淇偧鎴愰暱锛岀獊鐮村鐣岋紝鏈€缁堥鍗囨垚浠欍€?
馃搳 鏍稿績灞炴€?
   鈥?澧冪晫: 鐐兼皵鈫掔瓚鍩衡啋閲戜腹鈫掑厓濠粹啋鍖栫鈫掔偧铏氣啋鍚堜綋鈫掑ぇ涔樷啋娓″姭鈫掔湡浠?   鈥?鐏垫牴: 鍐冲畾淇偧閫熷害锛堟贩娌岀伒鏍规渶浣筹紝浼伒鏍规渶宸級
   鈥?鎮熸€? 褰卞搷绐佺牬鎴愬姛鐜囧拰鍔熸硶瀛︿範
   鈥?鏈虹紭: 褰卞搷閬囧埌瀹濈墿鍜屽閬囩殑姒傜巼
   鈥?鍛芥牸: 褰卞搷鏁翠綋杩愬娍
   鈥?涓氬姏: 琛屽杽绉痉鍙鍔狅紝浣滄伓浼氬噺灏?
馃幆 娓告垙鐜╂硶:
   1. 淇偧: 鎻愬崌淇负锛岃揪鍒?00%鍙皾璇曠獊鐮村鐣?   2. 鎺㈢储: 闅忔満閬亣浜嬩欢銆佸疂鐗┿€佸鍏芥垨鍏朵粬淇＋
   3. 绠＄悊: 浣跨敤鐗╁搧銆佸涔犲姛娉曘€佺Н绱祫婧?
鈿狅笍 娉ㄦ剰浜嬮」:
   鈥?瀵垮厓鏈夐檺锛岃鍙婃椂绐佺牬澧冪晫寤堕暱瀵垮懡
   鈥?绐佺牬鏈夊け璐ラ闄╋紝鍑嗗鍏呭垎鍐嶅皾璇?   鈥?鎺㈢储鏈夐闄╋紝浣嗕篃鍙兘鑾峰緱澶ф満缂?   鈥?闅忔椂瀛樻。锛岄槻姝㈡剰澶?
绁濋亾鍙嬩慨浠欓『鍒╋紝鏃╂棩椋炲崌锛?"""
        print(help_text)
        input("鎸夊洖杞﹁繑鍥?..")
    
    def run(self):
        """杩愯娓告垙"""
        while True:
            self.clear_screen()
            self.print_title()
            self.print_menu()
            
            choice = self.get_input("璇烽€夋嫨 (1-4): ")
            
            if choice == "1":
                # 鏂版父鎴?                self.player = self.create_character()
                self.world = World()
                self.game_loop()
                
            elif choice == "2":
                # 璇诲彇瀛樻。
                print("\n銆愯鍙栧瓨妗ｃ€?)
                print("瀛樻。鍔熻兘寮€鍙戜腑...")
                input("鎸夊洖杞︾户缁?..")
                
            elif choice == "3":
                # 娓告垙璇存槑
                self.show_help()
                
            elif choice == "4":
                # 閫€鍑?                print("\n鎰熻阿娓哥帺锛岀閬撳弸浠欑紭娣卞帤锛?)
                break


def main():
    """涓诲嚱鏁?""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
