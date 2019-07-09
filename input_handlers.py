import tcod as libtcod
from game_states import GameStates
def handle_keys(key, game_state) :
    # Movement keys

    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.SHOW_INVENTORY:
        return handle_inventory_keys(key)
    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP or key_char == 'i':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'k':
        return {'move':(0,1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'j':
        return {'move':(-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move':(1,0)}
    elif key_char == 'u':
        return {'move':(-1,-1)}
    elif key_char == 'o':
        return {'move':(1,-1)}
    elif key_char == 'm':
        return {'move':(-1, 1)}
    elif key_char == '.':
        return {'move':(1,1)}

    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'q':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}

    return handle_env_keys(key)

def handle_inventory_keys(key):
    index = key.c -ord('a')

    if index >= 0:
        return {'inventory_index':index}

    return handle_env_keys(key)

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    return handle_env_keys(key)

def handle_env_keys(key):
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+KEY_ENTER
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}
