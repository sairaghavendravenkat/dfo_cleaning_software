import datetime
import random
from datetime import datetime as dt
from pathlib import Path

import pandas as pd


def date_time_and_test_nummer_formatter(dataframe):
    """
    Format the date and time into DD.MM.YYYY and HH:MM format respectively
    and Format test nummer column values into non decimal form

    Args:
        dataframe : contains data into 2D form i.e, row & column form
    """
    try:
        dataframe["Testnummer"] = dataframe["Testnummer"].apply(
            lambda x: int(x))

        dataframe["Geburtsdatum"] = dataframe["Geburtsdatum"].apply(
            lambda x: pd.to_datetime(x, dayfirst=True).__format__("%d.%m.%Y")
        )

        dataframe["getestet um"] = dataframe["getestet um"].apply(
            lambda x: ""
        )
    except Exception as e:
        print("Something went wrong while formatting Date and Time!")


def ma_nummer_col_generator(dataframe):
    """
    Generate 'MA Nummer' column values to the table with random entries between 1 to 35

    Args:
        dataframe : contains data into 2D form i.e, row & column form
    """
    try:
        dataframe["MA-Nummer"] = dataframe["MA-Nummer"].apply(
            lambda x: random.randrange(1, 35)
        )
    except Exception as e:
        print("Something went wrong in MA Nummer generation!")


def sa_nummer_col_generator(dataframe):
    """
    Generate 'SA Nummer' column values to the table with 8 digit random unique values for only 3 euro tests

    Args:
        dataframe : contains data into 2D form i.e, row & column form
    """
    try:
        test_name = "0,00€ Corona-Schnelltest (3€ entfallen) (Besuch einer Freizeitveranstaltung, Besuch besonders gefährdeter Menschen, Rote Meldung in Corona-Warn-App)"
        three_euro_test_index_list = dataframe.index[
            dataframe["Test"] == test_name
        ].tolist()
        for index in three_euro_test_index_list:
            sa_number = "SA-" + str(random.randrange(11111111, 99999999))
            sa_nummer_col = list(dataframe["SA-Nummer"])
            while (sa_number in sa_nummer_col):
                sa_number = "SA-" + str(random.randrange(11111111, 99999999))
            dataframe.at[index, "SA-Nummer"] = sa_number
    except Exception as e:
        print("Something went wrong in SA Nummer generation!")


def blank_entry_finder(dataframe):
    """
    Removing rows which doesn't contain values in 'getestet von' column

    Args:
        dataframe : contains data into 2D form i.e, row & column form

    Returns:
        df: updated dataframe without blank entries
    """
    try:
        blank_entry_list = dataframe.index[dataframe["getestet von"]
                                           == "-"].tolist()
        df = dataframe.copy()
        for index in blank_entry_list:
            df = df.drop(index)
        return df
    except Exception as e:
        print("Something went wrong while searching Blank entry!")


def mohammad_merhi_data_remover(dataframe):
    """
    For removing rows which contains "Mohammed Merhi" as it is irrelevant

    Args:
        dataframe : contains data into 2D form i.e, row & column form

    Returns:
        df : contains dataframe without mohammad merhi entries
    """
    try:
        mohammad_merhi_data_list = dataframe.index[dataframe["Test"] == "Mohammed Merhi"].tolist(
        )
        df = dataframe.copy()
        for index in mohammad_merhi_data_list:
            df = df.drop(index)
        df = df.reset_index(drop=True)
        return df
    except Exception as e:
        print("Something went wrong while searching mohammad merhi data remover!")


def data_count_according_to_date(dataframe):
    """
    Used to calculate the number of test on every date in whole dataframe.

    Args:
        dataframe : contains data into 2D form i.e, row & column form

    Returns:
        dataframe: table which contains the count of every date, there are two columns: getestet am, gesamt
    """
    try:
        df = dataframe.copy()
        set_of_unique_dates = set(df["getestet am"])
        context_of_dates = {}
        for value in set_of_unique_dates:
            context_of_dates[value] = 0

        for value in set_of_unique_dates:
            for date in df["getestet am"]:
                if value == date:
                    context_of_dates[value] += 1
        dates = {
            "getestet am": list(context_of_dates.keys()),
            "gesamt": list(context_of_dates.values()),
        }
        dataframe_of_date = pd.DataFrame.from_dict(dates)
        dataframe_of_date = dataframe_of_date.sort_values(
            by=["getestet am"])
        dataframe_of_date = dataframe_of_date.reset_index(drop=True)
        return dataframe_of_date
    except Exception as e:
        print("Something went wrong in data count according to date !")


def excel_file_generator(
    bookingsystem_filename,
    handwritten_filename,
    output_filename,
    input_reported_numbers,
    context_of_input_data,
    arrival_time,
    departure_time,
    month_value,
    year_value
):
    """
    Generating Excel file with the help of dataframe and applying various filters on data

    Args:
        bookingsystem_filename: file name of the software generated file
        handwritten_filename: file name of the handwritten excel file
        output_filename: file name of the output file
        input_reported_numbers: contains value of input total number of test
        context_of_input_data: contains value of testreasons count with respect to their days
        arrival_time: opening time of test station
        departure_time: closing time of test station
        month_value: value of month 
        year_value: value of year

    """
    try:
        response = {
            "status": False,
            "message": 'Unsuccessful !'
        }
        response_of_excel_merger = merge_excel_file(
            bookingsystem_filename,
            handwritten_filename,
            input_reported_numbers,
            context_of_input_data,
            arrival_time,
            departure_time,
            month_value,
            year_value
        )
        dataframe = response_of_excel_merger['resultant_dataframe']
        dataframe_according_datewise = response_of_excel_merger['date_and_count_dataframe']

        if response_of_excel_merger['status'] == True:
            excel_file_path = (
                Path(__file__)
                .resolve()
                .parent.joinpath(f"static/media/output_files/{output_filename + '.xlsx'}")
            )
            with pd.ExcelWriter(excel_file_path) as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Sheet-1")
                dataframe_according_datewise.to_excel(
                    writer, index=False, sheet_name="Sheet-2"
                )
            response = {
                "status": True,
                "message": 'Successful !'
            }
            return response
        else:
            response = {
                "status": False,
                "message": response_of_excel_merger['message']
            }
            return response
    except Exception as e:
        print("Something went wrong in excel generation !")


def merge_excel_file(
    bookingsystem_filename,
    handwritten_filename,
    input_total_reported_numbers,
    context_of_input_data,
    opening_time,
    closing_time,
    month_value,
    year_value
):
    """
    Merging two excel files i.e, handwritten excel file and software generated excel file and applying various filters

    Args:
        bookingsystem_filename: file name of the software generated file
        handwritten_filename: file name of the handwritten excel file
        input_total_reported_numbers: contains value of input total number of test
        context_of_input_data: contains value of testreasons count with respect to their days
        opening_time: opening time of test station
        closing_time: closing time of test station
        month_value: month value selected
        year_value: year value selected
    """
    try:
        response = {
            "status": True,
            "message": "Sucessful !",
            "resultant_dataframe": None,
            "date_and_count_dataframe": None
        }

        excel_file_path_bookingsystem = (
            Path(__file__)
            .resolve()
            .parent.joinpath(f"static/media/input_files/{bookingsystem_filename}")
        )
        excel_file_path_handwritten = (
            Path(__file__)
            .resolve()
            .parent.joinpath(f"static/media/input_files/{handwritten_filename}")
        )

        dataframe_of_boookingsystem = pd.read_excel(
            excel_file_path_bookingsystem)
        dataframe_of_handwritten = pd.read_excel(excel_file_path_handwritten)

        '''
        for handling values of dates in both dataframes
        making dates in handwritten must be blank
        making dates in software must be in proper format (DD.MM.YYYY)
        '''
        date_handler_for_both_dataframe(
            dataframe_of_boookingsystem, dataframe_of_handwritten)

        """
            We are going to create a list that contains all data frames.
            The order of the data frames in this list will determine how the files get appended
        """
        all_df_list = [dataframe_of_boookingsystem, dataframe_of_handwritten]

        """
            this function will append all our data frames in that order,
            and assign the appended data frame to a variable dataframe_of_all_bookings
        """
        df_of_all_bookings = pd.concat(all_df_list, ignore_index=True)
        # initialising column of SA and MA Nummer
        df_of_all_bookings["MA-Nummer"] = ""
        df_of_all_bookings["SA-Nummer"] = ""

        master_df = df_of_all_bookings.copy()

        date_time_and_test_nummer_formatter(master_df)

        master_df = master_df.drop_duplicates(
            subset=["Testnummer"], keep="first")

        """
            for removing these columns :-
            "Buchung erstellt von", 
            "gebucht am", 
            "gebuchtes Datum", 
            "Firma", 
            "Anspruchsgruppe", 
            "Zahlungsart", 
            "Krankenkasse", 
            "Bezahlstatus", 
            "Dienstleistungsgruppe" 
        """
        master_df = master_df.drop(columns=["Buchung erstellt von", "gebucht am", "gebuchtes Datum", "Firma",
                                   "Anspruchsgruppe", "Zahlungsart", "Krankenkasse", "Bezahlstatus", "Dienstleistungsgruppe"])

        """
            for removing blank entries in 'getestet von' column
        """
        updated_master_df = blank_entry_finder(master_df)

        """
            for removing "getestet von" column
        """
        updated_master_df = updated_master_df.drop(columns=["getestet von"])

        if int(input_total_reported_numbers) > len(updated_master_df):
            print(int(input_total_reported_numbers))
            len_of_df = len(updated_master_df)
            response = {
                "status": False,
                "message": f"Please enter a value less than {len_of_df} because the total number of entries in the Excel file is less than the entered value!",
                "resultant_dataframe": None,
                "date_and_count_dataframe": None
            }
            return response

        """
            sorting is done on the basis of "getestet am" i.e, "tested on" column
        """
        updated_master_df = updated_master_df.sort_values(
            by=["getestet am"])

        updated_master_df = updated_master_df.reset_index(drop=True)

        working_df = updated_master_df.copy()

        response_of_required_df_generator = required_df_generator(working_df, context_of_input_data,
                                                                  input_total_reported_numbers, opening_time, closing_time, month_value, year_value)

        if response_of_required_df_generator['status'] == True:
            updated_master_df = response_of_required_df_generator[
                'dataframe']
        else:
            response = {
                "status": response_of_required_df_generator['status'],
                "message": response_of_required_df_generator['message'],
                "resultant_dataframe": None,
                "date_and_count_dataframe": None
            }
            return response

        final_df = updated_master_df

        """
            for adding "MA Nummer" and "SA-Nummer" column
        """
        ma_nummer_col_generator(final_df)
        sa_nummer_col_generator(final_df)

        """
            testnummer manipulator
        """
        output_df = test_nummer_manipulator(final_df)

        data_count_dataframe = data_count_according_to_date(output_df)

        response = {
            "status": True,
            "message": "Sucessful !",
            "resultant_dataframe": output_df,
            "date_and_count_dataframe": data_count_dataframe
        }
        return response
    except Exception as e:
        print("Something went wrong while merging excel sheets !")


def two_minutes_filter_and_shift_timing_feature(df_of_one_day, start_time, end_time, day):
    """
    Applying two minutes filter according to opening and closing time of test stations

    Args:
        df_of_one_day (dataframe): dataframe contains test reasons of one day only
        start_time (string): opening time of test station
        end_time (string): closing time of test station
        day (int): day value

    """
    try:
        response = {
            "status": False,
            "message": "Etwas ist schief gelaufen !",
            "dataframe": None
        }
        dataframe = df_of_one_day.copy()
        number_of_test_present_in_a_day = len(dataframe)
        start = dt.strptime(start_time, "%H:%M")
        end = dt.strptime(end_time, "%H:%M")
        difference = end - start
        possible_number_of_test_in_one_day = int(
            (difference.total_seconds())/120)
        if number_of_test_present_in_a_day > possible_number_of_test_in_one_day:
            response = {
                "status": False,
                # message : Please change your opening and closing times because you have input more entries
                # for the 2nd day than are allowed in this time duration. The maximum number of entries possible in one day is 180.
                "message": f"Bitte ändern Sie Ihre Öffnungs- und Schließzeiten, da Sie für den {day}. Tag mehr Einträge eingegeben haben als in dieser Zeitdauer erlaubt sind. Die maximale Anzahl an möglichen Einträgen an einem Tag beträgt {possible_number_of_test_in_one_day}.",
                "dataframe": None
            }
            return response

        time_interval = datetime.timedelta(minutes=2)
        """
        creating list which contains all possible values of time between the given opening and closing hours
        """
        possible_time_list = []
        initial_value = start
        final_value = end
        append_value = initial_value
        while (append_value != final_value):
            time = append_value.strftime("%H:%M")
            possible_time_list.append(time)
            append_value = append_value + time_interval

        for index in range(0, len(dataframe)):
            getestet_um_value = random.choice(possible_time_list)
            getestet_um_col_list = list(dataframe["getestet um"])
            while (getestet_um_value in getestet_um_col_list):
                getestet_um_value = random.choice(possible_time_list)
            dataframe.at[index, "getestet um"] = getestet_um_value

        dataframe = dataframe.sort_values(by=["getestet um"])
        dataframe = dataframe.reset_index(drop=True)
        response = {
            "status": True,
            "message": "Successful",
            "dataframe": dataframe
        }
        return response
    except Exception as e:
        print("Something went wrong in 2 mins filter")


def data_count_calculator_acc_to_test_reasons(filename):
    """
    Count the number of test on each day and generate dictionary

    Args:
        filename : name of the output file
    """
    try:
        file_path = (
            Path(__file__)
            .resolve()
            .parent.joinpath(f"static/media/output_files/{filename + '.xlsx'}")
        )
        dataframe = pd.read_excel(file_path)

        test_reasons_dict = {
            "reason_1": "Besucher, Behandelte oder Bewohner bestimmter Einrichtungen",
            "reason_2": "Nachweis zur Beendigung der Absonderung nach einer Corona Infektion",
            "reason_3": "Besuche in Krankenhäusern und Pflegeheimen",
            "reason_4": "Leistungsberechtigte im Rahmen eines persönlichen Budgets nach § 29 des 9. Buches SGB",
            "reason_5": "Pflegepersonen im Sinne des § 19 Satz 1 des 11. Buches SGB",
            "reason_6": "Teilnahme an klinischen Studien",
            "reason_7": "Kinder bis zum 5. Lebensjahr",
            "reason_8": "Zusammenlebend mit einer an SARS-CoV-2 erkrankten Person",
            "reason_9": "Kontraindikationen zur Durchführung von Covid-19-Impfungen",
            "reason_10": "Veranstaltung im Innenraum",
            "reason_11": "Corona-Warn App Warnung",
            "reason_12": "Kontakt zu einer Person aus einer Risikogruppe",
            "reason_13": "Kontakt zu einer Person über 60 Jahren",
            "reason_14": ""  # self paid
        }

        req_col = dataframe['Testgrund']
        test_reasons_count = {
            "reported_numbers": len(dataframe["Testgrund"]),
            "reason_1": (req_col == test_reasons_dict['reason_1']).sum(),
            "reason_2": (req_col == test_reasons_dict['reason_2']).sum(),
            "reason_3": (req_col == test_reasons_dict['reason_3']).sum(),
            "reason_4": (req_col == test_reasons_dict['reason_4']).sum(),
            "reason_5": (req_col == test_reasons_dict['reason_5']).sum(),
            "reason_6": (req_col == test_reasons_dict['reason_6']).sum(),
            "reason_7": (req_col == test_reasons_dict['reason_7']).sum(),
            "reason_8": (req_col == test_reasons_dict['reason_8']).sum(),
            "reason_9": (req_col == test_reasons_dict['reason_9']).sum(),
            "reason_10": (req_col == test_reasons_dict['reason_10']).sum(),
            "reason_11": (req_col == test_reasons_dict['reason_11']).sum(),
            "reason_12": (req_col == test_reasons_dict['reason_12']).sum(),
            "reason_13": (req_col == test_reasons_dict['reason_13']).sum(),
            "reason_14": (req_col.isnull()).sum()  # self paid
        }
        return test_reasons_count
    except Exception as e:
        print("Something went wrong while data count calculator !")


def date_handler_for_both_dataframe(software_dataframe, handwritten_dataframe):
    """
    format date according to the software and handwritten dataframe

    Args:
        software_dataframe : software generated data df
        handwritten_dataframe : manually written data df
    """
    try:
        software_dataframe["getestet am"] = software_dataframe["getestet am"].apply(
            lambda x: pd.to_datetime(str(x).split(" ")[0], dayfirst=True).__format__(
                "%d.%m.%Y") if x != "-" else ''
        )
        handwritten_dataframe['getestet am'] = handwritten_dataframe['getestet am'].apply(
            lambda x: "")
    except Exception as e:
        print("Something went wrong in date_handler_for_both_dataframe")


def required_df_generator(working_df, context_of_input_data, input_total_reported_numbers, opening_time, closing_time, month_value, year_value):
    """
    Generate the df by slicing and analysing test reasons, test, date and time 

    Args:
        working_df : dataframe of all data
        input_total_reported_numbers: contains value of input total number of test
        context_of_input_data: contains value of testreasons count with respect to their days
        opening_time: opening time of test station
        closing_time: closing time of test station
        month_value: month value selected
        year_value: year value selected

    """
    try:
        response = {
            "status": False,
            "message": "Etwas ist schief gelaufen !",
            "dataframe": None
        }
        total_test_in_input = 0
        for day in context_of_input_data.values():
            total_test_in_input += day["total"]
        if int(input_total_reported_numbers) != total_test_in_input:
            response = {
                "status": False,
                # The sum of all entries in days does not correspond to the total of all days' total entries. Please fill in correctly!
                "message": f"Die Summe aller Buchungen in Tagen entspricht nicht der Summe aller Buchungen aller Tage. Bitte richtig ausfüllen!",
                "dataframe": None
            }
            return response

        for day_key, day_value in context_of_input_data.items():
            total = sum(day_value.values()) - day_value['total']
            if total != day_value['total']:
                response = {
                    "status": False,
                    # Please enter the values ​​correctly as the total number of "Test Reasons" entries is greater than the number of entries on day 7.
                    "message": f"Bitte geben Sie die Werte korrekt ein, da die Gesamtzahl der „Testgründe“-Einträge größer ist als die Anzahl der Einträge am {day_key}. Tag.",
                    "dataframe": None
                }
                return response

        dataframe = working_df[:int(input_total_reported_numbers)]
        final_df = pd.DataFrame()
        initial_index = 0

        for day_key, day_value in context_of_input_data.items():
            final_index = day_value['total'] + initial_index
            req_df_of_one_day = dataframe[initial_index:final_index]
            initial_index = final_index
            if len(req_df_of_one_day) == 0:
                continue
            res_of_date_time_test_reasons_test_handler = date_time_test_reasons_test_handler(
                req_df_of_one_day, opening_time, closing_time, day_value, day_key, month_value, year_value)
            if res_of_date_time_test_reasons_test_handler['status'] == False:
                response = {
                    "status": False,
                    "message": res_of_date_time_test_reasons_test_handler['message'],
                    "dataframe": None
                }
                return response
            output_df = res_of_date_time_test_reasons_test_handler['dataframe']
            
            final_df = pd.concat([final_df, output_df])
        final_df = final_df.reset_index(drop=True)
        response = {
            "status": True,
            "message": "Successful!",
            "dataframe": final_df
        }
        return response
    except Exception as e:
        print("Something went wrong in required_df_generator")


def date_time_test_reasons_test_handler(req_df, opening_time, closing_time, context_of_one_day, day_value, month_value, year_value):
    """
    Generate df by analysing data of date, time and test reasons

    Args:
        req_df : dataframe of single day data
        context_of_one_day : input fields data of one day of test reasons and it's total
        day_value : day value
        opening_time : opening time of test stations
        closing_time : closing time of test stations
        context_of_one_day : input fields data of one day test reasons and it's total
        month_value : month value
        year_value : year value

    """
    try:
        response = {
            "status": False,
            "message": "Etwas ist schief gelaufen !",
            "dataframe": None
        }
        """
        for test reasons
        """
        response_test_reasons_handler = test_reasons_handler(
            req_df, context_of_one_day, day_value)
        if response_test_reasons_handler['status'] == False:
            response = {
                "status": False,
                "message": "Etwas ist schief gelaufen !",
                "dataframe": None
            }
            return response
        df_after_test_reasons_filter = response_test_reasons_handler['dataframe']

        """
        for time and date filter
        """
        if len(day_value) == 2:
            date_value = f"{day_value}.{month_value}.{year_value}"
        else:
            date_value = f"0{day_value}.{month_value}.{year_value}"
        df_after_test_reasons_filter["getestet am"] = df_after_test_reasons_filter['getestet am'].apply(
            lambda x: date_value)
        response_of_two_min_filter = two_minutes_filter_and_shift_timing_feature(
            df_after_test_reasons_filter, opening_time,  closing_time, day_value)
        if response_of_two_min_filter['status'] == False:
            response = {
                "status": False,
                "message": response_of_two_min_filter['message'],
                "dataframe": None
            }
            return response
        resultant_df = response_of_two_min_filter["dataframe"]
        response = {
            "status": True,
            "message": "Successful !",
            "dataframe": resultant_df
        }
        return response
    except Exception as e:
        print("Something went wrong in date_time_test_reasons_test_handler !")


def test_reasons_handler(dataframe, context_of_one_day, day_value):
    """
    Generate the df by analysing data of one day with respect to their desired test reasons and test product

    Args:
        dataframe : dataframe of single day
        context_of_one_day : input fields data of one day of test reasons and it's total
        day_value : day value

    """
    try:
        response = {
            "status": False,
            "message": "Etwas ist schief gelaufen !",
            "dataframe": None
        }
        day_context = {}
        for key, value in context_of_one_day.items():
            if key == 'total':
                continue
            key_value = key.split('_')[1]
            day_context[key_value] = value

        test_reasons_dict = {
            "1": "Besucher, Behandelte oder Bewohner bestimmter Einrichtungen",
            "2": "Nachweis zur Beendigung der Absonderung nach einer Corona Infektion",
            "3": "Besuche in Krankenhäusern und Pflegeheimen",
            "4": "Leistungsberechtigte im Rahmen eines persönlichen Budgets nach § 29 des 9. Buches SGB",
            "5": "Pflegepersonen im Sinne des § 19 Satz 1 des 11. Buches SGB",
            "6": "Teilnahme an klinischen Studien",
            "7": "Kinder bis zum 5. Lebensjahr",
            "8": "Zusammenlebend mit einer an SARS-CoV-2 erkrankten Person",
            "9": "Kontraindikationen zur Durchführung von Covid-19-Impfungen",
            "10": "Veranstaltung im Innenraum",
            "11": "Corona-Warn App Warnung",
            "12": "Kontakt zu einer Person aus einer Risikogruppe",
            "13": "Kontakt zu einer Person über 60 Jahren",
            "14": ""  # self paid
        }
        req_df = pd.DataFrame()
        dataframe_helper = dataframe.copy()
        inital_index = 0
        for index in range(1, 15):
            req_key = str(index)
            if day_context[req_key] == 0:
                continue
            final_index = day_context[req_key] + inital_index
            sliced_df = dataframe_helper[inital_index:final_index]
            inital_index = final_index
            helper_df = sliced_df.copy()
            helper_df["Testgrund"] = helper_df["Testgrund"].apply(
                lambda x: test_reasons_dict[req_key])

            if req_key == '1' or req_key == '2' or req_key == '3' or req_key == '4' or req_key == '5' or req_key == '6' or req_key == '7' or req_key == '8' or req_key == '9':
                test_name = "Kostenloser Corona-Schnelltest (Vulnerable) (Besucher von Pflege- und medizinischen Einrichtungen, Infizierte, Haushaltsangehörige von nachweislich Infizierten,  Studienteilnehmer Schwangere,  Kinder unter 5 Jahren Pflegende Angehörige, Chronisch Kranke)"
            elif req_key == "10" or req_key == '11' or req_key == '12' or req_key == '13':
                test_name = "0,00€ Corona-Schnelltest (3€ entfallen) (Besuch einer Freizeitveranstaltung, Besuch besonders gefährdeter Menschen, Rote Meldung in Corona-Warn-App)"
            else:
                test_name = "Selbstzahler Corona-Schnelltest"

            helper_df["Test"] = helper_df["Test"].apply(
                lambda x: test_name)

            req_df = pd.concat([req_df, helper_df])
        req_df = req_df.reset_index(drop=True)
        response = {
            "status": True,
            "message": "Successful !",
            "dataframe": req_df
        }
        return response
    except Exception as e:
        print("Something went wrong test_reasons_handler !")


def test_nummer_manipulator(dataframe):
    """
    Generating random unique values for testnummer column

    Args:
        dataframe : df which contains whole output data

    """
    try:
        df = dataframe.copy()
        testnummer_col_list = list(dataframe['Testnummer'])
        for index in range(len(dataframe)):
            test_nummer = int(str(random.randrange(10, 20)) +
                              str(random.randrange(111111, 999999)))
            while (test_nummer in testnummer_col_list):
                test_nummer = int(str(random.randrange(10, 20)) +
                                  str(random.randrange(111111, 999999)))
            df.at[index, "Testnummer"] = test_nummer
        print(df)
        return df
    except Exception as e:
        print("Something went wrong in test nummer manipulator")
