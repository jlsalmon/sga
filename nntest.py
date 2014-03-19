from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError
from pybrain.structure.modules   import LinearLayer
from scipy import diag, arange, meshgrid, where
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot


with open('classifier/data/data3.txt', 'r') as f:
    info_line = f.readline().split()
    data = [map(float, line.rstrip().split()) for line in f]
    # outputs = [[gene[-1]] for gene in data]
    # for gene in data:
    #     del gene[-1]

ds = ClassificationDataSet(6, 1)

for i, gene in enumerate(data):
    ds.addSample(gene[:-1], gene[-1])

tstdata, trndata = ds.splitWithProportion( 0.25 )

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

print ds.calculateStatistics()
print ds.nClasses

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]


fnn = buildNetwork( trndata.indim, 7, trndata.outdim, outclass=LinearLayer )

trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

#
# ticks = arange(-3.,6.,0.2)
# X, Y = meshgrid(ticks, ticks)
# # need column vectors in dataset, not arrays
# griddata = ClassificationDataSet(6,1, nb_classes=2)
# for i in xrange(X.size):
#     griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
# griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy


for i in range(20):
    trainer.trainEpochs( 1 )
    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

    # out = fnn.activateOnDataset(griddata)
    # out = out.argmax(axis=1)  # the highest output activation gives the class
    # out = out.reshape(X.shape)

#     figure(1)
#     ioff()  # interactive graphics off
#     clf()   # clear the plot
#     hold(True) # overplot on
#     for c in [0,1,2]:
#         here, _ = where(tstdata['class']==c)
#         plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
#     # if out.max()!=out.min():  # safety check against flat field
#     #     contourf(X, Y, out)   # plot the contour
#     ion()   # interactive graphics on
#     draw()  # update the plot
#
# ioff()
# show()
