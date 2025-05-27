import this

EXE_NAME = "NeonAbyss2.exe"
versionInfo = {
    "version": "2025.05.27.2358.0038",
    "lines": [
        "1、为新版本游戏提供支持",
        "2、移除修改无效的项目",
        "3、更新了版本号",
        "* 注意配置文件差异：可将旧的配置文件备份后删除，让程序创建默认配置以支持新增条目",
    ]
}
NB2_DATA = {
    "_DEFAULT_": dict(dll_name="UnityPlayer.dll", dll_offset=0x01C87660, offsets=[0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x0]),
    "GOLD": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x420, 0x10],
        "valueType": "d"
    },  # 金币
    "HEALTH": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x540, 0x10],
        "valueType": "d"
    },  # 血量
    "MAX_HEALTH": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x11E8, 0x10],
        "valueType": "d"
    },  # 血量上限
    "SHIELDS": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x570, 0x10],
        "valueType": "d"
    },  # 护盾
    "BOMBER": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x678, 0x10],
        "valueType": "d"
    },  # 手雷
    "KEYS": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0xED0, 0x10],
        "valueType": "d"
    },  # 钥匙
    "MANA": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x558, 0x10],
        "valueType": "d"
    },  # 水晶
    "MAX_MANA": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x1230, 0x10],
        "valueType": "d"
    },  # 水晶上限
    "GUN_SPEED": {
        "dll_name": "UnityPlayer.dll",
        "dll_offset": 0x01C87660,
        "offsets": [0x8, 0x90, 0x60, 0x68, 0x20, 0x18, 0x10, 0x18, 0x390, 0x10],
        "valueType": "d"
    },  # 射速
}
