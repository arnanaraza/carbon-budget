import subprocess
import datetime
import os

import get_extent
import glob
import shutil

def calc_all(tile_id):
    start = datetime.datetime.now()
    
    print "copy down biomass tile"
    biomass_tile = '{}_biomass.tif'.format(tile_id)
    copy_bio = ['aws', 's3', 'cp', 's3://WHRC-carbon/global_27m_tiles/final_global_27m_tiles/biomass_10x10deg/{}'.format(biomass_tile), '.']
    subprocess.check_call(copy_bio)
    
    print "get extent of biomass tile"
    xmin, ymin, xmax, ymax = get_extent.get_extent(biomass_tile)

    print "clip soil"
    soil_raster = 'hwsd_oc_final.tif'
    clip_soil_tile = '{}_soil.tif'.format(tile_id)
    clip_soil = ['gdal_translate', '-projwin', str(xmin), str(ymax), str(xmax), str(ymin), '-tr', '.00025', '.00025', '-co', 'COMPRESS=LZW', '-a_nodata', '-9999', soil_raster, clip_soil_tile]
    subprocess.check_call(clip_soil)

    print 'uploading soil tile to s3'
    copy_soil_tile = ['aws', 's3', 'cp', clip_soil_tile, 's3://gfw-files/sam/carbon_budget/data_inputs/soil/']
    subprocess.check_call(copy_soil_tile)
    
    print "rasterizing eco zone"
    fao_eco_zones = 'fao_ecozones_bor_tem_tro.shp'
    rasterized_eco_zone_tile = "{}_fao_ecozones_bor_tem_tro.tif".format(tile_id)
    rasterize = ['gdal_rasterize', '-co', 'COMPRESS=LZW', '-te', str(xmin), str(ymin), str(xmax), str(ymax),
    '-tr', '0.008', '0.008', '-ot', 'Byte', '-a', 'recode', '-a_nodata',
    '0', fao_eco_zones, rasterized_eco_zone_tile]
    subprocess.check_call(rasterize)

    print "resampling eco zone"
    resampled_ecozone =  "{}_res_fao_ecozones_bor_tem_tro.tif".format(tile_id)
    resample_ecozone = ['gdal_translate', '-co', 'COMPRESS=LZW', '-tr', '.00025', '.00025', rasterized_eco_zone_tile, resampled_ecozone]
    subprocess.check_call(resample_ecozone)

    print "upload ecozone to input data"
    cmd = ['aws', 's3', 'cp', resampled_ecozone, 's3://gfw-files/sam/carbon_budget/data_inputs/fao_ecozones_bor_tem_tro/']
    subprocess.check_call(cmd)
    
    print "clipping srtm"
    tile_srtm = '{}_srtm.tif'.format(tile_id)
    srtm = 'srtm.vrt'
    clip_srtm = ['gdal_translate', '-projwin', str(xmin), str(ymax), str(xmax), str(ymin), '-co', 'COMPRESS=LZW', srtm, tile_srtm]
    subprocess.check_call(clip_srtm)

    print "resampling srtm"
    tile_res_srtm = '{}_res_srtm.tif'.format(tile_id)
    resample = ['gdal_translate', '-co', 'COMPRESS=LZW', '-tr', '.00025', '.00025', tile_srtm, tile_res_srtm]
    subprocess.check_call(resample)

    print "clip precip"
    precip_raster = 'add_30s_precip.tif'
    clipped_precip_tile = '{}_clip_precip.tif'.format(tile_id)
    clip_precip_tile = ['gdal_translate', '-projwin', str(xmin), str(ymax), str(xmax), str(ymin), '-co', 'COMPRESS=LZW', precip_raster, clipped_precip_tile]
    subprocess.check_call(clip_precip_tile)

    print "resample precip"
    resample_precip_tile = '{}_res_precip.tif'.format(tile_id)
    resample_precip = ['gdal_translate', '-co', 'COMPRESS=LZW', '-tr', '.00025', '.00025', clipped_precip_tile, resample_precip_tile]
    subprocess.check_call(resample_precip)

    print 'writing carbon, bgc, deadwood, litter, total'
    calc_all_cmd = ['./calc_all.exe', tile_id]
    subprocess.check_call(calc_all_cmd)

    print 'uploading tiles to s3'
    tile_types  = ['carbon', 'bgc', 'deadwood', 'litter', 'soil', 'total_carbon']
    for tile in tile_types:
        if tile == 'total_carbon':
            tile_name = "{}_totalc.tif".format(tile_id)
        else:
            tile_name = "{0}_{1}.tif".format(tile_id, tile)
            
        tile_dest = 's3://gfw-files/sam/carbon_budget/carbon_061417/{}/'.format(tile)

        upload_tile = ['aws', 's3', 'cp', tile_name, tile_dest]
        subprocess.check_call(upload_tile)

    print "deleting intermediate data"
    tiles_to_remove = ['{0}_res_fao_ecozones_bor_tem_tro.tif'.format(tile_id), '{}_srtm.tif'.format(tile_id), '{}_totalc.tif'.format(tile_id), biomass_tile, '{}_soil.tif'.format(tile_id), '{}_deadwood.tif'.format(tile_id), '{}_litter.tif'.format(tile_id), '{}_bgc.tif'.format(tile_id), '{}_carbon.tif'.format(tile_id), '{}_total.tif'.format(tile_id), clip_srtm, tile_res_srtm, clipped_precip_tile, resample_precip_tile]

    for tile in tiles_to_remove:
        try:
            os.remove(tile)
        except:
            pass

    print "elapsed time: {}".format(datetime.datetime.now() - start)
#biomass_tile_list = ["10N_010W", "10N_020E", "10N_030E", "10N_040E", "10S_010E", "10S_020E", "10S_030E", "10S_040E", "10S_050E", "20N_010W", "20N_020W", "20N_030E", "20S_030E", "20S_040E", "30N_010E", "30N_050E", "30S_010E", "10S_140E", "20S_130E", "20S_140E", "30S_140E", "20N_010W", "20N_020W", "20N_030E", "30N_010E", "30N_020E", "30N_050E", "30N_070E", "30N_080E", "30N_090E", "30N_100E", "30N_110E", "40N_000E", "40N_010E", "40N_020E", "40N_020W", "40N_040E", "40N_050E", "40N_070E", "40N_080E", "40N_100E", "40N_110E", "50N_000E", "50N_010E", "50N_010W", "50N_020E", "50N_030E", "50N_040E", "50N_050E", "50N_060E", "50N_070E", "50N_080E", "50N_090E", "50N_100E", "50N_110E", "50N_120E", "50N_130E", "50N_140E", "50N_150E", "60N_000E", "60N_010E", "60N_010W", "60N_020E", "60N_030E", "60N_040E", "60N_050E", "60N_060E", "60N_070E", "60N_080E", "60N_090E", "60N_100E", "60N_110E", "60N_120E", "60N_130E", "60N_140E", "60N_150E", "60N_160E", "60N_170E", "70N_000E", "70N_010E", "70N_020E", "70N_020W", "70N_030E", "70N_030W", "70N_040E", "70N_050E", "70N_060E", "70N_070E", "70N_080E", "70N_090E", "70N_100E", "70N_110E", "70N_120E", "70N_130E", "70N_140E", "70N_150E", "70N_160E", "70N_170E", "70N_170W", "70N_180W", "80N_010E", "80N_020E", "80N_030E", "80N_050E", "80N_060E", "80N_070E", "80N_080E", "80N_090E", "80N_100E", "80N_110E", "80N_120E", "80N_130E", "80N_140E", "80N_150E", "80N_160E", "80N_170E", "80N_180W", "00N_070E", "00N_090E", "00N_100E", "00N_110E", "00N_120E", "00N_130E", "00N_140E", "00N_150E", "00N_160E", "10N_070E", "10N_080E", "10N_090E", "10N_100E", "10N_110E", "10N_120E", "10N_130E", "10N_140E", "10N_150E", "10N_160E", "10S_090E", "10S_100E", "10S_140E", "10S_150E", "20N_070E", "20N_080E", "20N_090E", "20N_100E", "20N_110E", "20N_120E", "20N_140E", "30N_070E", "30N_080E", "30N_090E", "30N_100E", "30N_110E", "30N_140E", "30N_150E", "40N_070E", "40N_080E", "20N_100W", "30N_090W", "30N_100W", "30N_110W", "30N_120W", "40N_070W", "40N_080W", "40N_090W", "40N_100W", "40N_110W", "40N_120W", "40N_130W", "50N_060W", "50N_070W", "50N_080W", "50N_090W", "50N_100W", "50N_110W", "50N_120W", "50N_130W", "60N_060W", "60N_070W", "60N_080W", "60N_090W", "60N_100W", "60N_110W", "60N_120W", "60N_130W", "60N_140W", "60N_150W", "60N_160W", "60N_170W", "60N_180W", "70N_030W", "70N_060W", "70N_070W", "70N_080W", "70N_090W", "70N_100W", "70N_110W", "70N_120W", "70N_130W", "70N_140W", "70N_150W", "70N_160W", "70N_170W", "70N_180W", "80N_060W", "80N_070W", "80N_080W", "80N_090W", "80N_100W", "80N_110W", "80N_120W", "80N_130W", "80N_140W", "80N_150W", "80N_160W", "80N_170W", "00N_040W", "00N_050W", "00N_060W", "00N_070W", "00N_080W", "00N_090W", "00N_100W", "10N_030W", "10N_050W", "10N_060W", "10N_070W", "10N_080W", "10N_090W", "10N_100W", "10S_040W", "10S_050W", "10S_060W", "10S_070W", "10S_080W", "20N_060W", "20N_070W", "20N_080W", "20N_090W", "20N_100W", "20N_110W", "20N_120W", "20S_030W", "20S_040W", "20S_050W", "20S_060W", "20S_070W", "20S_080W", "20S_090W", "20S_110W", "30N_080W", "30N_090W", "30N_100W", "30N_110W", "30N_120W", "30S_060W", "30S_070W", "30S_080W", "40S_070W", "40S_080W", "50S_060W", "50S_070W", "50S_080W"]
#biomass_tile_list = ['20N_110W']
biomass_tile_list = ['00N_010W', '00N_020W', '00N_030W', '00N_050E', '00N_060E', '00N_080E', '00N_110W', '00N_120W', '00N_130W', '00N_140W', '00N_150W', '00N_160W', '00N_170E', '00N_170W', '00N_180W', '10N_030W', '10N_040W', '10N_050W', '10N_060E', '10N_060W', '10N_070W', '10N_080W', '10N_090W', '10N_100W', '10N_110W', '10N_120W', '10N_130W', '10N_140W', '10N_150W', '10N_160W', '10N_170E', '10N_170W', '10N_180W', '10S_000E', '10S_010W', '10S_020W', '10S_030W', '10S_040W', '10S_050W', '10S_060E', '10S_060W', '10S_070E', '10S_070W', '10S_080E', '10S_080W', '10S_090W', '10S_100W', '10S_110W', '10S_120W', '10S_130W', '10S_140W', '10S_150W', '10S_160W', '10S_170W', '10S_180W', '20N_030W', '20N_040W', '20N_050W', '20N_060E', '20N_060W', '20N_070W', '20N_080W', '20N_090W', '20N_120W', '20N_130E', '20N_130W', '20N_140W', '20N_150E', '20N_150W', '20N_160E', '20N_160W', '20N_170E', '20N_170W', '20N_180W', '20S_000E', '20S_010W', '20S_020W', '20S_030W', '20S_040W', '20S_050W', '20S_060E', '20S_060W', '20S_070E', '20S_070W', '20S_080E', '20S_080W', '20S_090E', '20S_090W', '20S_100E', '20S_100W', '20S_110W', '20S_120W', '20S_130W', '20S_140W', '20S_150W', '20S_160W', '20S_170E', '20S_170W', '20S_180W', '30N_030W', '30N_040W', '30N_050W', '30N_060W', '30N_070W', '30N_080W', '30N_130E', '30N_130W', '30N_140W', '30N_150W', '30N_160E', '30N_160W', '30N_170E', '30N_170W', '30N_180W', '30S_000E', '30S_010W', '30S_020W', '30S_030W', '30S_040E', '30S_040W', '30S_050E', '30S_050W', '30S_060E', '30S_060W', '30S_070E', '30S_070W', '30S_080E', '30S_080W', '30S_090E', '30S_090W', '30S_100E', '30S_100W', '30S_110W', '30S_120W', '30S_130W', '30S_140W', '30S_150W', '30S_160E', '30S_160W', '30S_170W', '30S_180W', '40N_030W', '40N_040W', '40N_050W', '40N_060W', '40N_140W', '40N_150E', '40N_150W', '40N_160E', '40N_160W', '40N_170E', '40N_170W', '40N_180W', '40S_000E', '40S_010E', '40S_010W', '40S_020E', '40S_020W', '40S_030E', '40S_030W', '40S_040E', '40S_040W', '40S_050E', '40S_050W', '40S_060E', '40S_060W', '40S_070E', '40S_070W', '40S_080E', '40S_080W', '40S_090E', '40S_090W', '40S_100E', '40S_100W', '40S_110E', '40S_110W', '40S_120E', '40S_120W', '40S_130E', '40S_130W', '40S_140W', '40S_150E', '40S_150W', '40S_160W', '40S_170W', '40S_180W', '50N_020W', '50N_030W', '50N_040W', '50N_050W', '50N_140W', '50N_150W', '50N_160E', '50N_160W', '50N_170E', '50N_170W', '50N_180W', '50S_000E', '50S_010E', '50S_010W', '50S_020E', '50S_020W', '50S_030E', '50S_030W', '50S_040E', '50S_040W', '50S_050E', '50S_050W', '50S_060E', '50S_060W', '50S_070E', '50S_070W', '50S_080E', '50S_080W', '50S_090E', '50S_090W', '50S_100E', '50S_100W', '50S_110E', '50S_110W', '50S_120E', '50S_120W', '50S_130E', '50S_130W', '50S_140E', '50S_140W', '50S_150E', '50S_150W', '50S_160E', '50S_160W', '50S_170E', '50S_170W', '50S_180W', '60N_030W', '60N_040W', '60N_050W', '70N_010W', '70N_040W', '70N_050W', '80N_000E', '80N_010W', '80N_020W', '80N_030W', '80N_040E', '80N_040W', '80N_050W']

#for tile_id in biomass_tile_list:
#    print calc_all(tile_id)

