
from threading import Thread, Lock

from Bert_Bot.helpers.WinCap import imagecap
from Bert_Bot.helpers.Vision import ComputerVision
import cv2
from time import sleep, time
import win32gui, win32ui, win32con, win32api
from ctypes import windll
from collections import deque
import numpy as np

from Bert_Bot.helpers.HumanMouse import HumanMouse
from Bert_Bot.helpers.HumanKeyboard import HumanKeyboard, VKEY

"""
https://github.com/ClarityCoders/fishington.io-bot/blob/main/main/bot.py
https://github.com/ClarityCoders/ComputerVision-OpenCV/blob/master/Lesson3-TemplateMatching/Tutorial.ipynb
"""

class Bot:
    def __init__(self) -> None:
        self.imagecap = imagecap
        self.lock = Lock()

        self.frame_c = None
        self.frame = None
        self.th_existence = False
        self.th_health = False
        # self.window = self.frame_c

        self.matches = None
        self.window = None
        self.window2 = None
        self.mobpos1 = None
        self.mobpos2 = None


        self.cursor_all = deque(maxlen=2)
        self.cursor_all.append(0)
        self.cursor_all.append(0)

        self.kill_count = 0

        capture_thread = Thread(target=self.__frame_thread, daemon=True)
        process_thread = Thread(target=self.__farm_thread, daemon=True)
        existence_thread = Thread(target=self.__check_mob_existence, daemon=True)
        health_thread = Thread(target=self.__check_mob_health, daemon=True)
        imageprocesssing_thread = Thread(target=self.__get_mobs_position, daemon=True)

        self.mouse = HumanMouse(self.imagecap.get_screen_pos)
        self.keyboard = HumanKeyboard()

        capture_thread.start()
        process_thread.start()
        existence_thread.start()
        health_thread.start()
        imageprocesssing_thread.start()


        while cv2.waitKey(1) != ord('q'):
            try:
                cv2.imshow("vision", self.window)
                # cv2.imshow("vision2", self.window2)
                pass
            except Exception as e:
                print(e)
                pass
        # input("__")
        pass


    def __frame_thread(self):
        # while True:
        #     try:
        #         self.frame_c, self.frame = self.imagecap.capture_win_alt(self)

        #     except Exception as e:
        #         print(f"screen collect fail {e}")
        #         pass

        hdesktop = win32gui.GetDesktopWindow()
        (l, r, w, h) = win32gui.GetClientRect(hdesktop)
        hdc = win32gui.GetWindowDC(hdesktop)
        mfc_dc  = win32ui.CreateDCFromHandle(hdc)

        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        while True:
            try:
                """
                Returns a screenshot of the active window.
                https://stackoverflow.com/questions/69425612/createcompatibledc-or-deletedc-fail-in-continues-loop-in-python-possible-m
                If chrome is the window, you should just screenshot your whole screen and use that.
                """

                window_name = "Flyff Universe - Google Chrome"
                hwnd = win32gui.FindWindow(None, window_name)

                

                # If Special K is running, this number is 3. If not, 1
                result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

                bmpinfo = bitmap.GetInfo()
                bmpstr = bitmap.GetBitmapBits(True)

                img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
                self.frame_c = np.ascontiguousarray(img)[..., :3]  # make image C_CONTIGUOUS and drop alpha channel

                if not result:  # result should be 1
                    win32gui.DeleteObject(bitmap.GetHandle())
                    save_dc.DeleteDC()
                    mfc_dc.DeleteDC()
                    win32gui.ReleaseDC(hwnd, hdesktop)
                    raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")
                
                self.frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            except Exception as e:
                print(f"screen collect fail {e}")
                pass




    def __get_mobs_position(self):
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\aibat.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mushpang.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\fefern.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\lawolf2.png"
        mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\lawolf3.png"
        while True:
            try:
                m, df, mobpos1, mobpos2 = ComputerVision.get_all_mobs(self.frame_c, self.frame, mob_name)

                self.matches = m
                self.window = df
                self.mobpos1 = mobpos1
                self.mobpos2 = mobpos2
            except Exception as e:
                print(f"fail get mobs position {e}")
                pass

        # return m, df, mobpos1, mobpos2


    def __farm_thread(self):
        i = 0
        while True:
            try:
                # matches, df, mobpos1, mobpos2 = self.__get_mobs_position()
                # self.window = df
                
                # print(matches)
                # print(mobpos1,mobpos2)
                if len(self.matches) > 0:
                    # self.lock.acquire()
                    # print(mobpos)
                    # self.lock.release()
                    if self.kill_count % 2 == 0 and not np.all(self.mobpos2 == 0):
                        # print("kill close", self.kill_count, "mobpos1", self.mobpos1, "mobpos2", self.mobpos2)
                        self.__kill_mobs(mob_pos=self.mobpos2)
                    elif self.kill_count % 2 == 0 and not np.all(self.mobpos1 == 0):
                        # print("kill far", self.kill_count, "mobpos1", self.mobpos1, "mobpos2", self.mobpos2)
                        self.__kill_mobs(mob_pos=self.mobpos1)
                    elif self.kill_count % 2 != 0 and not np.all(self.mobpos1 == 0):
                        # print("kill far", self.kill_count, "mobpos1", self.mobpos1, "mobpos2", self.mobpos2)
                        self.__kill_mobs(mob_pos=self.mobpos1)
                    elif self.kill_count % 2 != 0 and not np.all(self.mobpos2 == 0):
                        # print("kill close", self.kill_count, "mobpos1", self.mobpos1, "mobpos2", self.mobpos2)
                        self.__kill_mobs(mob_pos=self.mobpos2)
                    else:
                        pass

            except Exception as e:
                print(f"fail farm {i} {e}")
                i += 1
                # self.__no_mobs_to_kill()
                pass


    def __kill_mobs(self, mob_pos):
        """
        This function kills the mobs by moving the mouse to the mob's position, clicking on it, and pressing the "1" key
        it then waits for the healthbar detection thread to return a positive, it presses the "s" key if no healthbar is seen to stop movement. 

        """
        # self.lock.acquire()
        # print("h")
        # self.lock.release()
        if self.th_health:
            # fight still going on
            pass
        else:
            self.mouse.move(to_point=mob_pos, duration=0)
            if self.th_existence:
                # self.lock.acquire()
                # self.lock.release()
                self.mouse.left_click()
                self.keyboard.hold_key(VKEY["numpad_1"], press_time=0.06)
                sleep(0.5)  # give time to the healtbar detection thread to return a positive

                if not self.th_health:
                    self.keyboard.hold_key(VKEY["s"], press_time=0.06)
                    print("reset")
                else:
                    fight_time = time()
                    while True:
                        print(self.th_health)
                        if not self.th_health:
                            self.kill_count += 1
                            print(self.kill_count)
                            self.keyboard.hold_key(VKEY["numpad_2"], press_time=0.06)
                            sleep(0.2)
                            self.keyboard.hold_key(VKEY["numpad_2"], press_time=0.06)
                            sleep(0.2)
                            self.keyboard.hold_key(VKEY["numpad_2"], press_time=0.06)
                            break
                        elif self.th_health and (time() - fight_time) >= int(3):
                            print("pressing 1")
                            self.keyboard.hold_key(VKEY["numpad_1"], press_time=0.06)
                            fight_time = time()
                        else:
                            pass
                    # while True:
                    pass
                
                    #     if not self.th_health:
                    #         self.kill_count += 1
                    #         print(self.kill_count)
                    #         break
                    #     else:
                    #         if (time() - fight_time) >= int(20):
                    #             print('fight time crossed')
                    #             print(time())
                    #             print(fight_time)
                    #             # self.keyboard.hold_key(VKEY["esc"], press_time=0.06)
                    #             self.keyboard.press_key(VKEY["esc"])
                    #             break
                    #         # print("sleep")
                    #         # sleep(float(1))
                    #         pass
        pass

    def __no_mobs_to_kill(self):
        print("No Mobs in Area, moving.")
        # self.keyboard.human_turn_back()
        self.keyboard.hold_key(VKEY["w"], press_time=0.05)
        self.keyboard.hold_key(VKEY["right_arrow"], press_time=0.02)
        # self.keyboard.press_key(VKEY["w"])
        # self.keyboard.press_key(VKEY["w"])
        # self.keyboard.press_key(VKEY["w"])
        # self.keyboard.press_key(VKEY["right_arrow"])
        
        sleep(0.1)
        self.keyboard.press_key(VKEY["s"])

    def __check_mob_existence(self):
        while True:
            cur1 = win32gui.GetCursorInfo()[1]
            sleep(0.1)
            cur2 = win32gui.GetCursorInfo()[1]
            if cur1 != cur2:
                self.th_existence = True
            else:
                self.th_existence = False


    def __check_mob_health(self):
        """
        description: This function checks if the mob is still alive by checking the health bar.
        
        """
        temp_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mob_life_bar2.png"
        thr = 0.75
        while True:
            try:
                thresh, _, df, _ = ComputerVision.template_match(self.frame, temp_name, thr, h1=150, h2=190, w1=540, w2=660)
                self.window2 = df
                self.th_health = thresh
            except Exception as e:
                print('fail check mob health', e)
                self.th_health = False

    def __check_player_health(self):
        """
        description: This function checks if the mob is still alive by checking the health bar.
        
        """
        temp_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\player_health.png"
        thr = 0.95
        while True:
            try:
                thresh, _, df, _ = ComputerVision.template_match(self.frame, temp_name, thr)
                self.window2 = df
                self.th_health = thresh
            except Exception as e:
                print('fail check mob health', e)
                self.th_health = False



if __name__ == '__main__':
    Bot()
    pass