import streamlit as st
from icrawler.builtin import GoogleImageCrawler
import os
import zipfile
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def clear_folder(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def download_images(query, limit):
    output_dir = 'downloaded_images'
    if not os.path.exists(output_dir):
        clear_folder(output_dir)
        
    crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    crawler.crawl(keyword=query, max_num=limit)
    return output_dir

def zip_images(directory):
    """Create a zip file """
    zip_file_path = 'downloaded_images.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for foldername, _, filenames in os.walk(directory):
            for filename in filenames:
                zipf.write(os.path.join(foldername, filename),
                            arcname=os.path.relpath(os.path.join(foldername, filename), 
                                                    os.path.join(directory, '..')))
    return zip_file_path

def send_email(recipient_email, zip_file_path):
    sender_email = "mrolaf2403@gmail.com" 
    sender_password = "agfm yhmb pzcm dpqk" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Downloaded Images"

    body = "Here are the images you requested"
    msg.attach(MIMEText(body, 'plain'))

    with open(zip_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(zip_file_path)}",
        )
        msg.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
    
st.title("Google Images Downloader")
st.write("Enter a search query to download images from Google Images.")

query = st.text_input("Search Query", "monkey smoking")
limit = st.number_input("Number of Images to Download", min_value=1, value=7)
email_address = st.text_input("Enter your Email Address", "daanishmittal24@gmail.com")

if st.button("Download and Send"):
    if query:
        with st.spinner("Downloading images..."):
            try:
                downloaded_images_path = download_images(query, limit)
                st.success(f"Downloaded {limit} images for '{query}'!")                
                zip_file_path = zip_images(downloaded_images_path)
                st.success(f"Images zipped into {zip_file_path}!")
                with open(zip_file_path, 'rb') as f:
                    st.download_button(
                        label="Download Images as ZIP",
                        data=f,
                        file_name='downloaded_images.zip',
                        mime='application/zip'
                    )
                for img in os.listdir(downloaded_images_path):
                    st.image(os.path.join(downloaded_images_path, img))

                if email_address:
                    with st.spinner("Sending email..."):
                        if send_email(email_address, zip_file_path):
                            st.success(f"Images successfully sent to {email_address}!")
                        else:
                            st.error("Failed to send email")
                else:
                    st.warning("Please enter an email address to send the images.")

            except Exception as e:
                st.error(f"Error downloading images: {str(e)}")
    else:
        st.warning("Please enter a search query.")

st.markdown("""
    <br><br>
    <h5 style='text-align: center;'>Made with ❤️ by <a href='https://github.com/daanishmittal24' target='_blank'> Daanish Mittal<br></a></h5>
""", unsafe_allow_html=True)
