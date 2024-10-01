import numpy as np
from matplotlib import pyplot as plt
import os

log_file = "./log.rhoSimpleFoam"

# Data extraction

Ux_res = np.array([])
Uy_res = np.array([])
Uz_res = np.array([])
p_res = np.array([])
k_res = np.array([])
eps_res = np.array([])
e_res = np.array([])

continuity_sum_local = np.array([])
continuity_global = np.array([])
continuity_cumulative = np.array([])

with open(log_file, 'r') as file:
    for line in file:
        if 'End' in line:
            stop_updates = True

        if 'Solving for Ux,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            Ux_res = np.append(Ux_res, float(var_aux[0]))

        if 'Solving for Uy,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            Uy_res = np.append(Uy_res, float(var_aux[0]))
        if 'Solving for Uz,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            Uz_res = np.append(Uz_res, float(var_aux[0]))

        if 'Solving for p,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            p_res = np.append(p_res, float(var_aux[0]))

        if 'Solving for k,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            k_res = np.append(k_res, float(var_aux[0]))
            
        if 'Solving for epsilon,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            eps_res = np.append(eps_res, float(var_aux[0]))
            
        if 'Solving for e,' in line:
            var_aux = line.split()
            var_aux = var_aux[11].split(',')
            e_res = np.append(e_res, float(var_aux[0]))

        if 'time step continuity errors' in line:
            var_aux = line.split()
            var_aux1 = var_aux[8].split(',')
            var_aux2 = var_aux[11].split(',')
            var_aux3 = var_aux[14].split(',')
            continuity_sum_local = np.append(continuity_sum_local, float(var_aux1[0]))
            continuity_global = np.append(continuity_global, float(var_aux2[0]))
            continuity_cumulative = np.append(continuity_cumulative, float(var_aux3[0]))


it = np.arange(1, len(p_res)+1, 1)

# Residuals plot
fig, ax = plt.subplots(figsize=(12,6))

if len(Ux_res) > 0:
    ax.plot(it, Ux_res, label = 'Ux')
if len(Uy_res) > 0:
    ax.plot(it, Uy_res, label = 'Uy')
if len(Uz_res) > 0:
    ax.plot(it, Uz_res, label = 'Uz')
if len(p_res) > 0:
    ax.plot(it, p_res, label = 'p')
if len(k_res) > 0:
    ax.plot(it, k_res, label = 'k')
if len(eps_res) > 0:
    ax.plot(it, eps_res, label = 'epsilon')
if len(e_res) > 0:
    ax.plot(it, e_res, label = 'e')
if len(continuity_sum_local) > 0:
    ax.plot(it, continuity_sum_local, label = 'continuity')

ax.set_title("Residuals")
ax.set_xlabel("Iterations")
ax.set_ylabel("Residuals")
ax.set_yscale("log")
ax.legend()
ax.grid(True, linestyle='-', alpha=0.5)

plt.tight_layout()
#plt.show()

output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "residuals.png")
fig.savefig(output_path, dpi=300, bbox_inches='tight')

# Continuity plot
fig, ax = plt.subplots(figsize=(12,6))

ax.plot(it, continuity_sum_local, label='Sum Local')
ax.plot(it, continuity_global, label='Global')
ax.plot(it, continuity_cumulative, label='Cumulative')

ax.set_title("Continuity")
ax.set_xlabel("Iterations")
ax.set_ylabel("Residuals")
ax.legend()
ax.grid(True, linestyle='-', alpha=0.5)

plt.tight_layout()
#plt.show()
output_path = os.path.join(output_dir, "continuity.png")
fig.savefig(output_path, dpi=300, bbox_inches='tight')



