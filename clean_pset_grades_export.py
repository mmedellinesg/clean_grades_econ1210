#%%
import os
import sys
import pandas as pd
# %%
def main(input_file_canvas, input_file_psets, pset):
    """
    Takes problem set Google Sheets file and formats it to upload to Canvas, using a model gradebook csv export.
    The model gradebook is a CSV file exported from Canvas, which contains the names of students and their IDs.
    Assumes that problem set grades are stored in sheets "PSET 1", "PSET 2", etc.
    """
    section = input_file_canvas.split('_')[-1].split('.')[0]
    outdir = input_file_canvas.split(
        os.path.basename(input_file_canvas)
    )[0]

    canvas = pd.read_csv(input_file_canvas)
    canvas['name_match'] = canvas['Student'].apply(
        get_name_match
    )

    relevant_col = [
        x for x in canvas.columns if f'Problem Set {pset}' in x
    ][0]

    # %%
    grades = pd.read_excel(
        input_file_psets, sheet_name='PSET '+str(pset)
    )

    grades['Student'] = (
        grades['Student']
            .str.lower()
            .str.strip()
        )

    grades['Grade'] = (
        grades['Grade']
            .astype(str)
            .replace('2025-03-03 00:00:00', '3/3')
            .replace('2025-02-03 00:00:00', '2/3')
            .replace('2025-01-03 00:00:00', '1/3')
            .replace('/3', '', regex=True)
            .astype(float)
    )

    # %%
    out = (
        canvas[
            ['name_match','Student', 'ID', 'SIS Login ID', 'Section']+[relevant_col]
        ].merge(
            grades.drop(columns='Section'), 
            how='left', 
            left_on='name_match', 
            right_on='Student', 
            suffixes=('', '_ps1')
        )
    )

    out[relevant_col] = out['Grade'].fillna(
        out[relevant_col]
    )

    out.drop(
        columns=['name_match', 'Student_ps1', 'Grade'], 
        inplace=True
    )
    # %%
    output_path = os.path.join(outdir,f'{section}_grades_ps{pset}.csv')
    comments_path = os.path.join(outdir,f'{section}_comments_ps{pset}.csv')

    out.drop(columns=relevant_col).rename(columns={
        'Comments': f'Comments {relevant_col}'
    }).to_csv(
        comments_path, 
        index=False
    )
    print(f"Comments saved to {comments_path}")

    out.drop(columns='Comments').to_csv(
        output_path, 
        index=False
    )
    print(f"Grades saved to {output_path}")

# %%

def get_name_match(name):
    name = name.lower()
    if ',' in name:
        name = name.split(',')[1].strip() + ' ' + name.split(',')[0].strip()
    else:
        pass
    return name


if __name__ == '__main__':
    input_file_canvas = sys.argv[1]
    input_file_psets = sys.argv[2]
    pset = int(sys.argv[3])
    main(input_file_canvas, input_file_psets, pset)