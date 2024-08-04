#!/usr/bin/env python3

from cortile import Cortile


def callback(ret):

    if ret.Name == 'Workplace':
        active_layout = ct.get_active_layout()
        if active_layout:
            print(f'Active layout: {active_layout.Name}', active_layout.Location)
        else:
            print(f'Active layout: {None}')

    if ret.Name == 'Windows':
        active_client = ct.get_active_client()
        if active_client:
            print(f'Active client: {active_client.Window.Id}', active_client.Latest)
        else:
            print(f'Active client: {None}')

    if ret.Name == 'Pointer':
        last_pointer = ret.Data
        if last_pointer:
            print(f'Last pointer: {next((k for k, v in last_pointer.Device.Button.items() if v), None)}', last_pointer.Device.Position)

    if ret.Name == 'Corner':
        last_corner = ret.Data
        if last_corner:
            print(f'Last corner: {last_corner.Name}', last_corner.Location)

    if ret.Name == 'Action':
        last_action = ret.Data
        if last_action:
            print(f'Last action: {last_action.Name}', last_action.Location)


if __name__ == '__main__':
    ct = Cortile()

    ct.listen(callback)

    client = ct.get_active_client()
    if client:
        id = client.Window.Id
        desk = ct.get_active_workspace()
        screen = ct.get_active_screen()

        # for layout in ct.get_active_layouts():
        #    print(f'Active layout: {layout.Name}', layout.Location)

        # print(ct.get_active_workspace())
        # print(ct.get_active_screen())

        # print(ct.get_workspace_count())
        # print(ct.get_screen_count())

        # print(ct.get_workspace_dimensions())
        # print(ct.get_screen_dimensions())

        # print(ct.get_windows())
        # print(ct.get_clients())

        # print(ct.desktop_switch(desk))

        # print(ct.window_activate(id))

        # print(ct.window_to_desktop(id, desk))
        # print(ct.window_to_position(id, x=1000, y=500))
        # print(ct.window_to_screen(id, desk))

        # print(ct.action_execute_enable(desk, screen))
        # print(ct.action_execute_disable(desk, screen))
        # print(ct.action_execute_toggle(desk, screen))
        # print(ct.action_execute_decoration(desk, screen))
        # print(ct.action_execute_restore(desk, screen))
        # print(ct.action_execute_cycle_next(desk, screen))
        # print(ct.action_execute_cycle_previous(desk, screen))
        # print(ct.action_execute_layout_vertical_left(desk, screen))
        # print(ct.action_execute_layout_vertical_right(desk, screen))
        # print(ct.action_execute_layout_horizontal_top(desk, screen))
        # print(ct.action_execute_layout_horizontal_bottom(desk, screen))
        # print(ct.action_execute_layout_maximized(desk, screen))
        # print(ct.action_execute_layout_fullscreen(desk, screen))
        # print(ct.action_execute_master_make(desk, screen))
        # print(ct.action_execute_master_make_next(desk, screen))
        # print(ct.action_execute_master_make_previous(desk, screen))
        # print(ct.action_execute_master_increase(desk, screen))
        # print(ct.action_execute_master_decrease(desk, screen))
        # print(ct.action_execute_slave_increase(desk, screen))
        # print(ct.action_execute_slave_decrease(desk, screen))
        # print(ct.action_execute_proportion_increase(desk, screen))
        # print(ct.action_execute_proportion_decrease(desk, screen))
        # print(ct.action_execute_window_next(desk, screen))
        # print(ct.action_execute_window_previous(desk, screen))
        # print(ct.action_execute_reset(desk, screen))

    ct.wait()
