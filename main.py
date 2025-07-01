
import hashlib
import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib
from concurrent.futures import ThreadPoolExecutor, as_completed
matplotlib.use('Agg')
import threading 

class Block:
    def __init__(self, index, data, previous_hash="0"):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = ""

    def compute_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

class Node:
    def __init__(self, name, power=1.0, latency=0.0):
        self.name = name
        self.power = power
        self.latency = latency
        self.blocks_mined = 0
        self.total_time = 0
        self.total_attempts = 0
        self.chain = []

    def mine_block(self, block, difficulty_bits):
        target = "0" * difficulty_bits
        attempts = 0
        start = time.time()
        hash_rate = self.power * 1000 

        while True:
            elapsed = time.time() - start
            expected_attempts = int(hash_rate * elapsed)
            to_try = expected_attempts - attempts
            if to_try <= 0:
                time.sleep(0.01) 
                continue

            for _ in range(to_try):
                hash_result = block.compute_hash()
                attempts += 1
                if hash_result.startswith(target):
                    block.hash = hash_result
                    duration = time.time() - start
                    self.total_time += duration
                    self.total_attempts += attempts
                    return block, attempts, duration
                block.nonce = random.randint(0, 1_000_000_000)

class PoWSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador PoW")
        self.difficulty = 2
        self.rounds = 3
        self.results = []
        self.setup_widgets()
        self.setup_node_table()

        for name, power, latency in [("Nó A", 0.4, 0.2), ("Nó B", 2.5, 0.1), ("Nó C", 2.0, 0.3)]:
            self.node_table.insert("", "end", values=(name, power, latency))

    def setup_widgets(self):
        self.log = tk.Text(self.root, height=20, width=70)
        self.log.pack(pady=10)
        controls = tk.Frame(self.root)
        controls.pack()
        ttk.Label(controls, text="Dificuldade (bits):").pack(side=tk.LEFT)
        self.diff_var = tk.IntVar(value=self.difficulty)
        ttk.Entry(controls, textvariable=self.diff_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(controls, text="Rodadas:").pack(side=tk.LEFT)
        self.rounds_var = tk.IntVar(value=self.rounds)
        ttk.Entry(controls, textvariable=self.rounds_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Iniciar Simulação", command=self.run_simulation).pack(side=tk.LEFT, padx=10)
        ttk.Button(controls, text="Gerar Gráficos", command=self.generate_graphs).pack(side=tk.LEFT, padx=10)

    def log_message(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def adjust_difficulty(self, block_times):
        if len(block_times) < 3:
            return self.difficulty
        avg = sum(block_times[-3:]) / 3
        if avg < 1.0:
            return self.difficulty + 1
        elif avg > 3.0 and self.difficulty > 1:
            return self.difficulty - 1
        return self.difficulty

    def add_node(self):
        name = self.entry_name.get()
        try:
            power = float(self.entry_power.get())
            latency = float(self.entry_latency.get())
        except ValueError:
            self.log_message("⚠️ Poder e latência devem ser números.")
            return
        self.node_table.insert("", "end", values=(name, power, latency))

    def remove_selected_node(self):
        selected = self.node_table.selection()
        for item in selected:
            self.node_table.delete(item)

    def get_nodes_from_table(self):
        nodes = []
        for item in self.node_table.get_children():
            name, power, latency = self.node_table.item(item)["values"]
            nodes.append(Node(name, float(power), float(latency)))
        return nodes


    def setup_node_table(self):
        frame = ttk.LabelFrame(self.root, text="Nós Participantes")
        frame.pack(pady=10)

        columns = ("Nome", "Poder", "Latência")
        self.node_table = ttk.Treeview(frame, columns=columns, show="headings", height=4)
        for col in columns:
            self.node_table.heading(col, text=col)
            self.node_table.column(col, width=100)
        self.node_table.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.node_table.yview)
        self.node_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack()

        self.entry_name = ttk.Entry(btn_frame, width=10)
        self.entry_name.insert(0, "Nó X")
        self.entry_name.pack(side=tk.LEFT, padx=2)

        self.entry_power = ttk.Entry(btn_frame, width=5)
        self.entry_power.insert(0, "1.0")
        self.entry_power.pack(side=tk.LEFT, padx=2)

        self.entry_latency = ttk.Entry(btn_frame, width=5)
        self.entry_latency.insert(0, "0.2")
        self.entry_latency.pack(side=tk.LEFT, padx=2)

        ttk.Button(btn_frame, text="Adicionar Nó", command=self.add_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover Selecionado", command=self.remove_selected_node).pack(side=tk.LEFT, padx=5)


    def simulate(self):
        self.nodes = self.get_nodes_from_table()

        self.log.delete(1.0, tk.END)
        self.difficulty = self.diff_var.get()
        self.rounds = self.rounds_var.get()
        previous_hash = "0"
        self.results = []
        block_times = []

        for round_num in range(1, self.rounds + 1):
            self.log_message(f"Rodada {round_num} (Dificuldade: {self.difficulty})")
            base_block = Block(round_num, f"Transações {round_num}", previous_hash)

            mining_tasks = []
            node_blocks = {}

            with ThreadPoolExecutor() as executor:
                for node in self.nodes:
                    def delayed_mine(n=node):
                        time.sleep(n.latency) 
                        new_block = Block(round_num, base_block.data, previous_hash)
                        result = n.mine_block(new_block, self.difficulty)
                        return n, *result

                    mining_tasks.append(executor.submit(delayed_mine))

                winner_result = None
                for future in as_completed(mining_tasks):
                    node, mined_block, attempts, duration = future.result()

                    if not winner_result:
                        winner_result = (node, mined_block, attempts, duration)
                    else:
                        if mined_block.hash != winner_result[1].hash:
                            self.log_message(f"Fork detectado entre {winner_result[0].name} e {node.name}")
                    
                    self.log_message(f"{node.name} tentou: {attempts} tentativas em {duration:.2f}s")
                    node_blocks[node.name] = mined_block

            winner_node, final_block, attempts, duration = winner_result
            previous_hash = final_block.hash
            winner_node.blocks_mined += 1
            winner_node.total_time += duration
            winner_node.total_attempts += attempts
            winner_node.chain.append(final_block)
            self.results.append((round_num, winner_node.name, duration))
            block_times.append(duration)

            propagation_threads = []
            for node in self.nodes:
                if node != winner_node:
                    def propagate(n=node):
                        time.sleep(n.latency)
                        if not any(b.index == final_block.index and b.hash == final_block.hash for b in n.chain):
                            n.chain.append(final_block)

                    t = threading.Thread(target=propagate)
                    t.start()
                    propagation_threads.append(t)

            for t in propagation_threads:
                t.join()

            self.log_message(f"{winner_node.name} venceu com {attempts} tentativas em {duration:.2f}s")
            self.difficulty = self.adjust_difficulty(block_times)

        self.log_message("\nResultado Final:")
        for node in self.nodes:
            avg_time = node.total_time / node.blocks_mined if node.blocks_mined else 0
            self.log_message(f"- {node.name}: {node.blocks_mined} blocos, média {avg_time:.2f}s/bloco, {node.total_attempts} tentativas")


    def generate_graphs(self):
        nomes = [n.name for n in self.nodes]
        blocos = [n.blocks_mined for n in self.nodes]
        tempos = [n.total_time / n.blocks_mined if n.blocks_mined else 0 for n in self.nodes]
        tentativas = [n.total_attempts for n in self.nodes]
        rodadas = [r[0] for r in self.results]
        vencedores = [r[1] for r in self.results]

        plt.figure(figsize=(8,5))
        plt.bar(nomes, blocos, color='mediumseagreen')
        plt.title("Blocos Minerados por Nó")
        plt.xlabel("Nó")
        plt.ylabel("Blocos Minerados")
        plt.tight_layout()
        plt.savefig("grafico_blocos.png")

        plt.figure(figsize=(8,5))
        plt.bar(nomes, tempos, color='cornflowerblue')
        plt.title("Tempo Médio por Bloco por Nó")
        plt.xlabel("Nó")
        plt.ylabel("Tempo Médio (s)")
        plt.tight_layout()
        plt.savefig("grafico_tempos.png")

        plt.figure(figsize=(8,5))
        plt.bar(nomes, tentativas, color='salmon')
        plt.title("Total de Tentativas por Nó")
        plt.xlabel("Nó")
        plt.ylabel("Tentativas")
        plt.tight_layout()
        plt.savefig("grafico_tentativas.png")

        plt.figure(figsize=(10,5))
        plt.plot(rodadas, vencedores, marker='o', linestyle='--', color='purple')
        plt.title("Nó Vencedor por Rodada")
        plt.xlabel("Rodada")
        plt.ylabel("Nó Vencedor")
        plt.xticks(rodadas)
        plt.tight_layout()
        plt.savefig("grafico_vencedores_por_rodada.png")

        self.log_message("Gráficos gerados e salvos com sucesso.")

    def run_simulation(self):
        self.root.after(100, self.simulate)

if __name__ == "__main__":
    root = tk.Tk()
    app = PoWSimulatorGUI(root)
    root.mainloop()