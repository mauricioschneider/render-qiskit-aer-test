from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Initialize the FastAPI application
app = FastAPI(
    title="Qiskit Quantum Circuit Simulator",
    description="Exposes a minimal Qiskit circuit simulation as an HTTP endpoint."
)

@app.get("/run-circuit")
def run_quantum_circuit():
    """
    Creates, simulates, and returns the results for a single-qubit 
    superposition circuit (Hadamard gate).
    """
    
    # --- Qiskit Simulation Logic ---
    
    # 1. Create a quantum circuit (1 qubit, 1 classical bit)
    qc = QuantumCircuit(1, 1)

    # 2. Apply a Hadamard gate (H) for superposition
    qc.h(0)

    # 3. Measure the qubit
    qc.measure(0, 0)

    # 4. Set up the Aer simulator
    simulator = AerSimulator()
    
    # Define the number of shots
    shots = 1024
    
    # 5. Run the circuit on the simulator
    job = simulator.run(qc, shots=shots)

    # 6. Get the results and the counts
    result = job.result()
    counts = result.get_counts(qc)
    
    # 7. Return the results as a dictionary (which FastAPI converts to JSON)
    return {
        "status": "success",
        "shots_run": shots,
        "circuit_description": "Single qubit in superposition (H gate, then measure).",
        "measurement_counts": counts
    }

# Example to run locally (Render handles the execution using the 'gunicorn' command below)
if __name__ == "__main__":
    import uvicorn
    # This is for local testing: 'http://127.0.0.1:8000/run-circuit'
    uvicorn.run(app, host="0.0.0.0", port=8000)