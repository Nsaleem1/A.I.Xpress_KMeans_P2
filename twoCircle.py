import random
import math

nodeNum = 64
locations = []

# two circle centers
for center_x in [0, 5]:  
    for _ in range(nodeNum):
        # random angle around circle
        angle = random.uniform(0, 2*math.pi)  
        x = center_x + math.cos(angle)
        y = 0 + math.sin(angle)
        locations.append((x, y))

with open("twoUnitCircles.txt", "w") as file:
    for x, y in locations:
        file.write(f"{x}\t{y}\n")

print(f"Success, twoUnitCircles.txt now contains {2*nodeNum} coordinates on two unit circles!")