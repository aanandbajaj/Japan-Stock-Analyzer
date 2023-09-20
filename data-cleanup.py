import csv
import os

# Specify the path to the existing CSV file
input_csv_path = r"/backend/scraped_data.csv"

# Specify the path for the new CSV file with modifications
output_csv_path = r"/backend/modified_data.csv"

# Read and process the existing CSV file
with open(input_csv_path, "r", newline="", encoding="utf-8") as input_csv_file:
    csv_reader = csv.reader(input_csv_file)

    # Initialize the modified CSV fiale
    with open(output_csv_path, "w", newline="", encoding="utf-8") as output_csv_file:
        csv_writer = csv.writer(output_csv_file)

        # Process each row in the existing CSV
        for row in csv_reader:
            # Remove last digit from the first column
            row[0] = row[0][:-1] + ".T"

            # Skip empty rows
            if any(cell.strip() for cell in row):
                csv_writer.writerow(row)

print("CSV processing complete.")
