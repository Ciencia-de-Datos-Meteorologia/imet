# import matplotlib.pyplot as plt
# import numpy as np

# # fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(3.5, 2.5),
# #                         layout="constrained")
# # # for each Axes, add an artist, in this case a nice label in the middle...
# # for row in range(2):
# #     for col in range(2):
# #         axs[row, col].annotate(f'axs[{row}, {col}]', (0.5, 0.5),
# #                             transform=axs[row, col].transAxes,
# #                             ha='center', va='center', fontsize=18,
# #                             color='darkgrey')
# # fig.suptitle('plt.subplots()')

# # plt.show()

# fig, ax = plt.subplots(figsize=(4, 3))
# np.random.seed(19680801)
# t = np.arange(100)
# x = np.cumsum(np.random.randn(100))
# lines = ax.plot(t, x)

# plt.show()
import matplotlib.pyplot as plt
import print_names

#Create a figure and an axis
places = [["lugar_1", 0.2, 0.8, "Etiqueta 1"],["lugar_2", 0.5, 0.5, "Etiqueta 2"],["lugar_3", 0.7, 0.3, "Etiqueta 3"]]

fig, ax = plt.subplots()  
print_names.print_names(places, ax, color='blue')  # Colocar las etiquetas en el gráfico
plt.show()  # Mostrar el gráfico