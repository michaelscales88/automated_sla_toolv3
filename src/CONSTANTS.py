import os
import openpyxl

from src.input_valididation import valid_input
from os import path

SELF_PATH = os.path.dirname(path.dirname(path.abspath(__file__)))
ROOT_DIRECTORY = os.path.dirname(path.dirname(path.abspath(__file__)))
wb = openpyxl.load_workbook('%s/bin/CONFIG.xlsx' % SELF_PATH)
constants_page = wb.get_sheet_by_name("CONSTANTS")

CALL_DETAILS_FIRST_PAGE_NAME = valid_input('B', 1, constants_page, 'S')
ABANDON_CALLS_GROUP_PAGE_NAME = valid_input('B', 2, constants_page, 'S')
SUMMARY_PAGE = valid_input('B', 3, constants_page, 'S')
CLIENT_LIST_SHEET = valid_input('B', 4, constants_page, 'S')
ARG_PATH = SELF_PATH + valid_input('B', 5, constants_page, 'S')
EXC_PATH = SELF_PATH + valid_input('B', 6, constants_page, 'S')
DOWNLOAD_PATH = SELF_PATH + valid_input('B', 7, constants_page, 'S')
MOD_CALL_DETAILS_PATH = valid_input('B', 8, constants_page, 'S')
USER_NAME = valid_input('B', 9, constants_page, 'S')
PASSWORD = valid_input('B', 10, constants_page, 'S')
LOGIN_TYPE = valid_input('B', 11, constants_page, 'S')
USER_NAME2 = valid_input('B', 12, constants_page, 'S')
PASSWORD2 = valid_input('B', 13, constants_page, 'S')
LOGIN_TYPE2 = valid_input('B', 14, constants_page, 'S')
ATTACH_DIR = valid_input('B', 15, constants_page, 'S')
ATTACH_DIR2 = valid_input('B', 16, constants_page, 'S')
HUNT_GROUP_FIRST_PAGE_NAME = valid_input('B', 17, constants_page, 'S')
HUNT_GRP_ROW = valid_input('B', 20, constants_page, 'N')