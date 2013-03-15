import redis
import json
import glob
import sys
import serial
import time

def main():
  r = redis.Redis()

  if len(sys.argv) >= 2:
    arduino = sys.argv[1]
  else:
    arduino = glob.glob('/dev/serial/by-id/*')[0]

  s = serial.Serial(arduino, 9600)

  for _ in xrange(20):
    s.readline()
  
  print "start"
  while True:
    parts = s.readline().strip().split(',')
    print parts
    at = float(parts[0])
    key = parts[1]
    others = parts[2:]
    if key == 'fsr':
      data = [int(x) for x in others]
      data = [data[0:5], data[5:10], data[10:15], data[15:20], data[20:25], data[25:30]]
    else:
      data = [int(x) for x in others]
    print data
  
    measurement = {
      'at' : at,
      't' : time.time(),
      'data' : data,
    }
    r.lpush(key, json.dumps(measurement))

if __name__ == '__main__':
  main()
