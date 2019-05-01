# -*- coding: utf-8 -*-
import configparser,sys,os,requests,base64,threading,time,ctypes,re,calendar,mysql.connector
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
from datetime import date
import gc


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
            self.cokkie = getcookie(self)
            Create_TableGKX(self)


        def Create_TableGKX(self):
                mydb = connect_sql(self)
                mycursor = mydb.cursor()
                mycursor.execute("SHOW TABLES")
                tables_list = [x[0] for x in mycursor]
                #CREATE TABLES
                if 'gkx' and 'gkx_wait' not in tables_list:
                    mycursor.execute("CREATE TABLE gkx (account_id INT AUTO_INCREMENT PRIMARY KEY, point BIGINT, point_total BIGINT)")
                    mycursor.execute("CREATE TABLE gkx_wait (id INT AUTO_INCREMENT PRIMARY KEY, userid VARCHAR(255),point INT,lastupdate DATETIME)")
                    print(' CREATE TABLE gkx , gkx_wait')
                mydb.close()
                del mydb,mycursor,tables_list
                drawpointgkx(self)


        def drawpointgkx(self):
            print(' # draw point funtion')
            while True:
                get_point(self)
                time.sleep(int(self.delay))


        def wdatabase(self,username,point):
            dxtime = time.strftime('%Y-%m-%d %H:%M:%S')
            npoint = int((point*get_today(1)))
            print((' '+dxtime+'  USER: {0} '+'GET POINT {1}').format(username,npoint),flush=True)
            csql = connect_sql(self)
            mycursor = csql.cursor()
            mycursor.execute(("SELECT "+self.game_acc_fld +" FROM "+self.table_login+" WHERE "+self.game_user_fld+" ='"+username+"' LIMIT 1"))
            acc_list = [x[0] for x in mycursor]
            if acc_list != []:
                accid = acc_list[0]
                mycursor.execute(("SELECT point FROM gkx_wait WHERE userid = '{0}' LIMIT 1").format(username))
                old_pointw = [x[0] for x in mycursor]
                if old_pointw != []:
                    OLDPW = int(old_pointw[0])
                    npoint = (npoint+OLDPW)
                    mycursor.execute(("DELETE FROM gkx_wait WHERE userid = '{0}'").format(username))
                    csql.commit()
                mycursor.execute(("SELECT point, point_total FROM gkx WHERE account_id = '{0}'").format(accid))
                listpoint = mycursor.fetchall()
                if listpoint != []:
                    nmpoint = (npoint +listpoint[0][0])
                    ntpoint = (npoint +listpoint[0][1])
                    mycursor.execute(("UPDATE gkx SET point = '{0}', point_total = '{1}' WHERE account_id = '{2}'").format(nmpoint,ntpoint,accid))
                    csql.commit()
                    csql.close()
                else:
                    sql = "INSERT INTO gkx (account_id, point,point_total) VALUES (%s, %s, %s)"
                    vals = (accid, npoint,npoint)
                    mycursor.execute(sql, vals)
                    csql.commit()
                    csql.close()

            else:
                mycursor.execute(("SELECT point FROM gkx_wait WHERE userid = '{0}' LIMIT 1").format(username))
                old_pointw = [x[0] for x in mycursor]
                if old_pointw != []:
                    npoint = (old_pointw[0]+npoint)
                    mycursor.execute(("UPDATE gkx_wait SET point = '{0}', lastupdate = '{1}' WHERE userid = '{2}'").format(npoint,dxtime,username))
                    csql.commit()
                    csql.close()
                else:
                    sql = ("INSERT INTO gkx_wait (userid, point,lastupdate) VALUES (%s, %s, %s)")
                    vals = (username, npoint,dxtime)
                    mycursor.execute(sql, vals)
                    csql.commit()
                    csql.close()

        def get_point(self):
            try:
                url = ("https://playserver.in.th:443/index.php/MyServerCheckPoint/index/"+self.server_psv)
                cokkie = {"ci_session": self.cokkie}
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": url, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                checkpoit = requests.post(url, headers=header, cookies=cokkie)
                soup = BeautifulSoup(checkpoit.text,"html.parser")
                div = soup.find_all("div")[19]
                userpoit = div.find_all("button",class_='btn-servercheckpoint-editpoint button')
                del div,soup,checkpoit,header,cokkie,url
                if userpoit != []:
                    resetpoint(self)
                    for i in userpoit:
                        point = i['data-point'].splitlines()
                        username = i['data-gameid'].splitlines()
                        wdatabase(self,str(username[0]),int(point[0]))
                del userpoit
            except:
                print(' An error occurred network,serverid ')
                self.cokkie = getcookie(self)

        def get_today(yum):
            my_date = date.today()
            today = calendar.day_name[my_date.weekday()]
            loadconfig = configparser.RawConfigParser()
            loadconfig.readfp(open(r"control/config.txt"))
            ssvote = loadconfig.get("votex2", today)
            if yum == 1:
                del loadconfig,today,my_date
                return int(ssvote)
            else:
                del ssvote,loadconfig,my_date
                return today

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


        def getcookie(self):
            try:
                url = "https://playserver.in.th:443/index.php/Login/login"
                header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://playserver.in.th/index.php/Login/logout", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                data={"email": self.user_psv, "password": self.passwd_psv}
                getcookie = requests.post(url, headers=header, data=data)
                ss_cookie,newcookie = getcookie.request.headers['Cookie'].split('=')
                return newcookie
            except:
                print('\n Please check user / password  -- > control/config.txt')

        def connect_sql(self):
            mydb = mysql.connector.connect(
                host= self.host,
                user= self.sqluser,
                passwd=self.sqlpasswd,
                database= self.sqldatabase
            )
            return mydb


        run(self)
