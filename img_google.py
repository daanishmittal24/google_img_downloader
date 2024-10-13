import streamlit as st
from icrawler.builtin import GoogleImageCrawler
import os
import zipfile
import shutil

def clear_folder(directory):
    """Clear the specified directory."""
    if os.path.exists(directory):
        shutil.rmtree(directory)  # Remove the directory and its contents
    os.makedirs(directory)  # Recreate the directory

def download_images(query, limit):
    # Directory to store downloaded images
    output_dir = 'downloaded_images'
    clear_folder(output_dir)  # Clear the folder before downloading new images

    # Initialize the Google Image Crawler
    crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    # Start crawling and downloading images
    crawler.crawl(keyword=query, max_num=limit)

    # Return the path to the downloaded images
    return output_dir

def zip_images(directory):
    zip_file_path = 'downloaded_images.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for foldername, _, filenames in os.walk(directory):
            for filename in filenames:
                zipf.write(os.path.join(foldername, filename),
                            arcname=os.path.relpath(os.path.join(foldername, filename), 
                                                    os.path.join(directory, '..')))
    return zip_file_path

# Streamlit user interface
st.title("Google Images Downloader")
st.write("Enter a search query to download images from Google Images.")

query = st.text_input("Search Query", "monkey smoking")
limit = st.number_input("Number of Images to Download", min_value=1, value=7)

if st.button("Download Images"):
    if query:
        try:
            downloaded_images_path = download_images(query, limit)
            st.success(f"Downloaded {limit} images for '{query}'!")

            # Provide a button to download the zip file
            zip_file_path = zip_images(downloaded_images_path)
            with open(zip_file_path, 'rb') as f:
                st.download_button(
                    label="Download Images as ZIP",
                    data=f,
                    file_name='downloaded_images.zip',
                    mime='application/zip'
                )
            
            # Display downloaded images
            for img in os.listdir(downloaded_images_path):
                st.image(os.path.join(downloaded_images_path, img))

        except Exception as e:
            st.error(f"Error downloading images: {str(e)}")
    else:
        st.warning("Please enter a search query.")
