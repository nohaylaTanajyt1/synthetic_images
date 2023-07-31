#!/bin/bash
#SBATCH --job-name=runFarm
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --gres=gpu:1
#SBATCH --mem-per-gpu=8G
#SBATCH --time=6:3:00:00
#SBATCH --output=logrunFarmv1_%A_%a.txt
#SBATCH --error=errorrunFarmv1_%A_%a.txt ##%A and %a are Slurm job ID and array task ID 



function run_blender() {
    i=$1
    k=$2
    blender --background --python /baie/nfs-cluster-1/data1/raid1/homedirs/nohayla.tanajyt/Stage/ScenesAssets/park/scripts/runFarm_${i}_${k}.py
}

# Run the blender command 10 times with different i and k values
run_blender 1 a
run_blender 1 b
run_blender 2 a
run_blender 2 b
run_blender 3 a
run_blender 3 b
run_blender 4 a
run_blender 4 b
run_blender 5 a
run_blender 5 b
