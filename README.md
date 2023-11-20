
# Thailand's Precipitation Dashboard

This is a project for DES424 Cloud-based Application Development.

### Precipitation Data

We use precipitation data obtained from [CHRS Satellite Data Portal](https://chrsdata.eng.uci.edu "PERSIANN"). The data we use is the PERSIANN-CCS data which is a real-time global high resolution (0.04° x 0.04° or 4km x 4km).

### Data Acquisition

To download the precipitation data from the above source, we call a Python script to download the file via FTP. The downloaded data is the daily precipitation data in a binary (.bin) format.

### Data Processing

The .bin file is first converted to GeoTiff (.tif) format of the whole globe. The example of the .tif file is shown below.

![Globe Tif File](https://imgur.com/a/uXRaFD3)
