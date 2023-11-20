# ----- Get command line arguments -----

import sys
date = sys.argv[1]

# ----- Change executing directory -----

import os
os.chdir("preprocess/downloaded-data")

# ----- Select Date -----
print("[1] Date conversion...")

from datetime import datetime

def convert_to_day_of_year(date_str):
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    day_of_year = date_obj.timetuple().tm_yday
    return day_of_year

# date = "29-06-2023"
day_of_year = convert_to_day_of_year(date)
year = date[-2:]

# ----- Download PERSIANN using FTP -----
print("[2] Downloading PERSIANN using FTP...")

import urllib.request

file_name = 'rgccs1d' + year + str(day_of_year).zfill(3) + '.bin.gz'

try:
    urllib.request.urlretrieve('ftp://persiann.eng.uci.edu/CHRSdata/PERSIANN-CCS/daily/'+file_name, file_name)
except:
    sys.exit("Error: File not found")

# ----- Extract .gz file -----
print("[3] Extracting .gx file...")

import gzip
import shutil

def extract_gz(gz_file, output_file):
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

gz_file = file_name
extracted_file = file_name[:-3]
print(f">>>>>>>>>>>> gz_file {gz_file}")
print(f">>>>>>>>>>>> extracted_file {extracted_file}")

extract_gz(gz_file, extracted_file)

# ----- Convert .bin to .tif -----
print("[4] Converting .bin to .tif file...")

import numpy as np
from osgeo import gdal, osr

bin_file = extracted_file

# Read the binary file
with open(bin_file, 'rb') as file:
    data = file.read()

# Convert the binary data to numpy array (3000x9000), 4-byte float, big-endian
array_data = np.frombuffer(data, dtype='>f4').reshape((3000, 9000))

# Create a GeoTIFF file

def convert_date_format(date_string):
    date_object = datetime.strptime(date_string, "%d-%m-%Y")
    new_format = date_object.strftime("%Y%m%d")

    return new_format

file_date_format = convert_date_format(date)
output_file_name = "globe_CCS_1d" + file_date_format + ".tif"
print(f">>>>>>>>>>>> output_file_name {output_file_name}")
driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create(output_file_name, 9000, 3000, 1, gdal.GDT_Int16, ['COMPRESS=LZW'])

# Set georeferencing information
dataset.SetGeoTransform([0.0, 0.04, 0, 60.0, 0, -0.04])
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)  # WGS84
dataset.SetProjection(srs.ExportToWkt())

# Convert the data to Int16 and write it to the dataset
array_data_int16 = array_data.astype(np.int16)
dataset.GetRasterBand(1).WriteArray(array_data_int16)
dataset.GetRasterBand(1).SetNoDataValue(-99)
dataset.FlushCache()

# Close the dataset
dataset = None

# ----- Crop .tif file to Thailand shape -----
print("[5] Cropping .tif to Thailand shape...")

tif_file_name = output_file_name
shapefile_path = './thailand-shape-files/Thailand.shp'
cropped_file_name = output_file_name[6:]

options = gdal.WarpOptions(cutlineDSName=shapefile_path,
                           cropToCutline=True,
                           dstNodata=0)

gdal.Warp(cropped_file_name, tif_file_name, options=options)

print(f">>>>>>>>>>>> cropped_file_name {cropped_file_name}")

# ----- Preprocess the .tif file to have SRS, Color, Alpha Band -----
print("[6] Preprocessing .tif file...")

import subprocess

def run_gdal_commands(input_folder, file_name):

    dirs_to_create = ['converted_type_with_srs', 'with_alpha', 'color', 'alpha', 'final_output']
    for dir_name in dirs_to_create:
        dir_path = os.path.join(input_folder, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    file = file_name
    input_file = os.path.join(input_folder, file)
    converted_file = os.path.join(input_folder, './converted_type_with_srs', file)
    with_alpha_file = os.path.join(input_folder, './with_alpha', file)
    color_file = os.path.join(input_folder, './color', file)
    alpha_file = os.path.join(input_folder, './alpha', file)
    final_output_file = os.path.join(input_folder, './final_output', file)
    tiles_output_folder = os.path.splitext(file)[0]

    # Execute GDAL commands
    subprocess.run(['gdal_translate', '-ot', 'Byte', '-a_nodata', '0', '-a_srs', 'EPSG:4326', input_file, converted_file])
    subprocess.run(['gdalwarp', '-dstalpha', converted_file, with_alpha_file])
    subprocess.run(['gdaldem', 'color-relief', with_alpha_file, 'color_table.txt', color_file])
    subprocess.run(['gdal_translate', '-b', '2', with_alpha_file, alpha_file])
    subprocess.run(['gdal_merge.py', '-separate', '-o', final_output_file, color_file, alpha_file])
    subprocess.run(['gdal2tiles.py', '-z', '0-10', final_output_file, tiles_output_folder])

# Example usage
folder_path = "."
run_gdal_commands(folder_path, cropped_file_name)

# ----- Delete unnecessary files -----
print("[7] Deleting unnecessary files...")

def delete_path(path):
    """Delete a file or folder at the specified path."""
    if not os.path.exists(path):
        print(f"The path {path} does not exist.")
        return

    # If it's a file, delete it
    if os.path.isfile(path):
        os.remove(path)
        print(f"File {path} has been deleted.")

    # If it's a directory, delete it and all its contents
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Folder {path} and all its contents have been deleted.")

delete_path(gz_file)
delete_path(extracted_file)
delete_path(output_file_name)
delete_path("converted_type_with_srs")
delete_path("with_alpha")
delete_path("color")
delete_path("alpha")
delete_path("final_output")

# ----- Move files -----
print("[8] Moving files...")

def move_path(source, destination):
    """Move a file or folder from the source path to the destination path."""
    if not os.path.exists(source):
        print(f"The source path {source} does not exist.")
        return

    # Adjust destination if source is a directory
    if os.path.isdir(source):
        destination = os.path.join(destination, os.path.basename(source))

    try:
        shutil.move(source, destination)
        print(f"Moved from {source} to {destination}.")
    except Exception as e:
        print(f"An error occurred: {e}")

move_path(cropped_file_name, "./tif")
move_path(cropped_file_name[:-4], "./tile")

tile_folder_name = cropped_file_name[:-4]

import boto3
import os
from concurrent.futures import ThreadPoolExecutor

def upload_file(s3_client, file_path, bucket_name, base_path):
    """Upload a file to an S3 bucket"""
    # Generate the object name based on file's relative path, including base directory
    object_name = os.path.relpath(file_path, os.path.dirname(base_path))
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        # print(f"{file_path} uploaded successfully as {object_name}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

tile_bucket = 'persiann-tile-files'  # replace with your bucket name
base_path = "./tile/" + tile_folder_name  # directory where your files are located

# Create an S3 client
s3_client = boto3.client('s3')

# Collect all file paths
files_to_upload = []
for dirpath, dirnames, filenames in os.walk(base_path):
    for f in filenames:
        files_to_upload.append(os.path.join(dirpath, f))

# Use ThreadPoolExecutor to upload files in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    for file_path in files_to_upload:
        executor.submit(upload_file, s3_client, file_path, tile_bucket, base_path)

def upload_single_file(s3_client, file_path, bucket_name, object_name=None):
    """Upload a single file to an S3 bucket"""
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"{file_path} uploaded successfully as {object_name}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

tif_bucket = 'persiann-tif-files'  # replace with your bucket name
tif_file_path = './tif/' + cropped_file_name  # path to the file you want to upload

# Upload the file
upload_single_file(s3_client, tif_file_path, tif_bucket)

delete_path("./tif/" + cropped_file_name)
delete_path("./tile/" + tile_folder_name)