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

    def __init__(self, log):
        self.__vcgm = Vcgencmd()
        self.__log = log

        self.__previousoutput = ""

    @staticmethod
    def __addlog(infostring, flag, info):
        response = infostring
        if flag:
            if infostring != "":
                if infostring[-1] != " ":
                    response = response + ", "
            response = response + info

        return response

    def undervoltage(self):
        output = self.__vcgm.get_throttled()

        infostring = ""

        if output['breakdown'][self.__UNDERVOLTED] or \
                output['breakdown'][self.__CAPPED] or \
                output['breakdown'][self.__THROTTLED] or \
                output['breakdown'][self.__SOFT_TEMPLIMIT]:

            infostring = 'Currently: '

            infostring = self.__addlog(infostring, output['breakdown'][self.__UNDERVOLTED],
                                       'Undervoltage')
            infostring = self.__addlog(infostring, output['breakdown'][self.__CAPPED], 'Capped')
            infostring = self.__addlog(infostring, output['breakdown'][self.__THROTTLED],
                                       'Throttled')
            infostring = self.__addlog(infostring, output['breakdown'][self.__SOFT_TEMPLIMIT],
                                       'Soft Temperature Limit')

        if output['breakdown'][self.__HAS_UNDERVOLTED] or \
                output['breakdown'][self.__HAS_CAPPED] or \
                output['breakdown'][self.__HAS_THROTTLED] or \
                output['breakdown'][self.__HAS_SOFT_TEMPLIMIT]:

            infostring = self.__addlog(infostring, True, 'Previously: ')

            infostring = self.__addlog(infostring, output['breakdown'][self.__HAS_UNDERVOLTED],
                                       'Undervoltage')
            infostring = self.__addlog(infostring, output['breakdown'][self.__HAS_CAPPED], 'Capped')
            infostring = self.__addlog(infostring, output['breakdown'][self.__HAS_THROTTLED],
                                       'Throttled')
            infostring = self.__addlog(infostring, output['breakdown'][self.__HAS_SOFT_TEMPLIMIT],
                                       'Soft Temperature Limit')

        if self.__previousoutput != infostring:
            self.__log.info(infostring)
            self.__previousoutput = infostring
