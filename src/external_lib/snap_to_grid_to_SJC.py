from lib.noglobal import noglobal
from external_lib.evaluation_function import calc_haversine
from tqdm import tqdm

import pandas as pd

from shapely.geometry import Point
import osmnx as ox
import momepy
import geopandas as gpd

import numpy as np
import warnings
warnings.simplefilter('ignore')


from lib.kalman_filter import generate_kalmanfilter,apply_kalmanfilter

from external_lib.outlier_correlation import outlier_correlation
from c_library import find_closest_using_multiple_point 





@noglobal()
def generate_grids(arg_df,target_collection,offset_param=0.001):
    df  = arg_df.copy();
    df = arg_df[arg_df["collectionName"]==target_collection]
        
    df["geometry"] = [ Point(p) for p in df[["lngDeg","latDeg"]].to_numpy()]
    ground_df = gpd.GeoDataFrame(df, geometry=df["geometry"])
    
    offset = offset_param
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
    

@noglobal()
def aasdf(x,grid,i):
    return np.float64(grid[x][i]);
    
        

@noglobal(excepts=["generate_grids","aasdf"])
def snap_to_grid_to_SJC(arg_df):
    df = arg_df.copy()

    output_list = [];
    bef_collectionName="";

    
    kf = generate_kalmanfilter()
    for key, each_df in tqdm(df.groupby(["collectionName","phoneName"])):
        tmp_df = each_df.copy();

        collectionName = key[0]

        


        if(not "SJC" in key[0]):
            output_list.append(tmp_df);
            continue;

        if (not (bef_collectionName == collectionName)):
            line_points = generate_grids(arg_df,collectionName);
            grids_list = line_points[["latDeg","lngDeg"]].to_numpy().tolist()

        num =  each_df[["latDeg","lngDeg"]].to_numpy().tolist()
        
        tmp_df["min_idx"] = find_closest_using_multiple_point (num,grids_list);
    
        tmp_df["latDeg"] = tmp_df["min_idx"].apply(lambda x: aasdf(x,grids_list,0))
        tmp_df["lngDeg"] = tmp_df["min_idx"].apply(lambda x: aasdf(x,grids_list,1))
                
        tmp_df = outlier_correlation(tmp_df)
        s = apply_kalmanfilter(tmp_df[["latDeg","lngDeg"]].to_numpy(),kf);
        tmp_df[["latDeg","lngDeg"]] = s

        output_list.append(tmp_df);

    return pd.concat(output_list,axis=0).sort_index();

@noglobal(excepts=["generate_grids","aasdf"])
def snap_to_grid_to_SJC_2_and_3(arg_df):
    df = arg_df.copy()

    output_list = [];
    bef_collectionName="";

    
    kf = generate_kalmanfilter()
    for key, each_df in tqdm(df.groupby(["collectionName","phoneName"])):
        tmp_df = each_df.copy();

        collectionName = key[0]

        
        if(not "SJC" in key[0]):
            output_list.append(tmp_df);
            continue;

        if ("SJC-1" in key[0]):
            output_list.append(tmp_df);
            continue;

        if (not (bef_collectionName == collectionName)):
            line_points = generate_grids(arg_df,collectionName);
            grids_list = line_points[["latDeg","lngDeg"]].to_numpy().tolist()

        num =  each_df[["latDeg","lngDeg"]].to_numpy().tolist()
        
        tmp_df["min_idx"] = find_closest_using_multiple_point (num,grids_list);
    
        tmp_df["latDeg"] = tmp_df["min_idx"].apply(lambda x: aasdf(x,grids_list,0))
        tmp_df["lngDeg"] = tmp_df["min_idx"].apply(lambda x: aasdf(x,grids_list,1))
                
        s = outlier_correlation(tmp_df)
        tmp_df["latDeg"] = s["latDeg"];
        tmp_df["lngDeg"] = s["lngDeg"];
        s = apply_kalmanfilter(tmp_df[["latDeg","lngDeg"]].to_numpy(),kf);
        tmp_df[["latDeg","lngDeg"]] = s

        output_list.append(tmp_df);

    return pd.concat(output_list,axis=0).sort_index();





    





        


        
            
        









