import pandas as pd
import os

excel_files = [
    #'fileparth',
   # 'file path2',
    #'file path3'
]
sheets_to_check = ["sheet1", "sheet2", "sheet3"] # replace with your sheet names 


results = pd.DataFrame()


for file in excel_files:
    for sheet in sheets_to_check:
        try:

            df = pd.read_excel(file, sheet_name=sheet, engine='openpyxl')

            
            filtered_rows = df[
                df.iloc[:, 1:4].apply(lambda row: row.astype(str).str.contains('Search name # replace with yours ', case=False).any(), axis=1)]

            # Append the filtered rows to the results DataFrame
            results = pd.concat([results, filtered_rows], ignore_index=True)

        except Exception as e:
            print(f"Error processing {file} - {sheet}: {e}")


results.to_excel('filtered_results.xlsx', index=False, engine='openpyxl')

print("Extraction complete. Check 'filtered_results.xlsx' for the results.")
