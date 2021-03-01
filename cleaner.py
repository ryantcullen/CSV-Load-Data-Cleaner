import csv
from datetime import datetime
from datetime import timedelta 

datetime_fmt = '%m/%d/%Y %H:%M'

def ToDateTime(datetime_str):
    return datetime.strptime(datetime_str, datetime_fmt)

# The start and end of the year
start = ToDateTime("1/1/2019 0:00")
end = ToDateTime("12/31/2019 23:45")

meterid = "#1010078549"
newRows = []

def InsertRows(missing_rows):
    # Loop to insert missing rows
    for i in range(missing_rows):
        # Calculate what the missing rows should be
        missing_datetime = (previous_datetime + (i+1)*timedelta(minutes=15)).strftime(datetime_fmt)
        
        # Create the new row to add (TODO: doesn't work if missing row is index is <260
        toAdd = [str(missing_datetime), float(newRows[line_count - 260 + i][1])]
        print("Added row: " + str(toAdd))
        newRows.append(toAdd)

    # Report the index of added missing rows in the new file
    print("Added {} rows".format(missing_rows))
    print("Location of added rows: {}".format(line_count))
    print('---')



# Open the file to read from it
with open('All Intervals Meter ' + meterid + '.csv') as readFile:
    # Initialize reader as a dictionary and set initial values
    csv_reader = csv.DictReader(readFile)
    line_count = 0
    found_start = False
    found_end = False
    current_datetime = start

    # Loop through each row in the file
    for row in reversed(list(csv_reader)):
        # Set column labels 
        if(len(newRows) == 0):
            newRows.append(["interval_start", "interval_kWh"])

        # Store values for current and previous dates/times
        previous_datetime = current_datetime
        current_datetime = ToDateTime(row["interval_start"])

        previous_minutes = int((previous_datetime - start).total_seconds()/60)
        current_minutes = int((current_datetime - start).total_seconds()/60)

        # Start cleaning when we have found the start of the year
        if current_datetime == start:
            found_start = True
        
        if found_start:
            # Keep iterating until we have found the end of the year
            if found_end == False:
                line_count += 1
                minute_difference = current_minutes - previous_minutes


                # Check if there is missing rows
                if(minute_difference > 15):
                    missing_rows = int((minute_difference/15) - 1)
                    InsertRows(missing_rows)
                
                # Add the current row to the new list of rows (if not a duplicate)
                if(minute_difference != 0):
                    newRow = [current_datetime, row["interval_kWh"]]
                    newRows.append(newRow)
            
            # Set 'True' if we have reached the end of the year
            if current_datetime == end:
                found_end = True
    
    # Report on the number of orignial rows processed, and the new number of rows after cleaning
    print("Processed: {} rows".format(line_count))
    print("Length of new file: {} rows".format(len(newRows) - 1))

# Write to the new file
with open("clean " + meterid + ".csv", 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(newRows)

# Close both files
readFile.close()
writeFile.close()
