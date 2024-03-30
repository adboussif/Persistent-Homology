import pandas as pd
from scipy.stats import ks_2samp

# Charger les distances Ras-Bebz
ras_bebz_df = pd.read_csv('/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/all_Ras.csv')
distances_ras_bebz = ras_bebz_df['Distance'].values

# Charger les distances Ras-Ras
ras_ras_df = pd.read_csv('/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/Ras_Ras.csv')
distances_ras_ras = ras_ras_df['Distance'].values

# Exécution du test de Kolmogorov-Smirnov
ks_statistic, p_value = ks_2samp(distances_ras_bebz, distances_ras_ras)

print(f"Statistique KS: {ks_statistic}")
print(f"P-value: {p_value}")
