from model.model import Model

myModel = Model()
myModel.buildGraph()

print("Nodi", myModel.getNumNodes(), "; Archi", myModel.getNumEdges())

myModel.getInfoConnessa(1234)