# %%

import math
import numpy as np
import pandas as pd
import PySimpleGUI as sg


# %% md

## 1. Conversion numeral system

# %%

# 10진법의 수를 m진법으로 나타내었을 때, 최고차항의 차수를 구하기
def finding_max(number, m):
    power = 0
    while True:
        if m ** power > number:
            break
        power += 1
    return int(power - 1)


# 기저숫자를 박스로 나타내기
def box(x, Base):
    if type(x) == list:
        return x
    elif x < 10:
        return x
    elif 9 < x < Base:
        return [x - 9]
    else:
        return print('The number can not be basis digit in Base', Base)


# 입력한 진법의 P를 구한다.
def digit_position_max(base):
    p = 0
    while True:
        if 10 ** (p - 1) > base - 1:
            break
        p += 1
    return int(p - 1)


# sigma를 정의함
def sigma(function, start, end):
    result = 0
    for i in range(start, end + 1):
        result += function(i)
    return result


# 10진법에서 m진법으로 변환하는 함수
def shift_10_to_m(number, m, mark_box=True, mark_base=True):
    n = finding_max(number, m)
    p = digit_position_max(m)

    def f(x):
        return (number // m ** x) * (10 ** (x * p - p))

    result = int(number + sigma(f, 1, n) * (10 ** p - m))

    if mark_box is False:
        result = str(result) + '*'
    else:
        number = str(result)

        zero = '0' * (p - (len(number) % p))
        number = zero + number
        sliced = []
        for i in range(0, len(number), p):
            sliced.append(number[i:i + p])
        result = ''
        for j in sliced:
            result = result + str(box(int(j), m))

        if result[0] == '0':
            result = str(result[1:])
        else:
            pass

    if mark_base is False:
        return result
    else:
        base = '_(%s)' % (m)
        return result + base

# m진법에서 10진법으로 변환하는 함수
def shift_m_to_10(number, m):
    # 쪼개서 숫자들만 갖고, 최고차항의 계수 구하기
    number = str(number)
    numbers = number.split('][')
    numbers[0] = numbers[0].replace('[', '')
    numbers[-1] = numbers[-1].replace(']', '')
    n = len(numbers)

    # 각 자리 숫자를 10진법으로 변환하기
    numbers_10 = []
    for x in numbers:
        numbers_10.append(int(x) + 9)
    numbers_10.reverse()

    result = 0
    for y in range(n):
        result = result + (numbers_10[y] * (m ** y))
    return result


# m진법에서 m^k진법으로 변환하는 함수
"""
number에 ''을 붙여서 []을 이용하여 입력할 것.
"""
def shift_m_to_mk(number, m, mk):
    if '][' in number:
        # 몇 제곱인지 구하기
        k = int(math.log10(mk) / math.log10(m))

        # 쪼개서 숫자들만 갖고, 최고차항의 계수 구하기
        numbers = number.split('][')
        numbers[0] = numbers[0].replace('[', '')
        numbers[-1] = numbers[-1].replace(']', '')

        # 자리 수 구하기
        n = len(numbers)
        v = int(math.ceil(n / k))

        # 각 자리 숫자를 10진법으로 변환하기
        numbers_10 = []
        for x in numbers:
            numbers_10.append(int(x) + 9)

        # 앞의 자리 수가 0인 것을 추가하기
        lack = n - ((n // v) * v)
        for x in range(0, lack):
            numbers_10 = [0] + numbers_10
        numbers_10.reverse()

        # sigma로 표현된 식을 j마다 구하고 str으로 이어 붙이기
        result = ''
        for j in list(range(0, v)):
            j = int(j)

            def f(i):
                position = int(k * j + i)
                return numbers_10[position] * (m ** i)

            result = '[' + str(sigma(f, 0, k - 1) - 9) + ']' + result

    # 기저숫자 하나인 경우
    else:
        result = str(number)

    base = '_(%s)' % (mk)
    return result + base


# m^k진법에서 m진법으로 변환하는 함수
"""
number에 ''을 붙여서 []을 이용하여 입력할 것.
"""
def shift_mk_to_m(number, mk, m):
    if '][' in number:
        # 몇 제곱인지 구하기
        k = int(math.log10(mk) / math.log10(m))

        # 쪼개서 숫자들만 갖고, 최고차항의 계수 구하기
        numbers = number.split('][')
        numbers[0] = numbers[0].replace('[', '')
        numbers[-1] = numbers[-1].replace(']', '')

        # 자리 수 구하기
        v = len(numbers)

        # 각 자리 숫자를 10진법으로 변환하기
        numbers_10 = []
        for x in numbers:
            numbers_10.append(int(x) + 9)
        numbers_10.reverse()

        result = ''
        for j in numbers_10:
            digit = shift_10_to_m(j, m, mark_box=True, mark_base=False)
            length = len(str(digit))
            # 앞에 0을 추가하여 k개를 맞춤
            if length != k:
                differ = int(k - length)
                for x in range(0, differ):
                    digit = '0' + digit
            result = digit + result

        # 앞에 0이 있으면 제거
        while True:
            if result[0] != '0':
                break
            result = result[1:]

    else:
        number = number.replace('[', '').replace(']', '')
        number = int(number) + 9
        result = shift_10_to_m(number, m, mark_box=True, mark_base=False)

    return result


#%% md

## 2. multiplication table

#%%

class mul_table:
    def __init__(self, Base):
        self.Base = Base

    def setdata(self, Base):
        self.Base = Base

    # 10진법 수를 넣으면 입력한 진법의 기저숫자로 출력
    def box(self, x):
        if type(x) == list:
            return x
        elif x < 10:
            return x
        elif 9 < x < self.Base:
            return [x - 9]
        else:
            return print('The number can not be basis digit in Base', self.Base)

    # 박스를 넣으면 원래 10진법 수를 출력
    def dec(self, x):
        if type(x) == int:
            return x
        elif type(x) == list:
            x = x[0]
            x = x + 9
            return x
        else:
            return print('It is can not be basis digit in Base', self.Base)

    # 기저숫자의 덧셈 정의. 기저숫자를 받으면 연산값을 10진법으로 출력한다.
    def add(self, x, y):
        if type(x) == list and type(y) == list:
            return self.dec(x) + self.dec(y)
        elif type(x) == list and type(y) == int:
            return self.dec(x) + y
        elif type(x) == int and type(y) == list:
            return x + self.dec(y)
        else:
            return x + y

    # 기저숫자의 곱셈 정의. 기저숫자를 받으면 연산값을 10진법으로 출력한다.
    def mul(self, x, y):
        if type(x) == list and type(y) == list:
            return self.dec(x) * self.dec(y)
        elif type(x) == list and type(y) == int:
            return self.dec(x) * y
        elif type(x) == int and type(y) == list:
            return x * self.dec(y)
        else:
            return x * y

    # 10진법의 수를 입력하면 Base^0(=1)의 자리의 숫자를 출력한다.
    def ponm_1(self, x):
        if not type(x) == int:
            return print('Maybe it is not value of function ; add or mul')
        else:
            return self.box(x % self.Base)

    # 10진법의 수를 입력하면 Base^1(=m)의 자리의 숫자를 출력한다.
    def ponm_m(self, x):
        if not type(x) == int:
            return print('Maybe it is not value of function ; add or mul')
        else:
            q = x // self.Base
            return self.box(q % self.Base)

    # Basis digit
    def Basis_digit(self):
        result = []
        len = int(self.Base)
        for x in range(len):
            result.append(self.box(x))
        return result

    # 곱셈값 1의 자리들만 가져옴
    def mul_table_1(self):
        # pandas display options
        pd.set_option('display.max_columns', self.Base)
        pd.set_option('display.width', self.Base * 100)

        # 0을 제외한 basis digit를 정의한다.
        Bd = self.Basis_digit()
        Pos_Basis_digit = Bd[1:]

        # Table의 index와 coulumn을 Pos_Basis_digit로 한다.
        ind_and_col = list(map(lambda i: str(i), Pos_Basis_digit))
        table_len = self.Base - 1

        value_1 = []
        for x in Pos_Basis_digit:
            for y in Pos_Basis_digit:
                result = self.mul(x, y)
                result = self.ponm_1(result)
                value_1.append(result)
        value_1 = np.array(value_1).reshape((table_len, table_len))
        return pd.DataFrame(value_1, index=ind_and_col, columns=ind_and_col)

    # 곱셈값 m의 자리들만 가져옴
    def mul_table_m(self):
        # pandas display options
        pd.set_option('display.max_columns', self.Base)
        pd.set_option('display.width', self.Base * 100)

        # 0을 제외한 basis digit를 정의한다.
        Bd = self.Basis_digit()
        Pos_Basis_digit = Bd[1:]

        # Table의 index와 coulumn을 Pos_Basis_digit로 한다.
        ind_and_col = list(map(lambda i: str(i), Pos_Basis_digit))
        table_len = self.Base - 1

        value_m = []
        for x in Pos_Basis_digit:
            for y in Pos_Basis_digit:
                result = self.mul(x, y)
                result = self.ponm_m(result)
                value_m.append(result)

        value_m = np.array(value_m).reshape((table_len, table_len))
        return pd.DataFrame(value_m, index=ind_and_col, columns=ind_and_col)

    # 곱셈값
    def mul_table_m1(self):
        # pandas display options
        pd.set_option('display.max_columns', self.Base)
        pd.set_option('display.width', self.Base * 100)

        # 0을 제외한 basis digit를 정의한다.
        Bd = self.Basis_digit()
        Pos_Basis_digit = Bd[1:]

        # Table의 index와 coulumn을 Pos_Basis_digit로 한다.
        ind_and_col = list(map(lambda i: str(i), Pos_Basis_digit))
        table_len = self.Base - 1

        value_1 = []
        for x in Pos_Basis_digit:
            for y in Pos_Basis_digit:
                result = self.mul(x, y)
                result = self.ponm_1(result)
                value_1.append(result)
        value_1 = np.array(value_1).reshape((table_len, table_len))

        value_m = []
        for x in Pos_Basis_digit:
            for y in Pos_Basis_digit:
                result = self.mul(x, y)
                result = self.ponm_m(result)
                value_m.append(result)
        value_m = np.array(value_m).reshape((table_len, table_len))

        value_m1 = []
        for x in range(table_len):
            for y in range(table_len):
                a = value_m[x][y]
                b = value_1[x][y]
                c = '%s%s' % (a, b)
                value_m1.append(c)
        value_m1 = np.array(value_m1).reshape((table_len, table_len))
        return pd.DataFrame(value_m1, index=ind_and_col, columns=ind_and_col)


# %% md

## 3. Decision prime number


# %%

# 정수를 입력하면 대략적으로 소수인지 아닌지를 판별하는 함수 정의
def rough_decide_print(integer):
    result = 'prime number or not'

    # 사용할 mu들을 설정하고, 소인수들을 리스트로 나열
    MU = [30030, 2310, 210, 30, 6]
    mu_prime_factor = [2, 3, 5, 7, 11, 13]

    # 초기에 30030으로 두고, 적당한 mu를 찾음
    mu = 30030
    for x in MU:
        if integer < x:
            mu = x
            mu_prime_factor = mu_prime_factor[:-2]

    # mu진법의 1의 자리 숫자를 구함
    remainder = integer % mu

    # 나머지와 mu와 서로소인지 확인함
    coprime = True
    for y in mu_prime_factor:
        z = float(remainder % y)
        if z == 0:
            coprime = False
            break

    if coprime == False:
        result = 'composite number'

    return result

# 정수를 입력하면 소수인지 판별하는 함수 정의
def decide_prime(integer):
    rough = rough_decide_print(integer)

    if rough == 'composite number':
        result = 'composite number'
    else:
        result = 'prime number'

        left = math.sqrt(integer)
        left = list(range(2, math.floor(left) + 1))
        right = list(range(2, integer // 2 + 1))

        while True:
            for a in left:
                for b in right:
                    if (a * b) / integer == (a * b) // integer:
                        result = 'composite number'
                        break
            break
    return result


# %%

# compile step1 : window1을 구축함
frame_layout1 = [
    [sg.T('It convert decimal number to other m adic system or the reverse')],
    [sg.T('and m adic system to m^k adic system or the reverse')],
    [sg.Text('Base from : ', size=(8, 1)), sg.InputText(key='base from')],
    [sg.Text('Integer : ', size=(8, 1)), sg.InputText(key='convert integer')],
    [sg.Text('Base to : ', size=(8, 1)), sg.InputText(key='base to')],
    [sg.Submit('Conversion')]
]
frame_layout2 = [
    [sg.T('It print out multiplication table in any base')],
    [sg.Text('Base : ', size=(8, 1)), sg.InputText(key='table Base')],
    [sg.Text('You can choose only the results you need')],
    [sg.Checkbox('position 1', key='position_1'),
     sg.Checkbox('position m', key='position_m'),
     sg.Checkbox('position m1', key='position_m1')],
    [sg.Text('You can save as csv file')],
    [sg.Checkbox('save', key='save'),
     sg.Checkbox('no save', key='no save')],
    [sg.Submit('Get table')]
]
frame_layout3 = [
    [sg.Text('It decide prime number or not in any integer')],
    [sg.Text('Integer : ', size=(8, 1)), sg.InputText(key='prime Base')],
    [sg.Submit('Is it prime?')]
]

layout1 = [
    [sg.Frame(' 1. Conversion numeral system ', frame_layout1, font='Any 12', title_color='blue')],
    [sg.Frame(' 2. Multiplication table ', frame_layout2, font='Any 12', title_color='blue')],
    [sg.Frame(' 3. Decision prime number ', frame_layout3, font='Any 12', title_color='blue')],
    [sg.Button('Exit')]
]

win1 = sg.Window('Numeral System Calculator').Layout(layout1)

# compile step2 : window2을 구축함
win2_active = False
while True:
    ev1, vals1 = win1.Read()

    if ev1 is None or ev1 == 'Exit':
        win1.Close()
        break

    if not win2_active and ev1 == 'Conversion':
        win2_active = True

        Base_from = int(vals1['base from'])
        integer = vals1['convert integer']
        Base_to = int(vals1['base to'])

        if Base_from == 10:
            integer = int(integer)
            layout2 = [[sg.Text('   ' + str(integer))],
                       [sg.Text('= ' + shift_10_to_m(integer, Base_to, mark_box=True, mark_base=True))],
                       [sg.Text('= ' + str(shift_10_to_m(integer, Base_to, mark_box=False, mark_base=True))
                                + str(' (p=') + str(digit_position_max(Base_to)) + str(')'))],
                       [sg.Button('Exit')]]
        elif Base_to == 10:
            integer = str(integer)
            base = '_(%s)' % (Base_from)
            layout2 = [[sg.Text('   ' + str(integer) + base)],
                       [sg.Text('= ' + str(shift_m_to_10(integer, Base_from)))],
                       [sg.Button('Exit')]]
        else:
            if Base_from < Base_to:
                integer = str(integer)
                base = '_(%s)' % (Base_from)
                layout2 = [[sg.Text('   ' + integer + base)],
                           [sg.Text('= ' + str(shift_m_to_mk(integer, Base_from, Base_to)))],
                           [sg.Button('Exit')]]
            else:
                integer = str(integer)
                base = '_(%s)' % (Base_from)
                layout2 = [[sg.Text('   ' + integer + base)],
                           [sg.Text('= ' + str(shift_mk_to_m(integer, Base_from, Base_to)) + '_(' + str(Base_to) + ')')],
                           [sg.Button('Exit')]]

        win2 = sg.Window('Conversion Numeral System', default_element_size=(2, 2), auto_size_text=True,
                         grab_anywhere=True, resizable=True).Layout(layout2)

        while True:
            ev2, vals2 = win2.Read()
            if ev2 is None or ev2 == 'Exit':
                win2_active = False
                win2.Close()
                break

    if not win2_active and ev1 == 'Get table':
        win1.Hide()
        win2_active = True

        object = mul_table(int(vals1['table Base']))
        Basis_digit = ', '.join(map(str, object.Basis_digit()))
        layout2 = [[sg.Text('Base :'), sg.Text(object.Base)],
                   [sg.Text('Basis digit : '), sg.Text(Basis_digit)]]

        if vals1['position_1'] == True:
            layout2.append([sg.Text('')])
            layout2.append([sg.Text('Multiplication table of position 1 :')])
            df_1 = object.mul_table_1()
            layout2.append([sg.Text(df_1)])

            if vals1['save'] == True:
                name = '%s adic system multiplication table of position 1.csv' % (object.Base)
                df_1.to_csv(name)

        if vals1['position_m'] == True:
            layout2.append([sg.Text('')])
            layout2.append([sg.Text('Multiplication table of position m :')])
            df_m = object.mul_table_m()
            layout2.append([sg.Text(df_m)])

            if vals1['save'] == True:
                name = '%s adic system multiplication table of position m.csv' % (object.Base)
                df_m.to_csv(name)

        if vals1['position_m1'] == True:
            layout2.append([sg.Text('')])
            layout2.append([sg.Text('Multiplication table :')])
            df_m1 = object.mul_table_m1()
            layout2.append([sg.Text(df_m1)])

            if vals1['save'] == True:
                name = '%s adic system multiplication table of position m1.csv' % (object.Base)
                df_m1.to_csv(name)

        layout2.append([sg.Button('Exit')])
        win2 = sg.Window('Multiplication table', default_element_size=(2, 2), auto_size_text=True, location=(10, 10),
                         size=(1000, 600), font='Courier', grab_anywhere=False, resizable=True).Layout(layout2)
        while True:
            ev2, vals2 = win2.Read()
            if ev2 is None or ev2 == 'Exit':
                win2_active = False
                win2.Close()
                win1.UnHide()
                break

    if not win2_active and ev1 == 'Is it prime?':
        win2_active = True

        prime_Base = int(vals1['prime Base'])
        layout2 = [[sg.Text(str(prime_Base) + ' is ' + decide_prime(prime_Base))],
                   [sg.Button('Exit')]]

        win2 = sg.Window('Decision prime number', default_element_size=(2, 2), auto_size_text=True,
                         grab_anywhere=True, resizable=True).Layout(layout2)
        while True:
            ev2, vals2 = win2.Read()
            if ev2 is None or ev2 == 'Exit':
                win2_active = False
                win2.Close()
                break





