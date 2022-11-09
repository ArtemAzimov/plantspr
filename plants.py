from datetime import date, datetime
import re


#перевод месяца на русский
def month_translator(match):
    month_dict = {'January':'января', 'February':'февраля', 'March':'марта', 'April':'апреля',
                 'May':'мая', 'June':'июня', 'July':'июля', 'August':'августа', 
                 'September':'сентября', 'October':'октября', 'November':'ноября', 'December':'декабря'}
    return month_dict[re.findall(r"\'(.*)\'", str(match))[0]]

#форматинг даты
def date_format():
    today = date.today()
    #current_date = today.strftime('%d.%m.%Y')
    long_date = today.strftime('%d %B %Y')
    mon_date = today.strftime('%B')
    x = re.sub(mon_date, month_translator, long_date)
    return f'{x} года'

#проверка на правильный ввод даты
def date_input(water_date):
    #water_date = input('Введите день полива (в формате дд.мм.гггг): ', )
    if re.match('(3[01]|[12][0-9]|[1-9]|0[1-9]).(1[0-2]|[1-9]|0[1-9]).(20[2-9][2-9]|[3-9][0-9][0-9][0-9])', water_date):
        x_water_date = datetime.strptime(water_date, '%d.%m.%Y').date()
        delta_days = date.today() - x_water_date
        if delta_days.days < 0:
            ddays = abs(delta_days.days)
            return f'Дней до следующего полива: {ddays}'
        else:
            return f'Дней от предыдущего полива:  {delta_days.days}'
    else:
        return('Введите дату не ранее 2022 года в формате дд.мм.гггг')