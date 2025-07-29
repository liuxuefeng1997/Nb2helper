EXE_NAME = "NeonAbyss2.exe"
versionInfo = {
    "version": "2025.07.29.1832.0049",
    "lines": [
        "1、修复问题",
        # "2、新增 飞行、无需钥匙、双倍金币、玩家是否死亡、宝箱判定范围 修改",
    ]
}
DEFAULT_DICT = {'dll_name': "UnityPlayer.dll", 'dll_offset': 0x01C87660, 'offsets': [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x0]}
NB2_DATA = {
    "_DEFAULT_": DEFAULT_DICT,
    "GOLD": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x420, 0x10],
        "valueType": "d"
    },  # 金币
    "HEALTH": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x540, 0x10],
        "valueType": "d"
    },  # 血量
    "MAX_HEALTH": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x11E8, 0x10],
        "valueType": "d"
    },  # 血量上限
    "SHIELDS": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x570, 0x10],
        "valueType": "d"
    },  # 护盾
    "BOMBER": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x678, 0x10],
        "valueType": "d"
    },  # 手雷
    "KEYS": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0xED0, 0x10],
        "valueType": "d"
    },  # 钥匙
    "MANA": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x558, 0x10],
        "valueType": "d"
    },  # 水晶
    "MAX_MANA": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x1230, 0x10],
        "valueType": "d"
    },  # 水晶上限
    "GUN_SPEED": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x10, 0x18, 0x390, 0x10],
        "valueType": "d"
    },  # 射速
    "MOVE_SPEED": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x0, 0x8, 0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x58, 0x18, 0x14B8],
        "valueType": "d"
    },  # 移速
    "TEMP_JUMP_SUM": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x0, 0x8, 0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x58, 0x18, 0x1500],
        "valueType": "d"
    },  # 跳跃次数
    "GUN_BALLISTICS": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x0, 0x8, 0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x58, 0x18, 0x318],
        "valueType": "d"
    },  # 弹道数量
    "GUN_RANGE": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x0, 0x8, 0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x58, 0x18, 0x360],
        "valueType": "d"
    },  # 射程
    "EXPLOSION_DAMAGE": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x0, 0x8, 0x8, 0x10, 0x28, 0x68, 0x20, 0x18, 0x58, 0x18, 0x768],
        "valueType": "d"
    },  # 爆炸伤害
    "FLY": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x590, 0x3C3],
        "valueType": "b"
    },  # 飞行
    "NO_KEY": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x590, 0x2F0],
        "valueType": "b"
    },  # 无需钥匙
    "DOUBLE_COIN": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x590, 0x76],
        "valueType": "b"
    },  # 双倍金币
    "ITEM_CAN_DESTROY": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x590, 0x0F0],
        "valueType": "b"
    },  # 物品可破坏
    "PLAYER_IS_DIE": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x1E4],
        "valueType": "b"
    },  # 玩家已死亡
    "BOX_PFX": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x10, 0x28, 0x68, 0x238, 0x590, 0x1F0],
        "valueType": "f"
    },  # 宝箱判断范围
}
