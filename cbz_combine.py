# Author: Lucas Jeanniot
# Version: 1.0
# Last Updated: 12/01/2022
# Feel Free to use and distribute this code, but please keep this header.
# If you improve this code, please share it with me, so I can benefit from it as well.
# If you have any questions or suggestions, please drop me a message over at lucasjeanniot.com

# This script processes a folder containing .cbz files, extracts the images, and renames them sequentially.
# It renames the .cbz files to .zip to extract the images and then renames them back to .cbz.
# The extracted images are renamed to "Page <number>.jpg" and saved in the output folder.

import os
import zipfile

def process_cbz_folder(input_folder, output_folder):
    page_count = 0

    # Create the output folder if it doesn't exist
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except PermissionError as e:
        print(f"Permission error: {e}")
        return
    except OSError as e:
        print(f"OS error: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while creating the output folder: {e}")
        return

    # Iterate over the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".cbz"):
            try:
                # Rename the file extension to .zip
                new_filename = os.path.splitext(filename)[0] + ".zip"
                old_filepath = os.path.join(input_folder, filename)
                new_filepath = os.path.join(input_folder, new_filename)
                os.rename(old_filepath, new_filepath)

                # Extract the contents of the zip file
                with zipfile.ZipFile(new_filepath, 'r') as zip_ref:
                    for page in zip_ref.namelist():
                        if page.endswith((".jpg", ".jpeg", ".png")):
                            try:
                                # Generate the new page name
                                page_name = f"Page {page_count}"
                                page_count += 1

                                # Extract the image file
                                zip_ref.extract(page, output_folder)
                                extracted_filepath = os.path.join(output_folder, page)

                                # Handle file conflicts by renaming if necessary
                                new_extracted_filepath = os.path.join(output_folder, f"{page_name}.jpg")
                                if os.path.exists(new_extracted_filepath):
                                    base, ext = os.path.splitext(new_extracted_filepath)
                                    counter = 1
                                    while os.path.exists(new_extracted_filepath):
                                        new_extracted_filepath = f"{base}_{counter}{ext}"
                                        counter += 1

                                # Rename the extracted file
                                os.rename(extracted_filepath, new_extracted_filepath)
                            except FileNotFoundError as e:
                                print(f"File not found during renaming: {e}")
                            except PermissionError as e:
                                print(f"Permission error during renaming: {e}")
                            except Exception as e:
                                print(f"An error occurred while renaming {page}: {e}")

                # Rename the file back to .cbz
                os.rename(new_filepath, old_filepath)
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except zipfile.BadZipFile as e:
                print(f"Bad zip file: {e}")
            except PermissionError as e:
                print(f"Permission error: {e}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

if __name__ == "__main__":
    try:
        input_folder = input("Enter the path to the input folder: ")
        output_folder = input("Enter the path to the output folder: ")
        process_cbz_folder(input_folder, output_folder)
    except FileNotFoundError as e:
        print(f"Input or output folder not found: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")