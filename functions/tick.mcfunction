# 1. Detect who died and add a death point
scoreboard players add @a[hasitem={item=totem_of_undying,location=slot.weapon.offhand,count=0}] deaths 0

# 2. Punish the player who died by lowering their health attribute
attribute @a[scores={deaths=1..}] minecraft:health base set 18
# Reset their death score so it doesn't loop infinitely
scoreboard players set @a[scores={deaths=1..}] deaths 0

# 3. Reward the player who got the elimination
# Since vanilla Bedrock commands struggle to pinpoint the exact PvP killer instantly without APIs,
# a highly reliable alternative is rewarding the closest player within a 10-block radius of the death.
execute at @a[scores={deaths=1..}] run attribute @p[rm=0.1,r=10] minecraft:health base set 22
