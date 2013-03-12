import redis
import json
import glob
import sys

def main():
  r = redis.Redis()

  if len(sys.argv) >= 2:
    arduino = sys.argv[1]
  else:
    arduino = glob.glob('/dev/serial/by-id/*')[0]

  with open(arduino, 'r') as serial:
    for _ in xrange(20):
      serial.readline()

    print "start"
    while True:
      parts = serial.readline().strip().split(',')
      print parts
      time = float(parts[0])
      key = parts[1]
      others = parts[2:]
      if key == 'fsr':
        data = [int(x) for x in others]
        data = [data[0:5], data[5:10], data[10:15], data[15:20], data[20:25], data[25:30]]
      else:
        data = [int(x) for x in others]
      print data

      measurement = {
        't' : time,
        'data' : data,
      }
      r.lpush(key, json.dumps(measurement))

if __name__ == '__main__':
  main()
