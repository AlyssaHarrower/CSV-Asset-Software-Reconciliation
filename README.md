# CSV-Asset-Software-Reconciliation
Python GUI that allows user to upload two .csv files and reads them. It then creates a .csv file that highlights inconsistencies.

For a real use case I coded this specifically to take a list of assets and their software and compare it against a software list.
If certain software is missing from the asset, it will add that asset into the new .csv file with the missing software listed next to it.

# HOW TO USE:
## 1. Make sure your csv files are formatted correctly.
### For your Asset List:
* First column has asset names and is named one of the following: 'asset name', 'asset', 'hostname', 'device', 'computer name'
* Second column is named 'software'
* All software in the 'software' column is separated by a '/' so the program can parse it correctly
* Capitalization doesn't matter
* See Asset List example in the CSV File Examples folder
### For your Software List:
* One column named "software list" with each software item in its own row
* Capitalization doesn't matter
* See Software List example in the CSV File Examples folder
## 2. User Interface
![image](https://github.com/user-attachments/assets/e1714b74-a9f6-4116-b066-143cbde8220a)
* Use buttons to upload the Asset List csv and the Software List csv.
* Once these are successfully uploaded and read you can click compare.
* A message will be printed in the section below showing which Assets are missing software and the software they are missing.
* It will then prompt you to save the new csv with the missing software info in it

# And that's it!
