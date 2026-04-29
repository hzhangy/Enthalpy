import numpy as np
import matplotlib.pyplot as plt

def audit_cpu_history():
    # 真实历史定标数据 (年份, 主频MHz, 功耗W)
    # 数据取自 Intel 历代旗舰典型值
    cpu_data = [
        (1971, 0.74, 0.5),   # 4004
        (1978, 5.0, 2.0),    # 8086
        (1985, 16.0, 3.0),   # 80386
        (1993, 66.0, 15.0),  # Pentium
        (2000, 1500.0, 50.0),# Pentium 4
        (2004, 3800.0, 115.0),# P4 Prescott (主频墙点)
        (2006, 2600.0, 65.0), # Core 2 Duo (转向多核降频)
        (2015, 4000.0, 91.0)  # Skylake
    ]
    years, freqs, tdps = zip(*cpu_data)
    years = np.array(years)
    freqs = np.array(freqs)
    tdps = np.array(tdps)

    print(">>> N.E.A. 摩尔定律主频墙审计：使用 Intel 真实历史参数...")
    print("-" * 65)
    
    # 计算逻辑：
    # H = 基准(1.33) + 外部压力(f_ext/B)
    # 在 1D 扩展中，主频即 f_ext。热耗散(TDP)代表了系统各向同性的噪音阻力。
    # 我们定义 H = 1.33 + (Freq_norm * TDP_norm) 的拓扑反馈
    
    # 归一化处理（以2004年为峰值参考）
    f_norm = freqs / 3800.0
    p_norm = tdps / 115.0
    
    # N.E.A. 焓计算公式：H = 1.33 + 0.67 * (负载比例)
    # 当负载比例=1时，H=2.0，触发维度坍缩（主频墙）
    h_values = 1.3333 + 0.6667 * (f_norm * p_norm)

    for i in range(len(years)):
        status = "CRITICAL" if h_values[i] > 1.9 else "Normal"
        print(f"年份: {years[i]} | 主频: {freqs[i]:>7} MHz | H 值: {h_values[i]:.4f} | 状态: {status}")

    plt.figure(figsize=(10, 6))
    plt.plot(years, h_values, 'k-o', label='CPU Topological Enthalpy H')
    plt.axhline(y=2.0, color='r', linestyle='--', label='1D Bandwidth Limit (Collapse)')
    plt.axvline(x=2004, color='blue', alpha=0.3, label='The 2004 Power Wall')
    
    plt.annotate('Dimensional Pivot to Multi-core', xy=(2004, 2.0), xytext=(1985, 2.1),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.title('Real-world Audit: Why CPU Frequencies Stopped at 4GHz')
    plt.xlabel('Year')
    plt.ylabel('System Enthalpy H')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    audit_cpu_history()