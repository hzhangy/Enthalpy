import numpy as np
import matplotlib.pyplot as plt

class HistoryAuditor:
    def __init__(self):
        self.H_LIMIT = 2.0
        self.H_BASE = 1.3333

    def audit_soviet_collapse(self):
        """场景1：苏联解体 (1960-1991)"""
        years = np.linspace(1960, 1991, 32)
        # 冗余度(各向同性)随体制僵化加速上升
        redundancy = 0.5 * np.exp((years - 1960) * 0.08)
        # 创新率(各向异性)在70年代后停滞
        innovation = 1.0 / (1 + (years - 1975)**2 * 0.01)
        # 计算系统总焓
        h_history = self.H_BASE + 0.1 * np.log(redundancy / (innovation + 1e-9))
        return years, h_history, 1991

    def audit_moore_law_pivot(self):
        """场景2：摩尔定律主频墙 (1970-2010)"""
        years = np.linspace(1970, 2010, 40)
        # 1D 频率增长带来的热噪声 (Isotropic Thermal Noise)
        heat_debt = np.exp((years - 1970) * 0.12) * 0.01
        # 制造工艺的各向异性增益
        process_gain = 0.8 * (years - 1970)
        h_history = 1.3333 + 0.05 * (heat_debt / (process_gain + 1e-9))
        return years, h_history, 2004 # 2004年主频墙崩溃

    def audit_human_aging(self):
        """场景3：人类寿命极限 (0-100岁)"""
        age = np.linspace(0, 100, 100)
        # 生物冗余(错误累积)随年龄指数增长 - Gompertz 规律
        bio_decay = 0.001 * np.exp(age * 0.08)
        # 代谢修复能力随年龄下降
        repair_xi = 1.0 / (1 + age * 0.02)
        h_history = 1.25 + 0.1 * np.log(bio_decay / (repair_xi + 1e-9))
        return age, h_history, 85 # 预期寿命

def run_suite():
    auditor = HistoryAuditor()
    print(">>> N.E.A. Paper X: 真实历史数据回测审计系统...")
    print("-" * 60)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

    # 1. 苏联结算
    y1, h1, event1 = auditor.audit_soviet_collapse()
    ax1.plot(y1, h1, 'r-', label='System Enthalpy H (USSR)')
    ax1.axhline(y=2.0, color='k', linestyle='--', label='Collapse Limit')
    ax1.axvline(x=event1, color='blue', alpha=0.3, label='Dissolution (1991)')
    ax1.set_title('Case 1: The Geopolitical Deadlock (USSR)')
    ax1.legend()

    # 2. 摩尔定律结算
    y2, h2, event2 = auditor.audit_moore_law_pivot()
    ax2.plot(y2, h2, 'g-', label='Compute Enthalpy H')
    ax2.axhline(y=1.5, color='orange', linestyle='--', label='Power Wall Threshold')
    ax2.axvline(x=event2, color='blue', alpha=0.3, label='Frequency Saturation (2004)')
    ax2.set_title('Case 2: The 1D Bandwidth Wall (Moore\'s Law)')
    ax2.legend()

    # 3. 寿命结算
    y3, h3, event3 = auditor.audit_human_aging()
    ax3.plot(y3, h3, 'm-', label='Biological Enthalpy H')
    ax3.axhline(y=2.0, color='k', linestyle='--', label='Biological Singularity')
    ax3.set_title('Case 3: The Winding Limit of Life (Aging)')
    ax3.set_xlabel('Age / Time Scale')
    ax3.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_suite()