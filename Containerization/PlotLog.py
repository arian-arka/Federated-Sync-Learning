import json
import matplotlib.pyplot as plt
import numpy as np

def readLog():
    f = open('logs.json','r')
    data = json.loads(f.read())
    f.close()
    return data


def nodeCalculatinAccuracyPerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} calculation'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Accuracy')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        lastCalcResult = -1
        y = []
        x = []
        for r in range(1,1+rounds):
            calculation_result = instance['rounds'][r-1]['test_of_train_result']
            if calculation_result is None:
                if lastCalcResult == -1:
                    continue
            x.append(r)
            y.append(calculation_result['score'][1])
            lastCalcResult = calculation_result['score'][1]
            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()

def nodeAggregationAccuracyPerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} aggregation'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Accuracy')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        lastCalcResult = -1
        y = []
        x = []
        for r in range(1,1+rounds):
            calculation_result = instance['rounds'][r-1]['test_of_aggregation_result']
            if calculation_result is None:
                if lastCalcResult == -1:
                    continue
            x.append(r)
            y.append(calculation_result['score'][1])
            lastCalcResult = calculation_result['score'][1]
            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()

def nodeCalculatinTimePerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} calculation time'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Time')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        y = []
        x = []
        for r in range(1,1+rounds):
            calculation_result = instance['rounds'][r-1]['test_of_train_result']
            x.append(r)
            if calculation_result is None:
                y.append(-1)
                continue
            y.append(instance['rounds'][r-1]['calculation_time'])

            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()

def nodeCommunicationTimePerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} communication time'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Time')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        y = []
        x = []
        for r in range(1,1+rounds):
            x.append(r)
            y.append(instance['rounds'][r-1]['communication_time'])

            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()

def nodeAggregatioTimePerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} aggregation time'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Time')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        y = []
        x = []
        for r in range(1,1+rounds):
            calculation_result = instance['rounds'][r - 1]['test_of_train_result']
            x.append(r)
            if calculation_result is None:
                y.append(-1)
                continue
            y.append(instance['rounds'][r-1]['aggregation_time'])

            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()

def nodeTotalTimePerRound(rounds):
    instances = readLog()

    labels = []
    plt.clf()
    plt.xlabel('{} {} total time'.format(rounds,'Rounds' if rounds > 1 else 'Round'))
    plt.ylabel('Time')

    for i in range(len(instances)):
        instance = instances[i]
        name = instance['name']
        y = []
        x = []
        for r in range(1,1+rounds):
            x.append(r)
            y.append(
                instance['rounds'][r-1]['calculation_time']+
                instance['rounds'][r-1]['communication_time']+
                instance['rounds'][r-1]['aggregation_time']
            )

            labels.append(
                (x[len(x) - 1],y[(len(y)-1)],name+'_c')
            )


        plt.step(x, y, label=name+'_a')
        plt.plot(x, y, 'o--', alpha=0.6)


    plt.grid(axis='x', color='0.95')
    plt.legend(title='Nodes')

    plt.show()


rounds = 20
nodeCalculatinAccuracyPerRound(rounds)
nodeAggregationAccuracyPerRound(rounds)
nodeCalculatinTimePerRound(rounds)
nodeCommunicationTimePerRound(rounds)
nodeAggregatioTimePerRound(rounds)
nodeTotalTimePerRound(rounds)
