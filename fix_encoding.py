import csv
import ftfy
import sys

def main(arg1, arg2):
    # input file
    csvfile = open(arg1, "r", encoding = "UTF8")
    reader = csv.DictReader(csvfile)

    # output stream
    outfile = open(arg2, "w", encoding = "Windows-1252") # Windows doesn't like utf8
    writer = csv.DictWriter(outfile, fieldnames = reader.fieldnames, lineterminator = "\n")

    # clean values
    # writer.writeheader()
    for row in reader:
        for col in row:
            row[col] = ftfy.fix_text(row[col])
        writer.writerow(row)

    # close files
    csvfile.close()
    outfile.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))