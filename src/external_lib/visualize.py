import plotly.express as px
from lib.noglobal import noglobal

@noglobal()
def visualize_trafic(_df,color_header:str=None, zoom=9,outputfile=None):
    df = _df.copy()

    center = {"lat":(df["latDeg"].max()  + df["latDeg"].min())/2, "lon": (df["lngDeg"].max()  + df["lngDeg"].min())/2}
    
    
    if (color_header == None):
        df["history"] =  [ i for i in range(df.shape[0])]
        color_header = "history"
    elif (color_header == "index"):
        df[color_header] = df.index

    
    fig = px.scatter_mapbox(df,                            
                            # Here, plotly gets, (x,y) coordinates
                            lat="latDeg",
                            lon="lngDeg",
                            
                            #Here, plotly detects color of series
                            color=color_header,
                            labels="phoneName",
                            
                            zoom=zoom,
                            center=center,
                            height=600,
                            width=800)
    fig.update_layout(mapbox_style='stamen-terrain')
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(title_text="GPS trafic")
    
    
    if (not outputfile == None):
        if (outputfile.endswith(".html")):
            fig.write_html(outputfile);
        elif(outputfile.endswith(".png")):
            fig.write_image(outputfile,format = "png")
        else:
            raise Exception("Sorry, I cannot understand the " + outputfile.split(".")[-1] +" file");
    else:
        return fig


def get_googlemap_url(df,zoom=14):
    cent_lat  = (df["latDeg"].max()  + df["latDeg"].min())/2
    cent_lon = (df["lngDeg"].max()  + df["lngDeg"].min())/2

    print(f"https://www.google.co.jp/maps/@{cent_lat},{cent_lon},{zoom}z?hl=ja")

    
    return f"https://www.google.co.jp/maps/@{cent_lat},{cent_lon},{zoom}z?hl=ja"





