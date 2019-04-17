class MyException(Exception):
    def __init__(self, msg):
        self.mes = msg

try:
    if 0 = 0:
        raise MyException('你的金额等于0!')
    else:
        print('余额充足!')
except MyException as e:
    print(e)
