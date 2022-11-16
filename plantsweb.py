from flask import Flask, render_template, request, escape
from plants import date_format, date_input
import mysql.connector

app = Flask(__name__)

#entry page
@app.route('/')
def entry_page():
    return render_template('entry.html',
                           the_title = 'Учет полива растений')

#result water date page
@app.route('/calc_date', methods=['POST'])      
def calc_date():
    water_date = request.form['water_date']
    results = date_input(water_date)
    current_date = date_format()
    return render_template('results.html', the_current_date = current_date, the_water_date = water_date, the_results = results)

#new plant page + SQL
@app.route('/new_plant', methods=['POST'])
def new_plant():
    plant_name = request.form['plant_name']
    if plant_name:
        with open('plantnames.log', 'a') as log:
            print(plant_name, file=log, end=', ')
        contents = []
        with open('plantnames.log') as rlog:
            for i in rlog:
                contents.append(i)
        print(contents)
        return render_template('new_plant.html', the_plant_name = plant_name, the_rlog =''.join(contents))
    else:
        return render_template('new_plant.html', the_plant_name = 'Вы не ввели название растения')

#authpage
@app.route('/authpage', methods=['GET'])
def authpage():
    return render_template('authpage.html')

#MySQL connection configuration
conconfig = {'host' : '127.0.0.1',
                'user' : 'client',
                'password' : 'client',
                'database' : 'maindb',}

#auth process
@app.route('/authproc', methods=['POST'])
def authproc():
    user = request.form['user']
    passw = request.form['passw']
    conn = mysql.connector.connect(**conconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM logins WHERE (%s) in user AND (%s) in pass"""    
    cursor.execute (_SQL, (user, passw))
    auth_list = cursor.fetchall()
    cursor.close()
    conn.close()
    if auth_list:
        return render_template('authsuc.html')
    else:
        return render_template('register.html')

#register page
@app.route('/registerpage', methods=['GET'])
def registerpage():
    return render_template('register.html')        

#register process
@app.route('/registerproc', methods=['POST'])
def registerproc():
    user = request.form['user']
    passw = request.form['passw']
    conn = mysql.connector.connect(**conconfig)
    cursor = conn.cursor()
    _SQL = """INSERT INTO logins (user, pass) VALUES (%s, %s, )"""    
    cursor.execute (_SQL, (user, passw))
    return render_template('registersuc.html') 

#1. создать юзера в MySQL рут и клиент
#2. создать датабейз мейндб
#3. создать таблицу логинс (айди, юзер, пассв, дата регистрации)
#4. создать вью
#4. дать права юзеру "клиент" на инсерт и селект из строк юзер и пассв в Вью
#5. 


if __name__ == '__main__':
    app.run(debug=True)

###############################################################################################################################################
###############################################################################################################################################
'''
def log_request(req, res: str) -> None:
    ##with open('vsearch.log', 'a') as log:
        ##print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    dbconfig = {'host' : '127.0.0.1',
                'user' : 'vsearch',
                'password' : 'pass',
                'database' : 'vsearchlogDB',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""
    cursor.execute (_SQL, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        'testAgent',                    ###working, short
                        #req.headers.get('User-Agent'), ###working, too much tablespace
                        #req.user_agent.browser,        ###not working
                        res, ))
    conn.commit()
    # _SQL = """select * from log"""
    # cursor.execute(_SQL)
    # for row in cursor.fetchall():
    #     print(row)
    cursor.close()
    conn.close()

@app.route('/viewlog')
def view_the_log():
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
'''