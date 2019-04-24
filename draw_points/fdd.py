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
            self.user = loadconfig.get("default", "user")
            self.passwd = loadconfig.get("default", "passwd")
            self.serverid = loadconfig.get("default", "serverid")
            self.host = loadconfig.get("mysql", "host")
            self.sqluser = loadconfig.get("mysql", "user")
            self.sqlpasswd = loadconfig.get("mysql", "passwd")
            self.sqldatabase = loadconfig.get("mysql", "database_name")
            self.table_name = loadconfig.get("mysql", "table_name")
            self.username = loadconfig.get("mysql", "columns_name")
            self.poit = loadconfig.get("mysql", "columns_point")
            self.cookiesX = getcookie(self)
            drawPlaypoints(self)

        def drawPlaypoints(self):
            Frist = 0
            while True:
                day = get_today(0)
                if Frist != day:
                    Frist = day
                    print(Fore.LIGHTCYAN_EX+' ['+Frist+'] today will receive points * '+str(get_today(1)),flush=True)
                    print(Style.RESET_ALL, flush=True)
                get_point(self)
                time.sleep(1)


        def connect_sql(self):
            mydb = mysql.connector.connect(
              host= self.host,
              user= self.sqluser,
              passwd=self.sqlpasswd,
              database= self.sqldatabase
            )
            return mydb

        def get_today(yum):
            my_date = date.today()
            today = calendar.day_name[my_date.weekday()]
            loadconfig = configparser.RawConfigParser()
            loadconfig.readfp(open(r"control/config.txt"))
            ssvote = loadconfig.get("votex2", today)
            if yum == 1:
                return ssvote
            else:
                return today
        def wdatabase(self,username,point,userid):
            del_point(self,userid)
            mydb = connect_sql(self)
            mycursor = mydb.cursor()
            sql = ("SELECT "+self.poit+" FROM "+self.table_name+" WHERE "+self.username+" ='"+username+"'")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for point_db in myresult:
                ssvote = (point*get_today(1))
                update_point = (int(point_db[0])+int(ssvote))
                sql = ("UPDATE "+self.table_name+" SET "+self.poit+" = '"+str(update_point)+"' WHERE "+self.username+" = '"+username+"'")
                mycursor.execute(sql)
                mydb.commit()
                getpointeiei =  (' user[*name] '+username +' get  point : '+ssvote)
                print(Fore.GREEN+getpointeiei, flush=True)
                print(Style.RESET_ALL, flush=True)


        def get_point(self):
            try:
                url = ("https://playserver.in.th:443/index.php/MyServerCheckPoint/index/"+self.serverid)
                cokkie = {"ci_session": self.cookiesX}
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": url, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                checkpoit = requests.post(url, headers=header, cookies=cokkie)
                soup = BeautifulSoup(checkpoit.text,"html.parser")
                div = soup.find_all("div")[19]
                userpoit = div.find_all("button",class_='btn-servercheckpoint-editpoint button')
                for i in userpoit:
                    userid = i['data-id'].splitlines()
                    point = i['data-point'].splitlines()
                    username = i['data-gameid'].splitlines()
                    wdatabase(self,str(username[0]),int(point[0]),userid[0])
            except:
                print('An error occurred network,serverid ')
                self.cookiesX = getcookie(self)



        def del_point(self,userid):
            try:
                data = {"gameid": '', "neededpage": '', "delpointid": userid, "editpointid": '', "editpointamt": ''}
                url = ("https://playserver.in.th:443/index.php/MyServerCheckPoint/index/"+self.serverid)
                cokkie = {"ci_session": self.cookiesX}
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": url, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                delusepoint = requests.post(url, headers=header, cookies=cokkie,data=data)
            except:
                self.cookiesX = getcookie(self)


        def getcookie(self):
            try:
                url = "https://playserver.in.th:443/index.php/Login/login"
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://playserver.in.th/index.php/Login/logout", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                data={"email": self.user, "password": self.passwd}
                getcookie = requests.post(url, headers=header, data=data)
                ss_cookie,newcookie = getcookie.request.headers['Cookie'].split('=')
                e = 0
                for i in newcookie:
                    e +=1
                xcookie = newcookie.replace(newcookie[e-10]+newcookie[e-9]+newcookie[e-8]+newcookie[e-7]+newcookie[e-6]+newcookie[e-5]+newcookie[e-4]+newcookie[e-3]+newcookie[e-2]+newcookie[e-1], "xxxxxxxxxxx")
                print(' Success : New cookie : '+ xcookie)
                return newcookie
            except:
                print(' Please check user / password  -- > control/config.txt')

        run(self)
