import numpy as np
import matplotlib.pyplot as plt

def run_path_pruning_audit(num_initial_futures=100, steps=60):
    initial_h = 1.65  # 模拟一个处于十字路口的系统
    h_limit = 2.0     # 逻辑存续底线
    
    # 存储路径
    paths = []
    alive_count_at_step = []

    print(f">>> N.E.A. 路径剪枝审计：从 {num_initial_futures} 个潜在未来中清算‘逻辑赤字’...")

    # 初始化100个可能的意图/路径
    current_states = np.full(num_initial_futures, initial_h)
    active_mask = np.ones(num_initial_futures, dtype=bool)
    all_path_data = [current_states.copy()]

    for s in range(steps):
        # 模拟各向同性噪音（随机波动）和系统自然损耗
        decay = 0.015
        # 不同的分支有不同的协同能力（随机各向异性）
        innovation = np.random.normal(0.01, 0.03, num_initial_futures)
        
        # 计算下一步焓变
        dh = decay - innovation
        current_states += dh
        
        # 执行“逻辑清算”：凡是 H >= 2.0 的路径，判定为“死锁”，永久湮灭
        active_mask = active_mask & (current_states < h_limit)
        
        # 抹除死掉的路径数据
        current_states[~active_mask] = np.nan 
        all_path_data.append(current_states.copy())
        alive_count_at_step.append(np.sum(active_mask))

    # 转换数据以便绘图
    all_path_data = np.array(all_path_data)
    
    plt.figure(figsize=(10, 6))
    plt.plot(all_path_data, color='gray', alpha=0.3, linewidth=0.5)
    # 突出显示最后还活着的路径
    alive_indices = np.where(active_mask)[0]
    for idx in alive_indices:
        plt.plot(all_path_data[:, idx], color='green', linewidth=1.5, alpha=0.8)

    plt.axhline(y=h_limit, color='red', linestyle='--', label='Bandwidth Bankruptcy (H=2.0)')
    plt.title(f'The Pruning of Time: {np.sum(active_mask)} Allowed Futures from {num_initial_futures}')
    plt.xlabel('Computational Steps (Time)')
    plt.ylabel('Enthalpy H')
    plt.grid(True, alpha=0.2)
    plt.show()

    print(f"--- 审计结算：")
    print(f"初始可能性: {num_initial_futures} | 最终显化路径: {np.sum(active_mask)}")
    print(f"逻辑淘汰率: {((num_initial_futures - np.sum(active_mask))/num_initial_futures)*100:.1f}%")

if __name__ == "__main__":
    run_path_pruning_audit()