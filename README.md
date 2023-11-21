
# Thailand's Precipitation Dashboard

This is a project for DES424 Cloud-based Application Development.

### Precipitation Data
------------
We use precipitation data obtained from [CHRS Satellite Data Portal](https://chrsdata.eng.uci.edu "PERSIANN"). The data we use is the PERSIANN-CCS data which is a real-time global high resolution (0.04° x 0.04° or 4km x 4km).

### Data Acquisition
------------
To download the precipitation data from the above source, we call a Python script to download the file via FTP. The downloaded data is the daily precipitation data in a binary (*.bin*) format.

### Data Processing
------------
**Step 1:**
The *.bin* file is first converted to GeoTiff (*.tif*) format of the whole globe. Then, add CRS information to be EPSG4326. The example of the *.tif* file is shown below.

![Globe Tif File](https://i.imgur.com/HfGWRMa.png)
> GeoTiff (.tif) file of the whole globe visualized in QGIS.

**Step 2:**
Processing the *.tif* file using `gdal` library. The *.tif* file of the whole globe is then cropped to be in Thailand shape using the shape file (*.shp*). The cropped *.tif* file will have 1 band and in black and white.

Next, we will convert the .tif file into color using a color table and add the alpha channel for transparency.

<div style="text-align:center"><img src="https://i.imgur.com/QZpIKPy.png" alt="Thailand Tif Filw" width="400" /></div>

> GeoTiff (.tif) file cropped to the shape of Thailand in black and white (LEFT).
> Colored .tif file with alpha channel (RIGHT).

**Step 3:**
Convert the *.tif* file to tiles using `gdal2tiles`. All tile files is contained within a folder and consist of many *.png* files with different zoom level. These tiles will be used for displaying layer over the world map in Leaflet.

<div style="text-align:center"><img src="https://i.imgur.com/hPYHvMl.png" alt="Tile File" width="500" /></div>
<div></div>

> Tile files generated from gdal2tiles.

**Step 4:**
Upload both *.tif* and tile files to Amazon Simple Storage Service (S3) buckets. There will be 2 buckets: one for *.tif* files and the other one for tile files.

### Web Application Framework
------------
The web application is developed in Django framework. In this project, it consists of 2 Django projects for frontend and backend. Each Django project is deployed in a container and contains all dependecies required to be able to handle the processes.
- **Frontend**
contains the HTML, CSS, JS for the user interface of the web application. It will also call the APIs in the backend side as well.

	- `/dashboard` 
	The dashboard display the precipitation visualization over Thailand on selected day.

- **Backend**: 
contains the Python script for handling all APIs call from the frontend. Here are the list of APIs.

	- `/api/checkdata` 
	Check if the data is already existed in S3 bucket or not.
	*Parameters*: foldername (eg. CCS_1d20230601)
	*Return type:* True or False
	
	- `/api/getprecip` 
	Get the precipitation data from the *.tif* file stored in the S3 bucket.
	*Parameters*: lat (string), lon (string), date (yyyymmdd format eg. June 1 = 20230601)
	*Return value:* Precipitation value
	
	- `/preprocess/load` 
	Load data of the specific date and perform data processing steps mentioned above and store it in S3 buckets.
	*Parameters*: date (dd-mm-yyyy format eg. June 1 = 01-06-2023)
	*Return value:* Success or Fail
