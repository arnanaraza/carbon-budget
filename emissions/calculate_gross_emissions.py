'''
This script calculates the gross emissions in tonnes CO2e/ha for every loss pixel.
The properties of each pixel determine the appropriate emissions equation, the constants for the equation, and the
carbon pool values that go into the equation.
'''

import subprocess
import datetime
import os
import sys
sys.path.append('../')
import constants_and_names as cn
import universal_util as uu

# Calls the function to mask pre-2000 plantations from the loss tiles before calculating emissions from them
def mask_pre_2000_plant(tile_id, sensit_type):

    print "Masking pre-2000 plantations for {}".format(tile_id)

    pre_2000_plant = '../carbon-budget/emissions/cpp_util/{0}_{1}.tif'.format(tile_id, cn.pattern_plant_pre_2000)
    if sensit_type == 'legal_Amazon_loss':
        loss_tile = '../carbon-budget/emissions/cpp_util/{0}_{1}.tif'.format(tile_id, cn.pattern_Brazil_annual_loss_processed)
    else:
        loss_tile = '../carbon-budget/emissions/cpp_util/{}.tif'.format(tile_id)
    out_tile = '../carbon-budget/emissions/cpp_util/{0}_{1}.tif'.format(tile_id, cn.pattern_loss_pre_2000_plant_masked)

    uu.mask_pre_2000_plantation(pre_2000_plant, loss_tile, out_tile, tile_id)


# Calls the c++ script to calculate gross emissions
def calc_emissions(tile_id, pools, sensit_type):

    print "Calculating gross emissions for", tile_id, "using", sensit_type, ":"

    start = datetime.datetime.now()

    # Runs the correct c++ script given the pools (biomass+soil or soil_only) and model type selected.
    # soil_only, no_shiftin_ag, and convert_to_grassland have special gross emissions C++ scripts.
    # The other sensitivity analyses and the standard model all use the same gross emissions C++ script.
    if (pools == 'soil_only') & (sensit_type == 'std'):
        emissions_tiles_cmd = ['../carbon-budget/emissions/cpp_util/calc_gross_emissions_soil_only.exe', tile_id]

    elif (pools == 'biomass_soil') & (sensit_type in ['convert_to_grassland', 'no_shifting_ag']):
        emissions_tiles_cmd = ['../carbon-budget/emissions/cpp_util/calc_gross_emissions_{}.exe'.format(sensit_type), tile_id]

    # This C++ script has an extra argument that names the input carbon pools and output emissions correctly
    elif (pools == 'biomass_soil') & (sensit_type not in ['no_shifting_ag', 'convert_to_grassland']):
        emissions_tiles_cmd = ['../carbon-budget/emissions/cpp_util/calc_gross_emissions_generic.exe', tile_id, sensit_type]

    else:
        raise Exception('Pool and/or sensitivity analysis option not valid')

    subprocess.check_call(emissions_tiles_cmd)


    # Identifies which pattern to use for counting tile completion
    pattern = cn.pattern_gross_emis_commod_biomass_soil
    if (pools == 'biomass_soil') & (sensit_type == 'std'):
        pattern = pattern

    if (pools == 'biomass_soil') & (sensit_type != 'std'):
        pattern = pattern + "_" + sensit_type
        print pattern

    elif pools == 'soil_only':
        pattern = pattern.replace('biomass_soil', 'soil_only')

    else:
        raise Exception('Pool option not valid')

    # Prints information about the tile that was just processed
    uu.end_of_fx_summary(start, tile_id, pattern)
