import csv

# The start and end of the year
start = "01/01/2019 00:00"
end = "12/31/2019 23:45"
meterid = "#1010078552"

# Open the file to read from it
with open('All Intervals Meter #1010078552.csv') as readFile:

    # Initialize reader as a dictionary and set initial values
    csv_reader = csv.DictReader(readFile)
    line_count = 0
    found_start = False
    found_end = False
    datetime = start
    newRows = []

    # Loop through each row in the file
    for row in reversed(list(csv_reader)):
        # Set column labels 
        if(len(newRows) == 0):
            newRows.append(["interval_start", "interval_kWh"])

        # Store values for current and previous dates/times
        previous_datetime = datetime
        datetime = row["interval_start"]
        time = datetime[-5:]
        previous_time = previous_datetime[-5:]
        minutes = int(time[:-3]) * 60 + int(time[-2:])
        previous_minutes = int(previous_time[:-3]) * 60 + int(previous_time[-2:])

        # Start cleaning when we have found the start of the year
        if datetime == start:
            found_start = True
        
        if found_start:
            # Keep iterating until we have found the end of the year
            if found_end == False:
                line_count += 1
                
                # Check for missing rows (TODO: doesn't work if last interval of the day is the one missing)
                if(minutes - previous_minutes > 15):
                    # Calculate the number of missing rows
                    missing_rows = int((minutes - previous_minutes)/15) - 1
                    # Loop to insert missing rows
                    for i in range(missing_rows):
                        # Calculate what the missing rows should be
                        neededMins = minutes - (missing_rows - i)*15
                        missingTime = '{:02d}:{:02d}'.format(*divmod(neededMins, 60))
                        # Create the new row to add (TODO: doesn't work if missing row is index is <260
                        toAdd = [datetime[:-5].strip() + ' ' + missingTime, float(newRows[line_count - 260][1])]
                        newRows.append(toAdd)
                        print("Added row: {}".format(toAdd))
                    print("Location of missing entries: {}".format(line_count))
                
                # Add the current row to the new list of rows
                newRow = [datetime, row["interval_kWh"]]
                newRows.append(newRow)
            
            if datetime == end:
                found_end = True
        
    print("Processed: {} rows".format(line_count))
    print("Length of new file: {} rows".format(len(newRows) - 1))

with open("clean " + meterid + ".csv", 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(newRows)

readFile.close()
writeFile.close()
