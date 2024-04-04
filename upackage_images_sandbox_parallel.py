import os
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor

def decompress_file(gz_path, target_path):
    """
    Function to decompress a single .gz file.
    """
    with gzip.open(gz_path, 'rb') as f_in:
        with open(target_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def decompress_gz_files(main_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    tasks = []

    # collect all compated files
    for subdir in os.listdir(main_dir):
        if subdir.startswith("DELVE_northcap_0_") and len(subdir) == 20:
            images_dir = os.path.join(main_dir, subdir, "images")
            if os.path.exists(images_dir):
                for file in os.listdir(images_dir):
                    if file.endswith('.gz'):
                        gz_path = os.path.join(images_dir, file)
                        target_path = os.path.join(target_dir, os.path.basename(file)[:-3])
                        tasks.append((gz_path, target_path))

    total_files = len(tasks)
    if total_files == 0:
        print("No .gz files found. Check the directory paths and file extensions.")
        return

    print(f"Total .gz files to process: {total_files}")

    #upack the files using the cores available
    processed_files = 0
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(decompress_file, gz_path, target_path) for gz_path, target_path in tasks]
        for future in concurrent.futures.as_completed(futures):
            processed_files += 1
            progress = (processed_files / total_files) * 100
            print(f"Progress: {progress:.2f}%")

# Example usage
decompress_gz_files('/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/DELVE_MORPHOLOGY_ALLSTAMPS_v2/0_split/outputs/', '/luidhy_docker/astrodados/DELVE_MORPHOLOGY_DATA/DELVE_MORPHOLOGY_ALLSTAMPS_v2/0_split/image_fits/')
