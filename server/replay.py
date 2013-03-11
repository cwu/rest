import csv

def csv_data(filename):
  with open(filename, "r") as csv_file:
    accel_reader = csv.reader(csv_file)
    data = [map(int, row) for row in accel_reader]

  i = 0
  while True:
    yield {
      'x' : data[i][0],
      'y' : data[i][1],
      'z' : data[i][2],
    }
    i = (i + 1) % len(data)
