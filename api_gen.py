import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import smtplib
from email.message import EmailMessage

def generate_quantum_api_key(length=52):
    total_bits_needed = length * 4
    MAX_QUBITS_PER_SHOT = 24
    simulator = AerSimulator()
    all_random_bits = []
    bits_generated = 0

    while bits_generated < total_bits_needed:
        qubits_this_shot = min(MAX_QUBITS_PER_SHOT, total_bits_needed - bits_generated)
        circuit = QuantumCircuit(qubits_this_shot, qubits_this_shot)
        circuit.h(range(qubits_this_shot))
        circuit.measure(range(qubits_this_shot), range(qubits_this_shot))

        compiled_circuit = transpile(circuit, simulator)
        job = simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(circuit)

        bit_chunk = list(counts.keys())[0]
        all_random_bits.append(bit_chunk)
        bits_generated += len(bit_chunk)

    random_bitstring = "".join(all_random_bits)
    random_integer = int(random_bitstring, 2)
    hex_string = hex(random_integer)[2:]
    api_key = hex_string.zfill(length)
    return api_key

def send_api_key_by_email(api_key, recipient_email):
    sender_email = os.environ.get('EMAIL_ADDRESS')
    app_password = os.environ.get('EMAIL_PASSWORD')

    if not sender_email or not app_password:
        raise ValueError("Email credentials (EMAIL_ADDRESS, EMAIL_PASSWORD) are not set in .env file.")

    msg = EmailMessage()
    msg['Subject'] = 'Your New Quantum-Powered API Key'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f"Welcome!\n\nYour new secure API Key is: {api_key}\n\nPlease store it safely.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    print("--- Quantum-Powered API Key Generator ---")
    new_api_key = generate_quantum_api_key(52)
    print(f"\nGenerated API Key: {new_api_key}")
    print(f"Key Length: {len(new_api_key)} characters")
