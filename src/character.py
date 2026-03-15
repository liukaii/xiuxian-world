import random
from typing import Dict, List, Optional
from config import GameConfig

class SpiritRoot:
    """鐏垫牴绯荤粺"""
    
    def __init__(self):
        self.quality = self._generate_quality()
        self.elements = self._generate_elements()
        self.main_element = self.elements[0] if self.elements else None
        self.cultivation_speed = GameConfig.SPIRIT_ROOT_QUALITIES[self.quality]["cultivation_speed"]
    
    def _generate_quality(self) -> str:
        """闅忔満鐢熸垚鐏垫牴鍝佽川"""
        rand = random.random()
        cumulative = 0
        for quality, data in GameConfig.SPIRIT_ROOT_QUALITIES.items():
            cumulative += data["probability"]
            if rand <= cumulative:
                return quality
        return "浼伒鏍?
    
    def _generate_elements(self) -> List[str]:
        """鐢熸垚鐏垫牴灞炴€?""
        quality_data = GameConfig.SPIRIT_ROOT_QUALITIES[self.quality]
        min_elem, max_elem = quality_data["elements"]
        num_elements = random.randint(min_elem, max_elem)
        
        if self.quality == "娣锋矊鐏垫牴":
            return GameConfig.ELEMENTS.copy()
        
        return random.sample(GameConfig.ELEMENTS, min(num_elements, len(GameConfig.ELEMENTS)))
    
    def get_description(self) -> str:
        """鑾峰彇鐏垫牴鎻忚堪"""
        elem_str = "銆?.join(self.elements)
        return f"{self.quality}锛坽elem_str}锛?
    
    def __str__(self):
        return self.get_description()


class Character:
    """瑙掕壊绯荤粺"""
    
    def __init__(self, is_player: bool = False):
        self.is_player = is_player
        self.name = self._generate_name()
        self.age = random.randint(15, 30)
        self.spirit_root = SpiritRoot()
        
        # 鍩虹灞炴€?        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.exp = 0
        self.realm_level = 0  # 瀵瑰簲 REALMS 绱㈠紩
        self.realm_progress = 0  # 褰撳墠澧冪晫杩涘害 0-100
        
        # 鐗规畩灞炴€?        self.comprehension = random.randint(1, 10)  # 鎮熸€?        self.luck = random.randint(1, 10)  # 鏈虹紭
        self.perception = random.randint(1, 10)  # 鎰熺煡
        
        # 澶╅亾灞炴€?        self.karma = 0  # 鍥犳灉涓氬姏
        self.destiny = random.randint(1, 10)  # 鍛芥牸
        
        # 璧勬簮
        self.spirit_stones = random.randint(0, 100)  # 鐏电煶
        self.items = []  # 鐗╁搧鏍?        self.skills = []  # 鍔熸硶
        
        # 鐘舵€?        self.is_alive = True
        self.location = None
        self.sect = None  # 鎵€灞為棬娲?        self.friends = []  # 濂藉弸
        self.enemies = []  # 鏁屼汉
    
    def _generate_name(self) -> str:
        """鐢熸垚闅忔満鍚嶅瓧"""
        surname = random.choice(GameConfig.SURNAMES)
        name = random.choice(GameConfig.NAMES)
        if random.random() > 0.5:
            name += random.choice(GameConfig.NAMES)
        return surname + name
    
    def get_realm_name(self) -> str:
        """鑾峰彇褰撳墠澧冪晫鍚嶇О"""
        if self.realm_level < len(GameConfig.REALMS):
            return GameConfig.REALMS[self.realm_level]["name"]
        return "鏈煡澧冪晫"
    
    def get_power(self) -> int:
        """璁＄畻鎴樻枟鍔?""
        base_power = GameConfig.REALMS[self.realm_level]["power"] if self.realm_level < len(GameConfig.REALMS) else 1
        progress_bonus = int(base_power * (self.realm_progress / 100))
        return base_power + progress_bonus + (self.comprehension * 10)
    
    def get_lifespan(self) -> int:
        """鑾峰彇褰撳墠澧冪晫瀵垮懡涓婇檺"""
        if self.realm_level < len(GameConfig.REALMS):
            return GameConfig.REALMS[self.realm_level]["lifespan"]
        return 100
    
    def get_remaining_life(self) -> int:
        """鑾峰彇鍓╀綑瀵垮懡"""
        return self.get_lifespan() - self.age
    
    def cultivate(self, days: int = 1) -> Dict:
        """淇偧"""
        results = {
            "exp_gained": 0,
            "realm_breakthrough": False,
            "messages": []
        }
        
        # 璁＄畻淇偧鏁堢巼
        base_gain = 10 * days
        speed_bonus = self.spirit_root.cultivation_speed
        comprehension_bonus = 1 + (self.comprehension / 10)
        luck_bonus = 1 + (self.luck / 20)
        
        total_gain = int(base_gain * speed_bonus * comprehension_bonus * luck_bonus)
        
        # 澧炲姞淇负
        self.realm_progress += total_gain
        results["exp_gained"] = total_gain
        results["messages"].append(f"淇偧{days}澶╋紝鑾峰緱{total_gain}鐐逛慨涓?)
        
        # 妫€鏌ョ獊鐮?        if self.realm_progress >= 100:
            breakthrough_result = self._try_breakthrough()
            results["realm_breakthrough"] = breakthrough_result["success"]
            results["messages"].extend(breakthrough_result["messages"])
        
        # 娑堣€楁椂闂?        self.age += days
        
        # 妫€鏌ュ鍛?        if self.age >= self.get_lifespan():
            self.is_alive = False
            results["messages"].append("瀵垮厓鑰楀敖锛岄亾娑堣韩姝?..")
        
        return results
    
    def _try_breakthrough(self) -> Dict:
        """灏濊瘯绐佺牬澧冪晫"""
        result = {"success": False, "messages": []}
        
        # 璁＄畻绐佺牬鎴愬姛鐜?        base_success = 0.5
        comprehension_bonus = self.comprehension / 20
        karma_penalty = abs(self.karma) / 100
        destiny_bonus = self.destiny / 20
        
        success_rate = base_success + comprehension_bonus - karma_penalty + destiny_bonus
        success_rate = max(0.1, min(0.95, success_rate))  # 闄愬埗鍦?0%-95%
        
        if random.random() < success_rate:
            # 绐佺牬鎴愬姛
            self.realm_level += 1
            self.realm_progress = 0
            self.max_hp += 50
            self.max_mp += 30
            self.hp = self.max_hp
            self.mp = self.max_mp
            
            new_realm = self.get_realm_name()
            result["success"] = True
            result["messages"].append(f"馃帀 绐佺牬鎴愬姛锛佽笍鍏new_realm}锛?)
            
            # 澶у鐣岀獊鐮寸殑鐗规畩鏁堟灉
            if self.realm_level in [2, 5, 8]:  # 閲戜腹銆佸悎浣撱€佹浮鍔?                result["messages"].append("鈿?澶╅檷寮傝薄锛屼慨涓哄ぇ娑紒")
                self.destiny += 1
        else:
            # 绐佺牬澶辫触
            self.realm_progress = max(0, self.realm_progress - 20)
            result["messages"].append("馃挃 绐佺牬澶辫触锛屼慨涓哄彈鎹?..")
            
            # 涓ラ噸澶辫触鍙兘鍙椾激
            if random.random() < 0.3:
                damage = self.max_hp // 4
                self.hp -= damage
                result["messages"].append(f"鍙楀埌鍙嶅櫖锛屾崯澶眥damage}鐐圭敓鍛?)
        
        return result
    
    def take_damage(self, damage: int) -> bool:
        """鍙楀埌浼ゅ"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            return True  # 姝讳骸
        return False
    
    def heal(self, amount: int):
        """鎭㈠鐢熷懡"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def add_item(self, item: Dict):
        """娣诲姞鐗╁搧"""
        self.items.append(item)
    
    def remove_item(self, item_name: str) -> bool:
        """绉婚櫎鐗╁搧"""
        for i, item in enumerate(self.items):
            if item["name"] == item_name:
                self.items.pop(i)
                return True
        return False
    
    def get_status(self) -> str:
        """鑾峰彇瑙掕壊鐘舵€?""
        status = f"""
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? {self.name:^35}  鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?澧冪晫: {self.get_realm_name():<12} 鎴樺姏: {self.get_power():<8} 鈹?鈹?骞撮緞: {self.age:<4}宀?   瀵垮厓: {self.get_remaining_life():<4}骞?     鈹?鈹?鐢熷懡: {self.hp}/{self.max_hp:<4}    娉曞姏: {self.mp}/{self.max_mp:<4}    鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鐏垫牴: {str(self.spirit_root):<28} 鈹?鈹?鎮熸€? {self.comprehension:<4}      鏈虹紭: {self.luck:<4}      鎰熺煡: {self.perception:<4} 鈹?鈹?鍛芥牸: {self.destiny:<4}      涓氬姏: {self.karma:<+4}                鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鐏电煶: {self.spirit_stones:<6}    鐗╁搧: {len(self.items):<4}浠?     鍔熸硶: {len(self.skills):<4}闂?鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?"""
        return status
    
    def __str__(self):
        return f"{self.name} ({self.get_realm_name()})"
