import random
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import GameConfig
from character import Character

class WorldEvent:
    """涓栫晫浜嬩欢"""
    
    def __init__(self, event_type: str, name: str, description: str):
        self.type = event_type
        self.name = name
        self.description = description
        self.timestamp = datetime.now()
    
    def __str__(self):
        return f"[{self.type}] {self.name}: {self.description}"


class World:
    """娓告垙涓栫晫"""
    
    def __init__(self):
        self.day = 1  # 娓告垙澶╂暟
        self.year = 1  # 娓告垙骞翠唤
        self.season = "鏄?  # 瀛ｈ妭
        self.weather = "鏅存湕"  # 澶╂皵
        
        # 涓栫晫鐘舵€?        self.world_cultivators = []  # 涓栫晫涓婄殑鍏朵粬淇＋
        self.events_history = []  # 浜嬩欢鍘嗗彶
        self.world_treasures = []  # 涓栫晫涓殑澶╂潗鍦板疂
        
        # 鐢熸垚鍒濆涓栫晫
        self._generate_world_cultivators(20)  # 鐢熸垚20涓垵濮嬩慨澹?        self._generate_world_treasures(10)  # 鐢熸垚10涓ぉ鏉愬湴瀹?    
    def _generate_world_cultivators(self, count: int):
        """鐢熸垚涓栫晫淇＋"""
        for _ in range(count):
            cultivator = Character(is_player=False)
            # 闅忔満鍒嗛厤澧冪晫锛堝ぇ閮ㄥ垎鍦ㄧ偧姘?閲戜腹锛?            realm_weights = [0.4, 0.3, 0.15, 0.08, 0.04, 0.02, 0.01, 0, 0, 0]
            cultivator.realm_level = random.choices(range(10), weights=realm_weights)[0]
            cultivator.realm_progress = random.randint(0, 80)
            cultivator.age = random.randint(20, cultivator.get_lifespan() - 20)
            self.world_cultivators.append(cultivator)
    
    def _generate_world_treasures(self, count: int):
        """鐢熸垚澶╂潗鍦板疂"""
        for _ in range(count):
            treasure = random.choice(GameConfig.TREASURES).copy()
            treasure["location"] = random.choice(GameConfig.REGIONS)["name"]
            treasure["found"] = False
            self.world_treasures.append(treasure)
    
    def advance_time(self, days: int = 1):
        """鎺ㄨ繘鏃堕棿"""
        self.day += days
        
        # 瀛ｈ妭鍙樺寲
        if self.day > 90:
            self.day = 1
            seasons = ["鏄?, "澶?, "绉?, "鍐?]
            current_idx = seasons.index(self.season)
            self.season = seasons[(current_idx + 1) % 4]
            
            if self.season == "鏄?:
                self.year += 1
        
        # 闅忔満澶╂皵鍙樺寲
        weathers = ["鏅存湕", "澶氫簯", "闃撮洦", "澶ч浘", "闆烽洦", "鐙傞"]
        self.weather = random.choice(weathers)
        
        # AI淇＋琛屽姩
        self._ai_cultivators_act(days)
        
        # 闅忔満鐢熸垚鏂颁簨浠?        if random.random() < 0.3:
            self._generate_random_event()
    
    def _ai_cultivators_act(self, days: int):
        """AI淇＋琛屽姩"""
        for cultivator in self.world_cultivators:
            if not cultivator.is_alive:
                continue
            
            # 绠€鍗旳I锛氬ぇ閮ㄥ垎鏃堕棿鍦ㄤ慨鐐?            if random.random() < 0.7:
                cultivator.cultivate(days)
            else:
                # 鎺㈢储鎴栧仛鍏朵粬浜嬫儏
                pass
            
            # 妫€鏌ユ浜?            if cultivator.age >= cultivator.get_lifespan():
                cultivator.is_alive = False
                event = WorldEvent(
                    "death",
                    f"{cultivator.name}瀵垮厓鑰楀敖",
                    f"{cultivator.get_realm_name()}淇＋{cultivator.name}鍦▄cultivator.age}宀佹椂閬撴秷韬"
                )
                self.events_history.append(event)
    
    def _generate_random_event(self):
        """鐢熸垚闅忔満涓栫晫浜嬩欢"""
        event_types = [
            ("birth", "鏂颁慨澹癁鐢?, 0.3),
            ("treasure", "澶╂潗鍦板疂鍑轰笘", 0.2),
            ("beast", "濡栧吔鏆村姩", 0.15),
            ("sect", "闂ㄦ淳鎷涙敹寮熷瓙", 0.2),
            ("disaster", "澶╃伨闄嶄复", 0.1),
            ("miracle", "澶╁湴寮傝薄", 0.05)
        ]
        
        event_type, event_name, _ = random.choice(event_types)
        
        descriptions = {
            "birth": "涓€鍚嶆柊鐨勪慨澹笍涓婁簡淇粰涔嬭矾",
            "treasure": "鏌愬湴鏈夌伒鍏夐棯鐜帮紝鍙兘鏈夊疂鐗╁嚭涓?,
            "beast": "濡栧吔妫灄涓殑濡栧吔寮€濮嬭簛鍔ㄤ笉瀹?,
            "sect": "鏌愬ぇ闂ㄦ淳寮€濮嬫嫑鏀舵柊寮熷瓙",
            "disaster": "澶╃伨闄嶄复锛屽嚒浜虹晫閬彈閲嶅垱",
            "miracle": "澶╃┖鍑虹幇寮傝薄锛屼技涔庢槸鏌愮棰勫厗"
        }
        
        event = WorldEvent(event_type, event_name, descriptions.get(event_type, "鏈煡浜嬩欢"))
        self.events_history.append(event)
        
        # 鏍规嵁浜嬩欢绫诲瀷浜х敓瀹為檯褰卞搷
        if event_type == "birth":
            new_cultivator = Character(is_player=False)
            self.world_cultivators.append(new_cultivator)
        elif event_type == "treasure":
            self._generate_world_treasures(1)
    
    def explore(self, player: Character) -> Dict:
        """鎺㈢储涓栫晫"""
        result = {
            "event": None,
            "messages": [],
            "rewards": []
        }
        
        # 鏍规嵁鐜╁鏈虹紭鍐冲畾閬囧埌鐨勪簨浠?        luck_factor = player.luck / 10
        
        # 鍔犳潈闅忔満閫夋嫨浜嬩欢
        events = GameConfig.EVENTS.copy()
        for event in events:
            if event["type"] == "treasure":
                event["probability"] *= (1 + luck_factor)
            elif event["type"] == "disaster":
                event["probability"] /= (1 + luck_factor * 0.5)
        
        # 褰掍竴鍖栨鐜?        total_prob = sum(e["probability"] for e in events)
        for event in events:
            event["probability"] /= total_prob
        
        selected = random.choices(events, weights=[e["probability"] for e in events])[0]
        
        # 澶勭悊浜嬩欢
        if selected["type"] == "treasure":
            result["event"] = "treasure"
            treasure = random.choice(GameConfig.TREASURES)
            player.add_item(treasure.copy())
            result["messages"].append(f"[鍙戠幇瀹濈墿] 浣犲彂鐜颁簡 {treasure['name']}锛?)
            result["messages"].append(f"   鍝佽川锛歿treasure['grade']}锛屾晥鏋滐細{treasure['effect']}")
            result["rewards"].append(treasure)
            
        elif selected["type"] == "cultivator":
            result["event"] = "cultivator"
            other = random.choice([c for c in self.world_cultivators if c.is_alive])
            result["messages"].append(f"[閬囧埌淇＋] 浣犻亣鍒颁簡 {other.name}锛坽other.get_realm_name()}锛?)
            
            # 闅忔満浜掑姩
            interaction = random.choice(["friendly", "neutral", "hostile"])
            if interaction == "friendly":
                result["messages"].append("   瀵规柟鐪嬭捣鏉ュ弸鍠勶紝浣犱滑浜ゆ祦浜嗕慨鐐煎績寰?)
                player.realm_progress += 5
            elif interaction == "hostile":
                result["messages"].append("   瀵规柟鐩厜涓嶅杽锛屼技涔庢兂瀵逛綘涓嶅埄锛?)
                # 鍙互瑙﹀彂鎴樻枟
            else:
                result["messages"].append("   浣犱滑浜掔浉鎵撻噺浜嗕竴鐣紝鍚勮嚜绂诲幓")
                
        elif selected["type"] == "beast":
            result["event"] = "beast"
            # 鏍规嵁鐜╁澧冪晫閫夋嫨濡栧吔
            suitable_beasts = [b for b in GameConfig.BEASTS if abs(b["realm"] - player.realm_level) <= 2]
            if suitable_beasts:
                beast = random.choice(suitable_beasts)
                result["messages"].append(f"[閬亣濡栧吔] 浣犻伃閬囦簡 {beast['name']}锛?)
                result["messages"].append(f"   澧冪晫鐩稿綋浜庯細{GameConfig.REALMS[beast['realm']]['name']}")
                # 杩欓噷鍙互瑙﹀彂鎴樻枟绯荤粺
            else:
                result["messages"].append("浣犳劅瑙夊埌浜嗗嵄闄╃殑姘旀伅锛屼絾鍙婃椂閬垮紑浜?)
                
        elif selected["type"] == "cave":
            result["event"] = "cave"
            result["messages"].append("[鍙戠幇娲炲簻] 浣犲彂鐜颁簡涓€澶勯殣绉樻礊搴滐紒")
            result["messages"].append("   娲炲簻涓技涔庢湁鍓嶄汉鐣欎笅鐨勪紶鎵?..")
            # 鍙互鑾峰緱鍔熸硶鎴栧疂鐗?            
        elif selected["type"] == "merchant":
            result["event"] = "merchant"
            result["messages"].append("[閬囧埌琛屽晢] 浣犻亣鍒颁簡涓€涓鍟?)
            result["messages"].append("   浠栧嚭鍞悇绉嶄慨鐐艰祫婧愶紝鍙互鐢ㄧ伒鐭宠喘涔?)
            
        elif selected["type"] == "master":
            result["event"] = "master"
            master = random.choice([c for c in self.world_cultivators if c.realm_level > player.realm_level + 2])
            result["messages"].append(f"[閬囧埌鍓嶈緢] 浣犻亣鍒颁簡鍓嶈緢楂樹汉 {master.name}锛坽master.get_realm_name()}锛夛紒")
            result["messages"].append("   鍓嶈緢鐪嬩綘棰囨湁璧勮川锛屾寚鐐逛簡鍑犲彞")
            player.realm_progress += 20
            player.comprehension += 1
            
        elif selected["type"] == "disaster":
            result["event"] = "disaster"
            disasters = ["灞卞穿", "娲按", "闆锋毚", "濡栧吔娼?, "榄斾慨琚嚮"]
            disaster = random.choice(disasters)
            result["messages"].append(f"[閬亣澶╃伨] 閬亣{disaster}锛?)
            damage = random.randint(10, 30)
            player.take_damage(damage)
            result["messages"].append(f"   浣犲彈浜嗕激锛屾崯澶眥damage}鐐圭敓鍛?)
            
        else:
            result["event"] = "nothing"
            peaceful_events = [
                "浣犲湪灞辨灄闂存极姝ワ紝蹇冨骞冲拰",
                "浣犵湅鍒版棩鍑烘棩钀斤紝鎰熸偀鑷劧涔嬮亾",
                "浣犲湪涓€澶勭伒姘斿厖娌涗箣鍦版墦鍧愮墖鍒?,
                "浣犲府鍔╀簡涓€涓糠璺殑鍑′汉",
                "浣犻噰闆嗕簡涓€浜涙櫘閫氱殑鑽夎嵂"
            ]
            result["messages"].append(f"[骞冲畨鏃犱簨] {random.choice(peaceful_events)}")
            player.karma += 1
        
        return result
    
    def get_world_status(self) -> str:
        """鑾峰彇涓栫晫鐘舵€?""
        alive_cultivators = sum(1 for c in self.world_cultivators if c.is_alive)
        total_treasures = len([t for t in self.world_treasures if not t.get("found", False)])
        
        status = f"""
----------------------------------------
           淇粰涓栫晫姒傚喌
----------------------------------------
鏃堕棿: 绗瑊self.year}骞?{self.season}瀛?绗瑊self.day}澶?澶╂皵: {self.weather}
----------------------------------------
涓栫晫淇＋: {alive_cultivators}浜哄瓨娲?鏈彂鐜扮殑瀹濈墿: {total_treasures}浠?杩戞湡浜嬩欢: {len(self.events_history)}浠?----------------------------------------
"""
        return status
    
    def get_recent_events(self, count: int = 5) -> List[str]:
        """鑾峰彇鏈€杩戜簨浠?""
        recent = self.events_history[-count:]
        return [str(e) for e in recent]
    
    def save(self) -> Dict:
        """淇濆瓨涓栫晫鐘舵€?""
        return {
            "day": self.day,
            "year": self.year,
            "season": self.season,
            "weather": self.weather,
            "cultivators_count": len(self.world_cultivators),
            "treasures_count": len(self.world_treasures),
            "events_count": len(self.events_history)
        }
