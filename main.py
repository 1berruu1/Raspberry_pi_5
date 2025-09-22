import itertools

import reportlab

from AuxFuncion import pdfGenfunction, readSerial, pasreData, voltToAirFlow, readSoundSensor
from Domain import PDFdata
from Repo import Repository, RepositorySQL


if __name__ == '__main__':
    testdata = PDFdata("SN1234567812",
                       [169.7, 269.8, 369.9, 470.0, 570.1, 670.2, 770.3, 870.4, 970.5, 1070.6, 1170.7, 1270.8,
                        1370.9, 1471.0, 1571.1, 1671.2, 1771.3, 1871.4, 1971.5, 2071.6, 2171.7, 2271.8, 2371.9, 2472.0, 2572.1,
                        2672.2, 2772.3, 2872.4, 2972.5, 3072.6, 3172.7, 3272.8, 3372.9, 3473.0, 3573.1, 3673.2, 3773.3, 3873.4,
                        3973.5, 4073.6, 4173.7, 4273.8, 4373.9, 4474.0, 4574.1, 4674.2, 4774.3, 4874.4, 4974.5, 5074.6, 5174.7, 5274.8,
                        5374.9, 5475.0, 5575.1, 5675.2, 5775.3, 5875.4, 5975.5],
                       379.5, 50.3)

    testdata2 = PDFdata("SN1234567810",
                       [[69.6, 169.7, 269.8, 369.9, 470.0, 570.1, 670.2, 770.3, 870.4, 970.5, 1070.6, 1170.7, 1270.8,
                        1370.9, 1471.0, 1571.1], [1671.2, 1771.3, 1871.4, 1971.5, 2071.6, 2171.7, 2271.8, 2371.9, 2472.0,
                        2572.1,2672.2, 2772.3, 2872.4, 2972.5, 3072.6, 3172.7, 3272.8, 3372.9, 3473.0, 3573.1, 3673.2, 3773.3,3873.4,
                        3973.5, 4073.6, 4173.7], [4273.8, 4373.9, 4474.0, 4574.1, 4674.2, 4774.3, 4874.4, 4974.5, 5074.6,5174.7, 5274.8,
                        5374.9, 5475.0, 5575.1, 5675.2, 5775.3, 5875.4, 5975.5]],
                       379.5, 50.3)


    testdata3 = PDFdata("SN1234567811",[0.78,4.80,4.02,0.90,1.11,1.15,1.26,1.18],13.0,50.0)

    testdata4 = PDFdata("SN1234567811", [[0.78, 4.80, 4.02],[ 0.90, 1.11]], 13.0, 50.0)

    repo = Repository()
    sqlrepo = RepositorySQL()



# TESTING SQL REPO

    # sqlrepo.saveData(testdata)
    # print(sqlrepo.returnAllData())
    # sqlrepo.deleteData("SN123456789")
    # sqlrepo.updateData("SN123456789",[100.0,200.0,300.0,400.0,500.0,600.0,700.0,800.0,900.0,1000.0,1100.0,1200.0,650.0],400.5,55.5)
    # print(sqlrepo.returnDataBySerial("SN123456789"))

# TESTING IN-MEMORY REPO and the Read/Parse functions

'''
In memory repo for reading Serial from a port
:param
    COM10 the serial port for the usb connected device
'''

    # readUSBData = readSerial('COM10', 9600)

    # PDF = PDFdata("SN1234567811",Airdata,379.5,45.6)
    # repo.saveData(PDF)
    # sqlrepo.saveData(PDF)
    # print(repo.get_data())





# TESTING PDF GENERATION
'''
pdfGenFunction takes the serial of an scanned machine and it will generate a PDF based
on that machines data.
'''

#     repo.saveData(testdata)
    # pdfGenfunction(repo.get_data_by_serial("SN1234567810"))
    # sqlrepo.saveData(PDF)
    # print("PDF generated!")

    # repo.saveData(testdata3)
    #
    # converted = voltToAirFlow(testdata3)
    # testdata3.setAirData(converted)
    # print(testdata3.getAirData())

# SOUND DATA FUNCTION
'''
readSoundSensor is used in order to gather data from files that are formated by the software 
for the Trotec SL400 audio software and it will read the file that is present in the same folder as the program

'''
#     repo.saveData(testdata)
#
#     new_sound_data = readSoundSensor("SoundReading.txt")
#     testdata.setSoundData(new_sound_data)
#     sqlrepo.saveData(testdata)
#   print(testdata.getSerial())
#   print(testdata.getSoundData())




# TESTING READING FROM BLUE TOOTH
'''
readBTData is the variable responsible for BT communication 
the arduino sends it's data and the parseData puts in two lists(idk why) so we use an intermediary list 
in order to get a full list of all the values

:param
    COM15 - is the port for the bluetooth module it can be different and it's certainly different for linux
    9600 - is the baudrate for the bluetooth module it's default and should not be changed
'''

# readBTData = readSerial('COM15', 9600)
#
#
# Airdata = pasreData(readBTData)
# FullList = list(itertools.chain(*Airdata))
# print(FullList)