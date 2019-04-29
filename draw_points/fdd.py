# -*- coding: utf-8 -*-
import configparser,sys,os,requests,base64,threading,time,ctypes,re,calendar,mysql.connector
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
from datetime import date

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class startdraw:

    def __init__(self):
        cls()
        print('\n [+] The system retrieve points from playserver to your server automatically\n Support : https://discord.gg/Mgu73TN')
        init(convert=True)
        self.method_1()
    def method_1(self):
        def run(self):
            loadconfig = configparser.RawConfigParser()
            loadconfig.readfp(open(r"control/config.txt"))
            self.user_psv = loadconfig.get("default", "user_psv")
            self.passwd_psv = loadconfig.get("default", "passwd_psv")
            self.server_psv = loadconfig.get("default", "server_psv")
            self.delay = loadconfig.get("default", "delay")
            self.host = loadconfig.get("mysql", "host")
            self.sqluser = loadconfig.get("mysql", "user_sql")
            self.sqlpasswd = loadconfig.get("mysql", "passwd_sql")
            self.sqldatabase = loadconfig.get("mysql", "database_name")
            self.table_login = loadconfig.get("mysql", "table_login")
            self.game_acc_fld = loadconfig.get("mysql", "game_acc_fld")
            self.game_user_fld = loadconfig.get("mysql", "game_user_fld")
            self.cokkie = 0
            Create_TableGKX(self)



        def Create_TableGKX(self):
            try:
                mydb = connect_sql(self)
                mycursor = mydb.cursor()
                mycursor.execute("SHOW TABLES")
                tabeldict = {}
                call_pserverna = """
-----------------------------------------------------------
|                   [{0}]
-----------------------------------------------------------"""
                p = call_pserverna.format(self.sqldatabase)
                print(p)
                u = 0
                for x in mycursor:
                    u += 1
                    if x[0] == 'gkx':
                        print(' ['+str(u)+'] > get tables name  ['+Fore.GREEN+x[0]+Style.RESET_ALL+'] ', flush=True)
                    elif x[0] == self.table_login:
                        print(' ['+str(u)+'] > get tables name  ['+Fore.GREEN+x[0]+Style.RESET_ALL+'] ', flush=True)
                    else:
                        print(' ['+str(u)+'] ? get tables name  ['+x[0]+']', flush=True)
                    tabeldict.update({x[0]:x[0]})
                print(p.splitlines()[1])
                if 'gkx' not in tabeldict:
                    print(Fore.RED+" ["+self.sqldatabase+"] don't have tabel name [GKX] "+Style.RESET_ALL)
                    print(('\n auto install GKX \n GKX need to retrieve data in tabel ['+Fore.GREEN+'{0}'+Style.RESET_ALL+'] \n [1] {1} \n [2] {2} \n').format(self.table_login,self.game_acc_fld,self.game_user_fld))
                    mycursor = mydb.cursor()
                    mycursor.execute("SHOW columns  FROM "+self.table_login)
                    myresult = mycursor.fetchall()
                    cl_check = {}
                    for x in myresult:
                        if x[0] == self.game_acc_fld:
                            cl_check.update({self.game_acc_fld:self.game_acc_fld})
                        if x[0] == self.game_user_fld:
                            cl_check.update({self.game_user_fld:self.game_user_fld})
                    if self.game_acc_fld and self.game_user_fld  in cl_check:
                        print(' INSTALL . . .')
                        mycursor = mydb.cursor()
                        print('\n CREATE TABLE gkx (account_id INT AUTO_INCREMENT PRIMARY KEY, point BIGINT)')
                        print(' CREATE TABLE gkx_wait (id INT AUTO_INCREMENT PRIMARY KEY, userid VARCHAR(255),point INT,lastupdate DATETIME)\n')
                        CREATEGKX_TABLE = """
        -----------------------------------------------------------
        |       account_id              |      point              |
        -----------------------------------------------------------
                 {0}                |         {1}                  \n
                         """

                        mycursor.execute(("SELECT {0}, {1} FROM {2}").format(self.game_acc_fld,self.game_user_fld,self.table_login))
                        myresult = mycursor.fetchall()
                        sql = "INSERT INTO gkx (account_id, point) VALUES (%s, %s)"
                        mycursor.execute("CREATE TABLE gkx (account_id INT AUTO_INCREMENT PRIMARY KEY, point BIGINT)")
                        mycursor.execute("CREATE TABLE gkx_wait (id INT AUTO_INCREMENT PRIMARY KEY, userid VARCHAR(255),point INT,lastupdate DATETIME)")
                        print(CREATEGKX_TABLE.splitlines()[1])
                        print(CREATEGKX_TABLE.splitlines()[2])
                        print(CREATEGKX_TABLE.splitlines()[3])
                        cop = CREATEGKX_TABLE.splitlines()[4]
                        for x in myresult:
                            val = (x[0], 0)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            time.sleep(0.01)
                            print(Fore.CYAN+CREATEGKX_TABLE.splitlines()[4].format(val,0))
                        print(Style.RESET_ALL)
                        cls()
                        self.cokkie = getcookie(self)
                        drawPlaypoints(self)
                    else:
                        if self.game_acc_fld not in cl_check:
                            print(Fore.RED+' fail to find > '+self.game_acc_fld+'  IN '+Style.RESET_ALL+ '['+Fore.GREEN+self.table_login+Style.RESET_ALL+']')
                        if self.game_user_fld in cl_check:
                            print(Fore.RED+' fail to find > '+self.game_user_fld+'  IN '+Style.RESET_ALL+ '['+Fore.GREEN+self.table_login+Style.RESET_ALL+']')
                        print('\n\n Please check your sql setting')
                        time.sleep(3)
                else:
                    cls()
                    self.cokkie = getcookie(self)
                    drawPlaypoints(self)
            except:
                print('Fail to connect to sql, please check your sql setting')

        def drawPlaypoints(self):
            frist = 0
            while True:
                nowdeata = time.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    day = get_today(0)
                    if frist != day:
                        frist = day
                        print('\n'+Fore.LIGHTCYAN_EX+' ['+frist+'] will receive points * '+str(get_today(1))+Style.RESET_ALL,flush=True)
                    get_point(self)
                    time.sleep(int(self.delay))
                except:
                    print(' '+nowdeata+Fore.RED+' : $GKX - error <no message error>  ;'+Style.RESET_ALL,flush=True)


        def get_today(yum):
            my_date = date.today()
            today = calendar.day_name[my_date.weekday()]
            loadconfig = configparser.RawConfigParser()
            loadconfig.readfp(open(r"control/config.txt"))
            ssvote = loadconfig.get("votex2", today)
            if yum == 1:
                return int(ssvote)
            else:
                return today


        def connect_sql(self):
            nowdeata = time.strftime('%Y-%m-%d %H:%M:%S')
            try:
                mydb = mysql.connector.connect(
                    host= self.host,
                    user= self.sqluser,
                    passwd=self.sqlpasswd,
                    database= self.sqldatabase
                )
                return mydb
            except:
                print(nowdeata+Fore.RED+' : $GKX - max_connections please chang your connections ;'+Style.RESET_ALL,flush=True)

        def wdatabase(self,username,point):
            try:
                dx = time.strftime('%Y-%m-%d %H:%M:%S')
                cdb = connect_sql(self)
                mycursor = cdb.cursor()
                sql = ("SELECT "+self.game_acc_fld +" FROM "+self.table_login+" WHERE "+self.game_user_fld+" ='"+username+"'")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for accid in myresult:
                    mycursor.execute("SELECT * FROM gkx_wait")
                    myresult = mycursor.fetchall()
                    for mb in myresult:
                        if username  in mb:
                            old_point = mb[2]
                            sql = ("DELETE FROM gkx_wait WHERE userid = '{0}'")
                            mycursor.execute(sql.format(username))
                            cdb.commit()
                    mycursor.execute(("SELECT point FROM gkx WHERE account_id = '{0}'").format(accid[0]))
                    getoldpoint = mycursor.fetchall()
                    for x in getoldpoint:
                        ssvote = (point*get_today(1))
                        newpoint = (int(ssvote)+int(x[0]))
                        sql = ("UPDATE gkx SET point = '"+str(newpoint)+"' WHERE account_id = '"+str(accid[0])+"'")
                        mycursor.execute(sql)
                        cdb.commit()
                        print((' '+dx+Fore.LIGHTBLUE_EX+' : $user {0} : get new point {1} Saved in gkx  ;'+Style.RESET_ALL).format(username,ssvote),flush=True)
                        cdb.close()
                        return 0
                    updateacc = "INSERT INTO gkx (account_id, point) VALUES (%s, %s)"
                    ssvote = (point*get_today(1))
                    newpoint = (int(ssvote)+int(old_point))
                    vals = (accid[0], newpoint)
                    mycursor.execute(updateacc, vals)
                    cdb.commit()
                    print((' '+dx+Fore.LIGHTBLUE_EX+' : $user {0} : get new point {1} Saved in  gkx  ;'+Style.RESET_ALL).format(username,ssvote),flush=True)
                    cdb.close()
                    return 0

                sqlwait = ("SELECT * FROM gkx_wait")
                mycursor.execute(sqlwait)
                myresult = mycursor.fetchall()
                for mb in myresult:
                    if username  in mb:
                        ssvote = (point*get_today(1))
                        newpoint = (int(ssvote)+int(mb[2]))
                        sql = ("UPDATE gkx_wait SET point = '"+str(newpoint)+"' WHERE userid = '"+username+"'")
                        mycursor.execute(sql)
                        cdb.commit()
                        print((' '+dx+Fore.YELLOW+' : $user {0} : get new point {1} Saved in gkx_wait  ;'+Style.RESET_ALL).format(username,ssvote),flush=True)
                        cdb.close()
                        return 0
                newSQ = "INSERT INTO gkx_wait (userid, point,lastupdate) VALUES (%s, %s, %s)"
                nowdeata = time.strftime('%Y-%m-%d %H:%M:%S')
                ssvote = (point*get_today(1))
                vals = (username, ssvote,nowdeata)
                mycursor.execute(newSQ, vals)
                print((' '+dx+Fore.YELLOW+' : $user {0} : get new point {1} Saved in gkx_wait  ;'+Style.RESET_ALL).format(username,ssvote),flush=True)
                cdb.commit()
                cdb.close()
                return 0
            except:
                print('error max_connections please chang your connections')






        def resetpoint(self):
            while True:
                try:
                    selfurl = ("https://playserver.in.th/index.php/MyServerCheckPoint/index/"+self.server_psv)
                    url = "https://playserver.in.th:443/index.php/MyServerCheckPoint/reset_point"
                    cokkie = {"ci_session": self.cokkie}
                    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": selfurl, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                    data={"server_id": self.server_psv}
                    requests.post(url, headers=header, cookies=cokkie, data=data)
                    return 0
                except:
                    self.cokkie = getcookie(self)



        def get_point(self):
            try:
                threads = []
                url = ("https://playserver.in.th:443/index.php/MyServerCheckPoint/index/"+self.server_psv)
                cokkie = {"ci_session": self.cokkie}
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": url, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                checkpoit = requests.post(url, headers=header, cookies=cokkie)
                soup = BeautifulSoup(checkpoit.text,"html.parser")
                div = soup.find_all("div")[19]
                userpoit = div.find_all("button",class_='btn-servercheckpoint-editpoint button')
                if userpoit != []:
                    resetpoint(self)
                    for i in userpoit:
                        point = i['data-point'].splitlines()
                        username = i['data-gameid'].splitlines()
                        wdatabase(self,str(username[0]),int(point[0]))
            except:
                print(' An error occurred network,serverid ')
                self.cokkie = getcookie(self)

        def getcookie(self):
            try:
                url = "https://playserver.in.th:443/index.php/Login/login"
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://playserver.in.th/index.php/Login/logout", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                data={"email": self.user_psv, "password": self.passwd_psv}
                getcookie = requests.post(url, headers=header, data=data)
                ss_cookie,newcookie = getcookie.request.headers['Cookie'].split('=')
                e = 0
                for i in newcookie:
                    e +=1
                xcookie = newcookie.replace(newcookie[e-10]+newcookie[e-9]+newcookie[e-8]+newcookie[e-7]+newcookie[e-6]+newcookie[e-5]+newcookie[e-4]+newcookie[e-3]+newcookie[e-2]+newcookie[e-1], "xxxxxxxxxxx")
                print('\n Success : new cookie : '+ xcookie)
                return newcookie
            except:
                print('\n Please check user / password  -- > control/config.txt')

        run(self)
