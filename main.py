# main.py

from fastapi import FastAPI
from qiskit import QuantumCircuit
# Import Qiskit-Aer components directly
from qiskit_aer import AerSimulator # The class for the modern method

# Initialize the FastAPI application
app = FastAPI(
    title="Qiskit Quantum Circuit Simulator",
    description="Exposes minimal Qiskit circuit simulations using modern and legacy-style Aer access."
)

def build_circuit():
    """Helper function to build the common circuit."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc

@app.get("/run-circuit-modern")
def run_modern_quantum_circuit():
    """
    Uses the modern Qiskit 1.x method: qiskit_aer.AerSimulator().
    """
    
    qc = build_circuit()
    
    # Modern approach: Instantiate the general simulator class
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

@app.get("/run-circuit-legacy")
def run_legacy_quantum_circuit():
    """
    Simulates the behavior of qiskit.Aer.get_backend("qasm_simulator") 
    using the Qiskit 1.x compatible path.
    """
    
    qc = build_circuit()
    
    # Qiskit 1.x compatible way to get the QASM simulator
    # By default, AerSimulator *is* the QASM simulator unless a method is specified.
    # To mimic the explicit 'qasm_simulator' selection, we use AerSimulator directly.
    simulator = AerSimulator() 
    shots = 1024
    
    # --- NOTE ON SIMULATION METHOD ---
    # In Qiskit 1.x, you typically configure AerSimulator() with a 'method' 
    # to select a specific backend (e.g., 'statevector', 'density_matrix').
    # Without a method, it defaults to a 'qasm_simulator'-like behavior.
    
    job = simulator.run(qc, shots=shots)

    result = job.result()
    counts = result.get_counts(qc)
    
    return {
        "method": "Legacy-Style Access (qiskit_aer.AerSimulator() used to mimic 'qasm_simulator')",
        "shots_run": shots,
        "measurement_counts": counts
    }

# Example to run locally (Render handles the execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)