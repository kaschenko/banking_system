# This is a sample Python script.
import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
Insert = 'INSERT INTO card (number, pin, balance ) VALUES  (?, ?, ?);'
cname = 0
pin = 0
a = 1
b = 1
def check_card(num_):
    num_ = str(num_)
    last_digit_in_original = num_[-1]
    num = list(map(int, num_))
    sum = 0
    for i in range(len(num) - 1):
        if i % 2 == 0:
            num[i] *= 2
        if num[i] > 9:
            num[i] -= 9
        sum += num[i]
    if sum % 10 == 0:
        ldig = 0
    else:
        ldig = 10 - sum % 10
    num_ += str(ldig)
    if last_digit_in_original == num_[-1]:
        return True
    else:
        return False
def add_card(number, pin, balance):
    conn.execute(f'INSERT INTO card (number, pin, balance ) VALUES  ({number}, {pin}, {balance})')
def convert():
    def pr():
        print('1. Create an account\n2. Log into account\n0. Exit')
    def menu():
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
    def card_name():
        f_num = str(int(4 * (10 ** 14)) + int(random.randrange(0, 10 ** 9)))
        num = list(map(int, f_num))
        sum = 0
        for i in range(len(num)):
            if i % 2 == 0:
                num[i] *= 2
            if num[i] > 9:
                num[i] -= 9
            sum += num[i]
        if sum % 10 == 0:
            ldig = 0
        else:
            ldig = 10 - sum % 10
        f_num += str(ldig)
        return int(f_num)
    def PIN():
            return int(random.randrange(1000, 9999))

    print('1. Create an account\n2. Log into account\n0. Exit')
    choice = int(input())
    if choice == 1:
        print('Your card has been created\nYour card number:')
        global cname
        cname = card_name()
        print(cname)
        print('Your card PIN:')
        global pin
        pin = PIN()
        print(pin)
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);
        INSERT INTO card (number, pin) VALUES  ({}, {});
        """.format(cname, pin))
        conn.commit()

    if choice == 2:
        print('Enter your card number:')
        new_cname = int(input())
        print('Enter your PIN:')
        new_pin = int(input())
        if (conn.execute('SELECT count(*) > 0 FROM card WHERE {} = number and {} = pin;'.format(str(new_cname), str(new_pin))).fetchall())[0][0]:
            print('You have successfully logged in!')
            global a
            a = 1
            def convert_2():
                global cname
                balance = (cur.execute(f'SELECT balance FROM card WHERE number = {new_cname};').fetchall())[0][0]
                menu()
                wish_ = int(input())
                if wish_ == 1:

                    print('Balance: ' + str((cur.execute(f'SELECT balance FROM card WHERE number = {new_cname};').fetchall())[0][0]))
                elif wish_ == 2:
                    print('Enter income:')
                    money = int(input())
                    balance += money
                    print('Income was added!')
                    conn.execute('UPDATE card SET balance = {} WHERE number = {};'.format(balance, new_cname))
                    conn.commit()
                elif wish_ == 3:

                    print('Transfer\nEnter card number:')
                    num = int(input())
                    if num == new_cname:
                        print('You can\'t transfer money to the same account!')
                    elif not check_card(num):
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif not ((conn.execute(f'SELECT count(*) > 0 FROM card WHERE number = {num}')).fetchall())[0][0]:
                        print('Such a card does not exist.')

                    else:
                        print('Enter how much money you want to transfer:')
                        sum_ = int(input())
                        if sum_ > balance:
                            print('Not enough money!')
                        else:
                            balance -= sum_
                            conn.execute('UPDATE card SET balance = {} WHERE number = {};'.format(balance, new_cname))
                            balance_transfer_card = (cur.execute(f'SELECT balance FROM card WHERE number = {num};').fetchall())[0][0]
                            balance_transfer_card += sum_
                            conn.execute('UPDATE card SET balance = {} WHERE number = {};'.format(balance_transfer_card, num))
                            conn.commit()
                            print('Success!\n')
                elif wish_ == 4:
                    conn.execute(f'DELETE FROM card WHERE number = {new_cname}')
                    conn.commit()
                    print('The account has been closed!')
                    global a
                    a = 0
                elif wish_ == 5:
                    print('You have successfully logged out!')

                    a = 0
                elif wish_ == 0:
                    print('Bye!')
                    a = 0
                    global b
                    b = 0
            while a == 1:
                convert_2()
        else:
            print('Wrong card number or PIN!')
    if choice == 0:
        print('Bye!')
        global b
        b = 0


while b == 1:
    convert()





