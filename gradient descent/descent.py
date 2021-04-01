import matplotlib.pyplot as plt
import math
import random

#E(w) = (w + 1)(w − 1)(w − 3)(w − 4)

def f(x):
    return (x+1.0)*(x-1.0)*(x-3.0)*(x-4.0)

def fp(x, a):
    return -a*(7+ 22*x - 21*(x*x)  + 4*(x*x*x))



range_ = []
f_ = []
target = 100000.0

for i in range(-2, 6):
    range_.append(i)
    f_.append(f(i))
    if(f(i) < target):
        target = f(i)

print("Min at " + str(target))
plt.plot(range_, f_)

#initialize w
w = random.randrange(-2, 6)
print("W initialized to " + str(w))
alpha = 1/40
#calculate adjustment with learning rate
last_update = 0
i = 0
while( f(w) > target):
    i+=1
    #print("w: " + str(w) + " f(w): " + str(f(w)))
    plt.scatter(w, f(w))
    plt.text(w, f(w), str(i))

    #calculate the update value
    error = target-f(w)
    update = (-alpha*(7.0+ 22.0*w - 21.0*(w*w)  + 4.0*(w*w*w)))
    if(update == last_update):
        w = random.randrange(-2, 6)
        print("w reinitalized to " + str(w))
    else:
        last_update = update
    #print("Updating w by " + str(update))
    w = w + update

    plt.scatter(w, f(w))
plt.text(w+.3, f(w)+.3, str(i+1))

plt.show()



