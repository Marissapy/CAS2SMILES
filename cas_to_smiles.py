"""
Author: Yan Pan
Contact: yanpan@zohomail.com

Description:
    This script reads a CSV file containing CAS numbers, queries each CAS number to retrieve the corresponding SMILES
    (Simplified Molecular Input Line Entry System) using the PubChem database, and outputs a new CSV file with the SMILES
    added as a new column.

Usage:
    python cas_to_smiles.py input.csv output.csv

Dependencies:
    - Python 3.x
    - pubchempy
    - pandas
    - tqdm
"""

import pubchempy as pcp  # Library to access PubChem database
import pandas as pd      # Library for data manipulation and CSV handling
import argparse          # Library for parsing command-line arguments
import sys               # Library for system-specific parameters and functions
from tqdm import tqdm    # Library for displaying progress bars

def get_smiles_by_cas(cas_number):
    """
    Retrieves the SMILES string for a given CAS number using PubChem.

    Parameters:
        cas_number (str): The CAS number of the compound.

    Returns:
        str: The corresponding SMILES string if found, otherwise an error message.
    """
    try:
        # Search for compounds using the CAS number
        compounds = pcp.get_compounds(cas_number, 'name')
        if not compounds:
            return "Not Found"
        
        # Retrieve the SMILES string of the first matched compound
        compound = compounds[0]
        return compound.isomeric_smiles
    except Exception as e:
        # Return the error message in case of an exception
        return f"Error: {e}"

def process_csv(input_file, output_file, cas_column='CAS'):
    """
    Processes the input CSV file to add a SMILES column based on CAS numbers.

    Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file where results will be saved.
        cas_column (str): The column name in the CSV that contains CAS numbers. Default is 'CAS'.
    """
    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)
        print(f"Successfully read input file: {input_file}")
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File {input_file} is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Check if the specified CAS column exists in the DataFrame
    if cas_column not in df.columns:
        print(f"Error: Column '{cas_column}' not found in the input file.")
        sys.exit(1)
    
    # Apply the get_smiles_by_cas function to each CAS number with a progress bar
    print("Retrieving SMILES for each CAS number...")
    tqdm.pandas()  # Initialize tqdm for pandas apply
    df['SMILES'] = df[cas_column].progress_apply(get_smiles_by_cas)
    
    try:
        # Write the updated DataFrame to the output CSV file
        df.to_csv(output_file, index=False)
        print(f"Successfully wrote output file: {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

def main():
    """
    The main function that parses command-line arguments and initiates the CSV processing.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Convert CAS numbers to SMILES and append to CSV.')
    parser.add_argument('input_csv', help='Path to the input CSV file containing CAS numbers.')
    parser.add_argument('output_csv', help='Path to the output CSV file with SMILES added.')
    parser.add_argument('--cas_column', default='CAS', help='Name of the column containing CAS numbers. Default is "CAS".')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Process the CSV file with the provided arguments
    process_csv(args.input_csv, args.output_csv, args.cas_column)

if __name__ == "__main__":
    main()
