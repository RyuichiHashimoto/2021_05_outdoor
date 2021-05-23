import plotly.express as px

def visualize_trafic(df, zoom=9,outputfile=None):
    

    center = {"lat":(df["latDeg"].max()  + df["latDeg"].min())/2, "lon": (df["lngDeg"].max()  + df["lngDeg"].min())/2}
    
    fig = px.scatter_mapbox(df,
                            
                            # Here, plotly gets, (x,y) coordinates
                            lat="latDeg",
                            lon="lngDeg",
                            
                            #Here, plotly detects color of series
                            color="phoneName",
                            labels="phoneName",
                            
                            zoom=zoom,
                            center=center,
                            height=600,
                            width=800)
    fig.update_layout(mapbox_style='stamen-terrain')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(title_text="GPS trafic")
    
    print(outputfile)
    print(type(outputfile))
        
    
    if (not outputfile == None):
        if (outputfile.endswith(".html")):
            fig.write_html(outputfile);
        elif(outputfile.endswith(".png")):
            fig.write_image(outputfile,format = "png")
        else:
            raise Exception("Sorry, I cannot understand the " + outputfile.split(".")[-1] +" file");
    else:
        return fig
    


    