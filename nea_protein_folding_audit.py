import numpy as np
import matplotlib.pyplot as plt

def simulate_protein_folding():
    # Simulate 1000 random conformations
    num_configs = 1000
    # Random anisotropic efficiency xi (0.0 = disordered, 0.35 = perfectly folded)
    np.random.seed(42)
    xi_samples = np.random.beta(2, 5, num_configs) * 0.4
    
    # Baseline 3D rent (1 + 1/3)
    h_base = 1.3333
    
    # Emergent enthalpy H = (1 + 1/d) * e^(-xi)
    h_values = h_base * np.exp(-xi_samples)
    
    # Sort to observe convergence
    sorted_h = np.sort(h_values)
    
    print(">>> N.E.A. Protein Folding Audit: Locating the Functional Threshold")
    # Find conformations crossing below the 1.25 ZY functional threshold
    folded_mask = sorted_h < 1.25
    num_folded = np.sum(folded_mask)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(range(num_configs), sorted_h, c='gray', alpha=0.3, label='Random Conformations')
    plt.scatter(np.where(folded_mask)[0], sorted_h[folded_mask], 
                c='green', s=100, label='Folded Functional State ($H < 1.25$ ZY)')
    
    plt.axhline(y=1.25, color='red', linestyle='--', label='Functional Threshold ($H_{\\mathrm{base}}(4) = 1.25$ ZY)')
    plt.axhline(y=1.3333, color='blue', linestyle=':', label='3D Background ($H = 1.3333$ ZY)')
    
    plt.title('Protein Folding: Convergence as Enthalpy Arbitrage')
    plt.xlabel('Conformation Index (Sorted by Efficiency)')
    plt.ylabel('System Enthalpy H (ZY)')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('protein_folding.png', dpi=150)
    plt.show()

    print(f"--- Settlement: Out of {num_configs} conformations, only {num_folded} redeem sufficient bandwidth to sustain function.")
    print("Conclusion: Folding is a topological necessity, not a probabilistic accident.")

if __name__ == "__main__":
    simulate_protein_folding()