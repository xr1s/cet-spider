import rwxl
from cetdb import chsi

if __name__ == '__main__':
    result = chsi.query(rwxl.gather('四六级准考证号.xls'))
    for stu_info in result:
        if isinstance(stu_info, Exception):
            print(*stu_info.args)
    valid = [r for r in result if not isinstance(r, Exception)]
    rwxl.assemble('cet-grades.csv', valid)
