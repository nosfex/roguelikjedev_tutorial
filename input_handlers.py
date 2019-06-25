import tcod as libtcod

def handle_keys(key) :
    # Movement keys
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

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+KEY_ENTER
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
