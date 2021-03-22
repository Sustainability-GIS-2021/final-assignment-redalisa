
def raster_processing(path):
    "This function converts a raster into a shapefile"
    ## Transfrom Raster into Shapefile 
    import os
    
    fp = os.path.join(path)
    # Open the file:
    raster = rasterio.open(fp)
    # Transform the raster into a shapefile
    # https://gis.stackexchange.com/questions/187877/how-to-polygonize-raster-to-shapely-polygons/187883

    mask = None
    with rasterio.Env():
            image = raster.read() # first band
            results = ({'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(shapes(image, mask=mask, transform=raster.transform)))

    geoms = list(results)
    pop_grid  = gpd.GeoDataFrame.from_features(geoms)
    pop_grid = pop_grid.drop((pop_grid.index[pop_grid['raster_val'] <= 0]))
    
    # Rename for a more intuitive meaning
    pop_grid = pop_grid.rename(columns = {"raster_val":"pop_cnt"})
    # Define the CRS
    pop_grid = pop_grid.set_crs("EPSG:4326")
    
    return pop_grid