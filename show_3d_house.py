""" 
This module shows the 3D house in the browser.
"""
import rasterio 
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

#def calculate_3d_house_volume(raster_chm):
#    """This method calculates the volume of the 3D house.
#    :raster_chm: CHM raster, type: rasterio.io.DatasetReader
#    :return: volume of the 3D house
#    """
#    CHM_array = raster_chm[0]
#    volume = np.sum(CHM_array)
#    return volume

#def calculate_3d_house_height(raster_chm):
#    """This method calculates the height of the 3D house.
#    :raster_chm: CHM raster, type: rasterio.io.DatasetReader
#    :return: height of the 3D house
#    """
#    CHM_array = raster_chm[0]
#    height = np.max(CHM_array)
#    return height

def show_3d_house(title, raster_chm):
    """This method shows the 3D house in the browser.
    :title: title of the plot, address is shown in the title
    :raster_chm: CHM raster, type: rasterio.io.DatasetReader
    """
    CHM_array = raster_chm[0]
    #Autorotate
    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    #Plot
    fig = go.Figure(data=[go.Surface(z=CHM_array, colorscale ='OrRd')]) # Create the figure from the CHM array
    fig.update_layout(
        title=f'Address: {title}', 
        title_x=0.5,
        scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye), #Autorotate
        updatemenus=[dict(type='buttons',
        showactive=False,
        y=1,
        x=0.8,
        xanchor='left',
        yanchor='bottom',
        pad=dict(t=45, r=10),
        #Autorotate
        buttons=[dict(label='Rotate',
                                 method='animate',
                                 args=[None, dict(frame=dict(duration=5, redraw=True), 
                                                             transition=dict(duration=0),
                                                             fromcurrent=True,
                                                             mode='immediate'
                                                            )]
                                            )
                                      ]
                              )
                        ],
        scene = dict(
            xaxis_title='Distance (m)',
            yaxis_title='Distance (m)',
            zaxis_title='Height'),
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="darkseagreen"
                ))
    fig.update_scenes(yaxis_autorange="reversed")

    #autorotate the plot, https://community.plotly.com/t/rotating-3d-plots-with-plotly/34776/2
    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z
    frames=[]

    for t in np.arange(0, 6.26, 0.01): 
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    fig.frames=frames

    fig.show() #show the plot in the browser





    