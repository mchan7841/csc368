import subprocess
import os
import shutil
import glob

DATA = [200000, [2000, 20000], 1000, 5000, 500]

def generate_int_sort(arg):
    cmd = [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/sequenceData/randomSeq",
        "-t", "int", str(arg), f"data/random_seq{arg}"
    ]
    subprocess.run(cmd)

def generate_spanning_forest(arg1, arg2):
    cmd = [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/graphData/randLocalGraph",
        "-d", "3", "-m", str(arg1), str(arg2), f"data/random_graph{arg1}"
    ]
    subprocess.run(cmd)

def generate_lrs(arg):
    cmd = f"tr -dc 'a-z' </dev/urandom | head -c {arg} > data/random_string{arg}"
    subprocess.run(cmd, shell=True)

def generate_convex_hull(arg):
    cmd = [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/geometryData/randPoints",
        "-s", "-d", "2", str(arg), f"data/random_points_2d_{arg}"
    ]
    subprocess.run(cmd)

def generate_nbody(arg):
    cmd = [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/geometryData/randPoints",
        "-S", "-d", "3", str(arg), f"data/random_points_3d_{arg}"
    ]
    subprocess.run(cmd)


def run_int_sort(arg, type, cpu):
    cmd = [
        "/u/csc368h/winter/pub/bin/gem5.opt",
        "-d", f"outputs/integer_sort/{type}",
        cpu,
        "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/integerSort/parallelRadixSort/isort",
        "--binary_args", f"data/random_seq{arg}"
    ]
    subprocess.run(cmd)

def run_sf(arg, type, cpu):
    cmd = [
        "/u/csc368h/winter/pub/bin/gem5.opt",
        "-d", f"outputs/spanning_tree/{type}",
        cpu,
        "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/spanningForest/ndST/ST",
        "--binary_args", f"data/random_graph{arg}"
    ]
    subprocess.run(cmd)

def run_lrs(arg, type, cpu):
    cmd = [
        "/u/csc368h/winter/pub/bin/gem5.opt",
        "-d", f"outputs/lrs/{type}",
        cpu,
        "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/longestRepeatedSubstring/doubling/lrs",
        "--binary_args", f"data/random_string{arg}"
    ]
    subprocess.run(cmd)

def run_convex_hull(arg, type, cpu):
    cmd = [
        "/u/csc368h/winter/pub/bin/gem5.opt",
        "-d", f"outputs/convex_hull/{type}",
        cpu,
        "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/convexHull/quickHull/hull",
        "--binary_args", f"data/random_points_2d_{arg}"
    ]
    subprocess.run(cmd)

def run_nbody(arg, type, cpu):
    cmd = [
        "/u/csc368h/winter/pub/bin/gem5.opt",
        "-d", f"outputs/nbody/{type}",
        cpu,
        "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/nBody/parallelCK/nbody",
        "--binary_args", f"data/random_points_3d_{arg}"
    ]
    subprocess.run(cmd)


def setup_data(data):
    generate_int_sort(data[0])
    generate_spanning_forest(data[1][0], data[1][1])
    generate_lrs(data[2])
    generate_convex_hull(data[3])
    generate_nbody(data[4])

def run_simulation(data, type, cpu):
    run_int_sort(data[0], type, cpu)
    run_sf(data[1][0], type, cpu)
    run_lrs(data[2], type, cpu)
    run_convex_hull(data[3], type, cpu)
    run_nbody(data[4], type, cpu)

def split_stats(input_dir, output_dir):
    for file in glob.glob(os.path.join(input_dir, "**/stats.txt"), recursive=True):
        parent_dir = os.path.basename(os.path.dirname(os.path.dirname(file)))
        subdir = os.path.basename(os.path.dirname(file))
        
        interest_dir = os.path.join(output_dir, parent_dir)
        os.makedirs(interest_dir, exist_ok=True)
        
        interest_file = os.path.join(interest_dir, f"{subdir}.txt")
        
        with open(file, "r") as f, open(interest_file, "w") as out_f:
            section = 0
            for line in f:
                if "---------- Begin Simulation Statistics ----------" in line:
                    section += 1
                elif "---------- End Simulation Statistics   ----------" in line:
                    continue
                if section == 2:
                    out_f.write(line)
        
        print(f"Processed: {file} → {interest_file}")





def run_all_simulations():
    # Generate data if needed
    # setup_data(DATA)

    # Baseline
    # run_simulation(DATA, "basic", "basic_cpu.py")

    # Prefetchers
    # run_simulation(DATA, "stride_prefetcher_l1i", "stride_prefetcher_l1i.py")
    # run_simulation(DATA, "stride_prefetcher_l1d", "stride_prefetcher_l1d.py")
    # run_simulation(DATA, "tagged_prefetcher_l1i", "tagged_prefetcher_l1i.py")
    # run_simulation(DATA, "tagged_prefetcher_l1d", "tagged_prefetcher_l1d.py")

    # Branch predictors
    # run_simulation(DATA, "local_predictor", "local_predictor.py")
    # run_simulation(DATA, "tournament_predictor", "tournament_predictor.py")

    # Isolate region of interest stats
    shutil.rmtree("filtered_outputs", ignore_errors=True)
    split_stats("outputs", "filtered_outputs")

if __name__ == "__main__":
    run_all_simulations()