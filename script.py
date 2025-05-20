import sys
import csv

def main():
    print("Nuclear Physics Coefficient Request")
    while True:
        print("Please input the number of what type of data you are requesting")
        print("1 - Total Attenuation Coefficient")
        input1 = input()
        if input1 == "1":
            total_attenuation_coefficient()
            break

def total_attenuation_coefficient():
    print("Please input the element abbreviation you are requesting")
    input2 = input()
    print("Opening " + input2 + ".csv")
    try:
        with open('attenuation/' + input2 + '.csv', 'r') as file:
            print("File opened successfully!")
    except FileNotFoundError:
        print("Error: Invalid file name.")
        sys.exit()
    print("Please input the energy value you are requesting")
    input3 = input()
    try:
        _ = float(input3)
    except ValueError:
        print("Error: Non-number energy input.")
        sys.exit()
    closest_low = 0.0
    closest_high = float('inf')
    low_coeff = 0.0
    high_coeff = float('inf')
    with open('attenuation/' + input2 + '.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            energy = float(row["Photon Energy"])
            if energy == float(input3):
                print("Your total attenuation coefficient: ", end='')
                print(row["Total Attenuation with Coherent Scattering"])
                sys.exit()
            elif energy < float(input3) and energy > float(closest_low):
                closest_low = energy
                low_coeff = float(row["Total Attenuation with Coherent Scattering"])
            elif energy > float(input3) and energy < float(closest_high):
                closest_high = energy
                high_coeff = float(row["Total Attenuation with Coherent Scattering"])
    if closest_low == 0.0 or closest_high == float('inf'):
        print("Cannot calculate total attenuation coefficient")
        sys.exit()
    difference = closest_high - closest_low
    percentage = (float(input3) - closest_low) / difference
    coefficient = low_coeff + percentage * (high_coeff - low_coeff)
    print("Your total attenuation coefficient: " + str(coefficient))

main()