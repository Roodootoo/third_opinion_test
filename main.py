import csv
from pathlib import Path

import pydicom


source_dir = Path("src")
output_dir = Path("out")
path_ratio_file = Path("path_ratio.csv")


def create_folders(folder_path):
    """ Create folders is does not exist in the directory """
    Path.mkdir(folder_path, parents=True, exist_ok=True)


def get_path_from_suid(dcm):
    """ Returns new filepath from dicom attributes """
    new_path = Path(f"{output_dir}/{dcm.StudyInstanceUID}/{dcm.SeriesInstanceUID}/")
    return new_path


def get_name_from_suid(dcm):
    """ Returns new filename from dicom attributes """
    new_name = Path(f"{dcm.SOPInstanceUID}.dcm")
    return new_name


def main():
    """ Main program. Save the anonymous dicom to a new directory. Write locations to path_ratio.csv"""
    with open(path_ratio_file, 'w', newline='') as csv_file:
        fieldnames = ['old_path', 'new_path']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        for dicom_file in source_dir.glob('*.dcm'):
            try:
                dcm = pydicom.dcmread(dicom_file)
            except pydicom.filereader.InvalidDicomError:
                continue  # skip non-dicom file
            dcm.PatientName = None
            dcm_path = get_path_from_suid(dcm)
            dcm_new_filename = get_name_from_suid(dcm)
            out_file = Path(f"{dcm_path}{dcm_new_filename}")
            create_folders(dcm_path)
            dcm.save_as(out_file)
            writer.writerow({'old_path': dicom_file, 'new_path': out_file})
            print(out_file)


if __name__ == '__main__':
    main()
