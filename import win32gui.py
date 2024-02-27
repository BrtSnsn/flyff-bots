import win32gui

while True:
    cursor_info = win32gui.GetCursorInfo()[1]
    print(cursor_info)
