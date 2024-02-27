
from threading import Thread, Lock

from Bert_Bot.helpers.WinCap import imagecap
from Bert_Bot.helpers.Vision import ComputerVision
import cv2
from time import sleep, time
import win32gui
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
            except:
                pass
        pass


    def __frame_thread(self):
        while True:
            try:
                self.frame_c, self.frame = self.imagecap.capture_win_alt(self)

            except Exception as e:
                print(f"screen collect fail {e}")
                pass

    def __get_mobs_position(self):
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\aibat.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mushpang.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\fefern.png"
        mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\lawolf2.png"
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
                    # print(mobpos1)
                    # print(type(mobpos2))
                    if self.kill_count % 2 == 0 and not np.all(self.mobpos2 == 0):
                        self.__kill_mobs(mob_pos=self.mobpos2)
                    elif self.kill_count % 2 == 0 and not np.all(self.mobpos1 == 0):
                        self.__kill_mobs(mob_pos=self.mobpos1)
                    elif self.kill_count % 2 != 0 and not np.all(self.mobpos1 == 0):
                        self.__kill_mobs(mob_pos=self.mobpos2)
                    elif self.kill_count % 2 != 0 and not np.all(self.mobpos2 == 0):
                        self.__kill_mobs(mob_pos=self.mobpos1)
                    else:
                        pass

            except Exception as e:
                print(f"fail farm {i} {e}")
                i += 1
                # self.__no_mobs_to_kill()
                pass


    def __kill_mobs(self, mob_pos):
        i = 0
        # self.lock.acquire()
        # print("h")
        # self.lock.release()
        self.mouse.move(to_point=mob_pos, duration=0)
        # th_exist = self.__check_mob_existence()
        # print(th_exist)
        # if th_exist:
        # print(self.th_health)
        # print(self.th_existence)
        if self.th_existence:
            self.lock.acquire()
            print("click", i)
            i += 1
            self.lock.release()
            # self.mouse.left_click()
            # self.keyboard.hold_key(VKEY["numpad_1"], press_time=0.06)
            # fight_time = time()
            # while True:
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
        temp_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mob_life_bar2.png"
        thr = 0.9
        try:
            thresh = ComputerVision.template_match(self.frame, temp_name, thr)
        except Exception as e:
            print(e)
            thresh = False
        # print("healthbar still visible?",thresh)
        self.th_health = thresh
        # return thresh




if __name__ == '__main__':
    Bot()
    pass