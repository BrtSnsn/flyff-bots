
from threading import Thread

from Bert_Bot.helpers.WinCap import imagecap
from Bert_Bot.helpers.Vision import ComputerVision
import cv2

# from foreground_vision_bot.libs.human_mouse.HumanMouse import HumanMouse

"""
https://github.com/ClarityCoders/fishington.io-bot/blob/main/main/bot.py
https://github.com/ClarityCoders/ComputerVision-OpenCV/blob/master/Lesson3-TemplateMatching/Tutorial.ipynb
"""

class Bot:
    def __init__(self) -> None:
        self.imagecap = imagecap
        Thread(target=self.__frame_thread, daemon=True).start()
        Thread(target=self.__farm_thread, daemon=True).start()
        self.window = None

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

            except:
                print("fail on screen collection")
                pass

    def __get_mobs_position(self):
        mob_name = r"C:\\Users\\bsa\\PycharmProjects\\flyff-bots\\Bert_Bot\\aibat.png"
        m, df, mobpos = ComputerVision.get_all_mobs(self.frame_c, self.frame, mob_name)

        return m, df, mobpos

    def __farm_thread(self):
        while True:
            try:
                matches, df, mobpos = self.__get_mobs_position()
                self.window = df
                # if matches:
                #     self.__kill_mobs(self, points=matches, window=df)
                #     pass
                pass
            except:
                pass


    def __kill_mobs(self, points, window):

        pass




if __name__ == '__main__':
    Bot()
    pass