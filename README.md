# Hitomi Downloader

## Introduction
Hitomi Downloader is a simple command line program to download images from the [Hitomi.la website](https://hitomi.la/) by gallery ID. The program is written in Python 3. The program uses multiprocessing to download the images quickly.

## Setting Up
1. Download and install the latest version of [Python](https://www.python.org/downloads/)
2. Open the Command Prompt (for Windows) or Terminal (for MacOS).
3. Run the following commands:
```
pip install requests
```

## Running the Program
1. Using the Command Prompt, change to the directory to where the file `hitomi_download_2.py` or `hitomi_downloader.py` is located. E.g. `cd D:\hitomi_downloader`
2. Run the following command: `python hitomi_download_2.py <ID> <P> <L>` (Use `python hitomi_downloader.py <ID> <P> <L>` for older galleries)
   1. ID - Gallery Number (retrieve the number from the address bar of the gallery page)
   2. P - Number of processes - specify 1 or more - the higher the number of processes, the quicker the images will be downloaded, but is limited to the performance of your machine. Recommended: 50 or less unless your machine can handle more.
   3. L - Last image number of the gallery - the program will download all images up to the image having this number. Specify '0' to download all the images.
   4. Examples:
      1. `python hitomi_download_2.py 12345 50 100` (Download gallery with ID 12345 using 50 processes up to the 100th image)
      2. `python hitomi_download_2.py 12345 50 0` (Download the entire gallery with ID 12345 using 50 processes)
   5. Note: The `hitomi_download_2.py` works for newer galleries. To download older galleries, try `hitomi_downloader.py` instead.
3. The image will be saved in the folder `hitomi/<Gallery_Number>`.
![image001.png](/images/img001.png)
