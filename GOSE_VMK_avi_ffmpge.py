import os
import sys
import requests
from bs4 import BeautifulSoup
import wget
from datetime import datetime, timedelta
import subprocess


# Function to translate the date including UTC time
def translate_date(date_part):
    year = date_part[:4]
    day_of_year = int(date_part[4:7])
    time = date_part[7:11]  # Extract the UTC time
    date = datetime.strptime(f"{year}-{day_of_year}", "%Y-%j")
    translated_date = date.strftime("%Y-%m-%d")
    translated_date_with_time = f"{translated_date}-{time}UTC"
    return translated_date_with_time

# Function to suggest the closest date if none found within the range
def suggest_closest_date(image_list, start_date_part, end_date_part):
    def extract_date_from_filename(filename):
        return filename.split('-')[0]

    image_list = sorted(image_list, key=extract_date_from_filename)

    closest_start_date = None
    closest_end_date = None

    for image in image_list:
        image_date = extract_date_from_filename(image)
        if image_date <= start_date_part:
            closest_start_date = image
        if image_date <= end_date_part:
            closest_end_date = image

    return closest_start_date, closest_end_date

# Function to save the last used date range
def save_last_date_range(start_date_part, end_date_part):
    with open("last_date_range.txt", "w") as file:
        file.write(f"start_date_part={start_date_part}\n")
        file.write(f"end_date_part={end_date_part}\n")

# Function to load the last used date range
def load_last_date_range():
    start_date_part = ""
    end_date_part = ""
    if os.path.exists("last_date_range.txt"):
        with open("last_date_range.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split("=")
                if parts[0] == "start_date_part":
                    start_date_part = parts[1]
                elif parts[0] == "end_date_part":
                    end_date_part = parts[1]
    return start_date_part, end_date_part

# Define satellite information
satellites = {
    "1": {
        "name": "GOES-16_(East)",
        "base_url": "https://cdn.star.nesdis.noaa.gov/GOES16/"
    },
    "2": {
        "name": "GOES-18_(West)",
        "base_url": "https://cdn.star.nesdis.noaa.gov/GOES18/"
    }
}

# Define channel information

channels = {
    "1": {
        "name": "GeoColor_(True_Color_Daytime_+_Multispectral_IR_at_night)",
        "subdirectories": ["ABI/FD/GEOCOLOR/"]
    },
    "2": {
        "name": "GLM_FED3+GeoColor_(Lightning_flash_extent_over_GeoColor)",
        "subdirectories": ["GLM/FD/EXTENT3/"]
    },
    "3": {
        "name": "AirMass_RGB_(RGB_based_on_data_from_IR_&_water_vapor)",
        "subdirectories": ["ABI/FD/AirMass/"]
    },
    "4": {
        "name": "Sandwich_RGB_(Blend_combines_IR_band_13_with_visual_band_3)",
        "subdirectories": ["ABI/FD/Sandwich/"]
    },
    "5": {
        "name": "Derived_Motion_Winds",
        "subdirectories": ["ABI/FD/DMW/"]
    },
    "6": {
        "name": "Day_Night_Cloud_Micro_Combo_RGB_(Day_show_phase_of_cloud_tops-night_distinguish_clouds_from_fog)",
        "subdirectories": ["ABI/FD/DayNightCloudMicroCombo/"]
    },
    "7": {
        "name": "Fire_Temperature_RGB_(RGB_used_to_highlight_fires)",
        "subdirectories": ["ABI/FD/FireTemperature/"]
    },
    "8": {
        "name": "Dust_RGB_(RGB_for_identifying_tropospheric_dust)",
        "subdirectories": ["ABI/FD/Dust/"]
    },
    "9": {
        "name": "Band_1_0.47_µm_(Blue-Visible)",
        "subdirectories": ["ABI/FD/01/"]
    },
    "10": {
        "name": "Band_2_0.64_µm_(Red-Visible)",
        "subdirectories": ["ABI/FD/02/"]
    },
    "11": {
        "name": "Band_3_0.86_µm_(Veggie-Near_IR)",
        "subdirectories": ["ABI/FD/03/"]
    },
    "12": {
        "name": "Band_4_1.37_µm_(Cirrus-Near_IR)",
        "subdirectories": ["ABI/FD/04/"]
    },
    "13": {
        "name": "Band_5_1.6_µm_(Snow/Ice-Near_IR)",
        "subdirectories": ["ABI/FD/05/"]
    },
    "14": {
        "name": "Band_6_2.2_µm_(Cloud_Particle-Near_IR)",
        "subdirectories": ["ABI/FD/06/"]
    },
    "15": {
        "name": "Band_7_3.9_µm_(Shortwave_Window-IR)",
        "subdirectories": ["ABI/FD/07/"]
    },
    "16": {
        "name": "Band_8_6.2_µm_(Upper-Level_Water_Vapor-IR)",
        "subdirectories": ["ABI/FD/08/"]
    },
    "17": {
        "name": "Band_9_6.9_µm_(Mid-Level_Water_Vapor-IR)",
        "subdirectories": ["ABI/FD/09/"]
    },
    "18": {
        "name": "Band_10_7.3_µm_(Lower-level_Water_Vapor-IR)",
        "subdirectories": ["ABI/FD/10/"]
    },
    "19": {
        "name": "Band_11_8.4_µm_(Cloud_Top-IR)",
        "subdirectories": ["ABI/FD/11/"]
    },
    "20": {
        "name": "Band_12_9.6_µm_(Ozone-IR)",
        "subdirectories": ["ABI/FD/12/"]
    },
    "21": {
        "name": "Band_13_10.3_µm_(Clean_Longwave_Window-IR)",
        "subdirectories": ["ABI/FD/13/"]
    },
    "22": {
        "name": "Band_14_11.2_µm_(Longwave_Window-IR)",
        "subdirectories": ["ABI/FD/14/"]
    },
    "23": {
        "name": "Band_15_12.3_µm_(Dirty_Longwave_Window-IR)",
        "subdirectories": ["ABI/FD/15/"]
    },
    "24": {
        "name": "Band_16_13.3_µm_(CO₂_Longwave-IR)",
        "subdirectories": ["ABI/FD/16/"]
    }
}


# Ask the user to select a satellite
print("Select a satellite:")
for key, satellite in satellites.items():
    print(f"{key}. {satellite['name']}")

selected_satellite = input("Enter the number of the satellite (1 or 2): ")

if selected_satellite not in satellites:
    print("Invalid satellite selection.")
    exit()

selected_satellite_info = satellites[selected_satellite]
base_url = selected_satellite_info["base_url"]

# Ask the user to select a channel
print("Select a channel:")
for key, channel in channels.items():
    print(f"{key}. {channel['name']}")

selected_channel = input("Enter the number of the channel: ")

if selected_channel not in channels:
    print("Invalid channel selection.")
    exit()

selected_channel_info = channels[selected_channel]
channel_name = selected_channel_info["name"]

# Define the selected link for the channel
for subdirectory in selected_channel_info["subdirectories"]:
    selected_link = base_url + subdirectory
    # Rest of the code remains the same as in your original script, starting from sending an HTTP GET request.
    # You can use the `selected_link` variable to fetch image links for the chosen channel.

# Define the URL of the website to scrape
base_url = selected_link


# Function to suggest the closest date if none found within the range
def suggest_closest_date(image_list, start_date_part, end_date_part):
    def extract_date_from_filename(filename):
        return int(filename.split('-')[0])

    image_list = sorted(image_list, key=extract_date_from_filename)

    closest_start_date = None
    closest_end_date = None

    for image in image_list:
        image_date = extract_date_from_filename(image)
        if image_date <= int(start_date_part):
            closest_start_date = image
        if image_date <= int(end_date_part):
            closest_end_date = image

    return closest_start_date, closest_end_date

# Function to create a video from downloaded images using FFmpeg
def create_video_from_images(image_directory, output_video_path, frame_rate=30):
    image_pattern = os.path.join(image_directory, "%05d.jpg")

    # Run FFmpeg to create the video
    try:
        cmd = [
            "ffmpeg",
            "-framerate", str(frame_rate),
            "-i", image_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]
        subprocess.run(cmd, check=True)
        print(f"Video created at: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e}")



# Send an HTTP GET request to the website
response = requests.get(base_url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = {}

    # Find all links that point to image files
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.jpg'):
            # Extract the resolution from the image filename
            resolution_parts = href.split('-')[-1].split('.')[0]
            if resolution_parts not in image_links:
                image_links[resolution_parts] = []
            image_links[resolution_parts].append(href)

    if not image_links:
        print("No image links found on the website.")
    else:
        # Filter out 'latest' and 'thumbnail' resolutions
        image_links = {resolution: images for resolution, images in image_links.items() if resolution not in ['latest', 'thumbnail']}

        # Sort resolutions from largest to smallest
        sorted_resolutions = sorted(image_links.keys(), key=lambda x: int(x.split('x')[0]), reverse=True)

        # Prompt the user to choose a resolution
        print("Available resolutions (sorted from largest to smallest):")
        for i, resolution in enumerate(sorted_resolutions, start=1):
            print(f"{i}. {resolution}")

        selected_resolution = int(input("Enter the number of the resolution to download: "))

        if 1 <= selected_resolution <= len(sorted_resolutions):
            resolution = sorted_resolutions[selected_resolution - 1]
            image_list = image_links[resolution]

            # Filter image list to only include files with "_GOES" in their names
            image_list = [image for image in image_list if "_GOES" in image]

            # Display the available date range and translate the dates
            start_date = image_list[0].split('-')[0]
            end_date = image_list[-1].split('-')[0]
            translated_start_date = translate_date(start_date)
            translated_end_date = translate_date(end_date)

            print(f"Available image date range {start_date} ({translated_start_date}) to {end_date} ({translated_end_date})")

            while True:
                # Load the last used date range
                last_start_date_part, last_end_date_part = load_last_date_range()

                # Ask the user to enter the date range
                start_date_part = input(
                    f"Enter the starting part of the date range (e.g., {start_date.split('_GOES16')[0]}): ") or last_start_date_part
                end_date_part = input(
                    f"Enter the ending part of the date range (e.g., {end_date.split('_GOES16')[0]} or 'max' for the largest possible value): ") or last_end_date_part

                # Save the entered date range as the last used date range
                save_last_date_range(start_date_part, end_date_part)

                # Convert 'max' to the largest possible value
                if end_date_part.lower() == 'max':
                    end_date_part = '99999999999'

                selected_images = [image for image in image_list if
                                   start_date_part <= image.split('-')[0] <= end_date_part]

                if selected_images:
                    # Display the first and latest image in the range with translated dates
                    first_image = selected_images[0]
                    latest_image = selected_images[-1]

                    first_date_part = first_image.split('-')[0]
                    latest_date_part = latest_image.split('-')[0]

                    translated_first_date = translate_date(first_date_part)
                    translated_latest_date = translate_date(latest_date_part)

                    print(f"First image: {first_image} ({translated_first_date})")
                    print(f"Latest image: {latest_image} ({translated_latest_date})")

                    # Calculate the number of images to be downloaded
                    num_images_to_download = len(selected_images)
                    print(f"Number of images to be downloaded: {num_images_to_download}")

                    confirm = input("Do you want to download these images? (y/n): ").lower()

                    if confirm == 'y':

                        # Create a new directory for storing downloaded images
                        output_directory = os.path.join(os.getcwd(),
                                                        f"{selected_satellite_info['name']}_{channel_name}_{translated_first_date}_{translated_latest_date}")
                        os.makedirs(output_directory, exist_ok=True)

                        # Set the path for the newly created file
                        downloaded_file_path = os.path.join(output_directory,
                                                            f"{selected_satellite_info['name']}_{channel_name}_{translated_first_date}_{translated_latest_date}.txt")

                        # Initialize a counter to keep track of the download order
                        download_order = 0

                        # Download the selected images
                        for selected_image_url in selected_images:
                            download_order += 1
                            image_name = f"{download_order:05d}.jpg"  # Rename based on download order
                            image_url = base_url + selected_image_url
                            image_path = os.path.join(output_directory, image_name)

                            wget.download(image_url, image_path)
                            print(f"Image '{image_name}' downloaded successfully.")

                        # ... (Your existing code)

                        while True:
                            # Prompt the user to create a video
                            create_video_option = input(
                                "Do you want to create a video from the downloaded images? (y/n): ").lower()

                            if create_video_option == 'y':
                                # Ask the user for the frame interval in milliseconds
                                frame_interval = int(input("Enter the frame interval in milliseconds: "))

                                # Calculate the frame rate based on the frame interval
                                frame_rate = 1000 / frame_interval

                                # Call the function to create the video
                                create_video_from_images(output_directory, downloaded_file_path.replace(".txt", ".mp4"),
                                                         frame_rate)
                            else:
                                # Prompt the user to start over or quit
                                restart_option = input(
                                    "Do you want to start over from selecting a satellite or quit the program? (s/q): ").lower()

                                if restart_option == 's':
                                    # Clear the previously selected images
                                    selected_images = []
                                    continue
                                elif restart_option == 'q':
                                    break  # Exit the loop and quit the program
                                else:
                                    print("Invalid input. Please enter 's' to start over or 'q' to quit.")
                                    continue



else:
    print(f"Failed to access the website. Status code: {response.status_code}")

