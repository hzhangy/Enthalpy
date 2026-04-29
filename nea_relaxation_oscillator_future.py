import numpy as np
import matplotlib.pyplot as plt

class RelaxationAuditor:
    def __init__(self, h_min=1.15, h_limit=2.0):
        self.h_min = h_min
        self.h_limit = h_limit

    def simulate_epoch(self, years=600, base_innovation=0.01, base_decay=0.02, 
                       innovation_pressure=0.5, decay_pressure=0.5):
        """
        修正的弛豫振荡模型：
        - 创新率随 H 升高而增强（压力驱动改革）
        - 衰减率随 H 升高而增强（内耗随复杂度增长）
        - 重置后 H 回到 1.33（3D 背景）
        """
        h = 1.33
        time_axis = []
        enthalpy_axis = []
        reset_times = []
        
        for t in range(years):
            pressure = (h - self.h_min) / (self.h_limit - self.h_min)
            # 确保 pressure 在 [0,1] 区间
            pressure = max(0.0, min(1.0, pressure))
            innovation = base_innovation * (1 + innovation_pressure * pressure)
            decay = base_decay * (1 + decay_pressure * pressure)
            
            dh = decay - innovation
            h += dh
            
            time_axis.append(t)
            enthalpy_axis.append(h)
            
            if h >= self.h_limit:
                reset_times.append(t)
                h = 1.33  # 重置
        
        return time_axis, enthalpy_axis, reset_times

def run_prediction_demo():
    auditor = RelaxationAuditor()
    years = 600  # 定义模拟时长
    
    # 内卷文明：高衰减压力，低创新压力响应
    t1, h1, r1 = auditor.simulate_epoch(years=years,
                                         base_innovation=0.012, base_decay=0.025,
                                         innovation_pressure=0.3, decay_pressure=0.7)
    # 弹性文明：高创新压力响应，低衰减基础
    t2, h2, r2 = auditor.simulate_epoch(years=years,
                                         base_innovation=0.018, base_decay=0.022,
                                         innovation_pressure=0.8, decay_pressure=0.4)
    
    print(f"内卷文明：{len(r1)} 次崩溃，平均周期 {years/len(r1) if r1 else 0:.1f} 年")
    print(f"弹性文明：{len(r2)} 次崩溃，平均周期 {years/len(r2) if r2 else 0:.1f} 年")
    
    plt.figure(figsize=(12,6))
    plt.plot(t1, h1, 'r-', label='Involuted System (high decay, low reform)')
    plt.plot(t2, h2, 'g-', label='Resilient System (high reform responsiveness)')
    for rt in r1:
        plt.axvline(x=rt, color='red', linestyle=':', alpha=0.3)
    for rt in r2:
        plt.axvline(x=rt, color='green', linestyle=':', alpha=0.3)
    plt.axhline(y=2.0, color='k', linestyle='--', label='Survival Limit (H=2.0)')
    plt.axhline(y=1.33, color='blue', linestyle='-.', alpha=0.5, label='3D Background')
    plt.xlabel('Time (years)')
    plt.ylabel('Total Enthalpy H')
    plt.title('N.E.A. Paper X: Relaxation Oscillator – Civilisation Cycles')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

if __name__ == "__main__":
    run_prediction_demo()
