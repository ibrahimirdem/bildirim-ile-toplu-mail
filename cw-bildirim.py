# -*- coding: cp1254 -*-
import mechanize
import smtplib
import re
import time

#Yeni bir yaznini paylasilip paylasilmadigini bu fonksiyon ile anlıyoruz.
def konu_kontrol():
   br = mechanize.Browser()

   br.set_handle_robots(False)
   br.addheaders = [("User-agent","Chrome")]

   kaynak = br.open("http://www.cyber-warrior.org/Forum/python-124,0.cwx").read()
   basliklar = re.findall('''<a href="(.*?)cwx" target="_self">(.*?)</a>''',kaynak)
   for i in range(5):
      del basliklar[0]

   return basliklar[0]

#Gonderilecek Mailler mail_listesi.txt icindeki kayitli maillerden cekiliyor.
alicim = open("mail_listesi.txt","r")
alici_liste = alicim.readlines()

#Buradan mail gonderme islemleri yapiliyor.
def mail_gonder(baslik,mesaj):
   gonderici_mail = "irdem007@gmail.com"
   gonderici_sifre = "Buraya mail sifreniz"
   mesaj = """From: Python Yeni Yazi
Subject: Cyber-Warrior Yeni Python Yazisi :)

Yazi basligi : %s
Link : http://www.cyber-warrior.org/Forum/%scwx

"""%(baslik,mesaj)

   server = smtplib.SMTP("smtp.gmail.com", 587)
   server.ehlo()
   server.starttls()
   server.ehlo()
   server.login(gonderici_mail,gonderici_sifre)

   try:
      server.sendmail(gonderici_mail, alici_liste, mesaj)
      print "[+] Basariyla kisilere bilgi maili gonderildi."
   except:
      print "[-] Bir sikinti olustu."

#İşlemlerin yapıldığı alan burası
#Sonsuz bir döngü kuruluyor.
while True:
   #konu_kontrol ile alinan bilgiler yeni_konu degiskenine aktariliyor.
   yeni_konu = konu_kontrol()
   #en son paylasilan yazinin bilgileri cekiliyor.
   dosya = open("baslik.txt","r")
   cekilen_veri = dosya.readlines()
   dosya.close()

   #en son paylasilan  yazi ile simdiki aynıysa pass ile geciyoruz.
   #yeni bir yazi paylasilincaya kadar bakiyor.
   if str(cekilen_veri[0])  == str(yeni_konu[0]):
      pass
   #Eger yeni baslasilan baslik ile kayitli baslik ayni degilse
   #yani yeni bir konu acildiysa islemler burada yapiliyor.
   else:
      #baslik ve link cekiliyor
      baslikk = yeni_konu[1]
      linkk = yeni_konu[0]
      print "[+] Yeni paylasilan bir yazi bulundu."
      print "[+] Yeni paylasilan yazi: %s"%str(baslikk)
      mail_gonder(baslikk,linkk)
      dosya = open("baslik.txt","w")
      dosya.write(mesajj)

   dosya.close()
   #10 sn sonra islemler yeniden tekrarlaniyor.
   time.sleep(10)
   
