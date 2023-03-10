# EXPOPRÜF V1

It is a project of data automation in which we are generating an Excel file after analysing two Excel sheets.

We are generating an Excel file by extracting data from the given two Excel files and applying various filters to it for getting desired data.

There are two excel files as the input:

- Software Generated File 
- Handwritten Master File

List of filters applied :
- remove duplicates entries
- creating MA Nummer column for all the entries which contains random number (acts like an ID of tester) between 1 to 35
- creating SA Nummer column which contains random and unique value for all the three euro test entries 
- formatting date and time value in DD.MM.YYYY format
- removing "Buchung erstellt von", "gebucht am", "gebuchtes Datum", "Firma", "Anspruchsgruppe", "Zahlungsart", "Krankenkasse", "Bezahlstatus", "Dienstleistungsgruppe", "getestet von" columns
- removing rows which contains blank entries in "getestet von" column
- removing rows which contains "mohammad merhi" in test column
- sorting data according to these column values "getestet am", "getestet um"
- getting data according to desired number of test reasons on specific days
- generating random and unique testnummer (i.e., unique test code)
- arranged time of entries according to opening and closing hours of test stations
- 2 minutes gap in every entry
- select box for choosing month and year value

There are three types of test:
- Three euro test
- Citizen test
- Self Paid test

**Note:**

- Software Generated Excel file contains the entries generated by the software after booking online of a single month only.
- A handwritten Excel file contains the manual entries made during the offline booking.

## Installation

- Install python (version = 3.10.7)

(If you are on windows, click the add to path option during installation; for Mac, match the version for compatibility.)

**Note:** For checking the version of python

```cmd
    python --version    (for windows)
    python3 -V          (for mac)
```

- Open the "EXPOPRÜF V1" folder in any code editor (for example: VS Code).

- Now open the terminal in the editor.

- To instal all of Python's required packages and libraries, we must execute:

```cmd
    pip install -r requirements.txt     (for windows)
    pip3 install -r requirements.txt     (for mac)
```

- After successful installation of all the packages.

- Run the following command on the terminal:

```cmd
    python app.py   (for windows)
    python3 app.py   (for mac)
```

- After running this command, a web page will appear on the [Local Server](http://127.0.0.1:8888/), where we can upload the Excel files and download the output excel file.

## How can I obtain the final output file?

1. Enter the total reported numbers, number of entries in each day, and the number of entries according to test reasons (the help button is on the navbar for getting a list of test reasons).
2. Upload both files to the file upload sections.
3. Click on the "Start" option.
4. "EXPOPRÜF V1" will instantly start the analyzing process.
5. Download your "MasterDatie" Excel file.

## Technology Stack

**Excel Automation:** Pandas (Python Library), Beautiful Soup (Python Library)

**Frontend:** Flask (Python Web Development Framework), HTML, CSS, and JS
