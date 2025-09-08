class PDFdata:
    def __init__(self,MachineSerial, AirData, LightData, SoundData):
        self.__MachineSerial = MachineSerial
        self.__AirData = AirData
        self.__LightData = LightData
        self.__SoundData = SoundData


    def getSerial(self):
        return self.__MachineSerial

    def getAirData(self):
        return self.__AirData

    def getAirdataByIndex(self, index):
        return self.__AirData[index]

    def getLightData(self):
        return self.__LightData

    def getSoundData(self):
        return self.__SoundData

    def setSerial(self, MachineSerial):
        self.__MachineSerial = MachineSerial

    def  setAirData(self, AirData):
        self.__AirData = AirData

    def setLightData(self, LightData):
        self.__LightData = LightData

    def setSoundData(self, SoundData):
        self.__SoundData = SoundData

    def __str__(self):
        return "Serial" + str(self.__Serial) + " AirData: " + str(self.__AirData) + " LightData: " + str(self.__LightData) + " SoundData: " + str(self.__SoundData)