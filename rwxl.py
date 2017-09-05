import xlrd
import csv

__possible_name = {'姓名', 'name', 'xm', 'un'}
__possible_ticket = {'准考证', '准考证号', 'zkzh', 'kh'}


def _get_index(header):
    """
    get indexes of name and ticket from excel file
    :param header: a list returned from sheet.row_values(0)
    :return: a tuple (index of name, index of ticket)
    """
    name_index, ticket_index = -1, -1
    for idx, title in enumerate(header):
        if title in __possible_name:
            name_index = idx
        if title in __possible_ticket:
            ticket_index = idx
    return name_index, ticket_index


def gather(xlsname):
    """
    Extract students' names and tickets from excel file
    :param xlsname: excel filename
    :return: all students' names and tickets in an iterable
    """
    stu_info = xlrd.open_workbook(xlsname).sheet_by_index(0)
    name, ticket = _get_index(stu_info.row_values(0))
    return zip(stu_info.col_values(name)[1:], stu_info.col_values(ticket)[1:])


def assemble(csvname, grades):
    """
    Write all grades into a csv file
    :param csvname: output file name
    :param grades: students information to be writen
    :return: None
    """
    with open(csvname, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('name', 'university', 'level', 'ticket',
                         'total', 'listening', 'comprehension', 'writing',
                         'oral ticket', 'oral rating'))
        for grade in grades:
            writer.writerow(grade)


if __name__ == '__main__':
    for name, ticket in gather('四六级准考证号.xlsx'):
        print(name, ticket)
