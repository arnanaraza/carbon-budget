'''
Converts 100m AGB2010 rasters (tropics only) from CCI Biomass into Hansen tiles.
There is no Saatchi_biomass_prep.py because this script just uses the utility warp_to_Hansen.
'''

import multiprocessing
import datetime
from multiprocessing.pool import Pool
from functools import partial
import os
import sys
sys.path.append('../')
import constants_and_names as cn
import universal_util as uu

def main ():

    # Create the output log
    uu.initiate_log()

    os.chdir(cn.docker_base_dir)

    # The list of tiles to iterate through
    #tile_id_list = uu.tile_list_s3(cn.WHRC_biomass_2000_unmasked_dir)
    #tile_id_list = ["00N_000E", "00N_050W", "00N_060W", "00N_010E", "00N_020E", "00N_030E", "00N_040E", "10N_000E", "10N_010E", "10N_010W", "10N_020E", "10N_020W"] # test tiles
    tile_id_list = ['20N_120E'] # test tile
    uu.print_log(tile_id_list)
    uu.print_log("There are {} tiles to process".format(str(len(tile_id_list))) + "\n")

    # By definition, this script is for the biomass swap analysis (replacing WHRC AGB with Saatchi/JPL AGB)
    sensit_type = 'cci_swap'

    # Downloads a folder with the tiles and the vrst of CCi Biomass 2010 map
    uu.s3_flexible_download(cn.CCI_raw_dir,cn.pattern_CCI_unmasked_processed, cn.CCI_raw_name, sensit_type,tile_id_list)

    # Converts the CCI AGB vrt to Hansen tiles
    source_raster = cn.CCI_raw_name
    out_pattern = cn.pattern_CCI_unmasked_processed
    dt = 'Float32'
    pool = multiprocessing.Pool(cn.count-5)  # count-5 peaks at 320GB of memory
    pool.map(partial(uu.mp_warp_to_Hansen, source_raster=source_raster, out_pattern=out_pattern, dt=dt), tile_id_list)

    # Checks if each tile has data in it. Only tiles with data are uploaded.
    upload_dir = cn.CCI_processed_dir
    pattern = cn.pattern_CCI_unmasked_processed
    pool = multiprocessing.Pool(cn.count - 5)  # count-5 peaks at 410GB of memory
    pool.map(partial(uu.check_and_upload, upload_dir=upload_dir, pattern=pattern), tile_id_list)


if __name__ == '__main__':
    main()
