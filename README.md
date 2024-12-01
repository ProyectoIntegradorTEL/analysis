# Nodo de analítica

## **Autores** ✒️

- Dylan Bermúdez Cardona
- Santiago Escobar León
- Kevin Steven Nieto Curaca
- Ricardo Urbina Ospina

#### **Descripción del Nodo**
Este nodo de analítica procesa señales de movimiento para extraer métricas clave relacionadas con la evaluación motora, específicamente en el contexto de pruebas clínicas como la **MDS-UPDRS** (Unified Parkinson's Disease Rating Scale). Utiliza algoritmos de análisis de señales para calcular parámetros como la intensidad, variabilidad, frecuencia dominante, entropía, y simetría de los movimientos. Este nodo permite la evaluación automatizada de bradicinesia, temblores, irregularidad y asimetría.

---

#### **Instalación y Ejecución**
1. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate # (macOS)
   .\venv\Scripts\activate # (Windows)
   ```

2. **Instalar las dependencias:**
   Asegúrate de tener el archivo `requirements.txt` en la misma carpeta que el código. Ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el nodo:**
   Para iniciar el servidor FastAPI, utiliza:
   ```bash
   uvicorn main:app --reload
   ```

4. **Endpoints principales:**
   - `/fft`: Procesa la Transformada Rápida de Fourier (FFT) para análisis de frecuencia.
   - `/analyze_signal`: Extrae métricas clínicas y biomecánicas de las señales de entrada.

---

#### **Explicación de Cálculos y Gráficos**

1. **Espectro de Frecuencia (FFT)**
   - **Qué hace:** Identifica las frecuencias dominantes en la señal de movimiento (Hz).
   - **Uso:** Útil para detectar patrones rítmicos asociados con movimientos repetitivos (e.g., zapateo o taconeo) o identificar temblores a frecuencias específicas.

2. **Correlaciones entre ejes**
   - **Qué hace:** Calcula las correlaciones de Pearson entre los ejes X, Y, y Z.
   - **Uso:** Evalúa la coordinación entre diferentes ejes de movimiento, destacando posibles asimetrías entre las extremidades o el tronco.

3. **Métricas de Amplitud**
   - **Mean Amplitude:** Promedio de la amplitud del movimiento.
   - **Peak Amplitude:** Máxima amplitud registrada.
   - **Range Amplitude:** Diferencia entre amplitud máxima y mínima.
   - **Uso:** Determinan la energía del movimiento, identificando bradicinesia si las amplitudes son bajas.

4. **Análisis de Entropía**
   - **Qué hace:** Calcula la entropía de muestra (Sample Entropy) para evaluar la irregularidad de la señal.
   - **Uso:** Un valor alto indica movimientos desordenados o poco predecibles, mientras que un valor bajo refleja movimientos regulares.

5. **Transformada Wavelet**
   - **Qué hace:** Analiza la señal en el dominio de tiempo-frecuencia utilizando la wavelet Morlet.
   - **Uso:** Detecta fluctuaciones en la frecuencia a lo largo del tiempo, útil para analizar movimientos no rítmicos o inestables.

6. **Análisis de Movimiento**
   - **Movement Intensity:** Energía promedio del movimiento.
   - **Movement Variability:** Variabilidad en la intensidad.
   - **Peak Movement:** Valor más alto alcanzado.
   - **Axis Symmetry:** Cuantifica la simetría entre ejes.
   - **Uso:** Evalúa tanto la fuerza como la consistencia de los movimientos.

7. **Métricas Clínicas**
   - **Bradicinesia Score:** Basado en la relación entre la intensidad del movimiento y su amplitud máxima. 
   - **Tremor Score:** Proporción entre la amplitud del temblor dominante y la variabilidad.
   - **Irregularity Score:** Derivado de la entropía.
   - **Asymmetry Score:** Basado en la desviación de la simetría entre los ejes X e Y.
   - **Uso:** Permite una evaluación automatizada de aspectos clínicos clave, alineada con criterios como el MDS-UPDRS.

---

#### **Estructura del Proyecto**
- **`main.py`:** Archivo principal que define los endpoints y cálculos.
- **`models.py`:** Define las clases para validar la entrada de datos.
- **`requirements.txt`:** Lista de dependencias necesarias.