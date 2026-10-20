import kagglehub
import shutil
import logging

from pathlib import Path

def extract_data(dataset, folder_path):
    logging.info(f"Downloading dataset {dataset} from Kaggle...")

    download_path = kagglehub.dataset_download(
        dataset
    )

    logging.info(f"Dataset downloaded to: {download_path}")

    folder_path.mkdir(parents=True, exist_ok=True)

    source_path = Path(download_path)

    for file in source_path.iterdir():
        if file.is_file():
            destination = folder_path / file.name

            logging.info(f"Moving file {file.name} to {destination}")

            shutil.copy2(file, destination)

    logging.info("Data download and move completed successfully.")