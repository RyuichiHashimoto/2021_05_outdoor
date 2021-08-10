import warnings
warnings.simplefilter('ignore')
from shapely.geometry import Point
import osmnx as ox
import momepy
import geopandas as gpd

from lib.noglobal import noglobal
from external_lib.evaluation_function import calc_haversine

import numpy as np
import pandas as pd


@noglobal()
def find_min_dist_2nd_version(point,grids):    
    
    dist_list = [calc_haversine(point[0],point[1],x,y) for x,y in grids]
    min_idx = np.argmin(dist_list)
    
    ret_val = [grids[min_idx][0],grids[min_idx][1],dist_list[min_idx]]
    
    return ret_val


@noglobal()
def generate_grids(arg_df,target_collection):
    df  = arg_df.copy();
    df = arg_df[arg_df["collectionName"]==target_collection]
        
    df["geometry"] = [ Point(p) for p in df[["lngDeg","latDeg"]].to_numpy()]
    ground_df = gpd.GeoDataFrame(df, geometry=df["geometry"])
    
    offset = 0.1**4
    bbox = ground_df.bounds + [-offset, -offset, offset, offset]
    
    east = bbox["minx"].min()
    west = bbox["maxx"].max()
    south = bbox["miny"].min()
    north = bbox["maxy"].max()
    G = ox.graph.graph_from_bbox(north, south, east, west, network_type='drive')
    
    original_nodes, original_edges = momepy.nx_to_gdf(G)
    
    edges = original_edges.dropna(subset=["geometry"]).reset_index(drop=True)
    
    hits = bbox.apply(lambda row: list(edges.sindex.intersection(row)), axis=1)
    
    tmp = pd.DataFrame({
    "pt_idx":np.repeat(hits.index,hits.apply(len)),
    "line_i":np.concatenate(hits.values)        
    })
    
    tmp = tmp.join(edges.reset_index(drop=True),on = "line_i")

    tmp = tmp.join(ground_df.geometry.rename("point"),on = "pt_idx")

    tmp = gpd.GeoDataFrame(tmp, geometry="geometry", crs=ground_df.crs)
    
    tmp["snap_dist"] = tmp.geometry.distance(gpd.GeoSeries(tmp["point"]))


    tolerance = 0.0005
    tmp = tmp.loc[tmp["snap_dist"] <= tolerance]
    tmp = tmp.sort_values(by = ["snap_dist"]);

    closest = tmp.groupby("pt_idx").first()

    cloest = gpd.GeoDataFrame(closest, geometry = "geometry")


    closest = gpd.GeoDataFrame(cloest, geometry = "geometry");
    closest =closest.drop_duplicates("line_i").reset_index(drop=True)
    
    
    line_points_list = []
    split = 50  # param: number of split in each LineString
    for dist in range(0, split, 1):
        dist = dist/split
        line_points = closest["geometry"].interpolate(dist, normalized=True)
        line_points_list.append(line_points)
        line_points = pd.concat(line_points_list).reset_index(drop=True)
        line_points = line_points.reset_index().rename(columns={0:"geometry"})
        line_points["lngDeg"] = line_points["geometry"].x
        line_points["latDeg"] = line_points["geometry"].y
        
    return line_points
    