import pubchempy as pcp
import pandas as pd
import os

output_file = 'smiles.xlsx'


def get_smiles(pubmed_id):
    try:
        print(f"Searching {pubmed_id}")
        compounds = pcp.get_compounds(pubmed_id, namespace='name')
        if compounds:
            name = compounds[0].isomeric_smiles
            print("Succeed", name)
            return name
        else:
            print(f"No compounds found for PubMed ID {pubmed_id}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Error'


def main():
    # Load data from Excel file
    df_input = pd.read_excel('py-smiles.xlsx')

    # Try to load the output file, create a new DataFrame if it doesn't exist
    if os.path.exists(output_file):
        df_output = pd.read_excel(output_file)
    else:
        df_output = pd.DataFrame(columns=df_input.columns.tolist() + ['SMILES'])

    for index, row in df_input.iterrows():
        pubmed_id = row['compound_name']
        # Check if this entry has already been processed
        if pubmed_id in df_output['compound_name']!=None:
            print(f"Skipping {pubmed_id}, already processed")
            continue

        smiles = get_smiles(pubmed_id)
        new_row = row.copy()
        new_row['SMILES'] = smiles
        df_output = df_output.append(new_row, ignore_index=True)

        # Save the result to the Excel file
        df_output.to_excel(output_file, index=False)


if __name__ == "__main__":
    main()
