# 基本说明
* 使用python3.13和PyQt5构建
* 配置文件会自动重载
# 功能重构
| 属性名          | 说明         | 重构状态 | 属性名           | 说明             | 重构状态    |
|----------------|-------------|----------|-----------------|-----------------|----------|
| GOLD            | 金币        | ✅       | GUN_SPEED        | 射速             |          |
| HEALTH          | 血量        | ✅       | GUN_BOLL         | 子弹伤害          |          |
| MAX_HEALTH      | 血量上限     | ✅       | GUN_LEVEL        | 武器等级          |          |
| SHIELDS         | 护盾        | ✅       | MOVE_SPEED       | 移动速度          |          |
| BOMBER          | 手雷        | ✅       | JUMP_HIGHER      | 跳跃高度          |          |
| BOMBER_ICE      | 冰霜手雷     | ⛔       | JUMP_SUM_NO_MARK | 无印记跳跃次数     |          |
| BOMBER_FIRE     | 火焰手雷     | ⛔        | JUMP_SUM         | 跳跃次数          |          |
| BOMBER_THUNDER  | 雷电手雷     | ⛔        | FIRE_LEVEL       | 火焰伤害等级       |          |
| BOMBER_DARK     | 暗手雷       | ⛔        | THUNDER_LEVEL    | 闪电伤害等级      |           |
| BOMBER_POISON   | 毒素手雷     | ⛔        | POISON_LEVEL     | 毒素伤害等级      |           |
| KEYS            | 钥匙         | ✅       | ICE_LEVEL        | 冰霜伤害等级     |           |
| MANA            | 水晶         | ✅       | BLAST_LEVEL      | 爆炸伤害等级     |           |
| MAX_MANA        | 水晶上限     | ✅       | MAGIC_LEVEL      | 魔法伤害等级      |           |
| GUN_LEN         | 射程         |        | TEC_LEVEL        | 科技伤害等级      |           |
| GUN_SUM         | 子弹列数     |         | BUBBLE_LEVEL     | 萌萌伤害等级      |           |
| DAMAGE          | 受击伤害     |         | PHYSICAL_LEVEL   | 物理伤害等级      |           |
| KNIFE_SPEED     | 近战武器攻速  |         | SOUL_LEVEL       | 暗灵伤害等级      |           |
| TIME_OF_DAMAGE  | 伤害持续时间  |         | CURSE_LEVEL      | 诅咒等级         |           |
| CRIT_RATE       | 暴击几率     |         | GOLD_SOUL_SUM    | 金色暗灵数量      |           |
| IS_FLY          | 是否飞行     |         | IS_MACHINE_DAMAGE  | 机器是否损坏    |           |
| BOX_WIN_PROB    | 宝箱获胜概率  |         |                    |               |          |
#### 注意
* ✅ 代表已实装
* ⛔ 代表已弃用
* 留空代表开发中
# 计划实现的功能
* 代码和程序优化
<br>
<br>
<br>
