from io import BytesIO
import  base64
from datetime import datetime
import streamlit as st

def get_image_download_link(fig,filename,text):
    buffered = BytesIO()
    fig.savefig(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main(fig):    ## Original image came from cv2 format, fromarray convert into PIL format
	img_file="plot_eem_{}.png".format(datetime.strftime(datetime.now(), '%d-%m-%y-%H:%M:%S'))
	button=st.markdown(get_image_download_link(fig,img_file,'Descargar '), unsafe_allow_html=True)
	return button