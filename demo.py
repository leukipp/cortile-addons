#!/usr/bin/env python3

from cortile import Cortile


def callback(event):

    if event.Name == 'Workplace':
        active_layout = ct.get_active_layout()
        if active_layout:
            print(f'Active layout: {active_layout.Name}', active_layout.Location)
        else:
            print(f'Active layout: {None}')

    if event.Name == 'Windows':
        active_client = ct.get_active_client()
        if active_client:
            print(f'Active client: {active_client.Window.Id}', active_client.Latest)
        else:
            print(f'Active client: {None}')

    if event.Name == 'Pointer':
        last_pointer = event.Data
        if last_pointer:
            print(f'Last pointer: {next((k for k, v in last_pointer.Device.Button.items() if v), None)}', last_pointer.Device.Position)

    if event.Name == 'Corner':
        last_corner = event.Data
        if last_corner:
            print(f'Last corner: {last_corner.Name}', last_corner.Location)

    if event.Name == 'Action':
        last_action = event.Data
        if last_action:
            print(f'Last action: {last_action.Name}', last_action.Location)


if __name__ == '__main__':
    ct = Cortile()

    ct.listen(callback)

    client = ct.get_active_client()
    if client:
        id = client.Window.Id
        desktop = ct.get_active_workspace()
        screen = ct.get_active_screen()

        for layout in ct.get_active_layouts():
            print(f'Active layout: {layout.Name}', layout.Location)

        for client in ct.get_active_clients():
            print(f'Active client: {client.Latest.Name}', client.Latest.Location)

        print(ct.get_active_workspace())
        print(ct.get_active_screen())

        print(ct.get_workspace_count())
        print(ct.get_screen_count())

        print(ct.get_workspace_dimensions())
        print(ct.get_screen_dimensions())

        print(ct.get_windows())
        print(ct.get_clients())

        # print(ct.desktop_switch(desktop))

        # print(ct.window_activate(id))

        # print(ct.window_to_desktop(id, desktop))
        # print(ct.window_to_position(id, x=1000, y=500))
        # print(ct.window_to_screen(id, screen))

        # print(ct.action_execute_enable(desktop, screen))
        # print(ct.action_execute_disable(desktop, screen))
        # print(ct.action_execute_toggle(desktop, screen))
        # print(ct.action_execute_decoration(desktop, screen))
        # print(ct.action_execute_restore(desktop, screen))
        # print(ct.action_execute_cycle_next(desktop, screen))
        # print(ct.action_execute_cycle_previous(desktop, screen))
        # print(ct.action_execute_layout_vertical_left(desktop, screen))
        # print(ct.action_execute_layout_vertical_right(desktop, screen))
        # print(ct.action_execute_layout_horizontal_top(desktop, screen))
        # print(ct.action_execute_layout_horizontal_bottom(desktop, screen))
        # print(ct.action_execute_layout_maximized(desktop, screen))
        # print(ct.action_execute_layout_fullscreen(desktop, screen))
        # print(ct.action_execute_master_make(desktop, screen))
        # print(ct.action_execute_master_make_next(desktop, screen))
        # print(ct.action_execute_master_make_previous(desktop, screen))
        # print(ct.action_execute_master_increase(desktop, screen))
        # print(ct.action_execute_master_decrease(desktop, screen))
        # print(ct.action_execute_slave_increase(desktop, screen))
        # print(ct.action_execute_slave_decrease(desktop, screen))
        # print(ct.action_execute_proportion_increase(desktop, screen))
        # print(ct.action_execute_proportion_decrease(desktop, screen))
        # print(ct.action_execute_window_next(desktop, screen))
        # print(ct.action_execute_window_previous(desktop, screen))
        # print(ct.action_execute_reset(desktop, screen))

    ct.wait()
