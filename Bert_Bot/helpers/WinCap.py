import cv2
import numpy as np
from ctypes import windll
import win32gui
import win32ui

class imagecap:
    def __init__(self):
        crop_area=(8, 30, 8, 8)
        self.crop_l = crop_area[0]
        self.crop_t = crop_area[1]
        self.crop_r = crop_area[2]
        self.crop_b = crop_area[3]

        self.w = 0
        self.h = 0
        self.offset_x = 0
        self.offset_y = 0
        # self.__update_size_and_offset()

        pass

    def capture_win_alt(self):
        """
        Returns a screenshot of the active window.
        """
        # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui

        windll.user32.SetProcessDPIAware() 
        window_name = "Flyff Universe - Google Chrome"
        self.hwnd = win32gui.FindWindow(None, window_name)

        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :3]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")
        
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img, img_gray


    def debug_window(self):
        # WINDOW_NAME = "Flyff Universe - Google Chrome"
        # WINDOW_NAME = "This PC"
        # WINDOW_NAME = "oracdecor.com | Kwalitatieve interieurdecoratie | Orac Decor® - Google Chrome"
        while cv2.waitKey(1) != ord('q'):
            screenshot, screen2 = self.capture_win_alt()
            cv2.imshow('Computer Vision', screenshot)
            # cv2.waitKey()
            # cv2.destroyAllWindows()

    def __update_size_and_offset(self):
        """
        Size doesn't change often, but it's a step to update the offset. Offset
        do change often, it updates when we move the target window.
        """
        # get the window size
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left - self.crop_l - self.crop_r
        self.h = bottom - top - self.crop_t - self.crop_b

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = left + self.crop_l
        self.offset_y = top + self.crop_t

    def get_screen_pos(self, pos):
        """
        Translate a pixel position on a screenshot image to a pixel position on the screen.

        :param pos: tuple (x, y). Position on the screenshot image.
        :return: tuple (x, y). Position on the screen.
        """
        # imagecap.__update_size_and_offset(self)
        # return (pos[0] + sel
        # f.offset_x, pos[1] + se
        # lf.offset_y)

        # middle of the rectangle
        x = pos[0] + (pos[2] // 2)
        y = pos[1] + (pos[3] // 2)

        # return (pos[0], pos[1])  # aibat offset
        return x, y + 30  # flyff offset