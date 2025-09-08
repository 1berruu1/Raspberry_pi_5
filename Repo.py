import sqlite3

class Repository:
    def __init__(self):
        self.__data = {}

    def saveData(self, PDFdata):
            self.__data[PDFdata.getSerial()] = PDFdata

    def get_data(self):
        return list(self.__data.values())

    def get_data_by_serial(self, Serial):
        return self.__data.get(Serial, None)


    def deleteData(self,Serial):
        del self.__data[Serial]


    def updateData(self, PDFdata):
        self.__data[PDFdata.getSerial()] = PDFdata



class RepositorySQL:
    def __init__(self):
        self.__conn = sqlite3.connect('OmegaUseful.db')
        self.create_table()

    def create_table(self):
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS PDFdata (MachineSerial TEXT PRIMARY KEY, AirData TEXT, LightData REAL, SoundData REAL)")
        self.__conn.commit()


    def saveData(self, PDFdata):
        machineSerial = PDFdata.getSerial()
        airData = ",".join(map(str, PDFdata.getAirData()))
        lightData = PDFdata.getLightData()
        soundData = PDFdata.getSoundData()
        self.__cursor.execute("INSERT INTO PDFData (MachineSerial, AirData, LightData, SoundData) "
                              "VALUES (?, ?, ?, ?)",
                              (machineSerial, airData, lightData, soundData))
        self.__conn.commit()

    def returnAllData(self):
        result = self.__cursor.execute("SELECT * FROM PDFdata")
        return result.fetchall()

    def returnDataBySerial(self, machineSerial):
        result = self.__cursor.execute("SELECT * FROM PDFdata WHERE MachineSerial = ?", (machineSerial,))
        return result.fetchone()

    def deleteData(self, machineSerial):
        self.__cursor.execute("DELETE FROM PDFdata WHERE MachineSerial = ?", (machineSerial,))
        self.__conn.commit()

    def updateData(self, machineSerial, airData, lightData, soundData):
        self.__cursor.execute("UPDATE PDFdata SET AirData = ?, LightData = ?, SoundData = ? WHERE MachineSerial = ?",
                              (",".join(map(str, airData)), lightData, soundData, machineSerial))
        self.__conn.commit()