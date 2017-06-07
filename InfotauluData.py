import time
from InfotauluCrawler import crawler, timeParser


#Hakee ja käsittelee InfotauluCrawler.py palauttamaa dataa.
#Hakee uudestaan kunnes saa kaksi ei-tyhjää listaa.


def getDataEspoo():
    return crawler("https://www.reittiopas.fi/pysakit/HSL:2432204", 11)


def getDataHelsinki():
    return crawler("https://www.reittiopas.fi/pysakit/HSL:2432205", 11)


def isEmpty(data):

    if data[0]:
        return False

    else:
        return True


def updateDataEspoo():

    espoo = []

    while True:
        espoo = getDataEspoo()

        if isEmpty(espoo):
            time.sleep(2)
            print('espoo returned empty')
            continue
        break

    espoo[0] = timeParser(espoo) # aika

    return espoo


def updateDataHelsinki():

    helsinki = []

    while True:
        helsinki = getDataHelsinki()

        if isEmpty(helsinki):
            time.sleep(2)
            print('helsinki returned empty')
            continue
        break

    helsinki[0] = timeParser(helsinki) # aika

    return helsinki


#poistaa aikaeron nykyhetkestä ja datanhakuhetkestä (ei välttämättä mitään hyötyä sillä ero on pieni)
def localSyncTime(data):

    timeDifference = time.time() - data[3]

    for x in range(0, len(data[0])):
        data[0][x] = data[0][x] - timeDifference

    return data
