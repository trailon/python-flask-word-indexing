
from flask import *
import requests
import operator
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'any random string'
kelimefrekanslari = []
kelimefrekanslari1 = []
kelimefrekanslarimain = []
tempkelimefrekanslari = []
kelimesayisi = {}
kelimesayisi1 = {}
kelimesayisimain = {}
tempkelimesayisi = {}


def sozluk(tumkelimeler,wordcount):
    for kelime in tumkelimeler:
        if kelime in wordcount:
            wordcount[kelime] += 1
        else:
            wordcount[kelime] = 1
    return wordcount
    
def sembolleritemizle(tumkelimeler):
    sembolsuzkelimeler = []
    semboller = "!@$#£^*()“_+\<>?,./;'[]-=" + chr(775)
    for kelime in tumkelimeler:
        for sembol in semboller:
            if sembol in kelime:
                kelime = kelime.replace(sembol,"")
        if(len(kelime) > 0 ):
            sembolsuzkelimeler.append(kelime)
    return sembolsuzkelimeler
    
def geturl(url,wordcount,wordfrequency,x,t):
    y=x
    z=t
    wordfrequency.clear()
    tumkelimeler = []
    tumkelimeler.clear()
    wordfrequency.clear()
    wordcount.clear()
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    frequencystring = ""
    keywordfreqstring = ""
        
    for kelimegruplari in soup.find_all("p"):
        icerik = kelimegruplari.text
        kelimeler = icerik.lower().split()
            
        for kelime in kelimeler:
            tumkelimeler.append(kelime)
                
    tumkelimeler = sembolleritemizle(tumkelimeler)
    wordcount = sozluk(tumkelimeler,wordcount)
        
    for anahtar,deger in sorted(wordcount.items(),key= operator.itemgetter(1),reverse=True):
        wordfrequency.append(anahtar+" = "+str(deger))
            
        
    if y==1:
        kelimefrekanslari=wordfrequency
    elif y==2:
        kelimefrekanslari1=wordfrequency
    elif y==3:
        kelimefrekanslarimain=wordfrequency
    elif y==4:
        tempkelimefrekanslari=wordfrequency
    
    for i in range (len(wordfrequency)):
        frequencystring = frequencystring+"\n"+wordfrequency[i]
    if z == 1:
        return frequencystring
    
    baglaclar ="için olduğunuz gibi tıklayın fakat ama belki çok biraz miktar küçük büyük değil iyi daha şey kaç kadar kötü meğer ile ya da yahut veyahut lakin ancak oysa halbuki ne var evet hayır bir bu iki üç olan öncesi sonrası nasıl kısmi olarak henüz her"
    tmp=0
    while tmp<5:
        if wordfrequency[tmp].split(" =")[0] in baglaclar:
            wordfrequency.pop(tmp)
        else:
            keywordfreqstring = keywordfreqstring+"\n"+wordfrequency[tmp]
            tmp=tmp+1
        if tmp==5:
            tmp=0
            break

    if z==2:
        return keywordfreqstring
    soup.reset()

def getscore(wordfreq,wordfreq1,x):
    def listToString(s): 
        str1 = "" 
        for ele in s: 
            str1 += ele  
        return str1 
    
    score = 1
    strvar = listToString(wordfreq)
    strvar1 = listToString(wordfreq1)
    sayilar ="0123456789"
    tempislem=""
    sonucstring=""
    adet = 0
    for i in range(5):
        if wordfreq[i].split(" =")[0]+" =" in strvar1:
            #sonucstring=sonucstring+"\n"+wordfreq[i].split(" =")[0]
            splittemp = wordfreq[i].split(" =")[0]+" ="
            tempskor=strvar1.split(splittemp)[1][1]
            adet += 1
            
            if strvar1.split(splittemp)[1][2] in sayilar:
                tempskor=tempskor+strvar1.split(splittemp)[1][2]
                
                if strvar1.split(splittemp)[1][3] in sayilar:
                    tempskor=tempskor+strvar1.split(splittemp)[1][3]
            tempislem=tempislem+tempskor+"*"
            score = score*int(tempskor)
    tempislem=tempislem+str(adet)+"*"
    score = score*adet
    tempislem = tempislem[:-1]
    tempislem = tempislem+"/"+str(len(wordfreq1)) 
    if len(wordfreq1)==0:
        score = score / 1
    else:
        score = score / len(wordfreq1)
    if x==2:
        score=score*7/10
    sonucstring=sonucstring+tempislem
    return sonucstring,score
    
a = ""
b = ""
c = ""
d = ""
e = ""           
suburlfreqstr = []
score = ""
    
@app.route("/", methods=['GET'])
def index():
    
    return render_template("home.html" )

@app.route('/firsturl', methods=['GET','POST'])
def firsturlfrequency():
    global a
    global b
    if request.method == "POST":
        url = request.form['url']
        freqstring = geturl(url,kelimesayisi,kelimefrekanslari,1,1)
        keywordfreq = geturl(url,kelimesayisi,kelimefrekanslari,1,2)
        a=freqstring
        b=keywordfreq
        return render_template("home.html",firsturlfrequencycontent=a,firsturlkeywordscontent=b )
    else:
        return render_template("home.html")

@app.route("/secondurl", methods=['GET','POST'])
def secondurlfrequency():
    global c
    global d
    if request.method == "POST":
        url = request.form['url']
        secondfreqstring = geturl(url,kelimesayisi1,kelimefrekanslari1,2,1)
        secondkeywordfreq = geturl(url,kelimesayisi1,kelimefrekanslari1,2,2)
        c = secondfreqstring
        d = secondkeywordfreq
        return render_template("home.html",firsturlfrequencycontent=a,firsturlkeywordscontent=b,secondurlfrequencycontent=c,secondurlkeywordscontent=d )
    else:
        return render_template("home.html")

@app.route("/score")
def score():
    global score
    score = getscore(kelimefrekanslari,kelimefrekanslari1,1)
    return render_template("home.html",firsturlfrequencycontent=a,firsturlkeywordscontent=b,secondurlfrequencycontent=c,secondurlkeywordscontent=d,score=score )

def suburls(url):
    links = []
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text,features="lxml")
    if "com" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".com"
    elif "org" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".org"
    elif "net" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".net"
    elif "edu" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".edu"
    elif "xyz" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".xyz"
    elif "biz" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".biz"
    elif "info" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".info"
    elif "html" in url:
        url = url.split(".")[0]+"."+url.split(".")[1]+".html"
    print(url)
    
    for link in soup.find_all('a'):
        if(link.get('href') != "#" and url in link.get('href')):
            links.append(link.get('href'))
    if url in links:
        links.remove(url)
    if url+"/" in links:
        links.remove(url+"/")
    for link in links:
        if link == url+"/":
            links.remove(link)
        if url not in links:
            links.remove(link)
        if link in links:
            links.remove(link)
    return links
allsuburls = []
@app.route("/suburlindexing", methods=['GET','POST'])
def suburlindexing():
    def listToString(s): 
        str1 = "" 
        for ele in s: 
            str1 += ele  
        return str1 
    if request.method == "POST":
        global suburlfreqstr
        sonuc = ""
        url = request.form['url']
        mainurlfreq = geturl(url,kelimesayisimain,kelimefrekanslarimain,3,1)
        mainurlkeyword = geturl(url,kelimesayisimain,kelimefrekanslarimain,3,2)
        global e
        e = mainurlkeyword
        global allsuburls
        allsuburls = suburls(url)
        a=0
        templist = []
        for suburl in allsuburls:
            tempkelimesayisi.clear()
            tempkelimefrekanslari.clear()
            suburlfreqstr = geturl(suburl,tempkelimesayisi,tempkelimefrekanslari,4,1)
            x,y=getscore(kelimefrekanslarimain,suburlfreqstr,2)
            sonuc = "||| " +suburl+" depth = 2 ,"+x+" |||"
            templist.append([sonuc]+[str(y)])
        sortkey = lambda skey:skey[1]
        templist.sort(key=sortkey,reverse=True)
        return render_template("suburlindex.html",mainurlkeyword = mainurlkeyword,subindexcont = templist )
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run()




    
    



