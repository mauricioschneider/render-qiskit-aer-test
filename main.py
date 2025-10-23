# main.py

from fastapi import FastAPI
from qiskit import QuantumCircuit
# 1. Modern Import: Use the universal simulator class directly
from qiskit_aer import AerSimulator
# 2. Legacy-Style Import: Import the Aer object to access its get_backend method
from qiskit_aer import Aer 

# Initialize the FastAPI application
app = FastAPI(
    title="Qiskit Quantum Circuit Simulator",
    description="Exposes minimal Qiskit circuit simulations using distinct Aer access methods."
)

def build_circuit():
    """Helper function to build the common circuit."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc

# -----------------------------------------------------------
# MODERN PATH: Direct class instantiation
# -----------------------------------------------------------
@app.get("/run-circuit-modern")
def run_modern_quantum_circuit():
    """
    Uses the modern Qiskit 1.x method: qiskit_aer.AerSimulator().
    """
    
    qc = build_circuit()
    
    # Modern approach: Instantiate the general simulator class
    # This is the standard, recommended way in Qiskit 1.x
    simulator = AerSimulator()
    shots = 1024
    
    job = simulator.run(qc, shots=shots)

    result = job.result()
    counts = result.get_counts(qc)
    
    return {
        "method": "Modern (qiskit_aer.AerSimulator())",
        "shots_run": shots,
        "measurement_counts": counts
    }

# -----------------------------------------------------------
# LEGACY-STYLE PATH: Using Aer.get_backend
# -----------------------------------------------------------
@app.get("/run-circuit-legacy")
def run_legacy_quantum_circuit():
    """
    Simulates the behavior of the deprecated qiskit.Aer.get_backend("qasm_simulator") 
    by using the Aer object imported from qiskit_aer.
    """
    
    qc = build_circuit()
    
    # Legacy-style approach: Call the get_backend method on the Aer object.
    # NOTE: In Qiskit 1.x, this 'Aer' object *must* be imported from qiskit_aer.
    # The result is the same type of simulator as AerSimulator().
    simulator = Aer.get_backend("qasm_simulator") 
    shots = 1024
    
    job = simulator.run(qc, shots=shots)

    result = job.result()
    counts = result.get_counts(qc)
    
    return {
        "method": "Legacy-Style (qiskit_aer.Aer.get_backend('qasm_simulator'))",
        "shots_run": shots,
        "measurement_counts": counts
    }

# Example to run locally (Render handles the execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)