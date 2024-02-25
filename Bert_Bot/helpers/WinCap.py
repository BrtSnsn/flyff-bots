import cv2
import numpy as np
from ctypes import windll
import win32gui
import win32ui

class imagecap:
    def __init__(self):
        self.window_name = "Flyff Universe - Google Chrome"
        pass

    def capture_win_alt(self):
        # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui

        # windll.user32.SetProcessDPIAware()
        window_name = "Flyff Universe - Google Chrome"
        hwnd = win32gui.FindWindow(None, window_name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :3]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
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

    def health_bar_view(self):
        WINDOW_NAME = "Flyff Universe - Google Chrome"
        health_bar_image = cv2.imread("C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\mob_life_bar.png", cv2.IMREAD_GRAYSCALE)
        
        while cv2.waitKey(1) != ord('q'):
            img_c, img = imagecap().capture_win_alt()
            img_copy = np.copy(img_c)
            # cv2.imshow('Computer Vision', img)
            result = cv2.matchTemplate(img, health_bar_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            w = health_bar_image.shape[1]
            h = health_bar_image.shape[0]

            cv2.rectangle(img_copy, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)
            cv2.imshow("vision", img_copy)
        pass

def main():
    WINDOW_NAME = "Flyff Universe - Google Chrome"
    mob_name = cv2.imread("C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\aibat.png", cv2.IMREAD_GRAYSCALE)
    
    while cv2.waitKey(1) != ord('q'):
        img_c, img = imagecap().capture_win_alt()
        img_copy = np.copy(img_c)
        # cv2.imshow('Computer Vision', img)
        result = cv2.matchTemplate(img, mob_name, cv2.TM_CCOEFF_NORMED)
        # cv2.imshow("vision", result)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        w = mob_name.shape[1]
        h = mob_name.shape[0]

        # cv2.rectangle(img_copy, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)
        # cv2.imshow("vision", img_copy)

        threshold = 0.75
        yloc, xloc = np.where(result >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        for (x, y, w, h) in rectangles:
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0,255,255), 2)
        
        cv2.imshow("vision", img_copy)
        
    pass

if __name__ == '__main__':

    imagecap().debug_window()
    # imagecap().health_bar_view()
    # main()