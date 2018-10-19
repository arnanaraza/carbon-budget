### Creates Hansen-style tiles for aboveground mangrove biomass (Mg/ha) from Lola Fatoyinbo's country
### mangrove data.
### Output tiles conform to the dimensions, resolution, and other properties of Hansen loss tiles.

import multiprocessing
import utilities
import mangrove_processing
import subprocess
import os

# Downloads zipped raw mangrove files
utilities.s3_file_download(os.path.join(utilities.mangrove_raw_dir, utilities.mangrove_raw), '.')

# Unzips mangrove images into a flat structure (all tifs into main folder using -j argument)
cmd = ['unzip', '-j', utilities.mangrove_raw]
subprocess.check_call(cmd)

# Creates vrt of all raw mangrove tifs
utilities.build_vrt(utilities.mangrove_vrt)

# Biomass tiles to iterate through
biomass_tile_list = utilities.tile_list(utilities.biomass_dir)
# biomass_tile_list = ['20S_020E', '20N_140E', '20N_120W','20N_100E', '20N_080E', '20N_030E', '20N_020E', '20N_010W', '20N_010E',
#                      '20N_000E', '10S_160W', '10S_130E', '10S_110E', '10S_100E', '10S_090E', '10S_080W', '10S_060W', '10S_060E',
#                      '10S_050E', '10S_040E'] # test tile
# biomass_tile_list = ['20S_120W'] # test tile
# biomass_tile_list = biomass_tile_list[62:]
print biomass_tile_list

# For multiprocessor use
# This script didn't work with count/4; perhaps that was using too many processors.
# It did work with ocunt/5, though.
count = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=count/5)
pool.map(mangrove_processing.create_mangrove_tiles, biomass_tile_list)

# # For single processor use, for testing purposes
# for tile in biomass_tile_list:
#
#     mangrove_processing.create_mangrove_tiles(tile)