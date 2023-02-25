#!/usr/bin/env python3

from vcgencmd import Vcgencmd


class Undervoltage:
    __UNDERVOLTED = '0'
    __CAPPED = '1'
    __THROTTLED = '2'
    __SOFT_TEMPLIMIT = '3'
    __HAS_UNDERVOLTED = '16'
    __HAS_CAPPED = '17'
    __HAS_THROTTLED = '18'
    __HAS_SOFT_TEMPLIMIT = '19'

    def __init__(self):
        self.__vcgm = Vcgencmd()

    def __print_log(self, flag, info):
        if flag:
            print(info, end=', ')

    def undervoltage(self):
        output = self.__vcgm.get_throttled()

        if output['breakdown'][self.__UNDERVOLTED] or output['breakdown'][self.__CAPPED] or output['breakdown'][
            self.__THROTTLED] or output['breakdown'][self.__SOFT_TEMPLIMIT]:
            print('Currently: ', end=' ')

            self.__print_log(output['breakdown'][self.__UNDERVOLTED], 'Undervoltage')
            self.__print_log(output['breakdown'][self.__CAPPED], 'Capped')
            self.__print_log(output['breakdown'][self.__THROTTLED], 'Throttled')
            self.__print_log(output['breakdown'][self.__SOFT_TEMPLIMIT], 'Soft Temp. Limit')

        if output['breakdown'][self.__HAS_UNDERVOLTED] or output['breakdown'][self.__HAS_CAPPED] or output[
            'breakdown'][self.__HAS_THROTTLED] or output['breakdown'][self.__HAS_SOFT_TEMPLIMIT]:
            print('Previously: ', end=' ')

            self.__print_log(output['breakdown'][self.__HAS_UNDERVOLTED], 'Capped')
            self.__print_log(output['breakdown'][self.__HAS_CAPPED], 'HAS_CAPPED')
            self.__print_log(output['breakdown'][self.__HAS_THROTTLED], 'Throttled')
            self.__print_log(output['breakdown'][self.__HAS_SOFT_TEMPLIMIT], 'Soft Temp. Limit')
