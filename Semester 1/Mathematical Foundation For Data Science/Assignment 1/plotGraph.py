import matplotlib.pyplot as plt
import math

dictionaryFEActual = {}
with open("forwardElimination.txt") as f:
    for line in f:
       (key, val) = line.split()
       dictionaryFEActual[int(key)] = float(val)

dictionaryFETheoretical = {}
with open("theoreticalForwardElimination.txt") as f:
    for line in f:
       (key, val) = line.split()
       dictionaryFETheoretical[int(key)] = float(val)

dictionaryBS = {}
with open("backSubstitution.txt") as f:
    for line in f:
       (key, val) = line.split()
       dictionaryBS[int(key)] = float(val)

# x axis values
x = [
    math.log10(1000),
    math.log10(2000),
    math.log10(3000),
    math.log10(4000),
    math.log10(5000),
    math.log10(6000),
    math.log10(7000),
    math.log10(8000),
    math.log10(9000),
    math.log10(10000)
]

print(dictionaryFEActual)


# corresponding y axis values
yFEActual = [
    math.log10(dictionaryFEActual[1000]),
    math.log10(dictionaryFEActual[2000]),
    math.log10(dictionaryFEActual[3000]),
    math.log10(dictionaryFEActual[4000]),
    math.log10(dictionaryFEActual[5000]),
    math.log10(dictionaryFEActual[6000]),
    math.log10(dictionaryFEActual[7000]),
    math.log10(dictionaryFEActual[8000]),
    math.log10(dictionaryFEActual[9000]),
    math.log10(dictionaryFEActual[10000])
    # math.log10(212),
    # math.log10(2144),
    # math.log10(7357),
    # math.log10(17552),
    # math.log10(33541),
    # math.log10(57401),
    # math.log10(91063),
    # math.log10(135565),
    # math.log10(189467),
    # math.log10(261535)
]

yFETheoretical = [
    math.log10(dictionaryFETheoretical[1000]),
    math.log10(dictionaryFETheoretical[2000]),
    math.log10(dictionaryFETheoretical[3000]),
    math.log10(dictionaryFETheoretical[4000]),
    math.log10(dictionaryFETheoretical[5000]),
    math.log10(dictionaryFETheoretical[6000]),
    math.log10(dictionaryFETheoretical[7000]),
    math.log10(dictionaryFETheoretical[8000]),
    math.log10(dictionaryFETheoretical[9000]),
    math.log10(dictionaryFETheoretical[10000])
    # math.log10(211.175),
    # math.log10(1690.03),
    # math.log10(5704.57),
    # math.log10(13522.8),
    # math.log10(26412.7),
    # math.log10(45642.3),
    # math.log10(72479.6),
    # math.log10(108193),
    # math.log10(154049),
    # math.log10(211317)
]

yBS = [
    math.log10(dictionaryBS[1000]),
    math.log10(dictionaryBS[2000]),
    math.log10(dictionaryBS[3000]),
    math.log10(dictionaryBS[4000]),
    math.log10(dictionaryBS[5000]),
    math.log10(dictionaryBS[6000]),
    math.log10(dictionaryBS[7000]),
    math.log10(dictionaryBS[8000]),
    math.log10(dictionaryBS[9000]),
    math.log10(dictionaryBS[10000])
    # math.log10(1),
    # math.log10(4),
    # math.log10(6),
    # math.log10(14),
    # math.log10(16),
    # math.log10(29),
    # math.log10(39),
    # math.log10(43),
    # math.log10(55),
    # math.log10(66)
]

 
#  Plot for Forward Elimination
plt.plot(x, yFEActual, color='green', linestyle='dashed', linewidth = 2,
         marker='o', markerfacecolor='blue', markersize=5)

plt.xlim(3, 4)
 

plt.xlabel('log (N) where N is input size of matrix \n 1000 <= N <= 10000')
plt.ylabel('log (time taken in ms)')

plt.title('Forward Elimination Time Taken')
plt.show()

# Plot for Backward Substitution
plt.plot(x, yBS, color='green', linestyle='dashed', linewidth = 2,
         marker='o', markerfacecolor='blue', markersize=5)

plt.xlim(3, 4)
 

plt.xlabel('log (N) where N is input size of matrix \n 1000 <= N <= 10000')
plt.ylabel('log (time taken in ms)')

plt.title('Back Substitution Time Taken')
plt.show()

# Plot for
plt.plot(x, yFEActual, color='green', linestyle='dashed', linewidth = 2,
         marker='o', markerfacecolor='blue', markersize=5, label='Actual Forward Elimination')
plt.plot(x, yFETheoretical, color='red', linestyle='dashed', linewidth = 2,
         marker='o', markerfacecolor='blue', markersize=5, label='Theoretical Forward Elimination')

plt.xlim(3, 4)
 

plt.xlabel('log (N) where N is input size of matrix \n 1000 <= N <= 10000')
plt.ylabel('log (time taken in ms)')

plt.title('Forward Elimination Time Taken Actual vs Theoretical')
plt.legend()
plt.show()