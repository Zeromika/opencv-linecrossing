import cv2
import numpy as np
# Classes Necessary For Detection
# ---------------------------------------------------------


class MaskObj:
    """
    Mask Object where Object holds key information to detected object
    """

    def __init__(self, center_x, center_y, width, height):
        """
        Mask Object Init
        :param arg1: description
        :param arg2: description
        :type arg1: type description
        :type arg1: type description
        :return: return description
        :rtype: the return type description
        """
        self.center_x = center_x
        self.center_y = center_y
        self.width = width

    def get_x(self):
        return self.center_x

    def get_y(self):
        return self.center_y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.get_height

    def __str__(self):
        return "Mask Object {center_x:"+self.center_x + ", center_y:" + center_y + "}"


class Line:
    """
    Line Object Required for usage of LineCrossTest
    """

    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2
        self.__color = (250, 0, 1)
        self.__linetype = 8
        self.__thickness = 2

    def getAttributes():
        return self.__point1, self.__point2, self.__color, self.__linetype, self.__thickness


class LineCrossTest:
    """
    Line Crossing Test Object

    :param line: Line with two coordinates p1, p2
    :param height: Height of the video
    :param width: Width of the video
    :type line: Line Object
    :type height: Float
    :type width: Float

    """

    def __init__(self, line, height, width):
        """
        Line Crossing Test Start
        """
        self.__line = line
        self.__height = height
        self.__width = width
        self.__mask = np.zeros((self.__height, self.__width, 3), np.uint8)

    def getMaskingResult(self, maskObj):
        frame = np.zeros((self.__height, self.__width, 3), np.uint8)
        point1, point2, color, linetype, thickness = self.__line.getAttributes()
        cv2.line(__mask, point1, point2, color, thickness, linetype)
        cv2.circle(frame, (maskObj.get_x(), maskObj.get_y()), maskObj.get_width(
        ), (0, 0, 255), thickness=-1, lineType=8, shift=0)
        if np.any(np.logical_and(frame, __mask)):
            return True
        else:
            return False

# END OF CLASS DEFINITONS
# ---------------------------------------------------------
