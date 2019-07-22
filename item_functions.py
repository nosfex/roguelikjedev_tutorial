import tcod as libtcod
from game_messages import Message, MessageLog

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed':True, 'message':Message('Your wounds start to feel better', libtcod.green)})

    return results

def cast_lighting(*args, **kwargs)
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range +1
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

        if target:
            results.append({'consumed': True, 'target': target, 'message': Message(' A Lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage), libtcod.yellow)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'consumed':False, 'target':None, 'message': Message('No enemy in range', libtcod.red)})

def cast_fireball(*args, **kwargs):
    entities    = kwargs.get('entities')
    fov_map     = kwargs.get('fov_map')
    damage      = kwargs.get('damage')
    radius      = kwargs.get('radius')
    target_x    = kwargs.get('target_x')
    target_y    = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message':Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The Fireball explodes, burning everything within {0}'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points. '.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))
    return results
