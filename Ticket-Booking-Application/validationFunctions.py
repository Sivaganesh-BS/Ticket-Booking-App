import re

class checkValidation:
    def emailCheck(email):
        emailMatch=re.fullmatch('[a-z]\\w.*@.*\\..*',email)
        return emailMatch

    def passwordCheck(password):
        check=re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',password)
        return check

    def phoneNoCheck(phone):
        m=None
        if len(phone)==10:
            m=re.fullmatch('[6-9]\\d{9}',phone)
        elif len(phone)==11:
            m=re.fullmatch('[0][6-9]\\d{9}',phone)
        elif len(phone)==12:
            m=re.fullmatch('[9][1][6-9]\\d{9}',phone)
        elif len(phone)==13:
            m=re.fullmatch('[+][9][1][6-9]\\d{9}',phone)

        return m
    



if __name__ == '__main__':
    res=checkValidation.emailCheck('abc@gmail.com')
    print(res)
