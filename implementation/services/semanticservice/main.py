import grpc 
from implementation.proto.semanticservice import semanticservice_pb2 as pb
from implementation.proto.semanticservice import semanticservice_pb2_grpc as gp
import json
import numpy as np
import datetime 
import time
import os
import io
from concurrent import futures
from absl import flags 
from absl import logging
from absl import app
#Imports for the unit conversion
import rdflib
from implementation.library.omlib.constants import OM_IDS, SI
from implementation.library.omlib.measure import om, Point, Measure
from implementation.library.omlib.omconstants import OM

FLAGS = flags.FLAGS
flags.DEFINE_string("host", "0.0.0.0:8080", "The Hostname of this service")

class Semcheck(gp.SemanticCheckServicer):

    def checkSemantic(self, semantics, context):
        print("Semantic check initialized...")
        error_description = "| "
        conversion_keys = []
        conversion_source = []
        conversion_destination = []
        serverPath = "services/semanticservice/"+semantics.serverName+ "Semantic.json"
        clientString = semantics.semanticDescription
        #python replaces the double quotes with single quotes at some point for some reason 
        clientString = clientString.replace("\'", "\"")
        clientData = json.loads(clientString)

        with open(serverPath) as serverFile:
            serverData = json.load(serverFile)

        #if both files identical nothing needs to be done 
        if serverData != clientData:
            print("something is wrong in client defintion, proceeding with detailed check ")
        else:
            response = pb.ServerResponse(response = True, description = "Check successful ")
            return response

        #chain of if statements to find exact errors within the client configuration 
        #check the included protos first (only ones used by client)
        for proto in clientData:
            if proto not in serverData:
                error_description = error_description+str(proto)+" not used by server | "
                continue
            #now checking the messages inside every proto
            for message in serverData[proto]:
                if (message not in clientData[proto]):
                    error_description = error_description+str(message)+" not defined in client | "
                    continue
                #variables used in each message
                for variable in serverData[proto][message]:
                    if(message in clientData[proto]) and (variable not in clientData[proto][message]):
                        error_description = error_description+str(variable)+ " not defined in client | "
                        continue
                    
                    #lastly semantic values of the variables
                    serverValue = serverData[proto][message].get(variable)
                    clientValue = clientData[proto][message].get(variable)
                    if  serverValue != clientValue :
                        #add the current message component with the correct server semantic to the converison list
                        conversion_keys.append(variable)
                        #currently whole URI, slice with [58:] if needed 
                        conversion_source.append(clientValue)
                        conversion_destination.append(serverValue)
                        error_description = error_description+"client uses: "+str(clientValue)+" but should be using: "+str(serverValue) + " for " + message + ": " + variable + " "

        conversion_list = pb.ConversionList(keys = conversion_keys, source = conversion_source, destination = conversion_destination)
        response = pb.ServerResponse(response = False, description = error_description, conversionList = conversion_list)
        return response

    #Unit conversion with omlib, seems not work properly
    #Conversion possible if both values UNIT from same DIMENSION 
    #Dimensions: Time, Length, Mass, Electric, Thermodynamic, Substance, Luminous; (SI)
    # def unitConversion(self, request, context):
    #     values = request.values
    #     keys = request.conversionList.keys
    #     source = request.conversionList.source
    #     destination = request.conversionList.destination 
    #     convertedValues = []

    #     for i in range(0,len(values)):
    #         omValue = om(values[i], OM.metre)
    #         omValue.convert(destination[i])
    #         convertedValues.append(omValue.numericalValue)

    #     response = pb.ConversionRequest()
    #     response.conversionList.CopyFrom(request.conversionList)
    #     response.values = convertedValues
    #     return response

    def unitConversion(self, request, context):
        values = request.values
        keys = request.conversionList.keys
        source = request.conversionList.source
        destination = request.conversionList.destination
        convertedValues = []
        response = pb.ConversionRequest()
        response.conversionList.CopyFrom(request.conversionList)

        g = rdflib.Graph()
        g.parse('http://www.qudt.org/2.1/vocab/unit')

        for i in range(0, len(source)):

            queryString = """SELECT ?o  WHERE{
            """+source[i]+ """ qudt:conversionMultiplier ?o .
            }  """
            res = g.query(queryString)
            for row in res:
                mult = float(row[0])
                print(type(mult))
            
            if(mult >= 0):
                val = values[i]*mult
            else:
                val = values[i]/mult

            queryString = """SELECT ?o  WHERE{
                """+destination[i]+ """ qudt:conversionMultiplier ?o .
            }  """
            res = g.query(queryString)
            for row in res:
                mult = float(row[0])

            if(mult >= 0):
                val = val/mult
            else:
                val = val*mult

            convertedValues.append(val)
        
        response.values.extend(convertedValues)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    gp.add_SemanticCheckServicer_to_server(Semcheck(),server)
    server.add_insecure_port(FLAGS.host)
    server.start()
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)

def main(argv):
    logging.info("Starting GRPC Server on %s" %FLAGS.host)
    serve()

if __name__ == '__main__':
    app.run(main)
