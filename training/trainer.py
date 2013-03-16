import glob
import csv
import os
from collections import defaultdict
from pybrain.datasets import ClassificationDataSet
from pybrain.structure import SoftmaxLayer, TanhLayer, SigmoidLayer, LinearLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
import sys
import cPickle as pickle
import subprocess

TRAINING_DIR = os.path.dirname(os.path.realpath(__file__))

POSITIONS = (
  'log',
  'starfish',
  'fetal',
  'fetalalt',
)

HIDDEN_NEURONS = 100
ITERATIONS = 5000

def data_set():
  data_files = glob.glob(os.path.join(TRAINING_DIR, 'data', '*'))
  data = defaultdict(dict)
  for filename in data_files:
    name, position = filename.split('.')[0].split('-')
    with open(filename, 'r') as csv_file:
      reader = csv.reader(csv_file)
      data[os.path.basename(name)][position] = [int(v) for row in reader  for v in row]
  return data

def main():
  ds = ClassificationDataSet(30, class_labels=POSITIONS)

  data = data_set()

  for name, positions in data.iteritems():
    for position, state in positions.iteritems():
      ds.addSample(state, [POSITIONS.index(position)])
  testing_ds, training_ds = ds.splitWithProportion( 0.25 )
  testing_ds._convertToOneOfMany()
  training_ds._convertToOneOfMany()
  ds._convertToOneOfMany()

  hidden = HIDDEN_NEURONS
  net = buildNetwork(ds.indim, hidden, ds.outdim, hiddenclass=SoftmaxLayer)

  trainer = BackpropTrainer(net, training_ds, verbose=True, learningrate=0.01, momentum=0.1)

  trainer.trainEpochs(ITERATIONS)

  wrong = 0
  for name, positions in data.iteritems():
    for position, state in positions.iteritems():
      guess = POSITIONS[net.activate(state).argmax()]
      if guess != position:
        wrong += 1
        print "%10s %10s %10s" % (name, position, guess)
  print 'wrong: ', wrong, '/', len(data) * 4

  out_name = 'network-wrong-%02d-hidden-%d.pickle' % (wrong, hidden)
  print "will save to '%s'" % out_name

  print "Do you want to use this? (y/n): ",
  answer = sys.stdin.readline().strip()
  while answer not in ('y', 'n'):
    print "Enter (y/n): ",
    answer = sys.stdin.readline().strip()

  if answer == 'y':
    with open(out_name, 'w') as f:
      pickle.dump(net, f)
    subprocess.call(['rm', 'network-good.pickle'])
    subprocess.call(['ln', '-s', out_name, 'network-good.pickle'])
    subprocess.call(['touch', os.path.join('..', 'server', 'app.py')])

if __name__ == '__main__':
  main()
