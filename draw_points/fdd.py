# -*- coding: utf-8 -*-
import configparser,sys,os,requests,threading,time,ctypes,calendar,mysql.connector
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver


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
            self.key = loadconfig.get("default", "key")
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
                    mycursor.execute("CREATE TABLE gkx (account_id INT AUTO_INCREMENT PRIMARY KEY, point BIGINT, total_point BIGINT)")
                    mycursor.execute("CREATE TABLE gkx_wait (id INT AUTO_INCREMENT PRIMARY KEY, userid VARCHAR(255),point INT,lastupdate DATETIME)")
                    print(' CREATE TABLE gkx , gkx_wait')
                    if 'duckdig' in tables_list:
                        messgle = input(' You want to pull points from Duckdig ? y/n : ')
                        if messgle == 'y':
                            mycursor.execute("SELECT * FROM duckdig")
                            list = mycursor.fetchall()
                            for x in list:
                                sql = "INSERT INTO gkx (account_id, point,total_point) VALUES (%s, %s, %s)"
                                vals = (x[0], x[1],x[2])
                                mycursor.execute(sql, vals)
                                mydb.commit()
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
                mycursor.execute(("SELECT point, total_point FROM gkx WHERE account_id = '{0}'").format(accid))
                listpoint = mycursor.fetchall()
                if listpoint != []:
                    nmpoint = (npoint +listpoint[0][0])
                    ntpoint = (npoint +listpoint[0][1])
                    mycursor.execute(("UPDATE gkx SET point = '{0}', total_point = '{1}' WHERE account_id = '{2}'").format(nmpoint,ntpoint,accid))
                    csql.commit()
                    csql.close()
                else:
                    sql = "INSERT INTO gkx (account_id, point,total_point) VALUES (%s, %s, %s)"
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
                checkpoit = requests.post(url, headers=header, cookies=self.cokkie)
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
                    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": selfurl, "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                    data={"server_id": self.server_psv}
                    requests.post(url, headers=header, cookies=self.cokkie, data=data)
                    return 0
                except:
                    self.cokkie = getcookie(self)

                    #import requests

                    #burp0_url = "https://playserver.in.th:443/index.php/MyServerCheckPoint/index/16448"
                    #burp0_cookies = {"ci_session": "6dslj6f5t002ss0p41q6sggca1hl2748", "__utma": "21391738.1036514921.1557339590.1557339590.1557339590.1", "__utmb": "21391738.6.10.1557339590", "__utmc": "21391738", "__utmz": "21391738.1557339590.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)", "__utmt": "1"}
                    #burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "th,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Referer": "https://playserver.in.th/index.php/MyServerStatus/index/16448", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                    #requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)




        def getcookie(self):
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            driver = webdriver.Chrome("drivers/chromedriver.exe",chrome_options=options)
            driver.get("https://playserver.in.th/index.php/Login")
            try:
                ib64 = driver.find_element_by_xpath("""//*[@id="loginform"]/div[3]/div[2]/img""").screenshot_as_base64
                print(" this pange use getcapcha ")
                while True:
                    captext = diffcap(self.key,ib64)
                    print(" succes --> capcha ;  "+captext["text"])
                    if captext["status"] == True:
                        driver.find_element_by_xpath("""//*[@id="code"]""").send_keys(captext["text"])
                        driver.find_element_by_xpath("""//*[@id="email"]""").clear()
                        driver.find_element_by_xpath("""//*[@id="password"]""").clear()
                        driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(self.user_psv)
                        driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(self.passwd_psv)
                        driver.find_element_by_xpath("""//*[@id="btnLogin"]""").click()
                        try:
                            driver.find_element_by_xpath("""/html/body/div[2]/div/div[1]/div/div[2]/div/div/ul[1]/li[1]/a""")
                            ncookie = {"ci_session": driver.get_cookie("ci_session")["value"], "__utma": driver.get_cookie("__utma")["value"], "__utmb": driver.get_cookie("__utmb")["value"], "__utmc": driver.get_cookie("__utmc")["value"], "__utmz": driver.get_cookie("__utmz")["value"], "__utmt": driver.get_cookie("__utmt")["value"]}
                            driver.close()
                            return ncookie
                        except:
                            ib64 = driver.find_element_by_xpath("""//*[@id="loginform"]/div[3]/div[2]/img""").screenshot_as_base64
                    elif captext["status"] == False:
                         reportIncorrectImageCaptcha(self.key,captext["taskId"])               
            except:
                try:
                    driver.find_element_by_xpath("""//*[@id="email"]""").clear()
                    driver.find_element_by_xpath("""//*[@id="password"]""").clear()
                    driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(self.user_psv)
                    driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(self.passwd_psv)
                    driver.find_element_by_xpath("""//*[@id="btnLogin"]""").click()
                    ncookie = {"ci_session": driver.get_cookie("ci_session")["value"], "__utma": driver.get_cookie("__utma")["value"], "__utmb": driver.get_cookie("__utmb")["value"], "__utmc": driver.get_cookie("__utmc")["value"], "__utmz": driver.get_cookie("__utmz")["value"], "__utmt": driver.get_cookie("__utmt")["value"]}
                    driver.close()
                    return ncookie
                except:
                    try:
                        ncookie = {"ci_session": driver.get_cookie("ci_session")["value"], "__utma": driver.get_cookie("__utma")["value"], "__utmb": driver.get_cookie("__utmb")["value"], "__utmc": driver.get_cookie("__utmc")["value"], "__utmz": driver.get_cookie("__utmz")["value"], "__utmt": driver.get_cookie("__utmt")["value"]}
                        driver.close()
                        return ncookie
                    except:
                        driver.close()
                        print("Unstable internet . . .")
                    


            return 0


        def connect_sql(self):
            mydb = mysql.connector.connect(
                host= self.host,
                user= self.sqluser,
                passwd=self.sqlpasswd,
                database= self.sqldatabase
            )
            return mydb
            
        def reportIncorrectImageCaptcha(key,taskid):
            header = { "Accept": "application/json","Content-Type": "application/json"}
            data = {
            "clientKey":key,
            "taskId": taskid
             }
            reprot = requests.post("https://api.anti-captcha.com/reportIncorrectImageCaptcha",timeout=500,headers=header,json=data).json()
            return reprot

        def diffcap(key,base64image):
            try:
                Taskdata = {
                    "clientKey":key,
                    "task":
                    {
                    "type":"ImageToTextTask",
                    "body":base64image,
                    "phrase":False,
                    "case":False,
                    "numeric":False,
                    "math":0,
                    "minLength":4,
                    "maxLength":4,
                    "comment":"This application has been report to anticapcha If your answer is wrong according to anticapcha policy from https://anti-captcha.com/clients/reports/refunds"
                    },
                    "softId":"904",
                    "languagePool":"en"
                    }
                createTask  = requests.post("https://api.anti-captcha.com/createTask",timeout=100,json=Taskdata).json()
                if createTask['errorId'] == 0:
                    TaskID = {
                           "clientKey":key,
                           "taskId": createTask['taskId']
                           }
                    for timeout in range(60):
                        captcha_id = requests.post("https://api.anti-captcha.com/getTaskResult",timeout=100, json = TaskID).json()
                        if captcha_id['status'] != 'processing':
                            captcha = {'status':True,'text':captcha_id['solution']['text'],'cost':captcha_id['cost'],'taskId':createTask['taskId']}
                            return captcha
                        else:
                            time.sleep(5)
                    else:
                        captcha = {'status':False,'errorDescription':createTask['errorDescription']}
                        return captcha
            except:
                return 0


        run(self)
