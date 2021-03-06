'''
This program takes inputs from the user, calculates the Reynolds number, uses the Reynolds and Prandtl numbers 
to determine all possible correlations based on the conditions, and calculates h (the convection heat transfer coefficient) for every
applicable cylindrical correlation.
'''
import numpy as np
import sys
import scipy.optimize as opt

#Load data from Tables 7.2 & 7.4 into arrays

T72=np.loadtxt("Table 7.2",delimiter=",")
T74=np.loadtxt("Table 7.4",delimiter=",")

#Inputs from user

correct=False
while not (correct):
    corr_type=input('What is the geometry of the correlation? e.g. cylinder: ')
    if corr_type == "cylinder":
        D=float(input("Enter the diameter of the tube (m): "))
        V=float(input("Enter the velocity of the fluid (m/s): "))
        nu=float(input("Enter the kinematic viscosity constant (m^2/s): "))
        Pr=float(input("Enter the Prandtl number: "))
        k=float(input("Enter the thermal conductivity (W/m*K): "))
        correct=True
    else:
        print("You've entered an invalid correlation. This program is terminating.")
        sys.exit()
print("\n")

#Part 1

#Correlation 7.52

Re_D=(V*D)/nu
print("For correlation 7.52 the Reynolds number is: " + str(Re_D))

for i in range(len(T72)):
    if Re_D > T72[i,0] and Re_D < T72[i,1]:
        C = float(T72[i,2])
        m = float(T72[i,3])
        Nu_D = C * Re_D**m * Pr**(1/3)
        h1 = Nu_D*k/D
        print("Correlation 7.52 fits and h = %9.5f " %h1 + " W/m^2*K")
print("\n")

#Correlation 7.53

Re_D=(V*D)/nu
print("For correlation 7.53 the Reynolds number is: " + str(Re_D))

for i in range(len(T74)):
    if Re_D > T74[i,0] and Re_D < T74[i,1]:
        C = float(T74[i,2])
        m = float(T74[i,3])
        Pr_s = float(input("What is the value of Pr_s?: "))
        if Pr < 10:
            n = .37
        elif Pr >= 10:
            n = .36
        Nu_D = C * Re_D**m * Pr**n * (Pr/Pr_s)**(1/4)
        h2 = Nu_D*k/D
        print("Correlation 7.53 fits and h = %9.5f " %h2 + " W/m^2*K")
print("\n")

#Correlation 7.54

Pr=float(input("Enter the Prandtl number evaluated at the film temperature: "))
nu=float(input("Enter the kinematic viscosity constant evaluated at the film temperature (m^2/s): "))
k=float(input("Enter the thermal conductivity evaluated at the film temperature (W/m*K): "))

Re_D=(V*D)/nu
print("For correlation 7.54 the Reynolds number is: " + str(Re_D))

if Re_D * Pr >= .2:
    Nu_D = 0.3 + (0.62 * Re_D**(1/2) * Pr**(1/3)) * (( 1 + (0.4 / Pr)**(2/3))**(-1/4)) * (1 + (Re_D / 282000)**(5/8))**(4/5)
    h3 = Nu_D*k/D
    print("Correlation 7.54 fits and h = %9.5f " %h3 + " W/m^2*K")

print("\n")
print("This is the end of the initial program. We hope you've found it useful!")
print("\n")

#Part 2

# Trying to use fsolve to find the unknown variable. This was an addition to our original plan and is not yet complete.

variables = ['Pr_s', 'Nu_D', 'h', 'V', 'D', 'nu', 'k']
values = ['Pr_s', 'Nu_D', 'h', 'V', 'D', 'nu', 'k']

unknown = input("Which variable are we solving for? (Pr_s, Nu_D, h, V, D, nu, k): ")

for i in range(len(values)):
    if values[i] == unknown:
        position = values.index(values[i])

print("All values assume SI units. Please enter the values only, and not the units.")

for i in range(len(values)):
    if i == position:
        values[i] = True
    else:
        values[i] = float(input("Please enter the value for " + values[i] + ": "))

Pr_s = values[0]
Nu_D = values[1]
h = values[2]
V = values[3]
D = values[4]
nu = values[5]
k = values[6]

print(variables[0:7])
print(values[0:7])

# Get Re_D and Pr

Pr = float(input("Please enter the Prandtl number (Pr): "))
if V == True or D == True or nu == True:
    Re_D = float(input("Please enter the Reynolds number (Re_D): "))
else:
    Re_D = (V*D)/nu


guesses = np.zeros(len(values))

# NOTE: If Pr_s is the unknown then this correlation won't work. In that case we'll have to force it to use correlation 7.5.3.

def f(guesses,values):
    if Re_D > T72[i,0] and Re_D < T72[i,1]:
        C = float(T72[i,2])
        m = float(T72[i,3])
        return (Nu_D - C * Re_D**m * Pr**(1/3), h - Nu_D*k/D)
    else:
        print("I think this is working...")

ans = opt.fsolve(f,guesses,args=(values))
print(ans)




        
'''
--------------------------------------------------------------------------------
import numpy as np
import sys
import scipy.optimize as opt

#Load data from Tables 7.2 & 7.4 into arrays

T72=np.loadtxt("Table 7.2.txt",delimiter=",")
T74=np.loadtxt("Table 7.4.txt",delimiter=",")

# Trying to use fsolve per Logan's instruction

variables = ['Pr_s', 'Nu_D', 'h', 'V', 'D', 'nu', 'k']
values = ['Pr_s', 'Nu_D', 'h', 'V', 'D', 'nu', 'k']

unknown = input("Which variable are we solving for? (Pr_s, Nu_D, h, V, D, nu, k): ")
#print(unknown)

for i in range(len(values)):
    if values[i] == unknown:
        position = values.index(values[i])
#        print(position)

print("All values must be entered in SI units.")

for i in range(len(values)):
    if i == position:
        values[i] = True
    else:
        values[i] = float(input("Please enter the value for " + values[i] + ": "))

Pr_s = values[0]
Nu_D = values[1]
h = values[2]
V = values[3]
D = values[4]
nu = values[5]
k = values[6]

print(variables[0:7])
print(values[0:7])
#print(Pr_s)
#print(Nu_D)
#print(h)
#print(V)
#print(D)
#print(nu)
#print(k)

# Get Re_D and Pr

Pr = float(input("Please enter the Prandtl number (Pr): "))
if V == True or D == True or nu == True:
    Re_D = float(input("Please enter the Reynolds number (Re_D): "))
else:
    Re_D = (V*D)/nu

print(Re_D)
print(Pr)



guesses = np.zeros(len(values))
print(guesses)

# NOTE: If Pr_s is the unknown then this correlation won't work. In that case we'll have to force it to use correlation 7.5.3.

def f(guesses,values):
    if Re_D > T72[i,0] and Re_D < T72[i,1]:
        C = float(T72[i,2])
        m = float(T72[i,3])
        return (Nu_D - C * Re_D**m * Pr**(1/3), h - Nu_D*k/D)
    else:
        print("I think this is working...")

ans = opt.fsolve(f,guesses,args=(values))
print(ans)

        

#Inputs from user
correct=False
while not (correct):
    corr_type=input('What is the geometry of the correlation? e.g. cylinder: ')
    if corr_type == "cylinder":
        D=float(input("Enter the diameter of the tube (m): "))
        V=float(input("Enter the velocity of the fluid (m/s): "))
        nu=float(input("Enter the kinematic viscosity constant (m^2/s): "))
        Pr=float(input("Enter the Prandtl number: "))
        k=float(input("Enter thermal conductivity (W/m*K): "))
        correct=True
    else:
        print("You've entered an invalid correlation. This program is terminating.")
        sys.exit()

#Determine appropriate correlation(s) from conditions

#Correlation 7.52

Re_D=(V*D)/nu
print(Re_D)

for i in range(len(T72)):
    if Re_D > T72[i,0] and Re_D < T72[i,1]:
        C = float(T72[i,2])
        m = float(T72[i,3])
        Nu_D = C * Re_D**m * Pr**(1/3)
        h1 = Nu_D*k/D
        print("Correlation 7.52 fits and h = %9.5f " %h1 + " W/m^2*K")
        
print(C)
print(m)
print(Nu_D)
print(h1)

#Correlation 7.53

Re_D=(V*D)/nu
print(Re_D)

for i in range(len(T74)):
    if Re_D > T74[i,0] and Re_D < T74[i,1]:
        C = float(T74[i,2])
        m = float(T74[i,3])
        Pr_s = float(input("What is the value of Pr_s?: "))
        if Pr < 10:
            n = .37
        elif Pr >= 10:
            n = .36
        print(n)
        Nu_D = C * Re_D**m * Pr**n * (Pr/Pr_s)**(1/4)
        h2 = Nu_D*k/D
        print("Correlation 7.53 fits and h = %9.5f " %h2 + " W/m^2*K")
        
print(C)
print(m)
print(Nu_D)
print(h2)

#Correlation 7.54

Pr=float(input("Enter the Prandtl number evaluated at Tf: "))
nu=float(input("Enter the kinematic viscosity constant evaluated at Tf (m^2/s): "))
k=float(input("Enter thermal conductivity evaluated at Tf (W/m*K): "))

Re_D=(V*D)/nu
print(Re_D)

if Re_D * Pr >= .2:
    Nu_D = 0.3 + (0.62 * Re_D**(1/2) * Pr**(1/3)) * (( 1 + (0.4 / Pr)**(2/3))**(-1/4)) * (1 + (Re_D / 282000)**(5/8))**(4/5)
    h3 = Nu_D*k/D
    print("Correlation 7.54 fits and h = %9.5f " %h3 + " W/m^2*K")
                  
print(C)
print(m)
print(Nu_D)
print(h3)


#Here is what I've done so far to add classes

class Correlation:
    def __init__(self,name,geometry):
        self.name = name
        self.geometry = geometry
        self.conditions = []
        
    def addConditions(self,condition):
        self.conditions.append(condition)
        

c52 = Correlation('7.52','cylinder')
c53 = Correlation('7.53','cylinder')
c54 = Correlation('7.54','cylinder')

c52.addConditions(T72)
c53.addConditions(T74)

print (c53.conditions[2,2])
'''
