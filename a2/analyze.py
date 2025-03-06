import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_sim_stats(file_path):
    stats_dict = {}
    print(file_path)
    with open(file_path, 'r') as file:
        # Skip the header line
        next(file)
        
        for line in file:
            line = line.strip()
            if line and not line.startswith('----------'):
                # Split by the first '#' to separate description
                parts = line.split('#', 1)
                data_part = parts[0].strip()
                
                # Extract key and value
                key_value = data_part.split()
                if len(key_value) >= 2:
                    key = key_value[0]
                    value = key_value[1]
                    
                    # Try to convert value to numeric if possible
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    
                    # Add to dictionary
                    stats_dict[key] = value
    
    return stats_dict

def load_data():
    df = dict()
    for benchmark in os.listdir("filtered_outputs"):
        df[benchmark] = dict() 
        for cpu in os.listdir("filtered_outputs/" + benchmark):
            df[benchmark][cpu.replace(".txt", "")] = parse_sim_stats("filtered_outputs/" + benchmark + "/" + cpu)
    return pd.DataFrame(data=df)

def create_graph(df, stat, cpus, name):
    benchmarks = ['Integer Sort', 'Spanning Forest', 'LRS', 'Convex Hull', 'Nbody']

    stats = [
        [df["integer_sort"][cpus[0]][stat], df["integer_sort"][cpus[1]][stat], df["integer_sort"][cpus[2]][stat]],
        [df["spanning_tree"][cpus[0]][stat], df["spanning_tree"][cpus[1]][stat], df["spanning_tree"][cpus[2]][stat]],
        [df["lrs"][cpus[0]][stat], df["lrs"][cpus[1]][stat], df["lrs"][cpus[2]][stat]],
        [df["convex_hull"][cpus[0]][stat], df["convex_hull"][cpus[1]][stat], df["convex_hull"][cpus[2]][stat]],
        [df["nbody"][cpus[0]][stat], df["nbody"][cpus[1]][stat], df["nbody"][cpus[2]][stat]]
    ]

    bar_width = 0.25
    x = np.arange(len(benchmarks))

    fig, ax = plt.subplots(figsize=(12, 7))

    rects1 = ax.bar(x - bar_width, [stat[0] for stat in stats], bar_width, label=cpus[0], color='#3498db')
    rects2 = ax.bar(x, [stat[1] for stat in stats], bar_width, label=cpus[1], color='#e74c3c')
    rects3 = ax.bar(x + bar_width, [stat[2] for stat in stats], bar_width, label=cpus[2], color='#2ecc71')

    ax.set_xlabel('Benchmarks', fontsize=12)
    ax.set_ylabel(stat, fontsize=12)
    ax.set_title('CPU Performance Comparison Across Benchmarks', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(benchmarks)
    ax.legend()

    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{round(height, 3)}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(rects1)
    add_labels(rects2)
    add_labels(rects3)

    plt.tight_layout()
    plt.savefig(f'graphs/{stat}_{name}.png')

if __name__ == "__main__":
    df = load_data()
    create_graph(df, "system.cpu.cpi", ["basic", "tagged_prefetcher", "stride_prefetcher"], "prefetch")