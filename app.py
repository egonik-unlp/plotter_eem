import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from pandas_to_np import main as conv2array
import numpy as np



st.header('Plotter de Matrices EEM')



st.markdown(
	'''
	Subir matriz EEM en formato x,y,z a partir de origin.
	'''
)

uploaded_files= st.sidebar.file_uploader(
	'Subir matriz en formato CSV',
	type=['csv'],
	accept_multiple_files=True
	)
if uploaded_files:
	titulos_graficos=['grafico {}'.format(i) for i in range(len(uploaded_files)) ]
	uploaded_files=list(uploaded_files)
	st.sidebar.write('Que tipos de gráfico desea generar: ')
	cnt=st.sidebar.checkbox('Contour')
	srf=st.sidebar.checkbox('Surface')
	no_plots=not(cnt and srf)

	if st.sidebar.button('Generar gráficos'):
		plt.rcParams.update(
			{ 
				'font.size':30
			}
		)
		plt.style.use('ggplot')
		
		dataframes=[pd.read_csv(file) for file in uploaded_files]
		arrays=[conv2array(file) for file in dataframes]
		nplots=len(arrays)
		nrows=int(np.ceil(nplots/3))
		figsize=20*nplots,15*(int(np.ceil(nplots/3)))
		if cnt:
			fig_cont, ax_cont = plt.subplots(ncols= len(dataframes), nrows=nrows,figsize=figsize)
			if len(arrays)>1:
				ax_con=ax_cont.flatten()
			else:
				ax_cont=np.array([ax_cont])
			for n,tuple in enumerate(arrays):
				ax_cont[n].contourf(*tuple, cmap='plasma', levels=1000)
				ax_cont[n].set_xlabel(r"$\lambda $ de emisión")
				ax_cont[n].set_ylabel(r"$\lambda $ de excitación")
				ax_cont[n].set_title(titulos_graficos[n])
			plt.tight_layout()
			plot = st.pyplot(fig_cont)
		if srf:
			fig_srf= plt.Figure(figsize= figsize)
		
			for n,tuple in enumerate(arrays):
				ax_srf=fig_srf.add_subplot(int('{}{}{}'.format(nrows, len(dataframes),n+1 )), projection='3d')
				ax_srf.plot_surface(*tuple, cmap='plasma')
				ax_srf.set_xlabel(r"$\lambda $ de emisión")
				ax_srf.set_ylabel(r"$\lambda $ de excitación")
			plt.tight_layout()
			plot = st.pyplot(fig_srf)
		if no_plots:
			img=Image.open('quedesea.jpeg')
			fig,ax=plt.subplots(1,1,figsize=(20,15))
			ax.imshow(img)
			plt.axes('off')
			plot=st.pyplot(fig)





