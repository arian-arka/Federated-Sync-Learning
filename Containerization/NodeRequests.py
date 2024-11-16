import json
import time

from NodeRequest import concurrentNodeRequests, areAllResponsesValid


#################################
## locking nodes
##

def lockNodes(nodes, lock):
    print('{} nodes'.format('Locking' if lock else 'Unlocking'))

    url = '/trainer/lock'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {'lock': lock}
        } for node in nodes
    ]

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('{} failed'.format('Locking' if lock else 'Unlocking'))

    print('{} nodes done'.format('Locking' if lock else 'Unlocking'))


#################################
## waiting for fast api servers to be ready to serve
## it means initialzing ml models,... and at the end the fast api server

def waitForNodesToBeReady(nodes):
    print('Waiting for nodes to be ready at first')

    url = '/health/check'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'GET',
        } for node in nodes
    ]

    while not areAllResponsesValid(concurrentNodeRequests(reqs), lambda x: x['ok'] is True):
        time.sleep(1.5)

    print('Nodes are ready')


#################################
## transferring initial data

def transferInitData(nodes):
    print('Transferring initialized data')

    url = '/trainer/init'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'data': json.dumps(node.initialization),
            'headers': {
                'Content-Type': 'application/json'
            }
        } for node in nodes
    ]

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('Transferring initial data failed')
        exit(1)

    print('Initialized data are ready')


#################################
## transferring datasets

def transferDatasets(nodes, datasets):  # datasets must be list of stringified jsons
    print('Transferring datasets')

    url = '/trainer/dataset'
    reqs = [
        {
            'url': nodes[i].env['self_url'] + url,
            'method': 'POST',
            'data': datasets[i],
            'headers': {
                'Content-Type': 'application/json'
            }
        } for i in range(len(nodes))
    ]

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('Transferring datasets failed')
        exit(1)

    print('Transferring datasets are ready')


#################################
## check if all nodes are ready

def areNodesReady(nodes):
    print('Waiting for nodes to be ready')

    url = '/trainer/ready'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'GET',
        } for node in nodes
    ]

    while not areAllResponsesValid(concurrentNodeRequests(reqs), lambda x: x['ok'] is True):
        time.sleep(1.5)
    print('Nodes are ready')


#################################
## init round before processing
def initRound(nodes, r):
    print('Initializing round', r)

    url = '/trainer/round/init'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('Initializing round', r, 'failed')
        exit(1)

    print('Round', r, 'initialized')


# then wait for "areNodesReady"


#################################
## Calculation of round
def calculateRound(nodes, r):
    print('Calculating round', r)

    url = '/trainer/round/calculate'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    lockNodes(nodes, True)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('calculation round', r, 'failed')
        exit(1)

    lockNodes(nodes, False)

    totalWaitTime = int(nodes[0].env['allowed_calculation_seconds'])

    print('Waiting for {} seconds for calculation ...'.format(totalWaitTime))

    time.sleep(totalWaitTime)

    print('Round', r, 'calculation done')

    time.sleep(1)


# then wait for "areNodesReady"
#################################
## Communication of round
def communicateRound(nodes, r):
    print('Communicate round', r)

    url = '/trainer/round/communicate'

    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    lockNodes(nodes, True)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('communication round', r, 'failed')
        exit(1)

    lockNodes(nodes, False)

    totalWaitTime = int(nodes[0].env['allowed_communication_seconds'])

    print('Waiting for {} seconds for communication ...'.format(totalWaitTime))

    time.sleep(totalWaitTime)

    print('Round', r, 'communication done')

    time.sleep(1)


# then wait for "areNodesReady"
#################################
## Aggregarion of round
def aggregateRound(nodes, r):
    print('Aggregate round', r)

    url = '/trainer/round/aggregate'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    lockNodes(nodes, True)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('aggregation round', r, 'failed')
        exit(1)

    lockNodes(nodes, False)

    totalWaitTime = int(nodes[0].env['allowed_aggregation_seconds'])

    print('Waiting for {} seconds for aggregation ...'.format(totalWaitTime))

    time.sleep(totalWaitTime)

    print('Round', r, 'aggregation done')

    time.sleep(1)

# then wait for "areNodesReady"
#################################
## Test of round
def calculationTestRound(nodes, r):
    print('Test calculation round', r)

    url = '/trainer/round/test/train'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    lockNodes(nodes, True)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('test calculation round', r, 'failed')
        exit(1)

    lockNodes(nodes, False)

    totalWaitTime = int(nodes[0].env['allowed_test_of_train_seconds'])

    print('Waiting for {} seconds for test calculation ...'.format(totalWaitTime))

    time.sleep(totalWaitTime)

    print('Round', r, 'calculation test done')

    time.sleep(1)

# then wait for "areNodesReady"
#################################
## Test of round
def aggregationTestRound(nodes, r):
    print('Test aggregation round', r)

    url = '/trainer/round/test/aggregation'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'POST',
            'json': {
                'round': r
            }
        } for node in nodes
    ]

    lockNodes(nodes, True)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('test aggregation round', r, 'failed')
        exit(1)

    lockNodes(nodes, False)

    totalWaitTime = int(nodes[0].env['allowed_test_of_aggregation_seconds'])

    print('Waiting for {} seconds for test aggregation ...'.format(totalWaitTime))

    time.sleep(totalWaitTime)

    print('Round', r, 'aggregation test done')

    time.sleep(1)

#################################
## Finish training

def finishTraining(nodes):
    print('Waiting for nodes to be finished')

    url = '/trainer/finish'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'GET',
        } for node in nodes
    ]

    while not areAllResponsesValid(concurrentNodeRequests(reqs)):
        time.sleep(1.5)

    print('Nodes are done')


#################################
## Gather logs

def gatherLogs(nodes, saveTo=None):
    print('Gathering logs')

    url = '/logs/gather'
    reqs = [
        {
            'url': node.env['self_url'] + url,
            'method': 'GET',
        } for node in nodes
    ]

    results = concurrentNodeRequests(reqs)

    if not areAllResponsesValid(concurrentNodeRequests(reqs)):
        print('Gathering logs failed')
        return None
    else:
        if saveTo:
            print('Saving logs to ', saveTo)
            f = open(saveTo, 'w')
            f.write(json.dumps(results))
            f.close()

        print('Logs are done')
        return results
