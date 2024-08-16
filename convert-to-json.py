import json
from datetime import datetime
import sys

def convert_to_json(input_file, output_file):
    data = []
    try:
        with open(input_file, 'r') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    # Remove any leading/trailing whitespace and split the line
                    fields = line.strip().split('\t')
                    
                    # Ensure we have all 6 fields
                    if len(fields) != 6:
                        print(f"Warning: Line {line_number} does not have 6 fields. Skipping.")
                        continue
                    
                    # Parse the date
                    try:
                        date_obj = datetime.strptime(fields[1], "%a, %m/%d/%Y")
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                    except ValueError as e:
                        print(f"Warning: Invalid date format on line {line_number}. Skipping. Error: {e}")
                        continue
                    
                    # Parse distance and elevation
                    try:
                        distance = float(fields[4].split()[0])
                        elevation = int(fields[5].split()[0])
                    except ValueError as e:
                        print(f"Warning: Invalid distance or elevation format on line {line_number}. Skipping. Error: {e}")
                        continue
                    
                    # Create a dictionary for this entry
                    entry = {
                        "type": fields[0],
                        "date": formatted_date,
                        "title": fields[2],
                        "time": fields[3],
                        "distance": distance,
                        "elevation": elevation
                    }
                    
                    data.append(entry)
                except Exception as e:
                    print(f"Error processing line {line_number}: {e}")
                    continue
        
        # Write the data to a JSON file
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)
        
        print(f"Conversion complete. JSON data written to {output_file}")
        print(f"Total entries processed: {len(data)}")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{input_file}' or write to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print ("Usage: python convert-to-json.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_to_json(input_file, output_file)