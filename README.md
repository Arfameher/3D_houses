# 3D_houses
To give a brief itroduction of this project you can refer to the description below.
- `Deployment strategy` :
  - GitHub page
  - PowerPoint
  - Jupyter Notebook
  - Python file
***
### Description
This is a solo project to print 3D visualization of the building of an address given as input by the user. 

The address is then searched in the csv file as to in which tiff file is it presnt. Once we know the tif file number, then it clips the house using the polygon coordinates we accessed using API.

It clips the DSM (Data surface model) and the DTM (Data terrain model) with the coordinates given and then the difference of these two gives us the CHM (Canopy height model) using which we can plot a 3D image of the house.
<p align="center">
  <img src="https://carpentries-incubator.github.io/geospatial-python/images/dc-spatial-raster/lidarTree-height.png"width="208" height="250" />
</p>

***
### Installation
Before running this code you need to have anaconda installed in your system and jupyter notebook running with basic libraries or Python IDE such as [Visual Studio Code](https://code.visualstudio.com/)

To run this code you have to clone the repository or download it as a zip file and run it. But before that we need to install some libraries to run this code.

- Create virtual environment to run this code. 
    - If you are using anaconda --> `conda create -n <yourenvname> python=x.x anaconda`
    - Activate your virtual environment -->
    `conda activate <yourenvname>`

- Now we will have to download libraries that are specifically used for this code to run and to read and write a GeoTiff file or a shape file. All these libraries are written in reuirements.txt file.
To install all these libraries do the folling steps:

    1. cd to the directory where `requirements.txt` is located
    2. run the command in your shell: 
        ```javascript
        pip install -r requirements.txt
        ``` 
***
### Repo Architecture

This repository has 2 versions, namely:
#### Jupyter Notebook version (.ipynb)
    - If you want to use the notebook version to run the code, all you need is the `3D_visualization.ipynb` and to download the required DSM and DTM tiff file from the references.

    - Then run the code, you need to input the address and run all the cells to get a 3D representation of the given address.

#### Python File version (.py)

    - If you want to use the python file version to run the code, you need the `main.py`, and the required DSM and DTM tiff file.
    - For the code to run, you need to run the command `python main.py` from the terminal and enter the address that you want to get a 3D representation of the address.

3D_houses
|
│README.md      : Explains the project
│main.py        : This is a python file for more robust output
| 
│3D_visualization.ipynb :   
│

***
### Usage
- Once you have all the libraries successfully installed you can open and run 3D_visualization.ipynb to get the output
    ```javascript
    jupyter notebook
    ```
  OR
cd to the directory where code is present and run the command from the terminal 
    ```javascript
    python main.py
    ```

***
### Visuals
- File containing the boundsof all tiff files.
<p align="center">
  <img src=""width="208" height="250" />
</p>

***
### References
The results we're interested in are DSM (Digital Surface Map) and DTM (Digital Terrain Map).

Which are already computed and available here :

- [DSM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m)
- [DTM](http://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m)


***
### Contributors
There are no contributors as of now, this is a solo project. If you wish to contribute to this repo, you are Welcome!
You can clone this repository and create a new branch and push your changes.

***
### Timeline
Oct - Nov 2021

Time limit: 2 weeks --> 25/10/2021 - 4/11/2021 

This is a solo project given to us at [BeCode](https://becode.org/) after completion of our study material related to data sciece libraries. I have used `pandas`, `numpy` and `matplotlib`.
The time that I took to finish this project was 2 weeks.

***
### Personaal Situation
This is a personal project given to me at [BeCode](https://becode.org/)
I am currently aspiring to be a Data Scientist. This is a 3D visualization of a given building in python using the data science libraries such as pandas, numpy and matplotlib.

Here is how you can contact me :

LinkedIn : [Arfameher](https://www.linkedin.com/in/arfa-meher/)  
Email : arfaameher@outlook.com