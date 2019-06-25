import tcod as libtcod
import tcod.event
from fov_functions import initialize_fov,recompute_fov
#import entity
from entity import Entity,get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from components.fighter import Fighter
from components.ai import BasicMonster
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    game_state = GameStates.PLAYERS_TURN
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall' : libtcod.Color(130, 110, 50),
        'light_ground' : libtcod.Color(200, 180, 50)
    }
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, "Player", blocks=True, fighter=fighter_component)
    npc = Entity(player_x -5, player_y, '@', libtcod.yellow, "NPC", blocks=True)
    entities = [player]
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False, libtcod.RENDERER_SDL2, 'C', True)
    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
    event = ''

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    player.fighter.attack(target)
                elif target.figher.hp > 0:
                    monster.fighter.attack(target)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                     entity.ai.take_turn(player, fov_map, game_map, entities)
            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
