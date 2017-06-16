#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import glob, os


# paper data
values_paper = []
labels_paper = []
with open("paper.dat",'r') as f:
    for line in f:
        values_paper.append(float(str.split(line)[1]))
        labels_paper.append(str.split(line)[0])

# study data
values_study = []
error_high = []
error_low = []
with open("study.dat", 'r') as f:
    for line in f:
        line = str.split(line)
        values_study.append(float(line[1]))
        error_high.append(float(line[2]))
        error_low.append(float(line[3]))

reduce = 0

x = []
x_fit = []
y_fit = []
y = []
labels = []
errors = []
fig, ax = plt.subplots(1,1)

for i in range(0,len(values_study)):
    if labels_paper[i] == "R2220A":
        continue
    if values_study[i] != 0:
        if reduce and (labels_paper[i] == "F2196A" or labels_paper[i] == "F2200A" or labels_paper[i] == "N2198A"):
            continue
        x.append(values_study[i])
        y.append(values_paper[i])
        errors.append(error_high[i])
        labels.append(labels_paper[i])
        if values_paper[i] != 0:
            x_fit.append(values_study[i])
            y_fit.append(values_paper[i])
# correct overlaps


yerr = errors


m, b = np.polyfit(x_fit,y_fit,1)

x = [m*item + b for item in x]

# labeling

ax.annotate("*predicted value of R2220A = 2.456", xy=(2, 0.1))
for i in range(0,len(y)):

    y_coord = y[i]
    # if labels[i] == "R2220A":
        # labels[i] = "R2220A*"
        # y[i] = x[i]
        # print x[i]
        # y_coord = y[i]
        # ax.annotate("*predicted value of R2220A = 2.456", xy=(2,-0.8))
    # if labels[i] == "Q2222A":
    #     y_coord = y_coord - 0.1
    if labels[i] == "H2315A":
        y_coord = y_coord - 0.5
        ax.annotate(labels[i], xy=(y_coord + 0.04, x[i] + 0.15))
        continue
    ax.annotate(labels[i], xy=(y_coord +0.05,x[i]))

# First illustrate basic pyplot interface, using defaults where possible.
ax.errorbar(y, x, yerr=yerr, fmt='o')
# ax.scatter(y,x)
ax.plot(y, y, '-')
# ax.errorbar(x,y, fmt='o')
# ax.set_xticks(x)
# ax.set_yticks(y)
# plt.setp(ax.get_xticklabels(), fontsize=10, rotation='vertical')
ax.set_xlabel(u"experimental ΔΔG (kcal/mol)")
ax.set_ylabel(u"predicted ΔΔG (kcal/mol)")
plt.xlim(0,4)
# ax.scatter(range(1,len(norm_values_paper)+1), norm_values_paper,color='red')

# count = 0
# for error in errors:
#     ax.annotate(error, xy=(x[count]+0.2, error+norm_values[count]))
#     ax.annotate(norm_values[count], xy=(x[count]+0.2, norm_values[count]))
#     count += 1


plt.show()
