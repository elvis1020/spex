#Interactive normalize function definition:
def nclick(event):
	toolbar = plt.get_current_fig_manager().toolbar
	if event.button==1 and toolbar.mode=='':
		plt.plot(event.xdata,event.ydata,'rs',ms=8,picker=5,label='cont_pnt')
	plt.draw()

def npick(event):
	if event.mouseevent.button==3:
		if hasattr(event.artist,'get_label') and event.artist.get_label()=='cont_pnt':
			event.artist.remove()

def ntype(event):
	global nmflag
	global gcont
	if event.key=='enter':
		cont_pnt_coord = []
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='cont_pnt':
				cont_pnt_coord.append(artist.get_data())
			elif hasattr(artist,'get_label') and artist.get_label()=='continuum':
				artist.remove()
		cont_pnt_coord = np.array(cont_pnt_coord)[...,0]
		sort_array = np.argsort(cont_pnt_coord[:,0])
		xnp,ynp = cont_pnt_coord[sort_array].T
		spline = splrep(xnp,ynp,k=3)
		continuum = splev(xo,spline)
		gcont=continuum
		plt.plot(xo,continuum,'r-',lw=2,label='continuum')
	elif event.key=='n':
		continuum = None
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='continuum':
				continuum = artist.get_data()[1]
				break
		if continuum is not None:
			plt.cla()
			plt.plot(xo,normy/continuum,'k-',label='normalized')
		gcont=continuum
	elif event.key=='r':
		plt.cla()
		plt.plot(xo,normy, obstyle, linewidth=0.5, label=obsname)
	
	elif event.key=='w':
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='normalized':
				data = np.array(artist.get_data())
				np.savetxt(obsname+'_norm.dat',data.T)
				print('saved to '+obsname+'_norm.dat')
	elif event.key=='x':
		print 'exiting normalizing mode. press enter on terminal'
		nmflag = False
		plt.gcf().canvas.mpl_disconnect(nclick)
		plt.gcf().canvas.mpl_disconnect(npick)
		plt.gcf().canvas.mpl_disconnect(nclick)
	elif event.key == 'a':
		print 'accepting fit and exiting normalizing mode. press enter on terminal'
		global yo
		yo=normy/gcont
		nmflag = False
		plt.gcf().canvas.mpl_disconnect(nclick)
		plt.gcf().canvas.mpl_disconnect(npick)
		plt.gcf().canvas.mpl_disconnect(nclick)
	plt.draw()
	

#multiplot body:
elif opc == 'in':
	plt.cla()
	print '\nleft-click on the spectrum to draw points for the continuum fit\nright-click to remove the point.\ngive commands on plotting window'
	print '\noptions:\nenter: fit continuum ; n: normalize to continuum ; r: clear\na: accept fit and exit ; w: write to a file ; x: exit normalizing mode'
	normy=[m for m in yo]
	plt.plot(xo,normy, obstyle, linewidth=0.5, label=obsname)
	plt.draw()
	nmflag=True
	plt.gcf().canvas.mpl_connect('key_press_event',ntype)
	plt.gcf().canvas.mpl_connect('button_press_event',nclick)
	plt.gcf().canvas.mpl_connect('pick_event',npick)
	while nmflag:
		whatever=raw_input()
