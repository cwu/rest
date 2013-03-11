import csv

def repeat_csv_data(filename):
  with open(filename, "r") as csv_file:
    accel_reader = csv.reader(csv_file, delimeter=",")
    data = [map(int, row) for row in accel_reader]

  i = 0
  while True:
    yield data[i]
    i = (i + 1) % len(data)
