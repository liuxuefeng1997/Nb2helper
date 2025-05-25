import this

EXE_NAME = "NeonAbyss2.exe"
versionInfo = {
    "version": "2025.05.26.0440.0036.beta",
    "lines": [
        "1、新版本数据变化，正在更新中",
        "2、新增英文语言",
        # "3、修复了一个可能导致程序关闭时弹出警告的问题",
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
    "GUN_LEN": {},  # 射程
    "GUN_SUM": {},  # 子弹列数
    "GUN_SPEED": {},  # 射速
    "GUN_BOLL": {},  # 子弹伤害
    "GUN_LEVEL": {},  # 武器等级
    "MOVE_SPEED": {},  # 移动速度
    "JUMP_HIGHER": {},  # 跳跃高度
    "JUMP_SUM_NO_MARK": {},  # 无印记跳跃次数
    "JUMP_SUM": {},  # 跳跃次数
    "FIRE_LEVEL": {},  # 火焰伤害等级
    "THUNDER_LEVEL": {},  # 闪电伤害等级
    "POISON_LEVEL": {},  # 毒素伤害等级
    "ICE_LEVEL": {},  # 冰霜伤害等级
    "BLAST_LEVEL": {},  # 爆炸伤害等级
    "MAGIC_LEVEL": {},  # 魔法伤害等级
    "TEC_LEVEL": {},  # 科技伤害等级
    "BUBBLE_LEVEL": {},  # 萌萌伤害等级
    "PHYSICAL_LEVEL": {},  # 物理伤害等级
    "SOUL_LEVEL": {},  # 暗灵伤害等级
    "CURSE_LEVEL": {},  # 诅咒等级
    "GOLD_SOUL_SUM": {},  # 金色暗灵数量
    "TEMP_SOUL_SUM": {},  # 临时暗灵数量
    "DAMAGE": {},  # 受击伤害
    "KNIFE_SPEED": {},  # 近战武器攻速
    "TIME_OF_DAMAGE": {},  # 伤害持续时间
    "CRIT_RATE": {},  # 暴击几率
    "GUN_EXP_PRT": {},  # 武器升级经验百分比
    "IS_FLY": {},  # 是否飞行
    "IS_MACHINE_DAMAGE": {},  # 机器是否损坏
    "BOX_WIN_PROB": {}  # 宝箱获胜概率
}
