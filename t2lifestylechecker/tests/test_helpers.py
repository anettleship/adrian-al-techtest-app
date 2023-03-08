from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_birth_year_from_constant_age_and_birthday(birthday_month_day: str, age: int) -> str:

    today_object = datetime.now() 
    user_birthday_this_year = str(today_object.year) + birthday_month_day
    user_birthday_this_year_obj = datetime.strptime(user_birthday_this_year, '%Y-%m-%d')
    user_dateofbirth_constant_age_obj = user_birthday_this_year_obj - relativedelta(years=age)
    
    if today_object < user_birthday_this_year_obj:
        user_dateofbirth_constant_age_obj = user_dateofbirth_constant_age_obj - relativedelta(years=1)

    return datetime.strftime(user_dateofbirth_constant_age_obj, '%Y-%m-%d') 
