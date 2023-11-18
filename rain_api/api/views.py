import os
from django.shortcuts import render
import rasterio
from rasterio.transform import from_origin
from django.http import JsonResponse
from pathlib import Path
from django.conf import settings

def get_precipitation_value(tiff_file, lat, lon):
    # Open the TIFF file
    with rasterio.open(tiff_file) as dataset:
        # Convert lat, lon to row, col
        row, col = dataset.index(lon, lat)

        # Read the pixel value at the given row, col
        try:
            precipitation_value = dataset.read(1)[row, col]
        except:
            precipitation_value = "N/A"

        return precipitation_value

# Create your views here.
def get_precip(request):
    
    date = request.GET.get('date')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    file_name = "CCS_1d" + str(date) + ".tif"
    file_path = Path(settings.BASE_DIR) / 'api' / 'tif' / file_name
    precip_value = get_precipitation_value(str(file_path), float(lat), float(lon))

    response = JsonResponse({'precip-value': str(precip_value)})
    response["Access-Control-Allow-Origin"] = "*"

    return response

def check_data_exist(request):
    folder_name = request.GET.get('foldername')

    folder_path = Path(settings.BASE_DIR) / 'preprocess' / 'downloaded-data' / 'tile' / folder_name

    response = JsonResponse({'folder-exist': bool(os.path.exists(folder_path) and os.path.isdir(folder_path))})
    response["Access-Control-Allow-Origin"] = "*"

    return response