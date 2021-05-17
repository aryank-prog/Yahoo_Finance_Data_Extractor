import xlsxwriter

def write(puts_dict):
    #create file (workbook) and worksheet
    outWorkbook = xlsxwriter.Workbook("out.xlsx")
    outSheet = outWorkbook.add_worksheet()

    #get titles of columns
    titles = []
    for key in puts_dict.keys():
        titles.append(key)
    
    #declare and gather data
    #lists of columns

    #write headers
    for item in range(len(titles)):
        outSheet.write(0, item, titles[item])

    #write data to file
    for item in range(len(puts_dict[titles[0]])):
        outSheet.write(item+1, 0, puts_dict[titles[0]][item])
        outSheet.write(item+1, 1, puts_dict[titles[1]][item])
        outSheet.write(item+1, 2, puts_dict[titles[2]][item])
        outSheet.write(item+1, 3, puts_dict[titles[3]][item])
        outSheet.write(item+1, 4, puts_dict[titles[4]][item])
        outSheet.write(item+1, 5, puts_dict[titles[5]][item])
        outSheet.write(item+1, 6, puts_dict[titles[6]][item])

    outWorkbook.close()