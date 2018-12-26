import universal_util


##### Constants

# Number of biomass tiles
biomass_tile_count = 280

# Biomass to carbon ratio
biomass_to_c = 0.5

# Carbon to CO2 ratio
c_to_co2 = 3.67

# m2 per hectare
m2_per_ha = 100 * 100

# Aboveground to belowground biomass ratios
above_to_below_natrl_forest = 0.26
above_to_below_mangrove = 0.608


########
# File names and directories
########

### Biomass tiles
# Woods Hole aboveground biomass 2000 version 4 tiles
pattern_biomass = "t_aboveground_biomass_ha_2000"
biomass_dir = 's3://gfw2-data/climate/WHRC_biomass/WHRC_V4/Processed/'

# Lola Fatoyinbo aboveground mangrove biomass tiles
mangrove_biomass_raw_dir = 's3://gfw2-data/climate/carbon_model/mangrove_biomass/raw_from_Lola_Fatoyinbo_20180911/'
mangrove_biomass_raw_file = 'MaskedSRTMCountriesAGB_WRI.zip'

pattern_mangrove_biomass = 'mangrove_agb_t_ha'
mangrove_biomass_dir = 's3://gfw2-data/climate/carbon_model/mangrove_biomass/processed/20181226/'


### Inputs to carbon pools
# FAO ecozones
pattern_fao_ecozone_raw = 'fao_ecozones_bor_tem_tro_20180619.zip'
fao_ecozone_raw_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/raw/{}'.format(pattern_fao_ecozone_raw)
pattern_fao_ecozone_processed = 'res_fao_ecozones_bor_tem_tro'
fao_ecozone_processed_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/processed/fao_ecozones_bor_tem_tro/'

# Precipitation
precip_raw_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/raw/add_30s_precip.tif'
pattern_precip = 'res_precip'
precip_processed_dir = 's3://gfw2-data/gfw2-data/climate/carbon_model/inputs_for_carbon_pools/processed/precip/'

# Soil C
soil_C_raw_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/raw/hwsd_oc_final.tif'
pattern_soil_C = 'soil_t_C_ha'
soil_C_processed_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/processed/soil/'

# Elevation
srtm_raw_dir = 's3://gfw2-data/analyses/srtm/'
pattern_srtm = 'res_srtm'
srtm_processed_dir = 's3://gfw2-data/climate/carbon_model/inputs_for_carbon_pools/processed/srtm/'


### Carbon pools
### NOTE: the patterns for the carbon pools must be set separately in carbon_pools/calc_carbon_pools.cpp
# Base location for all carbon pools
base_carbon_pool_dir = 's3://gfw2-data/climate/carbon_model/carbon_pools/20180815/'

# Aboveground carbon
pattern_agc = 't_AGC_ha'
agc_dir = '{}/aboveground_C'.format(base_carbon_pool_dir)

# Belowground carbon
pattern_bgc = 't_BGC_ha'
bgc_dir = '{}/belowground_C'.format(base_carbon_pool_dir)

# Deadwood
pattern_deadwood = 't_deadwood_C_ha'
deadwood_dir = '{}/deadwood_C'.format(base_carbon_pool_dir)

# Litter
pattern_litter = 't_litter_C_ha'
litter_dir = '{}/litter_C'.format(base_carbon_pool_dir)

# Soil
pattern_soil_pool = 't_soil_C_ha'
soil_C_pool_dir = '{}/soil_C'.format(base_carbon_pool_dir)

# All carbon pools combined
pattern_total_C = 't_total_C_ha'
total_C_dir = '{}/total_carbon'.format(base_carbon_pool_dir)


### Gross emissions
pattern_gross_emissions = 'disturbance_model_noData_reclass'
gross_emissions_dir = 's3://gfw2-data/climate/carbon_model/output_emissions/20180828/disturbance_model_noData_removed/'



# Spreadsheet with annual gain rates
gain_spreadsheet = 'gain_rate_continent_ecozone_age_20181017.xlsx'

# Annual Hansen loss tiles (2001-2015)
loss_dir = 's3://gfw2-data/forest_change/hansen_2015/Loss_tiles/'

# Hansen gain tiles (2001-2012)
pattern_gain = 'Hansen_GFC2015_gain'
gain_dir = 's3://gfw2-data/forest_change/tree_cover_gain/gaindata_2012/'

# Tree cover density 2000 tiles
pattern_tcd = 'Hansen_GFC2014_treecover2000'
tcd_dir = 's3://gfw2-data/forest_cover/2000_treecover/'

# Intact forest landscape 2000 tiles
pattern_ifl = 'res_ifl_2000'
ifl_dir = 's3://gfw2-data/climate/carbon_model/other_emissions_inputs/ifl_2000/'

# Processed FAO ecozone shapefile
cont_ecozone_shp = 'fao_ecozones_fra_2000_continents_assigned_dissolved_FINAL_20180906.zip'

# Number of gain years for non-mangrove natural forests
pattern_gain_year_count_natrl_forest = 'gain_year_count_natural_forest'
gain_year_count_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/gain_year_count_natural_forest/20181031/'

# Number of gain years for mangroves
pattern_gain_year_count_mangrove = 'gain_year_count_mangrove'
gain_year_count_mangrove_dir = 's3://gfw2-data/climate/carbon_model/gain_year_count_mangrove/20181031/'

# Forest age category tiles
pattern_age_cat_natrl_forest = 'forest_age_category_natural_forest'
age_cat_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/forest_age_category_natural_forest/20180921/'


# Annual aboveground biomass gain rate for non-mangrove natural forests
pattern_annual_gain_AGB_natrl_forest = 'annual_gain_rate_AGB_t_ha_natural_forest'
annual_gain_AGB_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/annual_gain_rate_AGB_natural_forest/20181102/'

# Annual aboveground biomass gain rate for mangroves
pattern_annual_gain_AGB_mangrove = 'annual_gain_rate_AGB_t_ha_mangrove'
annual_gain_AGB_mangrove_dir = 's3://gfw2-data/climate/carbon_model/annual_gain_rate_AGB_mangrove/20181102/'

# Annual belowground biomass gain rate for non-mangrove natural forests
pattern_annual_gain_BGB_natrl_forest = 'annual_gain_rate_BGB_t_ha_natural_forest'
annual_gain_BGB_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/annual_gain_rate_BGB_natural_forest/20181102/'

# Annual belowground biomass gain rate for mangroves
pattern_annual_gain_BGB_mangrove = 'annual_gain_rate_BGB_t_ha_mangrove'
annual_gain_BGB_mangrove_dir = 's3://gfw2-data/climate/carbon_model/annual_gain_rate_BGB_mangrove/20181102/'


# Cumulative aboveground gain for natural forests
pattern_cumul_gain_AGC_natrl_forest = 'cumul_gain_AGC_t_ha_natural_forest_2001_15'
cumul_gain_AGC_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/cumulative_gain_AGC_natural_forest/20181104/'

# Cumulative aboveground gain for mangroves
pattern_cumul_gain_AGC_mangrove = 'cumul_gain_AGC_t_ha_mangrove_2001_15'
cumul_gain_AGC_mangrove_dir = 's3://gfw2-data/climate/carbon_model/cumulative_gain_AGC_mangrove/20181102/'

# Cumulative aboveground gain for natural forests
pattern_cumul_gain_BGC_natrl_forest = 'cumul_gain_BGC_t_ha_natural_forest_2001_15'
cumul_gain_BGC_natrl_forest_dir = 's3://gfw2-data/climate/carbon_model/cumulative_gain_BGC_natural_forest/20181104/'

# Cumulative aboveground gain for mangroves
pattern_cumul_gain_BGC_mangrove = 'cumul_gain_BGC_t_ha_mangrove_2001_15'
cumul_gain_BGC_mangrove_dir = 's3://gfw2-data/climate/carbon_model/cumulative_gain_BGC_mangrove/20181102/'


# Annual aboveground gain rate for all forest types
pattern_annual_gain_combo = 'annual_gain_rate_AGB_BGB_t_ha_all_forest_types'
annual_gain_combo_dir = 's3://gfw2-data/climate/carbon_model/annual_gain_rate_all_forest_types/20181105/'

# Cumulative gain for all forest types
pattern_cumul_gain_combo = 'cumul_gain_AGC_BGC_t_ha_all_forest_types_2001_15'
cumul_gain_combo_dir = 's3://gfw2-data/climate/carbon_model/cumulative_gain_all_forest_types/20181105/'

# Net emissions for all forest types and all carbon pools
pattern_net_flux = 'net_emis_t_CO2_ha_all_forest_types_all_drivers_2001_15'
net_flux_dir = 's3://gfw2-data/climate/carbon_model/net_emissions_all_forest_types_all_drivers/20181107/'

# Tile summary spreadsheets
tile_stats = 'tile_stats_{}.txt'.format(universal_util.date)
tile_stats_dir = 's3://gfw2-data/climate/carbon_model/tile_stats/'

# The area of each pixel in m^2
pattern_pixel_area = 'hanson_2013_area'
pixel_area_dir = 's3://gfw2-data/analyses/area_28m/'

# Locations of tsvs from model output
tsv_output_dir = 's3://gfw2-data/climate/carbon_model/model_output_tsv/20181119/'

# Location of raw Hadoop output
hadoop_raw_dir = 'gfw2-data/climate/carbon_model/model_output_Hadoop/raw/'

# Location of processed (cumsummed) Hadoop output
hadoop_processed_s3_dir = 'gfw2-data/climate/carbon_model/model_output_Hadoop/processed/'
hadoop_processed_local_dir = 'C:\GIS\Carbon_model\model_output_Hadoop'

