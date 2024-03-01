import cv2
import numpy as np
from collections import deque


class ComputerVision:
    def __init__(self) -> None:
        # i = 0
        pass
        
    def get_point_near_center(center, points):
        dist_two_points = lambda center, point: ((center[0] - (point[0] + point[2] / 2)) ** 2 + (center[1] - (point[1] + point[3] / 2)) ** 2) ** (1 / 2)
        closest_dist = 999999  # Start with a big number for smaller search
        best_point = deque(maxlen=2)
        best_point.append(np.array([0, 0, 0, 0]))
        best_point.append(np.array([0, 0, 0, 0]))
        # best_point.append(0)
        # best_point[0] = None
        # print(best_point)
        # best_point[1] = None
        # i = 0
        # print("start")
        for point in points:
            dist = dist_two_points(center, point)
            # print(dist, closest_dist, point)
            if dist < closest_dist:
                closest_dist = dist
                best_point.append(point)
                # print(best_point)
        # Return the second most nearest point or the nearest point if just have one point.
        # Because the nearest mob sometimes is already dead and we don't want to select it.
        # global i
        # if i == 0:
        #     i = -1
        # elif i == -1:
        #     i = 0
        # print("Done", best_point[0], best_point[1])
        return best_point[0], best_point[1]

    @staticmethod
    def get_all_mobs(img_c, img, mob_name_path: str, th):
        # img_c, img = imagecap().capture_win_alt()
        mob_name = cv2.imread(mob_name_path, cv2.IMREAD_GRAYSCALE)
        img_copy = np.copy(img_c)
        # cv2.imshow('Computer Vision', img)
        result = cv2.matchTemplate(img, mob_name, cv2.TM_CCOEFF_NORMED)
        # cv2.imshow("vision", result)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        w = mob_name.shape[1]
        h = mob_name.shape[0]

        # cv2.rectangle(img_copy, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)
        # cv2.imshow("vision", img_copy)

        # threshold = 0.80
        yloc, xloc = np.where(result >= th)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        for (x, y, w, h) in rectangles:
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0,255,255), 2)
        
        # cv2.imshow("vision", img_copy)
            
        frame_w = img_copy.shape[1]
        frame_h = img_copy.shape[0]
        frame_center = (frame_w // 2, frame_h// 3 * 2)
        # frame_center = (frame_w // 2, frame_h // 6 * 5)

        # print(frame_center, frame_w, frame_h)
        cv2.rectangle(img_copy, (0,0), frame_center, (0,255,255), 2)


        mob_pos1, mob_pos2 = ComputerVision.get_point_near_center(frame_center, rectangles)

        
        # print(mob_pos)

        # x = mob_pos[0] + (mob_pos[2] // 2)
        # y = mob_pos[1] + (mob_pos[3] // 2)
        # text = f"({mob_pos1})"
        font_face = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 5
        font_color = (0, 0, 200)
        font_thickness = 3
        # (text_w, text_h), _ = cv2.getTextSize(text, font_face, font_scale, font_thickness)
        # text_offset_x = (w - text_w) // 2
        # text_offset_y = text_h + 5
        i = 0
        for each in [mob_pos1, mob_pos2]:
            text = str(i)
            i+=1
            x = each[0] + (each[2] // 2)
            y = each[1] + (each[3] // 2)
            text_pos = (x, y)
            cv2.putText(
                img_copy,
                text,
                text_pos,
                font_face,
                font_scale,
                font_color,
                font_thickness,
            )
            cv2.drawMarker(
                img_copy,
                text_pos,
                color=(0,0,200),
                markerType=cv2.MARKER_CROSS,
                markerSize=40,
                thickness=2,
            )
        return rectangles, img_copy, mob_pos1, mob_pos2
    
    @staticmethod
    def template_match(img, image_path: str, threshold, h1 = False, h2 = None, w1 = None, w2 = None):     
        if not h1:
            img_crop = img
        else:
            img_crop = img[h1:h2, w1:w2]
        
        # img_crop = img[150:190, 540:660]
        # img_crop = img[h1:h2, w1:w2]
        # img_crop = img
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(img_crop, template, cv2.TM_CCOEFF_NORMED)
        # _, max_val, _, _ = cv2.minMaxLoc(result)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        passed_threshold = max_val >= threshold

        w = template.shape[1]
        h = template.shape[0]

        cv2.rectangle(img_crop, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

        point = (max_loc[0] + w / 2, max_loc[1] + h / 2)

        return passed_threshold, max_val, img_crop, result, point
    
    def contour_compare(img, threshold, h1, h2, w1, w2):
        """
        dit moet wel pixel perfect zijn dus begin maar de kijken met pyautogui.mouseInfo()
        """
        thresh = False
        image = img[h1:h2, w1:w2]   
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        # max is 900
        threshold = 300
        # print(threshold, area)
        if area < threshold:
            # print("The healthbar has dropped below the limit.")
            thresh = True
        else:
            # print("The healthbar is still above the limit.")
            thresh = False
            pass
        
        return thresh, image
