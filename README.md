# GOSE_VMK (GOSE Video Maker)
GOSE_VMK allow you to download GESO-16/18 satellite images from NOAA websites, filter them by Channle, date and resolution, and create a video from the downloaded images.
Its created to achive a higher resolution more flexable time range and more channle than the video creator on NOAA website.
It support both GOSE-16 and GOSE-18 satellite with 24 different channle to select and support resolution up to 21696*21696 and 10848*10848 for video.

## Features

- Satellite and channel selection
- Date and resolution filtering for images
- Option to create videos from downloaded images using FFmpeg

## How It Works

The script executes the following steps:

1. Satellite and Channel Selection: Users select the desired satellite and channel from provided options.
2. Resolution Selection: After fetching available images, users choose the image resolution for download.
3. Date Range Input: Users input a date range to filter the images, with an option to use previously used ranges.
4. Download Images: Images within the selected date and resolution are downloaded to the local system.
5. Video Creation (Optional): Users can choose to compile the downloaded images into a video, specifying frame rate and other parameters.

## Notes

- This script is compatible with Python 3.10
- The result will be the downloaded images and video in avi format.


## Requirements

- Python 3.10
- ffmpeg


## Setup 

#### 1a. Install Python 3.10 for your specific operating system.
#### [Python 3.10 For Windows](https://www.python.org/downloads/windows/)
#### [Python 3.10 For MacOS](https://www.python.org/downloads/macos/)
#### [Python 3.10 For Linux/UNIX](https://www.python.org/downloads/source/)
#### 1b. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.
#### 2. Create a new Conda environment:
###### In Anaconda Prompt (miniconda3)
  `conda create --name GOSE_VMK python=3.10`

  `conda activate GOSE_VMK`
  
#### 3. Install the required libraries:

`pip install requests`

`pip install beautifulsoup4`

`pip install wget`

#### 4. To ensure combind image into video, you also need to have `ffmpeg` installed on your system. Below are instructions for installing `ffmpeg` on different platforms.

### Installing ffmpeg

```bash

# Ubuntu or Debian

sudo apt update && sudo apt install ffmpeg

# Arch Linux

sudo pacman -S ffmpeg

# MacOS (using Homebrew) If you don't have Homebrew installed, you can install it from https://brew.sh/.

brew install ffmpeg

# Windows (using Chocolatey) If you don't have Chocolatey installed, you can install it from https://chocolatey.org/.
# To install chocolatey run Anaconda Powershell Prompt (miniconda3) in Admin and run
# Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install ffmpeg

# Windows (using Scoop) If you don't have Scoop installed, you can install it from https://scoop.sh/.

scoop install ffmpeg

```

#### 4. Clone the repository: 

`git clone https://github.com/Megumin6626/GOSE_VMK.git`

#### 5. Change to the project directory: 

`cd GOSE_VMK`

#### 6. Run the script to start: 

`python GOSE_VMK_avi_ffmpge.py`

Follow the on-screen instructions to select a satellite, Channel and time.

After the finish downloading all image you can choose to create a video from images and enter the time for frame interval.

## Flow Chart to illustrate how the code works:
```bash

1. Start
|
2. Prompt user to select a satellite
|
3. Prompt user to select a channel
|
4. Fetch available images and display resolutions
|
5. User selects desired resolution
|
6. Input date range (use last or specify new)
|
7. Display selected image range and confirm download
|
8. Download selected images
   |
   8.1. Save images to specified directory
   |
   8.2. Option to create video from downloaded images
       |
       8.2.1. User inputs frame interval
       |
       8.2.2. Calculate frame rate and generate video
|
9. Option to restart or exit
|
10. End
```


## Code explan 

#### `translate_date(date_part)`

Converts a Julian date format to a standard date format, adding time and UTC notation.

#### `suggest_closest_date(image_list, start_date_part, end_date_part)`

Finds the closest available images if the specified date range does not match exactly, helping to ensure users still get relevant data.

#### `save_last_date_range(start_date_part, end_date_part) and load_last_date_range()`

These functions save and retrieve the last used date range, providing a convenient option for frequent users to repeat similar queries without re-entering dates.

#### `create_video_from_images(image_directory, output_video_path, frame_rate=30)`

Compiles downloaded images into a video. It uses FFmpeg to stitch images together based on a specified frame rate, which is dynamically calculated from the user-provided frame interval.

#### `Satellite and Channel Configuration`

Maintains a structured dictionary of satellites and channels, allowing the script to be easily updated or extended with new satellite data or imaging techniques.




