import time
import re
from selenium import webdriver


#Ottaa urlin ja luvun ja palauttaa listan listoja. Luku määrää amountko bussia listoihin tulee(luvut yli 20 eivät välttämättä toimi).
#Käyttää https://www.reittiopas.fi/pysakit/HSL:xxxxxxx tyyppisiä urleja.
#Returnin tiedot:
#   0 on bussien ajat
#   1 on bussien numerot
#   2 on bussien päämäärät
#   3 on 'timestamp' sekuntteina


if __name__ == "__main__":
    pass

else:
    def crawler(url, amount):

        #phantomjs hakee urlin ja säilöö sen html muuttujaan
        driver = webdriver.PhantomJS()
        driver.get(url)

        #lisää time.sleep() aikaa jos ei toimi
        time.sleep(7)
        html = driver.page_source
        driver.quit()

        #bus arrival time/time from arrival
        #jos aikaa on alle 10 min reittiopas antaa tiedon muodossa 'x min'
        #jos aikaa on alle 1 min reittiopas antaa tiedon muodossa 'Now'
        regexTime = '(Now|\d+ min|\d\d:\d\d)'
        regexFindTime = re.findall(regexTime, html)
        timeList = []

        #lisätään määrätty määrä uuteen listaan
        if len(regexFindTime) >= amount:

            for x in range(0, amount):
                timeList.append(regexFindTime[x])

        #bus number
        regexBus = 'bus\">(\d\d\d|\d\d\d[a-z])'
        regexFindBus = re.findall(regexBus, html)
        busList = []

        #lisätään määrätty määrä uuteen listaan
        if len(regexFindBus) >= amount:
            for x in range(0, amount):
                busList.append(regexFindBus[x])

        #destination
        regexDestination = "destination\">([^0-9<]+)<"
        regexFindDestination = re.findall(regexDestination, html)
        destinationList = []

        #lisätään määrätty määrä uuteen listaan
        if len(regexFindDestination) >= amount:
            for x in range(0, amount):
                destinationList.append(regexFindDestination[x])

        #int(time.time()) antaa ajan sekuntteina epoch:ista
        return [timeList, busList, destinationList, int(time.time())]


#muuttaa kaikki ajat samanlaisiksi, käyttää koneen omaa aikaa
#stop on crawler palauttama pysakki data
    def timeParser(stop):

        times = []

        for i in range(0, len(stop[0])):

            if stop[0][i] == 'Now':
                #lisätään 20 sekunttia sillä tiedämme vain että "Now" < 1 min
                times.append(time.time() + 20)

            elif stop[0][i].endswith('min'):
                minutes = int(stop[0][i][0])
                times.append(time.time() + (minutes * 60))

            else:
                hours = time.strftime("%H")
                minutes = time.strftime("%M")

                #haetaan tunnit ja verrataan tämänhetkiseen aikaan
                hourDelta =  int(stop[0][i][0] + stop[0][i][1]) - int(hours)
                minuteDelta =  int(stop[0][i][3] + stop[0][i][4]) - int(minutes)

                secondDelta = (hourDelta * 60 * 60) + (minuteDelta * 60)

                times.append(time.time() + secondDelta)

        return times
