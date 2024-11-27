from fastapi import FastAPI
from models import Item, SensorInput
from scipy.fft import fft, fftfreq
import numpy as np

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "description": item.description}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/fft")
def fftAsAService(signal:SensorInput):
    fs = 22  # frecuencia de muestreo
    accSignalX = [reading.x for reading in signal.accelerometer]
    accSignalX = np.array(accSignalX)-np.mean(accSignalX)
    spectrum = fft(accSignalX)
    freqs = fftfreq(len(accSignalX), 1/fs)
    half_spectrum = np.abs(spectrum[:len(spectrum) // 2])
    return {"frequency":freqs.tolist(), "spectrum":half_spectrum.tolist()}