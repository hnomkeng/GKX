<p align="center">
  <img src="https://user-images.githubusercontent.com/47280575/56685374-04cf5880-66fc-11e9-88ff-0f9f7b6e5de8.png" alt="GKX : LOGO" width="226">
  <br>
  :octocat:(syntaxp) ติดต่อ #support ได้ที่   <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSakv86QJPY-E6rxMEo_WzAwYUzyndjdY_d-Zu2ZOr9UuMjClxy5A" alt="discord logo" width="25" height="25">  <a href="https://discord.gg/Mgu73TN">Discord</a>
</p>



<p align="center">GKX ช่วยคุณจัดการ Server ในส่วนของคะแนนโหวตที่มาจาก Playserver </p>

<p align="center"><img src="https://user-images.githubusercontent.com/47280575/56681389-7656d900-66f3-11e9-9522-596e6f377442.gif" alt="sample"></p>

<p align="center"><em>The example above was created with GKX. Check it out at <a href="https://www.youtube.com/watch?v=lrXmNNkPIMo">Playserver นับคะแนนเข้าเซิฟ Auto</a>.</em></p>

Features
------------

* **Get point, Add point** — With GKX, ดึง Point ของ User ที่ได้จากการโหวตจาก Playserver แล้วนำมา Update ใน Database ของ Server คุณอัตโนมัติ แบบ real time ระบบจะไม่นำเข้าคะแนนของ User ที่ไม่มีชื่อใน Database

* **PointX2** — มีระบบ คูณคะแนนที่ได้จากการโหวต อัตโนมัติ โดยสามารถเข้าไปตั่งได้ใน [config.txt](https://github.com/syntaxp/GKX/blob/master/control/config.txt) ในส่วนของหัวข้อ [votex2]  ตามวันที่ต้องการให้มีการคูณคะแนน


------------------------------

การเริ่มต้นกับ GKX นั้นง่ายมาก! เพียงแค่ทำตามคำแนะนำด้านล่าง

Getting Started with GKX
------------------------------

### ข้อกำหนดเบื้องต้น

ตรวจสอบคุณสมบัติของคุณ:

 - **Linux or Windows** — macOS  อาจใช้งานได้ แต่ไม่รองรับ 
 - **สำหรับ Linux หรือ VPS** — จะต้องมี `Python3.5+` และต้องติดตั่ง `package`ให้ครบ แนะนำติดต่อ :octocat: <a href="https://discord.gg/Mgu73TN">support</a>
  - **Server ต้องไม่มีการเชื่อมระบบกับ Duckdig**
  
### เริ่มต้น/การตั้งค่า
1. Fork หรือ <a href="https://github.com/syntaxp/GKX/archive/master.zip">Dowloads</a> this repository on GitHub.
2. แตกไฟล์ในส่วนของ GKX-master.zip ให้เรียบร้อยจากนั้นเข้าไปที่ `GKX-master\control` จะพบไฟล์ `config.txt` ให้เปิดขึ้นมา

2.1. ในส่วนนี้จะแบ่งการตั่งค่าออกเป็น สามส่วน default, mysql, votex2 การเซ็ต config เราจะเซ็ตหลังเครื่องหมาย เท่ากับ(=)

```python

[default]
user_psv = # email หรือ user ที่ใช้ในการสร้างกระทู้โหวตใน Playserver
passwd_psv =  # password ที่ใช้ในการสร้างกระทู้โหวตใน Playserver
server_psv =  # ไอดีของเซิฟเวอร์ตัวอย่างเช่น  url คือ " https://playserver.in.th/index.php/Server/Testver-16448 " ไอดีจะอยู่ข้างหลังซึ่งก็คือ 16448
delay = 0 #ดีเลการดึงข้อมูล

[mysql]
host = #host ของ server
user_sql = #user ที่ใช้ login 
passwd_sql = #password 
database_name = #name database ชื่อของ database

table_login = login  #ค่านี้มสามารถใช้ได้เลยหากเซิฟเวอร์ไม่ได้ปรับแต่ง database ของเกม
game_acc_fld = account_id
game_user_fld = userid


[votex2] #ตั่งค่าวันที่ต้องการให้มีการโหวต *
Monday = 1
Tuesday = 1
Wednesday = 2
Thursday = 1
Friday = 1
Saturday = 2
Sunday = 1
```

