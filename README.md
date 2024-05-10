# GOSE_VMK (GOSE Video Maker)
GOSE_VMK allow you to download GESO-16/18 satellite images from NOAA websites, filter them by Channle, date and resolution, and create a video from the downloaded images.
Its created to achive a higher resolution more flexable time range and more channle than the video creator on NOAA website.
It support both GOSE-16 and GOSE-18 satellite with 24 different channle to select and support resolution up to 21696*21696 and 10848*10848 for video.

## Notes

- This script is compatible with Python 3.10
- The result will be the downloaded images and video in avi format.


## Requirements

- Python 3.10
- ffmpeg


## Setup (CPU Only version)

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
