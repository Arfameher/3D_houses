import csv                              # To write a csv file for bounds.
import pandas as pd
import rasterio                         # We can read in a GeoTiff file into a dataset using rasterio module.

def bounds():

    """Create a csv file that reads each tif file and stores the bounds of 
        each one of them as a rown in the .csv file
    """

    with open('bounds.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["File_number", "Bounds:Left", "Bounds:Bottom" , "Bounds:Right" , "Bounds:Top"])
    
    for i in range(1,44):
        if i < 10:
            df = rasterio.open(f"DSM/DSM_k0{i}.tif")
            
            with open ("bounds.csv", 'a', newline='') as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow([i , df.bounds.left , df.bounds.bottom , df.bounds.right , df.bounds.top])
            
        else:
            df = rasterio.open(f"DSM/DSM_k{i}.tif")
            
            with open ("bounds.csv", 'a', newline='') as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow([i , df.bounds.left , df.bounds.bottom , df.bounds.right , df.bounds.top])

bounds()
df = pd.read_csv("bounds.csv")
bounds