import time

import NodeRequests

import Dataset

from Properties import properties
from Node import nodes

def workflow(nodes):
    logsPath = properties['logs_path']

    rounds = properties['rounds']

    NodeRequests.waitForNodesToBeReady(nodes)

    NodeRequests.transferInitData(nodes)

    NodeRequests.areNodesReady(nodes)

    for r in range(1,rounds+1):
        NodeRequests.transferDatasets(nodes, [
            Dataset.datasetToJson(d) for d in Dataset.splitDatasets(len(nodes),r)
        ])

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)

        NodeRequests.initRound(nodes, r)

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)

        NodeRequests.calculateRound(nodes, r)

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)
        
        NodeRequests.calculationTestRound(nodes,r)

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)

        NodeRequests.communicateRound(nodes, r)

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)

        NodeRequests.aggregateRound(nodes, r)

        time.sleep(1)

        NodeRequests.aggregationTestRound(nodes,r)

        time.sleep(1)

        NodeRequests.areNodesReady(nodes)

    NodeRequests.finishTraining(nodes)

    time.sleep(1)

    NodeRequests.areNodesReady(nodes)

    NodeRequests.gatherLogs(nodes, logsPath)

