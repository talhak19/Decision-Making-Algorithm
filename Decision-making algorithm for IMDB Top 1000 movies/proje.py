import pandas as pd
import numpy as np
from colorama import Fore,Back
from colorama import Style



df = pd.read_csv(
    
    'imdb_top_1000.csv'

)

df["Genre"] = df.Genre.apply(lambda x : x.lower())
def ture_gore_sirala():

    liste=[]
    kullanici_turler=[]
    list1 = df['Genre'].apply(lambda text: text.split(',')[0]).tolist()
    for i in list1:
        if i not in liste:
            liste.append(i)
    print("Film türleri bunlardır: ")
    print(liste)
    x = int(input("İçinden en fazla 3 tür seçimi yapabilirsiniz, kaç tür seçmek istiyorsunuz ?:"))
    if (x < 1 or x>3):
        while(x <1 or x > 3):
             x = int(input("Lütfen 1-3 arasi bir sayi giriniz:"))
    for i in range(0,x):
        genre =str(input("Tür giriniz:")).lower()
        if genre in liste: 
            kullanici_turler.append(genre)
        else:
            while(genre not in liste):    
                genre =str(input("Lutfen gecerli bir tur giriniz:")).lower()
            kullanici_turler.append(genre)
    _ture_gore_sirala(kullanici_turler)
    

def _ture_gore_sirala(liste):
          uzunluk = len(liste)
          index_no=[]
          for i in range(0,len(liste)):
              a = liste[i]
              turu_iceren_df = df.loc[df['Genre'].str.contains(a, case=False)]
              index_no.append(turu_iceren_df.index)
              print(a,"adli turun barindigi filmlerin puan ortalaması:",turu_iceren_df.IMDB_Rating.mean())
          for i,k in zip(index_no,liste):
              print(k,"adlı turun bulundugu filmler;\n")
              print(df.loc[i, 'Series_Title':'IMDB_Rating':])
          
          if uzunluk ==2:          #Öneri oluşturulması için burada datasetinde türler alfabetik sıralanıyordu
               if liste[0] < liste[1]:  #Ama kullanıcımız alfabetik olarak türleri girmemiş olabilir, burda alfabetik sıraya göre düzenliyoruz
                   tur_1 = liste[0]
                   tur_2 = liste[1]
               else:
                   tur_1 = liste[1]
                   tur_2 = liste[0]
               tur_tek_liste =[tur_1,tur_2]
               ture_gore_sirala_oneri(tur_tek_liste)
          elif uzunluk==3:
              if liste[0] < liste[1]:
                   tur_1 = liste[0]
                   tur_2 = liste[1]
                   if tur_2 < liste[2]:
                       tur_3 = liste[2]
                   else:
                       tur_2 = liste[2]
                       tur_3 = liste[1]
                       if tur_2 < tur_1:
                           tur_1 = liste[2]
                           tur_2 = liste[0]
              else:
                   tur_1 = liste[1]
                   tur_2 = liste[0]
                   tur_3 = liste[2]
                   if tur_2 < tur_3:
                       tur_3 = liste[2]
                   else:
                       tur_2 = liste[2]
                       tur_3 = liste[0]
                       if tur_2 < tur_1:
                           tur_1 = liste[2]
                           tur_2 = liste[1]
              tur_tek_liste =[tur_1,tur_2,tur_3]
              ture_gore_sirala_oneri(tur_tek_liste)
          
          
              
def ture_gore_sirala_oneri(tur_tek_liste):          #Buradaki öneri sistemi kullanıcının girdiği türlerin hepsini bir arada bulunduran filmlerin
    listToStr = ', '.join(map(str, tur_tek_liste))  #yönetmenlerini göstermek. Bu türlerin hepsini seven bir kullanıcı, o yönetmenin diğer filmlerini de
    print(listToStr)                                #sevebilir diye, yönetmene göre sıralama ekranına gidip gitmeyeceğini soruyoruz.
    turler = df["Genre"]
    yonetmenler=[]
    turu_iceren_df = df.loc[df["Genre"].str.contains(listToStr, case=False)]
    if not turu_iceren_df.empty:
        print(turu_iceren_df.loc[:,'Series_Title':'Genre':])
        yonetmenler.extend(turu_iceren_df["Director"].unique())
        print(listToStr,"turlerin barindigi filmlerin puan ortalaması:",turu_iceren_df.IMDB_Rating.mean())
    else:
        print("Girdiginiz turlerin hepsini barindiran bir film yok.\n")
    if yonetmenler:
        print("Bu turlerin bir arada bulundugu filmlerin yonetmen listesi asagidadir")
        print(yonetmenler)
        a = int(input("Buna göre yonetmen siralamasi yapmak ister misiniz ? (1:Evet) : "))
        if a == 1:
            yonetmene_gore_sirala()
    

def yonetmene_gore_sirala():
    list1 = df['Director'].apply(lambda text: text.split(',')[0]).tolist()
    liste=[]

    for i in list1:
        if i not in liste:
            liste.append(i)
    director = str(input("Yonetmen adi giriniz: "))
    if director in liste:
        yonetmen = df.loc[df['Director'] == director]
    else:
        while(director not in liste): 
            director = str(input("Gecerli bir yonetmen adi giriniz: ")) 
        yonetmen = df.loc[df['Director'] == director]
        
    print(yonetmen.loc[:,'Series_Title':'Director':])
    print(director,"adli yonetmenin IMDB ilk 1000 listesindeki filmlerinin puan ortalaması:",yonetmen.IMDB_Rating.mean())
    rat = yonetmen.IMDB_Rating.mean()
    yonetmene_gore_sirala_oneri(yonetmen,rat)
    
def yonetmene_gore_sirala_oneri(yonetmen,rating):
    print("Bunlari da sevebilirsiniz : \n")
    index_no = []                       ##Buradaki öneri sisteminde de bu yönetmeni seven bir insan, yönetmenin çektiği türdeki filmleri de sevebilir diye düşündüm
    for i in(df.index):                 ##O yüzden aynı türlerdeki fakat o yönetmene ait olmayan eşleşen filmlerin 10 tane(eğer varsa) (Rating sırası ile) bastırılmasını düşündüm
        for k in(yonetmen.index):       
            if (df.loc[i,"Genre"] == yonetmen.loc[k,"Genre"] )  & (df.loc[i,"Director"] != yonetmen.loc[k,"Director"]):
                if i not in index_no:
                    index_no.append(i)
    l = 0
    for c in index_no:
        if l == 10:
            break
        print(df.loc[c,"Series_Title":"Director":],"\n")
        l = l+1
            
def vizyon_yilina_göre_sirala():
    ##Burada bir öneri sistemi tasarlamadım, sadece insanlar belirli yillar arasındaki filmleri de
    ##görmek isterse diye bir fonksiyon yazdim.
    print("Hangi tarihler arasindaki filmleri siralamak istersiniz, lütfen giris yapiniz.")
    iy_year = str(input("Baslangic yilini giriniz: "))
    while(iy_year < "1920"):
        iy_year =str(input("En düsük baslangic yili 1920'dir. Lutfen tekrar giris yapiniz:  "))
    ms_year =  str(input("Bitis yilini giriniz: "))
    if ms_year < iy_year:
        while (ms_year < iy_year):
            ms_year = str(input("Bitis yili baslangic yilindan buyuk ya da esit olmalidir.Tekrar giris yapiniz: "))
    
    yillar = df.loc[(df['Released_Year'] >= iy_year) & (df['Released_Year'] <= ms_year)]
    print(yillar.loc[:,'Series_Title':'Released_Year':])

def oyuncuya_gore_sirala():
    index_no=[]
    sayac = 0
    rol=[]
    roles = ['Star1', 'Star2', 'Star3', 'Star4']
    oyuncu=str(input("Filmlerini gormek istediginiz oyuncuyu giriniz(tam adi dogru bir sekilde): "))
    for i in roles:

        oyuncu_olan_df = df.loc[df[i]==oyuncu]
        if not oyuncu_olan_df.empty:
            index_no.append(oyuncu_olan_df.index)
            rol.append(i)
        else:
            print("Bu oyuncu ",i,"olarak yer almamistir.")
            sayac = sayac +1 
    if sayac != 4:
        print(oyuncu,"\nBu filmlerde oynamistir: ")
    for i,k in zip(index_no,rol):
              print(df.loc[i, 'Series_Title':'IMDB_Rating':],"rolu:",k)
              print("")
    if sayac == 4:
        print("Oyuncunun IMDB siralamasinda filmi yoktur.")
    else:    
        
        oyuncuya_gore_sirala_oneri(oyuncu, index_no)
    
    
##Bu oyuncuya gore sıralama, öneri fonksiyonlarının en zorlu kısmıydı benim için.
#Buradaki mantık ise şu ; girdiğimiz oyuncunun filmlerini almadan(tekrar aynı filmi önermemek için),
##Aldığımız index_no parametresi(oyuncunun oynadıgı filmler) ile bir for döngüsünde dönüp
##O filmlerde rol alan diğer oyuncuları bir listeye ekliyoruz.
## Ana mantık o oyuncuyu izlemeyi seven kullanıcının, onla beraber rol alan oyuncuların filmlerini de
##İzlemeyi sevebileceğini düşünmek.
def oyuncuya_gore_sirala_oneri(oyuncu,index_no):
    oyuncu_listesi=[]
    roles = ['Star1', 'Star2', 'Star3', 'Star4']
    dftemp = df.loc[(df["Star1"] != oyuncu) & (df["Star2"] != oyuncu) & (df["Star3"] != oyuncu) & (df["Star4"] != oyuncu)]
    indeks = []
    for i in index_no:
        for k in roles:
            oyuncu_listesi.extend((df.loc[i,k].unique()))
    if oyuncu in oyuncu_listesi:
        oyuncu_listesi.remove(oyuncu)
    for i in oyuncu_listesi:
        for k in roles:
            if not dftemp.loc[dftemp[k] == i].empty:
                eslesen_oyuncu_indexleri = dftemp.loc[dftemp[k] == i].index.values.tolist() 
                for c in eslesen_oyuncu_indexleri:
                    if c not in indeks:
                        indeks.append(c)
    print("Bu oyuncuyu izlemeyi seven kullanıcılar, bunlari da sevebilir ; \n")
    locker = 0
    for i in indeks:
        if locker == 10:
            break
        print(dftemp.loc[i, 'Series_Title':'IMDB_Rating':] ,"\n")
        locker = locker +1
def main():

    print(f'{Fore.YELLOW}{Style.BRIGHT}IMDB ilk 1000 {Style.RESET_ALL}film analizi uygulamasina hos geldiniz!{Style.RESET_ALL}\n')
    secim = 0
    while (secim != 5):
        print(f'{Fore.RED}{Style.DIM}1- {Fore.RED}{Style.BRIGHT}Ture gore sırala')
        print(f'{Fore.RED}{Style.DIM}2- {Fore.RED}{Style.BRIGHT}Oyuncuya gore sırala')
        print(f'{Fore.RED}{Style.DIM}3- {Fore.RED}{Style.BRIGHT}Yonetmene gore sırala')
        print(f'{Fore.RED}{Style.DIM}4- {Fore.RED}{Style.BRIGHT}Vizyon yilina gore sırala')
        print(f'{Fore.RED}{Style.DIM}5- {Fore.RED}{Style.BRIGHT}Cikis{Style.RESET_ALL}\n')
        print(f'{Fore.CYAN}{Style.BRIGHT}{Back.BLACK}{Style.DIM}Lutfen yapmak istediginiz siralama turunu seciniz {Style.RESET_ALL}\n')
        secim = int(input("Seciminiz : "))
        # pd.set_option("display.max_columns", None)
        # pd.set_option("display.max_rows", None) ##Tüm satır ve sütunları görmeye ayarlamak için
        if secim == 1:
            ture_gore_sirala()
        elif secim == 2:
            oyuncuya_gore_sirala()
        elif secim == 3:
            yonetmene_gore_sirala()
        elif secim == 4:
            vizyon_yilina_göre_sirala()
        elif secim == 5:
            print("İyi gunler dileriz")
            secim = 5
        else:
              secim = int(input("Lutfen gecerli bir giris yapiniz : "))

main()