import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from download import main as download
from pandas_to_np import main as conv2array
import numpy as np



st.header('Plotter de Matrices EEM')



st.markdown(
	'''
	Subir matriz EEM en formato x,y,z a partir de Origin Por el momento es importante no incluir las unidades.\n En otras palabras solo debe haber una fila de titulo y los datos en el archivo.
	'''
)

uploaded_files= st.sidebar.file_uploader(
	'Subir matriz en formato CSV. ',
	type=['csv'],
	accept_multiple_files=True
	)
if uploaded_files:
	titulos_graficos=['grafico  {}'.format(file.name) for file in uploaded_files ]
	uploaded_files=list(uploaded_files)
	st.sidebar.write('Que tipos de gráfico desea generar: ')
	cnt=st.sidebar.checkbox('Contour')

	srf=st.sidebar.checkbox('Surface')
	no_plots=not(cnt or srf)
	# az=altura=30
	# submit=False
	
	with st.sidebar:
		with st.form(key='form1'):
			if srf:
				try:
					az=float(st.text_input('Ángulo azimutal ', '30'))
					altura=float(st.text_input('Altura', '30'))
					asignado='flapo'
				except ValueError:
					print('Solo se aceptan valores numericos')
					az=alt=30.0
			cmap=st.selectbox('Mapa de colores',[ 'plasma',' cividis', 'copper', 'jet', 'inferno'])
			submit = st.form_submit_button('Generar Gráficos')

		# with st.form(key='form2'):
			
		# 	cambio= st.form_submit_button('Modificar Título')





	if submit:
		plt.style.use('ggplot')
		plt.rcParams.update(
			{ 
				'font.size':21
			}
		)
		
		
		dataframes=[pd.read_csv(file) for file in uploaded_files]
		# st.write(dataframes[0])
		arrays=[conv2array(file) for file in dataframes]
		# st.write(type(arrays[0]))
		nplots=len(arrays)
		ncols=3
		nrows=int(np.ceil(nplots/3))
		figsize_cnt=18*nplots,15*(int(np.ceil(nplots/3)))				
		figsize_srf=30*nplots,15*(int(np.ceil(nplots/3)))

		if cnt:
			fig_cont, ax_cont = plt.subplots(ncols= ncols, nrows=nrows,figsize=figsize_cnt, dpi=250)
			if len(arrays)>1:
				ax_cont=ax_cont.flatten()
			else:
				ax_cont=np.array([ax_cont])
			for n,tuple in enumerate(arrays):
				ax_cont[n].contourf(*tuple, cmap=cmap)
				ax_cont[n].set_xlabel(r"$\lambda $ de emisión (nm)")
				ax_cont[n].set_ylabel(r"$\lambda $ de excitación (nm)")
				ax_cont[n].set_title(titulos_graficos[n])
			plt.tight_layout()
	
			plot = st.pyplot(fig_cont)
			down_cont=download(fig_cont)
		if srf:
			fig_srf= plt.Figure(figsize= figsize_srf, dpi=250,tight_layout=True)
		
			for n,tuple in enumerate(arrays):
				ax_srf=fig_srf.add_subplot(int('{}{}{}'.format(nrows, ncols,n+1 )), projection='3d')
				ax_srf.view_init(altura, az)
				ax_srf.plot_surface(*tuple, cmap=cmap)
				ax_srf.set_xlabel(r"$\lambda $ de emisión (nm)")
				ax_srf.set_ylabel(r"$\lambda $ de excitación (nm)")
			# plt.tight_layout()
			plot = st.pyplot(fig_srf)
			down_srf=download(fig_srf)
		if no_plots:
			st.subheader('No se seleccionó ningún tipo de gráfico! ')
			img=Image.open('quedesea.jpeg')
			fig,ax=plt.subplots(1,1)
			ax.imshow(img)
			plt.axis('off')
			plot=st.pyplot(fig)





