import os
import numpy as np
from astropy.io import fits
import pandas as pd

#fits_directory = "/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/CONTROL_SAMPLE_CNN/DOMINGUEZ_galaxies/DOMINGUES2018_images/imagensdescomp/"
#fits_directory = "/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/CONTROL_SAMPLE_CNN/DOMINGUEZ_galaxies/DOMINGUES2018_images/imagensdescomp/"
fits_directory = "/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/CONTROL_SAMPLE_CNN/G10_galaxies/G10_images/"
fits_files = [f for f in os.listdir(fits_directory) if f.endswith('.fits')]
print(len(fits_files))
fits_files_subset = fits_files[:203134]

# Initialize lists to store the data
filenames = []
ids = []
g_m_values = []
g_s_values = []
r_m_values = []
r_s_values = []
i_m_values = []
i_s_values = []
z_m_values = []
z_s_values = []
g_flags = []
r_flags = []
i_flags = []
z_flags = []
g_zero_percentage_list = []
r_zero_percentage_list = []
i_zero_percentage_list = []
z_zero_percentage_list = []
g_min_percentage_list = []
r_min_percentage_list = []
i_min_percentage_list = []
z_min_percentage_list = []

total_files = len(fits_files_subset)

for idx, fits_file in enumerate(fits_files_subset):
    # Print progress
    print(f"Processing file {idx + 1} of {total_files}")

    # Initialize flags and values for each band
    g_flag = 0
    r_flag = 0
    i_flag = 0
    z_flag = 0
    g_m = 0
    g_s = 0
    r_m = 0
    r_s = 0
    i_m = 0
    i_s = 0
    z_m = 0
    z_s = 0
    # Initialize zero percentage values for each band
    g_zero_percentage = 0.0
    r_zero_percentage = 0.0
    i_zero_percentage = 0.0
    z_zero_percentage = 0.0
    # Initialize minimum percentage values for each band
    g_min_percentage = 0.0
    r_min_percentage = 0.0
    i_min_percentage = 0.0
    z_min_percentage = 0.0
    
    file_id = int(fits_file.split('_')[1].split('.')[0])
    # Load the FITS file
    with fits.open(os.path.join(fits_directory, fits_file)) as hdul:
        # Loop through the bands (g, r, i, z)
        for band_index, band in enumerate(['g', 'r', 'i', 'z']):
            # Extract the data for the current band
            band_data = hdul[band_index].data
            m, s = np.median(band_data), np.std(band_data)
            min_value, max_value = np.min(band_data),np.max(band_data)
            ####calculate the percentage of zeros for each band
            num_zero_pixels = np.sum(band_data == 0)
            total_pixels = band_data.size
            percentage_zero_pixels = (num_zero_pixels / total_pixels) * 100
            #####calculate the percentage of pixels with minimum values in order to identify the stripes
            num_min_pixels = np.sum(band_data == min_value)
            percentage_min_pixels = (num_min_pixels / total_pixels) * 100
            # Assign m and s values for each band
            if band == 'g':
                g_m = m
                g_s = s
                g_zero_percentage = percentage_zero_pixels
                g_min_percentage = percentage_min_pixels
            elif band == 'r':
                r_m = m
                r_s = s
                r_zero_percentage = percentage_zero_pixels
                r_min_percentage = percentage_min_pixels
            elif band == 'i':
                i_m = m
                i_s = s
                i_zero_percentage = percentage_zero_pixels
                i_min_percentage = percentage_min_pixels
            elif band == 'z':
                z_m = m
                z_s = s
                z_zero_percentage = percentage_zero_pixels
                z_min_percentage = percentage_min_pixels
            # Check if both m and s are zero
            if m != 0 or s != 0:
                if band == 'g':
                    g_flag = 1
                elif band == 'r':
                    r_flag = 1
                elif band == 'i':
                    i_flag = 1
                elif band == 'z':
                    z_flag = 1

    # Append data for this file to the lists
    filenames.append(fits_file)
    ids.append(file_id)
    g_m_values.append(g_m)
    g_s_values.append(g_s)
    r_m_values.append(r_m)
    r_s_values.append(r_s)
    i_m_values.append(i_m)
    i_s_values.append(i_s)
    z_m_values.append(z_m)
    z_s_values.append(z_s)
    g_flags.append(g_flag)
    r_flags.append(r_flag)
    i_flags.append(i_flag)
    z_flags.append(z_flag)
    g_zero_percentage_list.append(g_zero_percentage)
    r_zero_percentage_list.append(r_zero_percentage)
    i_zero_percentage_list.append(i_zero_percentage)
    z_zero_percentage_list.append(z_zero_percentage)
    g_min_percentage_list.append(g_min_percentage)
    r_min_percentage_list.append(r_min_percentage)
    i_min_percentage_list.append(i_min_percentage)
    z_min_percentage_list.append(z_min_percentage)

# Create a DataFrame from the data
data = {
    'Filename': filenames,
    'QUICK_OBJECT_ID': ids,
    'g_m': g_m_values,
    'g_s': g_s_values,
    'r_m': r_m_values,
    'r_s': r_s_values,
    'i_m': i_m_values,
    'i_s': i_s_values,
    'z_m': z_m_values,
    'z_s': z_s_values,
    'gband': g_flags,
    'rband': r_flags,
    'iband': i_flags,
    'zband': z_flags,
    #################
    'g_zero_percentage':g_zero_percentage_list,
    'r_zero_percentage':r_zero_percentage_list,
    'i_zero_percentage':i_zero_percentage_list,
    'z_zero_percentage':z_zero_percentage_list,
    'g_min_percentage':g_min_percentage_list,
    'r_min_percentage':r_min_percentage_list,
    'i_min_percentage':i_min_percentage_list,
    'z_min_percentage':z_min_percentage_list,
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
#csv_filename = "/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/CONTROL_SAMPLE_CNN/DOMINGUEZ_galaxies/preprocessing_DOMINGUEZ_images_withdiagnostics.csv"
csv_filename = "/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/CONTROL_SAMPLE_CNN/G10_galaxies/preprocessing_G10galaxies_withdiagnostics.csv"

df.to_csv(csv_filename, index=False)

print(f"CSV file saved: {csv_filename}")
