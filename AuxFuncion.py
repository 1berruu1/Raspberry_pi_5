import time
import serial
from picamera2 import Picamera2 #note only works on linux
from Exceptions import PDFException, SensorException
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Image
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os, os.path
import logging
import cv2

# Log file config used in every function

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)-s - %(funcName)s - %(message)s ",
    filename="log.txt",
    level=logging.ERROR,
    filemode="a",
    datefmt="%d/%m/%Y %H:%M:%S"
)


# button = Button(4)


def readLightSensor():
    """
    Reads data from the light sensor.
    Returns:
        The sensor reading (to be implemented).
    """
    pass

def readSoundSensor(file):
    """
      Reads the third column of a CSV file (skipping the header) and returns its values as a list.

      Args:
          file: Path to the CSV file containing sound sensor data.

      Returns:
          List of values from the third column of the CSV file.
      """
    try:
        values = pd.read_csv(file,skiprows=1, usecols=[2])
        value_column_3 = values.iloc[:, 0].tolist()
        return value_column_3
    except FileNotFoundError as e:
        logging.error(e)
        raise SensorException("File does not exist",234)





def cameraSerial():
    """
    Captures video from the default camera, detects and decodes QR codes in real time, and returns the decoded data.

    The function opens the default camera, processes each video frame to detect and decode QR codes using OpenCV,
    and displays the video feed with visual feedback. If a QR code is detected and decoded, the data is printed
    to the console and returned. The function exits when a QR code is found or when the 'q' key is pressed.

    Returns:
        str: The decoded QR code data if found, otherwise None.
    """


    picam2 = Picamera2()
    picam2.start()
    detector = cv2.QRCodeDetector

    while True:
        img = picam2.capture_array()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        data, bounding_box = detector.detectAndDecode(img)


        if bounding_box is not None:
            bounding_box = bounding_box.astype(int)
            n = len(bounding_box)
            for i in range(n):
                pt1 =tuple(bounding_box[i][0])
                pt2 =tuple(bounding_box[i][1])
                cv2.line(img,pt1,pt2,color=(255,0,0),thickness=2)
                if data:
                    print("data found", data)
                    return data

        cv2.imshow("camera", img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cv2.destroyAllWindows()


def voltToAirFlow(PDFdata):
    """
    Converts voltage readings to air flow values.
    Args:
        PDFdata: An object containing air data readings.
    Returns:
        List of converted air flow values.
    Raises:
        SensorException: If a voltage reading is out of range.
    """
    data = PDFdata.getAirData()
    results = []

    for i in data:
        try:
            if 1.0 < i < 5.0:
                results.append(round((i - 1 ) * 2, 2))
            else:
                logging.error("Voltage reading is out of range")
                raise SensorException("Out of range", 8)
        except SensorException as e:
            logging.error(e)
    return results

def pdfGenfunction(PDFdata):
    """
    Generates a PDF report with air data tables and a matplotlib line plot.
    Args:
        PDFdata: An object containing air data readings.
    Raises:
        PDFException: If there is an error creating or building the PDF.
    """
    raport = PDFdata
    data_arrays = raport.getAirData()
    elements = []

    if data_arrays and isinstance(data_arrays[0], float):
        data_arrays = [data_arrays]

    for idx, arr in enumerate(data_arrays):
        try:
            table_data = [[f"Reading {idx + 1}"]]
            num_columns = 5
            for i in range(0, len(arr), num_columns):
                row = arr[i:i + num_columns]
                if len(row) < num_columns:
                    row += [""] * (num_columns - len(row))
                table_data.append(row)
            table = Table(table_data)
            elements.append(table)
            elements.append(Spacer(1, 20))
        except PDFException as e:
            logging.error(e)
            raise PDFException("Error creating tables", 6)

        avg = sum(arr) / len(arr) if arr else 0
        table_data2 = [[f'Average {idx + 1}'], [avg]]
        table2 = Table(table_data2)
        elements.append(table2)
        elements.append(Spacer(1, 20))

    flat_data = []
    for arr in data_arrays:
        flat_data.extend(arr)

    try:
        df = pd.DataFrame({'Reading': range(1, len(flat_data) + 1), 'Value': flat_data})
        plt.figure(figsize=(6, 3))
        plt.plot(df['Reading'], df['Value'], marker='o', color='blue')
        plt.title('Air Flux Table')
        plt.xlabel('Reading')
        plt.ylabel('Value')
        plt.grid(True)
        plt.tight_layout()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.savefig(tmpfile.name)
            plt.close()
            img = Image(tmpfile.name, width=400, height=200)
            elements.append(img)
            elements.append(Spacer(1, 40))
    except Exception as e:
        logging.error(e)
        raise PDFException("Error drawing matplotlib plot", 360)

    try:
        doc = SimpleDocTemplate("Raport.pdf", pagesize=letter)
        doc.build(elements)
        os.unlink(tmpfile.name)
    except PDFException as e:
        logging.error(e)
        raise PDFException("Error building pdf", 302)

def readSerial(port, baudrate, timeout=2):
    """
    Reads lines from a serial port until a timeout occurs. Can be used for bluetooth communication
    Args:
        port: Serial port name (e.g., 'COM10').
        baudrate: Baud rate for serial communication.
        timeout: Time in seconds to wait after last line before stopping.
    Returns:
        String containing all lines read from the serial port.
    Raises:
        SensorException: If no lines are read.
    """
    ser = serial.Serial(port, baudrate, timeout=0.1)
    lines = []
    timer = None
    try:
        while True:
            line = ser.readline().decode().rstrip()
            if line:
                lines.append(line)
                timer = time.time()
            elif timer and time.time() - timer > timeout:
                break

        return "\n".join(lines)
    except SensorException as e:
        logging.error(e)


def pasreData(data):
    """
    Parses sensor data from a string into a list of float values.
    Args:
        data: String containing sensor readings, separated by commas and newlines.
    Returns:
        List of lists, where each sublist contains float values from one line.
    """
    sensor_readings = []
    lines = data.strip().split("\n")
    for line in lines:
        parts = line.split(",")
        values = []
        for part in parts:
            part = part.strip()
            if part != '':
                try:
                    values.append(float(part))
                except ValueError as e:
                    logging.error(e)
        sensor_readings.append(values)
    return sensor_readings

