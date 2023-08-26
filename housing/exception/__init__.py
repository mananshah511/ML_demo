import os
import sys

class HousingException(Exception):

    def __init__(self, error_message:Exception, error_details:sys):
        super().__init__(error_message)
        self.error_message = HousingException.get_detailed_error_message(error_message=error_message,error_details=error_details)


    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_details:sys):
        _ , _ ,exec_tb = error_details.exc_info()
        line_number = exec_tb.tb_frame.f_lineno
        file_nme = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occured in script:{file_nme} at line number {line_number} error message is {error_message}"
        return error_message
    

