import os
import boto3
from django.shortcuts import render
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from django.http import JsonResponse
from pathlib import Path
from django.conf import settings
from botocore.exceptions import ClientError

def get_precipitation_value(tiff_file, lat, lon):
    s3 = boto3.client('s3')

    # Download the .tif file from S3 into memory
    obj = s3.get_object(Bucket="persiann-tif-files", Key=tiff_file)

    # Open the TIFF file LOCAL
    # with rasterio.open(tiff_file) as dataset:
    #     # Convert lat, lon to row, col
    #     row, col = dataset.index(lon, lat)

    #     # Read the pixel value at the given row, col
    #     try:
    #         precipitation_value = dataset.read(1)[row, col]
    #     except:
    #         precipitation_value = "N/A"

    #     return precipitation_value

    # CLOUD
    with MemoryFile(obj['Body'].read()) as memfile:
        with memfile.open() as dataset:
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
    # precip_value = get_precipitation_value(str(file_path), float(lat), float(lon)) # LOCAL
    precip_value = get_precipitation_value(file_name, float(lat), float(lon)) # CLOUD

    response = JsonResponse({'precip-value': str(precip_value)})
    response["Access-Control-Allow-Origin"] = "*"

    return response

def check_file_in_s3(bucket_name, file_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Try to get the object
        s3.head_object(Bucket=bucket_name, Key=file_name)
        return True
    except ClientError as e:
        # If a client error is thrown, then check if it was a 404 error.
        # If it was a 404 error, then the object does not exist.
        if e.response['Error']['Code'] == '404':
            return False
        else:
            # The object may exist, but another error was encountered.
            raise

def check_data_exist(request):
    folder_name = request.GET.get('foldername')

    # folder_path = Path(settings.BASE_DIR) / 'preprocess' / 'downloaded-data' / 'tile' / folder_name

    bucket_name = 'persiann-tif-files'
    file_name = folder_name + '.tif'

    # response = JsonResponse({'folder-exist': bool(os.path.exists(folder_path) and os.path.isdir(folder_path))})
    response = JsonResponse({'folder-exist': check_file_in_s3(bucket_name, file_name)})
    response["Access-Control-Allow-Origin"] = "*"

    return response