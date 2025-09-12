import sqlite3
import pathlib

class Repository:
    """
    In-memory repository for storing PDFdata objects, indexed by their serial number.
    """
    def __init__(self):
        """
        Initializes the repository with an empty data dictionary.
        """
        self.__data = {}

    def saveData(self, PDFdata):
        """
        Saves a PDFdata object to the repository.
        Args:
            PDFdata: The PDFdata object to store.
        """
        self.__data[PDFdata.getSerial()] = PDFdata

    def get_data(self):
        """
        Returns all stored PDFdata objects as a list.
        Returns:
            List of PDFdata objects.
        """
        return list(self.__data.values())

    def get_data_by_serial(self, Serial):
        """
        Retrieves a PDFdata object by its serial number.
        Args:
            Serial: The serial number to look up.
        Returns:
            The PDFdata object if found, else None.
        """
        return self.__data.get(Serial, None)

    def deleteData(self, Serial):
        """
        Deletes a PDFdata object from the repository by serial number.
        Args:
            Serial: The serial number of the object to delete.
        """
        del self.__data[Serial]

    def updateData(self, PDFdata):
        """
        Updates an existing PDFdata object in the repository.
        Args:
            PDFdata: The updated PDFdata object.
        """
        self.__data[PDFdata.getSerial()] = PDFdata



class RepositorySQL:
    """
    SQLite-based repository for persistent storage of PDFdata records.
    """
    def __init__(self):
        """
        Initializes the database connection and ensures the table exists.
        """
        self.__conn = sqlite3.connect('OmegaUseful.db')
        self.create_table()

    def create_table(self):
        """
        Creates the PDFdata table in the database if it does not exist.
        """
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS PDFdata (MachineSerial TEXT PRIMARY KEY, AirData TEXT, LightData REAL, SoundData REAL)"
        )
        self.__conn.commit()

    def saveData(self, PDFdata):
        """
        Inserts a new PDFdata record into the database.
        Args:
            PDFdata: The PDFdata object to store.
        """
        machineSerial = PDFdata.getSerial()
        airData = ",".join(map(str, PDFdata.getAirData()))
        lightData = PDFdata.getLightData()
        soundData = ",".join(map(str, PDFdata.getSoundData()))
        self.__cursor.execute(
            "INSERT INTO PDFData (MachineSerial, AirData, LightData, SoundData) VALUES (?, ?, ?, ?)",
            (machineSerial, airData, lightData, soundData)
        )
        self.__conn.commit()

    def returnAllData(self):
        """
        Retrieves all PDFdata records from the database.
        Returns:
            List of tuples representing all records.
        """
        result = self.__cursor.execute("SELECT * FROM PDFdata")
        return result.fetchall()

    def returnDataBySerial(self, machineSerial):
        """
        Retrieves a PDFdata record by its serial number.
        Args:
            machineSerial: The serial number to look up.
        Returns:
            Tuple representing the record, or None if not found.
        """
        result = self.__cursor.execute("SELECT * FROM PDFdata WHERE MachineSerial = ?", (machineSerial,))
        return result.fetchone()

    def deleteData(self, machineSerial):
        """
        Deletes a PDFdata record from the database by serial number.
        Args:
            machineSerial: The serial number of the record to delete.
        """
        self.__cursor.execute("DELETE FROM PDFdata WHERE MachineSerial = ?", (machineSerial,))
        self.__conn.commit()

    def updateData(self, machineSerial, airData, lightData, soundData):
        """
        Updates an existing PDFdata record in the database.
        Args:
            machineSerial: The serial number of the record to update.
            airData: The new air data (list of values).
            lightData: The new light data value.
            soundData: The new sound data value.
        """
        self.__cursor.execute(
            "UPDATE PDFdata SET AirData = ?, LightData = ?, SoundData = ? WHERE MachineSerial = ?",
            (",".join(map(str, airData)), lightData, soundData, machineSerial)
        )
        self.__conn.commit()
