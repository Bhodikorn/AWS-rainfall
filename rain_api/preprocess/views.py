# from django.shortcuts import render
# import subprocess
# from django.http import JsonResponse

# # Create your views here.
# def load2(request):
#     date = request.GET.get('date') # Date in dd-mm-yyyy format

#     subprocess.run(['python3', 'persiann_preprocess.py', 'date'])

#     response = JsonResponse({'date': date, 'result': 1})
#     response["Access-Control-Allow-Origin"] = "*"

#     return response

# Import necessary modules
from subprocess import run
from django.http import HttpResponse

# Your Django view
def load(request):
    date = request.GET.get('date') # Date in dd-mm-yyyy format
    script_path = 'preprocess/persiann_preprocess.py'

    # Running the script
    result = run(['python3', script_path, date], capture_output=True, text=True)

    # Handling the output
    if result.returncode == 0:
        return HttpResponse(f"Script executed successfully: {result.stdout}")
    else:
        return HttpResponse(f"Error in script execution: {result.stderr}")
