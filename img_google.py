import streamlit as st
from icrawler.builtin import GoogleImageCrawler
import os
import zipfile
import shutil

def clear_folder(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def download_images(query, limit):
    output_dir = 'downloaded_images'
    clear_folder(output_dir)
    crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    crawler.crawl(keyword=query, max_num=limit)
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

st.title("Google Images Downloader")
st.write("Enter a search query to download images from Google Images.")

query = st.text_input("Search Query", "monkey smoking")
limit = st.number_input("Number of Images to Download", min_value=1, value=7)

if st.button("Download Images"):
    if query:
        with st.spinner("Downloading images..."):
            try:
                downloaded_images_path = download_images(query, limit)
                st.success(f"Downloaded {limit} images for '{query}'!")
                zip_file_path = zip_images(downloaded_images_path)
                with open(zip_file_path, 'rb') as f:
                    st.download_button(
                        label="Download Images as ZIP",
                        data=f,
                        file_name='downloaded_images.zip',
                        mime='application/zip'
                    )
                for img in os.listdir(downloaded_images_path):
                    st.image(os.path.join(downloaded_images_path, img))
            except Exception as e:
                st.error(f"Error downloading images: {str(e)}")
    else:
        st.warning("Please enter a search query.")


st.markdown("""
    <br><br>
    <h5 style='text-align: center;'>Made with ❤️ by <a href='https://github.com/daanishmittal24' target='_blank'> Daanish Mittal<br></a></h5>
""", unsafe_allow_html=True)
