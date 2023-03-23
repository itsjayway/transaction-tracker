# transaction-tracker
method of visualizing spending within a time range. Used personal downloaded csv data from Santander bank. 

## Usage
1) `python -m venv venv`
2) `. ./venv/Scripts/activate`
3) `pip install -r requirements.txt`
4) `python main.py mar23`

- You'll need to download a csv file from your bank site (and modify the code if it's not Santander).
- `mar23` can be replaced with the source filename (with the file extension)
  - code will generate output files with the same name as the input, with `.json` output
