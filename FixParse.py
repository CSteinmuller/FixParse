import datetime
import calendar

class Security:
    def __init__ (self, secType, secName, mature, productComplex, legs, assetTag):
        self.type = secType
        self.name = secName
        self.hasLegs = legs
        self.complex = productComplex
        self.asset = assetTag

        #Edge case that popped up
        if "" in mature:
            mature = mature[:mature.find("")]

        if (len(mature) == 6):
            self.maturity = datetime.date(int(mature[0:4]), int(mature[4:]), 1)
        if (len(mature) == 8):
            if not ("w" in mature):
                self.maturity = datetime.date(int(mature[0:4]), int(mature[4:6]), int(mature[6:]))
            else:
                week = int(mature[7:])

                if (week == 1):
                    self.maturity = datetime.date(int(mature[0:4]), int(mature[4:6]), 1)
                else:
                    findday = calendar.Calendar(0)

                    weekOffset = 0
                    for j in findday.itermonthdays(int(mature[0:4]), int(mature[4:6])):
                        if (j == 0):
                            weekOffset += 1

                    weekOffset = ((week - 1) * 7)

                    self.maturity = datetime.date(int(mature[0:4]), int(mature[4:6]), weekOffset)
            #self.hasLegs = legs

futures = []
option = []
uds = []
irs = []
complexes = ["2", "4", "5", "12", "14","15", "16", "17"]
complexShadow = [0,0,0,0,0,0,0,0]
fastest = []

#Read file
with open('secdef.dat') as dataFile:
    data = dataFile.readlines()

#Itererate and read in tag data
for x in range(len(data)):
    securityType = data[x][data[x].find("167=")+4:data[x].find("461=")-1]
    securityName = data[x][data[x].find("55=")+3:data[x].find("48=")-1]
    mature = data[x][data[x].find("200=")+4:data[x].find("15=")-1]

    if not (data[x].find("462=") == -1):
        complex = data[x][data[x].find("462=")+4:data[x].find("207=")-1]
    else:
        complex = ""

    leg = "555=" in data[x]
    assetTag = data[x][data[x].find("6937=")+5:data[x].find("55=")-1]

    current = Security(securityType, securityName, mature, complex, leg, assetTag)

    if (securityType == "FUT"):
        futures.append(current)

        if (complex in complexes):
            complexShadow[complexes.index(complex)] += 1
    elif (securityType == "OOF"):
        option.append(current)
    elif (securityType == "MLEG"):
        uds.append(current)
    elif (securityType == "IRS"):
        irs.append(current)

for j in range(len(futures)):
    if (futures[j].hasLegs == False) and (futures[j].asset == "GE"):
        fastest.append(futures[j])
final = sorted(fastest, key=lambda security : security.maturity)

#Part 1
print("The number of securities that are futures is: %s" %len(futures))
print("The number of securities that are options on future is: %s" %len(option))
print("The number of securities that are spreads with mixed type legs is: %s" %len(uds))
print("The number of securities that are interest rate swaps is: %s" %len(irs))

#Part 2
print("The number of agriculture/commidity futures is: %s" %complexShadow[0])
print("The number of currency futures is: %s" %complexShadow[1])
print("The number of equity futures is: %s" %complexShadow[2])
print("The number of futures classified as other is: %s" %complexShadow[3])
print("The number of intrest rate futures is: %s" %complexShadow[4])
print("The number of FX cash futures is: %s" %complexShadow[5])
print("The number of energy futures is: %s" %complexShadow[6])
print("The number of metal futures is %s" %complexShadow[7])

#Part 3
print("The names of the 4 earleist expiring futures with asset GE and no legs are:")
for k in range (0, 4):
    print (final[k].name)
