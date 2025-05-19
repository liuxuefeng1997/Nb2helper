default_config_data = {
    "DAMAGE": {
        "_self": "受击伤害",
        "enable": False,
        "value": 1
    },
    "GOLD": {
        "_self": "金币",
        "lock": False,
        "enable": False,
        "value": 199
    },
    "KEYS": {
        "_self": "钥匙",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER": {
        "_self": "手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER_ICE": {
        "_self": "冰霜手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER_FIRE": {
        "_self": "火焰手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER_THUNDER": {
        "_self": "雷电手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER_DARK": {
        "_self": "暗手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "BOMBER_POISON": {
        "_self": "毒素手雷",
        "lock": False,
        "enable": False,
        "value": 9
    },
    "MANA": {
        "_self": "水晶",
        "lock": False,
        "lock_to_max": True,
        "enable": False,
        "value": 5
    },
    "SHIELDS": {
        "_self": "护盾",
        "lock": False,
        "enable": False,
        "value": 0
    },
    "HEALTH": {
        "_self": "血量",
        "lock": False,
        "lock_to_max": True,
        "enable": False,
        "value": 8
    },
    "GUN_LEN": {
        "_self": "射程",
        "enable": False,
        "value": 1
    },
    "GUN_SPEED": {
        "_self": "射速",
        "enable": False,
        "value": 1
    },
    "GUN_SUM": {
        "_self": "弹道",
        "enable": False,
        "value": 1
    },
    "GUN_BOLL": {
        "_self": "子弹伤害",
        "enable": False,
        "value": 1
    },
    "GUN_LEVEL": {
        "_self": "武器等级",
        "lock": False,
        "enable": False,
        "value": 1
    },
    "MOVE_SPEED": {
        "_self": "移速",
        "enable": False,
        "value": 11
    },
    "JUMP_HIGHER": {
        "_self": "跳跃高度",
        "enable": False,
        "value": 95
    },
    "JUMP_SUM": {
        "_self": "跳跃次数",
        "enable": False,
        "value": 0
    },
    "JUMP_SUM_NO_MARK": {
        "_self": "跳跃次数（无印记）",
        "enable": False,
        "value": 0
    },
    "FIRE_LEVEL": {
        "_self": "火焰伤害等级",
        "enable": False,
        "value": 1
    },
    "THUNDER_LEVEL": {
        "_self": "闪电伤害等级",
        "enable": False,
        "value": 1
    },
    "POISON_LEVEL": {
        "_self": "毒素伤害等级",
        "enable": False,
        "value": 1
    },
    "ICE_LEVEL": {
        "_self": "冰霜伤害等级",
        "enable": False,
        "value": 1
    },
    "BLAST_LEVEL": {
        "_self": "爆炸伤害等级",
        "enable": False,
        "value": 1
    },
    "MAGIC_LEVEL": {
        "_self": "魔法伤害等级",
        "enable": False,
        "value": 1
    },
    "TEC_LEVEL": {
        "_self": "科技伤害等级",
        "enable": False,
        "value": 1
    },
    "BUBBLE_LEVEL": {
        "_self": "萌萌伤害等级",
        "enable": False,
        "value": 1
    },
    "PHYSICAL_LEVEL": {
        "_self": "物理伤害等级",
        "enable": False,
        "value": 1
    },
    "SOUL_LEVEL": {
        "_self": "暗灵伤害等级",
        "enable": False,
        "value": 1
    },
    "GOLD_SOUL_SUM": {
        "_self": "金色暗灵数量",
        "enable": False,
        "value": 0
    },
    "TEMP_SOUL_SUM": {
        "_self": "临时暗灵数量",
        "lock": False,
        "enable": False,
        "value": 0
    },
    "CURSE_LEVEL": {
        "_self": "诅咒等级",
        "enable": False,
        "value": 0
    },
    "KNIFE_SPEED": {
        "_self": "近战武器攻速",
        "enable": False,
        "value": 1
    },
    "TIME_OF_DAMAGE": {
        "_self": "伤害持续时间",
        "enable": False,
        "value": 1
    },
    "CRIT_RATE": {
        "_self": "暴击几率",
        "enable": False,
        "value": 0
    }
}
NB2 = {
    "GOLD": 0x210,  # 金币
    "HEALTH": 0x258,  # 血量(会暴毙，不推荐使用，可通过修改护盾变相无敌)
    "MAX_HEALTH": 0x588,  # 血量上限
    "SHIELDS": 0x288,  # 护盾
    "BOMBER": 0x2A0,  # 手雷
    "BOMBER_ICE": 0x438,  # 冰霜手雷
    "BOMBER_FIRE": 0xC18,  # 火焰手雷
    "BOMBER_THUNDER": 0x8E8,  # 雷电手雷
    "BOMBER_DARK": 0x540,  # 暗手雷
    "BOMBER_POISON": 0x1128,  # 毒素手雷
    "KEYS": 0x4F8,  # 钥匙
    "MANA": 0x270,  # 水晶
    "MAX_MANA": 0x5B8,  # 水晶上限
    "GUN_LEN": 0x198,  # 射程
    "GUN_SUM": 0x168,  # 子弹列数
    "GUN_SPEED": 0x1C8,  # 射速
    "GUN_BOLL": 0x180,  # 子弹伤害
    "GUN_LEVEL": 0x13E0,  # 武器等级
    "MOVE_SPEED": 0x6A8,  # 移动速度
    "JUMP_HIGHER": 0x4C8,  # 跳跃高度
    "JUMP_SUM_NO_MARK": 0x1488,  # 无印记跳跃次数
    "JUMP_SUM": 0x6D8,  # 跳跃次数
    "FIRE_LEVEL": 0x1038,  # 火焰伤害等级
    "THUNDER_LEVEL": 0x1050,  # 闪电伤害等级
    "POISON_LEVEL": 0x1068,  # 毒素伤害等级
    "ICE_LEVEL": 0x1080,  # 冰霜伤害等级
    "BLAST_LEVEL": 0x1140,  # 爆炸伤害等级
    "MAGIC_LEVEL": 0x1248,  # 魔法伤害等级
    "TEC_LEVEL": 0xF18,  # 科技伤害等级
    "BUBBLE_LEVEL": 0x14A0,  # 萌萌伤害等级
    "PHYSICAL_LEVEL": 0x660,  # 物理伤害等级
    "SOUL_LEVEL": 0x1980,  # 暗灵伤害等级
    "CURSE_LEVEL": 0x1110,  # 诅咒等级
    "GOLD_SOUL_SUM": 0x19E0,  # 金色暗灵数量
    "TEMP_SOUL_SUM": 0x19F8,  # 临时暗灵数量
    "DAMAGE": 0x2E8,  # 受击伤害
    "KNIFE_SPEED": 0xE28,  # 近战武器攻速
    "TIME_OF_DAMAGE": 0x1200,  # 伤害持续时间
    "CRIT_RATE": 0x15F0  # 暴击几率
}
EXE_NAME = "NeonAbyss2.exe"
DLL_NAME = "UnityPlayer.dll"
DLL_OFFSET = 0x01C9D460
MEM_OFFSETS = [0x8, 0x10, 0x28, 0x50, 0x20, 0x18, 0x10, 0x18, 0x0]
# MEM_OFFSETS = [0x8, 0x10, 0x28, 0x50, 0x180, 0x310, 0x468]  武器升级经验百分比
uplogs = {
    "version": "2025.05.19.1958.0028",
    "lines": [
        "1、新增：新增一些修改项",
        "2、新增：新增每次启动时创建配置文件模板，包含所有配置",
        "* 注意配置文件差异：可将旧的配置文件备份后删除，让程序创建默认配置以支持新增条目",
        "",
        "使用提示：",
        "1、程序会自动检测配置文件更改，修改配置文件即可使修改生效",
        "2、修改配置时务必注意不要破坏文件结构，否则可能导致错误，可使用包内JSON编辑器以避免出现问题",
        "3、程序首次运行会自动创建默认配置文件",
        "4、锁定至最大值开关说明（\"lock_to_max\": true|false）默认为true，关闭时锁定至设定值"
    ]
}
