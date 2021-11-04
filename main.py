import matplotlib
import requests     
import rasterio                         # We can read in a GeoTiff file into a dataset using rasterio module       
import rioxarray                        # To clip the area of the house from a tiff file.
import json
import csv                              # To write a csv file for bounds.
import numpy as np                   
import pandas as pd
from matplotlib import pyplot as plt    # Plotting the CHM model and to get the final 3D house representation.
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import plotly.graph_objects as go
from matplotlib import animation
from shapely import geometry            # To get the polygon of the address

import time                             # To calculate the total time taken for the program to run
start = time.time()                     



def details(address: str):
    req = requests.get(f"https://loc.geopunt.be/v4/Location?q={address}").json()
    info = {'address' : address, 
                'x_value' : req['LocationResult'][0]['Location']['X_Lambert72'],
                'y_value' : req['LocationResult'][0]['Location']['Y_Lambert72'],
                'street' : req['LocationResult'][0]['Thoroughfarename'],
                'house_number' : req['LocationResult'][0]['Housenumber'], 
                'postcode': req['LocationResult'][0]['Zipcode'], 
                'municipality' : req['LocationResult'][0]['Municipality']}
    
    detail = requests.get("https://api.basisregisters.vlaanderen.be/v1/adresmatch", 
                          params={"postcode": info['postcode'], 
                                  "straatnaam": info['street'],
                                  "huisnummer": info['house_number']}).json()
    building = requests.get(detail['adresMatches'][0]['adresseerbareObjecten'][0]['detail']).json()
    build = requests.get(building['gebouw']['detail']).json()
    info['polygon'] = [build['geometriePolygoon']['polygon']['coordinates']]
    
    return info


def check_DSM_DTM(x,y):
    """ 
    To check which tiff file contains the address location.
    check which tif contains the location to identify the DSM/DTM file.
    """
    bounds = pd.read_csv("bounds.csv")
    for i in range(0,43):
        if (x >= bounds.loc[i, 'Bounds:Left'] and x <= bounds.loc[i,'Bounds:Right']) and \
            (y >= bounds.loc[i, 'Bounds:Bottom'] and y <= bounds.loc[i, 'Bounds:Top']):

            global res
            res = i + 1
            global resultDTM
            if i < 9:
                print(f"The house is in this tif --> DSM_k0{i+1}.tif")
                resultDTM = f"DTM/DTM_k0{res}.tif"
                return f"DSM/DSM_k0{i+1}.tif"


            else:
                print(f"The house is in this tif --> DSM_k{i+1}.tif")
                resultDTM = f"DTM/DTM_k{res}.tif"
                return f"DSM/DSM_k{i+1}.tif"

# To get the polygon shape from the given coordinates.
def plot_polygon(polygon):

    poly = geometry.Polygon(polygon[0][0])
    print(poly)                           


# To calculate the chm using the DTM and DSM and then plot the 3D model.
def CHM(polygon, result, resultDTM):

    clipped = [ {'type': 'Polygon','coordinates': polygon[0]}] # Defining the coordinates of the polygon.

    dsm = rioxarray.open_rasterio(result, masked =True).rio.clip(clipped, from_disk=True)
    global dsm_arr
    dsm_arr = dsm.values
    dtm = rioxarray.open_rasterio(resultDTM,masked=True).rio.clip(clipped, from_disk=True)
    global dtm_arr
    dtm_arr = dtm.values
    clipped_chm = dsm - dtm # To get the chm of the house.

    chm = clipped_chm[0]

    chm1 = np.where(np.isnan(chm), 0, chm) # Filling all the nan values with 0.

    chm_ = np.pad(chm1, pad_width = 1, mode = "constant", constant_values = 0) # Giving it a padding of 0's around the border to get the image.

    rchm = np.fliplr(chm_) # Invert the house model

    return rchm

def plot3d_plotly(dsm_arr, dtm_arr):
    dsm_arr = dsm_arr.squeeze()
    dtm_arr = dtm_arr.squeeze()
    np.where_are_NaNs = np.isnan(dsm_arr)
    dsm_arr[np.where_are_NaNs] = 0
        
    np.where_are_NaNs = np.isnan(dtm_arr)
    dtm_arr[np.where_are_NaNs] = 0
        
    dsm_arr = np.pad(dsm_arr,[(1, ), (1, )], mode='constant')
    dtm_arr = np.pad(dtm_arr,[(1, ), (1, )], mode='constant')

    chm= dsm_arr + dtm_arr
    N = chm.shape[0]
    M = chm.shape[1] 
        
    clipped = pd.DataFrame(chm)
    fig = go.Figure(data=[go.Surface(z=clipped)])
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                        highlightcolor="limegreen", project_z=True))
    fig.update_layout(title=address, autosize=True)

    fig.update_layout(scene = dict(
                        xaxis_title='Breath of building(sq.m)',
                        yaxis_title='Length of building(sq.m)',
                        zaxis_title='Height of building(sq.m)'),
                        width=700,
                        margin=dict(r=20, b=10, l=10, t=10))

    fig.show()

def plot3d(rchm):

    ny = rchm.shape[0]
    nx = rchm.shape[1]
    x = range(nx)
    y = range(ny)
    x1, y1 = np.meshgrid(x, y)
    fig = plt.figure(figsize = (7,7))
    ax = fig.add_subplot(111, projection='3d')
    chm3d = ax.plot_surface(x1, y1, rchm, linewidth=0.1,rstride=1, cstride=1,cmap=cm.summer, edgecolor='none')

    def rotate(angle):
        ax.view_init(azim=angle) 
        plt.draw()
        plt.pause(.001)
        
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0,362,2),interval=100)
    #rot_animation.save(f"{address}.gif")
    
    end = time.time()
    time1 = end - start
    print(f"Time taken to run : {time1}Seconds")
    plt.show()
    plt.close()


def main():
    # Ask user to input the address for 3D visualization.
    global address
    address =  input("Enter an address: ")
    info = details(address)

    # Using the x and y coordinates of the address check in which tiff file is the location present.

    x = info["x_value"]
    y = info["y_value"]
    result = check_DSM_DTM(x,y)


    polygon = info["polygon"]
    plot_polygon(polygon)

    rchm = CHM(polygon, result, resultDTM)
    # To plot using plotly
    plot3d_plotly(dsm_arr,dtm_arr)
    # To plot 3D model of house.
    plot3d(rchm)

main()