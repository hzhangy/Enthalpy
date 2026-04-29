import numpy as np
import matplotlib.pyplot as plt

def run_dynasty_audit():
    # Real historical data: Dynasty | Lifespan (years)
    dynasties = [
        ("Tang",    289),
        ("Song",    319),
        ("Ming",    276),
        ("Qing",    268)
    ]
    
    # N.E.A. audit parameters
    H_START = 1.3333  # 3D stable baseline
    H_LIMIT = 2.0000  # 1D collapse threshold
    
    # Isotropic decay rate in agrarian civilizations
    # Land consolidation erodes per-capita bandwidth
    DECAY_RATE = 0.0022 

    print(">>> N.E.A. Dynasty Cycle Audit: The 2.0 Bandwidth Wall")
    print("-" * 60)
    print(f"{'Dynasty':<10} | {'Actual':<8} | {'N.E.A. Predicted':<16} | {'Error'}")
    print("-" * 60)

    results = []
    for name, actual_years in dynasties:
        predicted_years = (H_LIMIT - H_START) / DECAY_RATE
        error = abs(predicted_years - actual_years) / actual_years
        results.append((name, actual_years, predicted_years, error))
        print(f"{name:<10} | {actual_years:<8} | {predicted_years:<12.1f} | {error:.2%}")

    # Enthalpy trajectory
    t = np.linspace(0, 350, 100)
    h_path = H_START + DECAY_RATE * t
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, h_path, 'r-', linewidth=2, label='Civilizational Enthalpy H')
    plt.axhline(y=H_LIMIT, color='black', linestyle='--', label='The 2.0 ZY Threshold (Collapse)')
    
    for name, actual, _, _ in results:
        plt.axvline(x=actual, color='gray', alpha=0.3)
        plt.text(actual, 1.4, name, rotation=90, fontsize=10)
        
    plt.title('Dynasty Cycle Audit: The 2.0 Bandwidth Wall')
    plt.xlabel('Years')
    plt.ylabel('System Enthalpy H (ZY)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('dynasty_fitting.png', dpi=150)
    plt.show()

if __name__ == "__main__":
    run_dynasty_audit()