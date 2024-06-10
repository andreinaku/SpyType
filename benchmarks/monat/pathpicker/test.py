# import screenFlags

# a = screenFlags.ScreenFlags.initFromArgs([])
# b = a.args
# c = b.clean
import pickle
import io
import stateFiles

filePath = stateFiles.getPickleFilePath()
lineObjs = pickle.load(io.open(filePath)) # cheating 'rb'
