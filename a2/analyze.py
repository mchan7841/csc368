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
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{round(height, 3)}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    benchmarks = ['Integer Sort', 'Spanning Forest', 'LRS', 'Convex Hull', 'Nbody']

    stats = []
    for benchmark in ['integer_sort', 'spanning_tree', 'lrs', 'convex_hull', 'nbody']:
        benchmark_stats = []
        for cpu in cpus:
            benchmark_stats.append(df[benchmark][cpu][stat])
        stats.append(benchmark_stats)

    bar_width = 0.8 / len(cpus)
    x = np.arange(len(benchmarks))

    _, ax = plt.subplots(figsize=(12, 7))

    for i, cpu in enumerate(cpus):
        rects = ax.bar(x + i * bar_width - (len(cpus) - 1) * bar_width / 2, [stat[i] for stat in stats], bar_width, label=cpu)
        add_labels(rects)

    ax.set_xlabel('Benchmarks', fontsize=12)
    ax.set_ylabel(stat, fontsize=12)
    ax.set_title(f'{name} {stat.rsplit('.', 1)[-1]}', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(benchmarks)
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'graphs/{stat.rsplit('.', 1)[-1]}_{name}.png')


if __name__ == "__main__":
    df = load_data()
    
    ## Prefetcher graphs
    l1d_metrics = [
        "system.cpu.l1d.prefetcher.demandMshrMisses",
        "system.cpu.l1d.prefetcher.pfIssued",
        "system.cpu.l1d.prefetcher.pfUnused",
        "system.cpu.l1d.prefetcher.pfUseful",
        "system.cpu.l1d.prefetcher.pfUsefulButMiss",
        "system.cpu.l1d.prefetcher.accuracy",
        "system.cpu.l1d.prefetcher.coverage",
        "system.cpu.l1d.prefetcher.pfHitInCache",
        "system.cpu.l1d.prefetcher.pfHitInMSHR",
        "system.cpu.l1d.prefetcher.pfHitInWB",
        "system.cpu.l1d.prefetcher.pfLate",
        "system.cpu.l1d.prefetcher.pfIdentified",
        "system.cpu.l1d.prefetcher.pfBufferHit",
        "system.cpu.l1d.prefetcher.pfInCache",
        "system.cpu.l1d.prefetcher.pfRemovedDemand",
        "system.cpu.l1d.prefetcher.pfRemovedFull",
    ]
    l1i_metrics = [
        "system.cpu.l1i.prefetcher.demandMshrMisses",
        "system.cpu.l1i.prefetcher.pfIssued",
        "system.cpu.l1i.prefetcher.pfUseful",
        "system.cpu.l1i.prefetcher.pfUsefulButMiss",
        "system.cpu.l1i.prefetcher.accuracy",
        "system.cpu.l1i.prefetcher.coverage",
        "system.cpu.l1i.prefetcher.pfHitInCache",
        "system.cpu.l1i.prefetcher.pfHitInMSHR",
        "system.cpu.l1i.prefetcher.pfHitInWB",
        "system.cpu.l1i.prefetcher.pfLate",
        "system.cpu.l1i.prefetcher.pfIdentified",
        "system.cpu.l1i.prefetcher.pfBufferHit",
        "system.cpu.l1i.prefetcher.pfInCache",
        "system.cpu.l1i.prefetcher.pfRemovedDemand",
        "system.cpu.l1i.prefetcher.pfRemovedFull"
    ]
    for metric in l1i_metrics:
        create_graph(df, metric, ["tagged_prefetcher_l1i", "stride_prefetcher_l1i"], "l1i_prefetch")
    for metric in l1d_metrics:
        create_graph(df, metric, ["tagged_prefetcher_l1d", "stride_prefetcher_l1d"], "l1d_prefetch")