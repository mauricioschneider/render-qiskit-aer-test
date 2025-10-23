# main.py

from fastapi import FastAPI
from qiskit import QuantumCircuit
# Note: For Qiskit 1.x, the 'Aer' object is typically accessed 
# via the qiskit_aer package, but we can also check for the 
# legacy access point if needed. For simplicity and correctness
# with the newer versions, we'll import AerSimulator for the modern route
# and demonstrate the get_backend approach in the function itself.
from qiskit_aer import AerSimulator # Used for the original endpoint
# Import the legacy access point for the Qiskit.Aer path
from qiskit.providers.aer import Aer # Required for the legacy get_backend call

# Initialize the FastAPI application
app = FastAPI(
    title="Qiskit Quantum Circuit Simulator",
    description="Exposes minimal Qiskit circuit simulations using both modern and legacy Aer methods."
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
    
    # Build the circuit
    qc = build_circuit()
    
    # Set up the Aer simulator using the modern approach
    simulator = AerSimulator()
    shots = 1024
    
    # Run the circuit
    job = simulator.run(qc, shots=shots)

    # Get the results
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
    Uses the older, explicit Qiskit method: qiskit.Aer.get_backend("qasm_simulator").
    """
    
    # Build the circuit
    qc = build_circuit()
    
    # 4. Set up the Aer simulator using the legacy approach
    # We access the QASM simulator via the qiskit.providers.aer.Aer object
    # This is equivalent to the old qiskit.Aer.get_backend
    simulator = Aer.get_backend("qasm_simulator")
    shots = 1024
    
    # 5. Run the circuit
    job = simulator.run(qc, shots=shots)

    # 6. Get the results
    result = job.result()
    counts = result.get_counts(qc)
    
    return {
        "method": "Legacy (Aer.get_backend('qasm_simulator'))",
        "shots_run": shots,
        "measurement_counts": counts
    }

# Example to run locally (Render handles the execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)