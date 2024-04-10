
import random
import operator

old_invos = {
'myo' : [1,2,10],
'blas' : [1,4,12],
'scorp' : [100,100,100],
'frail' : [15,15,35],
'vol' : [9,13,17],
'reentry' : [20,25,40],
'relent' : [30,7,13],
'solar' : [18,11,12],
'bees' : [100,100,100],
'doom' : [100],
'quartet' : [16],
'totemic' : [100],
'dynamic' : [9],
'redflag' : [27]
}

new_invos = {
'myo' : [1,2,8],
'blas' : [1,4,8],
'manti' : [3,8,13],
'frail' : [15,15,35],
'vol' : [9,13,17],
'reentry' : [20,25,40],
'relent' : [3,10,18],
'solar' : [18,11,12],
'bees' : [20,40,60],
'doom' : [20],
'quartet' : [14],
'totemic' : [20],
'dynamic' : [9],
'redflag' : [27]
}

upgradeweight = 6


def pickone(thisrun,invos,round):
    possibles = []
    adj_invos = dict(invos)
    if round < 7:
        del adj_invos['redflag']
        del adj_invos['dynamic']
    elif round == 12:
        del adj_invos['reentry']
        del adj_invos['redflag']
        del adj_invos['dynamic']
    for invo in adj_invos:
        if len(invos[invo]) == 3:
            if thisrun[invo] == 3:
                pass
            elif thisrun[invo] >= 1:
                possibles += [invo for i in range(upgradeweight)]
            elif thisrun[invo] == 0:
                possibles += [invo]
            else:
                raise ValueError('invo tier is too low or high at ' + thisrun[invo])
        elif len(invos[invo]) == 1:
            if thisrun[invo] == 1:
                pass
            elif thisrun[invo] == 0:
                possibles += [invo]
            else:
                raise ValueError(invo + ' invo tier is too low or high at ' + thisrun[invo])
    return random.choice(possibles)

def pickoneofthree(thisrun,invos,round):
    a = pickone(thisrun,invos,round)
    b = a
    while b == a:
        b = pickone(thisrun,invos,round)
    c = b
    while c in [a,b]:
        c = pickone(thisrun,invos,round)
    choices = [a,b,c]
    weights = [invos[k][thisrun[k]] for k in choices]
    #print([(choices[x],thisrun[choices[x]]+1) for x in range(3)])
    if weights[0] <= weights[1] and weights[0] <= weights[2]:
        ret = a
    elif weights[1] <= weights[2]:
        ret = b
    else:
        ret = c
    # print(ret)
    return ret
    

 
              
def fullrun(invos):
    thisrun = {key:0 for key in invos}
    thisrun['blas'] = 1
    for i in range(2,13):
        chosen = pickoneofthree(thisrun,invos,i)
        thisrun[chosen] += 1
    return thisrun

def difficulty(thisrun):
    pts = 0
    for invo in thisrun:
        involevel = thisrun[invo]
        if involevel != 0:
            pts += invos[invo][involevel-1]
    return pts

def sortdict(dct):
    return dict(sorted(dct.items(), key=lambda item: -1 * item[1]))

worst8_new = ['frail','quartet','solar','reentry','bees','doom','totemic','redflag']
best4_new = ['blas','myo','vol','manti']
statsbest4_new = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
stats8_new = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
worst4_new = ['bees','doom','totemic','redflag']
stats4_new = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
avg_new = {}
num_trials = 1000
for i in range(num_trials):
    thisrun1 = fullrun(new_invos)
    count8_new = 0
    count4_new = 0
    countbest4_new = 0
    for key in thisrun1:
        if key not in avg_new:
            avg_new[key] = thisrun1[key]
        else:
            avg_new[key] += thisrun1[key]
        if key in worst4_new:
            count8_new += thisrun1[key]
            count4_new += thisrun1[key]
        elif key in worst8_new:
            count8_new += thisrun1[key]
        elif key in best4_new:
            countbest4_new += thisrun1[key]
        else:
            pass
    stats8_new[count8_new] += 1
    stats4_new[count4_new] += 1
    statsbest4_new[countbest4_new] += 1

for key in avg_new:
    avg_new[key] /= num_trials
print('new: ', sortdict(avg_new))
print('worst 8 which are :', worst8_new, ' taken: ', stats8_new)
print('worst 4 which are :', worst4_new, ' taken: ', stats4_new)
print('best 4 which are :', best4_new, ' taken: ', statsbest4_new)


worst8_old = ['relent','redflag','quartet','reentry','bees','doom','totemic','scorp']
stats8_old = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
worst4_old = ['bees','doom','totemic','scorp']
stats4_old = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
best4_old = ['blas','myo','vol','frail']
statsbest4_old = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
avg_old = {}
for i in range(num_trials):
    thisrun1 = fullrun(old_invos)
    count8_old = 0
    count4_old = 0
    countbest4_old = 0
    for key in thisrun1:
        if key not in avg_old:
            avg_old[key] = thisrun1[key]
        else:
            avg_old[key] += thisrun1[key]
        if key in worst4_old:
            count8_old += thisrun1[key]
            count4_old += thisrun1[key]
        elif key in worst8_old:
            count8_old += thisrun1[key]
        elif key in best4_old:
            countbest4_old += thisrun1[key]
        else:
            pass
    stats8_old[count8_old] += 1
    stats4_old[count4_old] += 1
    statsbest4_old[countbest4_old] += 1
            
for key in avg_old:
    avg_old[key] /= num_trials
print('old: ', sortdict(avg_old))
print('worst 8 which are :', worst8_old, ' taken: ', stats8_old)
print('worst 4 which are :', worst4_old, ' taken: ', stats4_old)
print('best 4 which are :', best4_old, ' taken: ', statsbest4_old)
