import json
import random
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class GameConfig:
    """娓告垙閰嶇疆"""
    
    # 淇偧澧冪晫
    REALMS = [
        {"name": "鐐兼皵鏈?, "lifespan": 100, "power": 1, "desc": "寮曟皵鍏ヤ綋锛屽垵姝ヨ秴鍑?},
        {"name": "绛戝熀鏈?, "lifespan": 200, "power": 10, "desc": "濂犲畾閬撳熀锛屾寮忓叆閬?},
        {"name": "閲戜腹鏈?, "lifespan": 500, "power": 100, "desc": "鍑濈粨閲戜腹锛屾硶鍔涘ぇ澧?},
        {"name": "鍏冨┐鏈?, "lifespan": 1000, "power": 1000, "desc": "鍏冨┐鍒濇垚锛屽彲澶鸿垗閲嶇敓"},
        {"name": "鍖栫鏈?, "lifespan": 2000, "power": 10000, "desc": "绁炶瘑澶ф垚锛屾劅鎮熸硶鍒?},
        {"name": "鐐艰櫄鏈?, "lifespan": 5000, "power": 100000, "desc": "铏氬疄鐩哥敓锛岃Е鎽稿ぇ閬?},
        {"name": "鍚堜綋鏈?, "lifespan": 10000, "power": 1000000, "desc": "澶╀汉鍚堜竴锛屾垬鍔涙棤鍙?},
        {"name": "澶т箻鏈?, "lifespan": 20000, "power": 10000000, "desc": "澶ч亾宸叉垚锛岀瓑寰呴鍗?},
        {"name": "娓″姭鏈?, "lifespan": 50000, "power": 100000000, "desc": "娓″姭椋炲崌锛屼節姝讳竴鐢?},
        {"name": "鐪熶粰", "lifespan": -1, "power": 1000000000, "desc": "椋炲崌浠欑晫锛屼笌澶╁湴鍚屽"}
    ]
    
    # 浜旇鍏冪礌
    ELEMENTS = ["閲?, "鏈?, "姘?, "鐏?, "鍦?]
    
    # 鐏垫牴鍝佽川
    SPIRIT_ROOT_QUALITIES = {
        "浼伒鏍?: {"probability": 0.60, "cultivation_speed": 0.5, "elements": (4, 5)},
        "鐪熺伒鏍?: {"probability": 0.30, "cultivation_speed": 1.0, "elements": (2, 3)},
        "澶╃伒鏍?: {"probability": 0.08, "cultivation_speed": 2.0, "elements": (1, 1)},
        "鍙樺紓鐏垫牴": {"probability": 0.015, "cultivation_speed": 2.5, "elements": (2, 2)},
        "娣锋矊鐏垫牴": {"probability": 0.005, "cultivation_speed": 3.0, "elements": (5, 5)}
    }
    
    # 鍔熸硶鍝佽川
    SKILL_GRADES = ["榛勯樁", "鐜勯樁", "鍦伴樁", "澶╅樁", "浠欓樁"]
    
    # 鐗╁搧鍝佽川
    ITEM_GRADES = ["鍑″搧", "鐏靛搧", "鍦板搧", "澶╁搧", "浠欏搧"]
    
    # 鍦板尯绫诲瀷
    REGIONS = [
        {"name": "鍑′汉鍩庨晣", "type": "mortal", "danger": 0, "spirit": 1},
        {"name": "鑽掗噹", "type": "wild", "danger": 10, "spirit": 5},
        {"name": "鐏佃剦灞辫剦", "type": "spirit", "danger": 30, "spirit": 50},
        {"name": "濡栧吔妫灄", "type": "beast", "danger": 50, "spirit": 40},
        {"name": "绂佸湴杈圭紭", "type": "forbidden", "danger": 80, "spirit": 80},
        {"name": "涓婂彜閬楄抗", "type": "ruin", "danger": 90, "spirit": 100}
    ]
    
    # 闅忔満浜嬩欢绫诲瀷
    EVENTS = [
        {"type": "treasure", "name": "鍙戠幇澶╂潗鍦板疂", "probability": 0.05},
        {"type": "cultivator", "name": "閬囧埌鍏朵粬淇＋", "probability": 0.15},
        {"type": "beast", "name": "閬亣濡栧吔", "probability": 0.20},
        {"type": "cave", "name": "鍙戠幇娲炲簻", "probability": 0.03},
        {"type": "merchant", "name": "閬囧埌琛屽晢", "probability": 0.08},
        {"type": "master", "name": "閬囧埌鍓嶈緢楂樹汉", "probability": 0.02},
        {"type": "disaster", "name": "閬亣澶╃伨", "probability": 0.05},
        {"type": "nothing", "name": "骞冲畨鏃犱簨", "probability": 0.42}
    ]
    
    # 濮撴皬
    SURNAMES = [
        "鏉?, "鐜?, "寮?, "鍒?, "闄?, "鏉?, "璧?, "榛?, "鍛?, "鍚?,
        "寰?, "瀛?, "鑳?, "鏈?, "楂?, "鏋?, "浣?, "閮?, "椹?, "缃?,
        "姊?, "瀹?, "閮?, "璋?, "闊?, "鍞?, "鍐?, "浜?, "钁?, "钀?,
        "绋?, "鏇?, "琚?, "閭?, "璁?, "鍌?, "娌?, "鏇?, "褰?, "鍚?,
        "鑻?, "鍗?, "钂?, "钄?, "璐?, "涓?, "榄?, "钖?, "鍙?, "闃?
    ]
    
    # 鍚嶅瓧
    NAMES = [
        "浜?, "椋?, "闆?, "鐢?, "澶?, "鍦?, "鐜?, "榛?, "瀹?, "瀹?,
        "娲?, "鑽?, "鏃?, "鏈?, "鏄?, "杈?, "灞?, "娌?, "娴?, "宸?,
        "闈?, "绾?, "绱?, "鐧?, "榛?, "閲?, "鏈?, "姘?, "鐏?, "鍦?,
        "闀?, "鐢?, "姘?, "鎭?, "鏃?, "鏋?, "澶?, "鍒?, "娣?, "娌?,
        "閫?, "閬?, "鑷?, "鍦?, "椋?, "娓?, "铏?, "绌?, "鐏?, "濡?,
        "淇?, "鐪?, "鐐?, "閬?, "鎮?, "娉?, "鏈?, "璇€", "蹇?, "鎰?
    ]
    
    # 澶╂潗鍦板疂
    TREASURES = [
        {"name": "鐧惧勾鐏佃姖", "grade": "鍑″搧", "effect": "鎭㈠鐢熷懡", "value": 100},
        {"name": "鍗冨勾浜哄弬", "grade": "鐏靛搧", "effect": "澧炲姞淇负", "value": 500},
        {"name": "鏈辨灉", "grade": "鍦板搧", "effect": "绐佺牬杈呭姪", "value": 2000},
        {"name": "榫欒鑽?, "grade": "澶╁搧", "effect": "娲楅珦浼愰", "value": 10000},
        {"name": "涔濊浆閲戜腹", "grade": "浠欏搧", "effect": "璧锋鍥炵敓", "value": 100000}
    ]
    
    # 濡栧吔
    BEASTS = [
        {"name": "閲庣嫾", "realm": 0, "power": 5, "drop": "鐙肩毊"},
        {"name": "鐚涜檸", "realm": 0, "power": 15, "drop": "铏庨"},
        {"name": "閾佽儗鐔?, "realm": 1, "power": 50, "drop": "鐔婅儐"},
        {"name": "鐏汗璞?, "realm": 2, "power": 200, "drop": "鐏汗鐨?},
        {"name": "闈掗楣?, "realm": 3, "power": 1000, "drop": "楣扮窘"},
        {"name": "閲戠敳锜?, "realm": 4, "power": 5000, "drop": "锜掍腹"},
        {"name": "鐑堢劙鐙?, "realm": 5, "power": 20000, "drop": "鐙績鐏?}
    ]

# 鍏ㄥ眬娓告垙鐘舵€?game_state = {
    "player": None,
    "world": None,
    "turn": 0,
    "saved_at": None
}
