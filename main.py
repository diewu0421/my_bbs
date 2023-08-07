import time

import win32com.client


def click(dm, x, y):
    dm.moveto(x, y)
    time.sleep(0.1)
    dm.leftclick()


def dm_action():
    dm = win32com.client.Dispatch("dm.dmsoft")
    print(dm.ver())
    dm_ret = dm.reg("yonghu84f875b03fb0d5c536a56a631156628a", "yk0061141")
    print(dm_ret)

    dm_ret = dm.BindWindowEx(198208, "dx2", "windows", "windows", "", 0)
    print(dm_ret)

    ret, x, y = dm.FindColor(68, 0, 2000, 2000, "fd4948-000000", 1.0, 0)
    print(ret, x, y)
    click(dm, x, y)

    pass


if __name__ == '__main__':
    dm_action()
