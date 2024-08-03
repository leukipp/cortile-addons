#!/usr/bin/env python3

from cortile import Cortile


def callback(ret):
    print(f'{ret.Name} update')

    if ret.Name == 'Pointer':
        active_button = ct.get_active_button()
        if active_button:
            print(f'Active button: {active_button.Button}')

    if ret.Name == 'Windows':
        active_client = ct.get_active_client()
        if active_client:
            print(f'Active client: {active_client.Latest.Name}', active_client.Window.Id)

    if ret.Name == 'Workplace':
        active_layout = ct.get_active_layout()
        if active_layout:
            print(f'Active layout: {active_layout.Name}', active_layout)

    print()


if __name__ == '__main__':
    ct = Cortile()

    ct.listen(callback)

    ct.wait()
