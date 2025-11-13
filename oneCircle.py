import random
import math

nodeNum = 50  # number of points
locations = []

for _ in range(nodeNum):
    angle = random.uniform(0, 2*math.pi)  # pick a random angle
    x = math.cos(angle)  # x-coordinate on unit circle
    y = math.sin(angle)  # y-coordinate on unit circle
    locations.append((x, y))

with open("oneCircle.txt", "w") as file:
    for x, y in locations:
        file.write(f"{x}\t{y}\n")

print(f"Success, oneCircle.txt now contains {nodeNum} coordinates on a unit circle perimeter!")