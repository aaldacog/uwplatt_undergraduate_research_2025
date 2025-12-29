from .base_player import BasePlayer
import random

from .base_player import BasePlayer
import random


class QuantumPlayer(BasePlayer):
    """
    Optimized quantum player that pre-generates quantum random numbers in batches
    for much better performance.
    """
    # Class-level cache for quantum components
    _simulator = None
    _import_error = None
    _quantum_buffer = []
    _buffer_index = 0
    _buffer_size = 1000  # Pre-generate 1000 quantum random numbers at once

    @classmethod
    def _initialize_quantum(cls):
        """Initialize quantum components once (class-level cache)"""
        if cls._import_error is not None:
            return False

        if cls._simulator is None:
            try:
                from qiskit_aer import AerSimulator
                cls._simulator = AerSimulator()
                return True
            except ImportError as e:
                cls._import_error = e
                return False
        return True

    @classmethod
    def _refill_quantum_buffer(cls):
        """Refill the quantum random number buffer"""
        if not cls._initialize_quantum():
            # Fallback to classical random for buffer
            cls._quantum_buffer = [random.randint(0, 255) for _ in range(cls._buffer_size)]
            cls._buffer_index = 0
            return

        try:
            from qiskit import QuantumCircuit, transpile

            # Generate many random numbers at once using 8 qubits (256 possible values)
            qc = QuantumCircuit(8, 8)
            qc.h(range(8))  # Create superposition of all 256 possible values
            qc.measure(range(8), range(8))

            # Execute once to get many random numbers
            compiled_qc = transpile(qc, cls._simulator)
            job = cls._simulator.run(compiled_qc, shots=cls._buffer_size)
            result = job.result()
            counts = result.get_counts()

            # Convert all results to numbers and expand based on shot counts
            cls._quantum_buffer = []
            for binary_string, count in counts.items():
                number = int(binary_string, 2)
                # Add each number 'count' times to maintain distribution
                cls._quantum_buffer.extend([number] * count)

            cls._buffer_index = 0

        except Exception as e:
            # Fallback to classical random for buffer
            cls._quantum_buffer = [random.randint(0, 255) for _ in range(cls._buffer_size)]
            cls._buffer_index = 0

    def get_move(self, game):
        """Get move using quantum randomness with batch optimization"""
        valid_moves = game.get_valid_moves()

        # For very small move sets, quantum isn't worth the overhead
        if len(valid_moves) <= 2:
            return random.choice(valid_moves)

        # Get next quantum random number from buffer
        if self._buffer_index >= len(self._quantum_buffer):
            self._refill_quantum_buffer()

        quantum_number = self._quantum_buffer[self._buffer_index]
        self._buffer_index += 1

        # Map quantum random number to valid move
        move_index = quantum_number % len(valid_moves)
        return valid_moves[move_index]

# class QuantumPlayer(BasePlayer):
#     def get_move(self, game):
#         valid_moves = game.get_valid_moves()
#
#         try:
#             # Qiskit 1.0+ compatible code
#             from qiskit import QuantumCircuit, transpile
#             from qiskit_aer import AerSimulator
#             from qiskit.visualization import plot_histogram
#
#             # Create a quantum circuit with enough qubits
#             num_qubits = max(1, len(valid_moves).bit_length())
#             qc = QuantumCircuit(num_qubits, num_qubits)
#
#             # Apply Hadamard gates to create superposition
#             for i in range(num_qubits):
#                 qc.h(i)
#
#             # Measure the qubits
#             qc.measure(range(num_qubits), range(num_qubits))
#
#             # Execute the circuit - Qiskit 1.0+ syntax
#             simulator = AerSimulator()
#
#             # Transpile circuit for the simulator
#             compiled_circuit = transpile(qc, simulator)
#
#             # Execute the circuit
#             job = simulator.run(compiled_circuit, shots=1)
#             result = job.result()
#             counts = result.get_counts()
#
#             # Convert the result to an integer
#             quantum_number = int(list(counts.keys())[0], 2)
#
#             # Map the quantum number to a valid move
#             move_index = quantum_number % len(valid_moves)
#             return valid_moves[move_index]
#
#         except ImportError as e:
#             # Fallback to classical randomness if Qiskit is not available
#             print(f"Qiskit not available: {e}, using classical random fallback")
#             return random.choice(valid_moves)
#         except Exception as e:
#             # Fallback for any Qiskit-related errors
#             print(f"Quantum computation failed: {e}, using classical random fallback")
#             return random.choice(valid_moves)