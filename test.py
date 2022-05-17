import csv
  
if __name__ == '__main__':

    result_list = [["w"], [1], ["3"]]


    filename = "CSV/test.csv"
    with open(filename, 'w') as csvfile:
        # Creating csv writer object
        csvwriter = csv.writer(csvfile)

        for item in result_list:
            csvwriter.writerow(item)
            csvfile.flush()