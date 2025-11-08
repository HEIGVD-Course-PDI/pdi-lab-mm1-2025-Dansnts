"""Plot performance metrics of M/M/1 queueing system.

NB : This script was mostly written by ChatGPT
"""
import matplotlib.pyplot as plt
import numpy as np
import main_mm1 as mm1

def plot_mm1_performance():
    """Plot E[T] and E[N] as functions of utilization rho."""
    service_rate = 50.0  # Fixed service rate
    utilizations = []
    mean_response_times = []
    mean_clients = []
    analytical_response_times = []
    analytical_clients = []
    
    # Test utilizations from 0.1 to 0.95 (avoiding rho=1)
    arrival_rates = np.linspace(5, 47.5, 15)  # From 5 to 47.5 (rho=0.1 to 0.95)
    
    print("Running M/M/1 simulations for different utilizations...")
    print("=" * 60)
    
    for arrival_rate in arrival_rates:
        rho = arrival_rate / service_rate
        print(f"Running simulation: λ={arrival_rate:.1f}/s, μ={service_rate}/s, ρ={rho:.2f}")
        
        # Run simulation
        result = mm1.main(arrival_rate=arrival_rate, service_rate=service_rate, sim_duration=5000)
        
        # Calculate analytical results
        analytical_E_T = 1 / (service_rate - arrival_rate) if arrival_rate < service_rate else float('inf')
        analytical_E_N = rho / (1 - rho) if rho < 1 else float('inf')
        
        utilizations.append(rho)
        mean_response_times.append(result['E[T]'])
        mean_clients.append(result['E[N]'])
        analytical_response_times.append(analytical_E_T)
        analytical_clients.append(analytical_E_N)
        
        print(f"  Simulation: E[T]={result['E[T]']:.4f}s, E[N]={result['E[N]']:.4f}")
        print(f"  Analytical: E[T]={analytical_E_T:.4f}s, E[N]={analytical_E_N:.4f}")
        print("-" * 40)
    
    # Plot mean response time E[T] vs utilization
    plt.figure(figsize=(10, 6))
    plt.plot(utilizations, mean_response_times, 'bo-', linewidth=2, markersize=4, label='Simulation')
    plt.plot(utilizations, analytical_response_times, 'r--', linewidth=2, label='Analytical')
    plt.xlabel('Utilization (ρ)')
    plt.ylabel('Mean Response Time E[T] (seconds)')
    plt.title('M/M/1 Queue: Mean Response Time vs Utilization\n(λ varies, μ=50/s constant)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('mm1_t.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Plot mean number of clients E[N] vs utilization
    plt.figure(figsize=(10, 6))
    plt.plot(utilizations, mean_clients, 'bo-', linewidth=2, markersize=4, label='Simulation')
    plt.plot(utilizations, analytical_clients, 'r--', linewidth=2, label='Analytical')
    plt.xlabel('Utilization (ρ)')
    plt.ylabel('Mean Number of Clients E[N]')
    plt.title('M/M/1 Queue: Mean Number of Clients vs Utilization\n(λ varies, μ=50/s constant)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('mm1_n.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nPlots saved as 'mm1_t.png' and 'mm1_n.png'")

if __name__ == "__main__":
    plot_mm1_performance()