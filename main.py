from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Item, SensorInput
from scipy.fft import fft, fftfreq
from scipy.stats import pearsonr
import numpy as np
import pywt

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173, http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def center_signal(signal):
    """Centra la señal restando la media"""
    return np.array(signal)-np.mean(signal)

def normalize_signal(signal):
    """Nomaliza la media a 0 y la desviación estandar a 1"""
    return (np.array(signal)-np.mean(signal))/np.std(signal)

def get_amplitude_metrics(signal):
    """Extrae las métricas de amplitud de la señal"""
    return {
        "mean_amplitude": float(np.mean(signal)), 
        "std_amplitude": float(np.std(signal)), 
        "peak_amplitude": float(np.max(signal)), 
        "min_amplitude": float(np.min(signal)),
        "range_amplitude": float(np.max(signal)-np.min(signal))
    }
    
def unbiased_correlation(signal1, signal2):
    """Calcula la correlación de Pearson sin sesgo"""
    # Centramos las señales pero mantenemos su escala
    signal1_centered = center_signal(signal1)
    signal2_centered = center_signal(signal2)
    
    correlation, p_value = pearsonr(signal1_centered, signal2_centered)
    
    return {
        "correlation": correlation,
        "p_value": p_value,
        "significance": "significant" if p_value < 0.05 else "not significant"
    }

def sample_entropy(signal, m=2, r=0.2):
    """Calcula Sample Entropy con señal normalizada pero guarda métricas originales"""
    original_metrics = get_amplitude_metrics(signal)
    normalized_signal = normalize_signal(signal)
    
    N = len(normalized_signal)
    r = r*np.std(signal)
    
    template_matches = lambda x, m: sum(
        np.all(np.abs(normalized_signal[i:i+m]-x)<r) for i in range(N-m)
    )
    
    B = sum(template_matches(normalized_signal[i:i+m], m) for i in range(N-m))
    A = sum(template_matches(normalized_signal[i:i+m+1], m+1) for i in range(N-m))
    
    entropy = -np.log(A/B) if A > 0 and B > 0 else 0
    
    return {
        "entropy":entropy,
        "amplitude_metrics":original_metrics
    }

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

@app.post("/analyze_signal")
def analyze_signal(signal: SensorInput):
    fs = 22 # frecuencia de muestreo
    
    # Extraer señales originales de los tres ejes
    acc_x = np.array([reading.x for reading in signal.accelerometer])
    acc_y = np.array([reading.y for reading in signal.accelerometer])
    acc_z = np.array([reading.z for reading in signal.accelerometer])
    
    original_metrics = get_amplitude_metrics(acc_x)
    
    # Correlaciones entre ejes
    correlations = {
        "x_y": unbiased_correlation(acc_x, acc_y),
        "x_z": unbiased_correlation(acc_x, acc_z),
        "y_z": unbiased_correlation(acc_y, acc_z)
    }
    
    # FFT con señal solo centrada
    acc_x_centered = center_signal(acc_x)
    spectrum = fft(acc_x_centered)
    freqs = fftfreq(len(acc_x_centered), 1/fs)
    half_spectrum = np.abs(spectrum[:len(spectrum) // 2])
    
    # Wavelet preservando amplitud
    scales = np.arange(1, 32)
    wavelet = 'morl'
    coefficients, frequencies = pywt.cwt(acc_x_centered, scales, wavelet)
    
    # Entropia
    entropy_results = sample_entropy(acc_x)
    
    # Analisis de movimiento
    movement_analysis = {
        "movement_intensity": original_metrics["mean_amplitude"],
        "movement_variability": original_metrics["std_amplitude"],
        "peak_movement": original_metrics["peak_amplitude"],
        "axis_symetry": correlations["x_y"]["correlation"]
    }
    
    # Calcular caracteristicas del temblor
    tremor_frequencies = freqs[np.argmax(half_spectrum) + 1]
    tremor_amplitude = np.max(half_spectrum[1:])
    
    return {
        "original_metrics": {
            "min amplitude": original_metrics["min_amplitude"],
            "range amplitude": original_metrics["range_amplitude"],
        },
        "correlations": correlations,
        "fft": {
            "frequency":freqs.tolist(), "spectrum":half_spectrum.tolist(),
            "dominat_frequency":tremor_frequencies,
            "tremor_amplitude":tremor_amplitude
        },
        "wavelet": {
            "coefficients": coefficients.tolist(),
            "frequencies": frequencies.tolist(),
            "scales": scales.tolist()
        },
        "entropy": entropy_results,
        "movement_analysis": movement_analysis,
        "clinical_metrics": {
            "bradykinesia_score": float(1 - movement_analysis["movement_intensity"]/original_metrics["peak_amplitude"]),
            "tremor_score": float(tremor_amplitude/original_metrics["std_amplitude"]),
            "irregularity_score": float(entropy_results["entropy"]),
            "asymmetry_score": float(1 - abs(correlations["x_y"]["correlation"])) # 0 = simetrico, 1 = asimetrico
        }
    }