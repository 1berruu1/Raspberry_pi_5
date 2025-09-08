import time
import gpiozero
import serial
import reportlab
from Domain import PDFdata
from Exceptions import PDFException, SensorException
from Repo import Repository, RepositorySQL
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Spacer
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF
from gpiozero import Button

# button = Button(4)


def readLightSensor():
    pass

def readSoundSensor():
    pass

def cameraSerial():
    pass

#TODO calcul de conversie live pe ce returneaza voltaj si sa vad care este eroarea de conversie si sa le afisam separat
#TODO Docstrings pt functii




def voltToAirFlow(PDFdata):
    data = PDFdata.getAirData()
    voltage_error = 0.2

    step = 0.01

    def convert(x):
        if 0.76 <= x <= 1.24:
            return 0.0
        elif 1.70 < x < 2.18:
            return 2.0
        elif 2.99 < x < 3.47:
            return 4.0
        elif 4.01 < x < 4.49:
            return 6.0
        elif 4.49 < x < 4.90:
            return 8.0
        elif 4.90 < x < 5.24:
            return 10.0
        else:
            return None

    if data and isinstance(data[0], list):
        return [[convert(x) for x in sublist] for sublist in data]
    else:
        return [convert(x) for x in data]



#TODO Graficul sa fie facut co matplotlib sau pandas


def pdfGenfunction(PDFdata):
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
            raise PDFException("Error creating tables", 6)
        except PDFException as e:
            print(e)

        avg = sum(arr) / len(arr) if arr else 0
        table_data2 = [[f'Average {idx + 1}'], [avg]]
        table2 = Table(table_data2)
        elements.append(table2)
        elements.append(Spacer(1, 20))

    flat_data = []
    for arr in data_arrays:
        flat_data.extend(arr)

    try:
        drawing = Drawing(400, 200)
        drawing.add(String(200, 180, 'Air Flux Table', fontSize=14, textAnchor='middle'))
        lp = LinePlot()
        lp.x = 50
        lp.y = 50
        lp.height = 100
        lp.width = 300
        lp.data = [list(enumerate(flat_data))]
        lp.lines[0].strokeColor = colors.blue
        drawing.add(lp)
        elements.append(drawing)
        elements.append(Spacer(1, 40))
        raise PDFException("Error drawing tables", 360)
    except PDFException as e:
        print(e)

    try:
        doc = SimpleDocTemplate("Raport.pdf", pagesize=letter)
        doc.build(elements)
        raise PDFException ("Error building pdf", 302)
    except PDFException as e:
        print(e)

def readSerial(port, baudrate, timeout=2):
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
            if not lines:
                raise SensorException("error appending line", 456)
        return "\n".join(lines)
    except SensorException as e:
        print(e)

def pasreData(data):
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
                except ValueError:
                    pass
        sensor_readings.append(values)
    return sensor_readings


# the main function that will run all the logic


# def flagFunc():
#     Device = PDFdata
#     port = 'COM10'
#     baudrate = 9600
#     while True:
#         flag = 0
#         if flag == 0 & button.when_activated:
#             Scamera = cameraSerial()
#             Device.setSerial(Scamera)
#             flag = 1
#         if flag == 1 & button.when_activated:
#             readAirData = readSerial(port, baudrate)
#             pasreData(readAirData)
#
#             flag = 2
#         elif flag == 2 & button.when_deactivated:
#             # execute code light
#             readLightData = readLightSensor()
#             Device.setLightData(readLightData)
#             flag = 3
#         elif flag == 3 & button.when_activated:
#             # execute code sound
#             readSoundData = readSoundSensor()
#             Device.setSoundData(readSoundData)
#             flag = 4
#         elif flag == 4 & button.when_activated:
#             pdfGenfunction(Device)
#             exit()






