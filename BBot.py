
from threading import Thread, Lock

from Bert_Bot.helpers.WinCap import imagecap
from Bert_Bot.helpers.Vision import ComputerVision
import cv2
from time import sleep, time

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
        Thread(target=self.__frame_thread, daemon=True).start()
        sleep(1)
        Thread(target=self.__farm_thread, daemon=True).start()
        self.window = None

        self.mouse = HumanMouse(self.imagecap.get_screen_pos)
        self.keyboard = HumanKeyboard()

        while cv2.waitKey(1) != ord('q'):
            try:
                cv2.imshow("vision", self.window)
            except:
                pass


        pass


    def __frame_thread(self):
        while True:
        # while cv2.waitKey(1) != ord('q'):
            try:
                self.frame_c, self.frame = self.imagecap.capture_win_alt(self)

            except Exception as e:
                print(f"screen collect fail {e}")
                pass

    def __get_mobs_position(self):
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\aibat.png"
        # mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mushpang.png"
        mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\fefern.png"
        # try:
        m, df, mobpos = ComputerVision.get_all_mobs(self.frame_c, self.frame, mob_name)
        # except Exception as e:
        #     print(e)

        return m, df, mobpos

    def __farm_thread(self):
        i = 0
        while True:
            try:
                matches, df, mobpos = self.__get_mobs_position()
                self.window = df
                if len(matches) > 0:
                    # self.lock.acquire()
                    # print(mobpos)
                    # self.lock.release()
                    self.__kill_mobs(mob_pos=mobpos)
                    pass
            except Exception as e:
                print(f"fail farm {i} {e}")
                i += 1
                self.__no_mobs_to_kill()
                pass


    def __kill_mobs(self, mob_pos):
        # self.lock.acquire()
        # print("h")
        # self.lock.release()
        self.mouse.move(to_point=mob_pos, duration=0.1)
        if self.__check_mob_existence():
            # self.lock.acquire()
            # print("hh")
            # self.lock.release()
            self.mouse.left_click()
            self.keyboard.hold_key(VKEY["F1"], press_time=0.06)
            fight_time = time()
            while True:
                if not self.__check_mob_health():
                    break
                else:
                    if (time() - fight_time) >= int(15):
                        print('fight time crosse')
                        print(time())
                        print(fight_time)
                        self.keyboard.hold_key(VKEY["esc"], press_time=0.06)
                        break
                    print("sleep")
                    sleep(float(1))
                    pass
        pass

    def __no_mobs_to_kill(self):
        print("No Mobs in Area, moving.")
        self.keyboard.human_turn_back()
        self.keyboard.hold_key(VKEY["w"], press_time=2)
        sleep(0.1)
        self.keyboard.press_key(VKEY["s"])

    def __check_mob_existence(self):
        temp_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\sword.png"
        thresh = ComputerVision.template_match(self.frame, temp_name)
        print("sword?",thresh)
        return thresh
    
    def __check_mob_health(self):
        temp_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\mob_life_bar.png"
        thresh = ComputerVision.template_match(self.frame, temp_name)
        print("healthbar still visible?",thresh)
        return thresh




if __name__ == '__main__':
    Bot()
    pass