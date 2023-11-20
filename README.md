
# Thailand's Precipitation Dashboard

This is a project for DES424 Cloud-based Application Development.

### Precipitation Data

We use precipitation data obtained from [CHRS Satellite Data Portal](https://chrsdata.eng.uci.edu "PERSIANN"). The data we use is the PERSIANN-CCS data which is a real-time global high resolution (0.04° x 0.04° or 4km x 4km).

### Data Acquisition

To download the precipitation data from the above source, we call a Python script to download the file via FTP. The downloaded data is the daily precipitation data in a binary (*.bin*) format.

### Data Processing

**Step 1:**
The *.bin* file is first converted to GeoTiff (*.tif*) format of the whole globe. Then, add CRS information to be EPSG4326. The example of the *.tif* file is shown below.

![Globe Tif File](https://i.imgur.com/HfGWRMa.png)
> GeoTiff (.tif) file of the whole globe visualized in QGIS.

**Step 2:**
Processing the *.tif* file using `gdal` library. The *.tif* file of the whole globe is then cropped to be in Thailand shape using the shape file (*.shp*). The cropped *.tif* file will have 1 band and in black and white.

Next, we will convert the .tif file into color using a color table and add the alpha channel for transparency.

<img src="https://i.imgur.com/gecjE1e.png" alt="Thailand Tif Filw" width="200" /><img src="https://i.imgur.com/l8qENdf.png" alt="Thailand Tif Filw" width="210" />

> GeoTiff (.tif) file cropped to the shape of Thailand (LEFT).
> GeoTiff (.tif) file of Thailand in color (RIGHT).
