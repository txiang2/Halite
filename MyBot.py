from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("<O>_<O>")

def set_interior(unprocessed, check, interior, weights):
    if len(unprocessed) == 0:
        return

    still_unprocessed = []

    for loc in unprocessed:
        if weights[(loc.x + 1) % gameMap.width][loc.y] == check:
            weights[loc.x][loc.y] = check + 1
            interior.append(loc)
        elif weights[loc.x][(loc.y + 1) % gameMap.height] == check:
            weights[loc.x][loc.y] = check + 1
            interior.append(loc)
        elif weights[loc.x][loc.y - 1] == check:
            weights[loc.x][loc.y] = check + 1
            interior.append(loc)
        elif weights[loc.x - 1][loc.y] == check:
            weights[loc.x][loc.y] = check + 1
            interior.append(loc)
        else:
            still_unprocessed.append(loc)

    set_interior(still_unprocessed, check + 1, interior, weights)

def getdamage(loc):
    dmg = 0
    for d in CARDINALS:
        neighborSite = gameMap.getSite(loc, d)
        if neighborSite.owner != myID:
            dmg += 1
            if neighborSite.owner != 0:
                dmg += 1
    return dmg

while True:

    gameMap = getFrame()

    weights = [[0 for y in range(gameMap.height)] for x in range(gameMap.width)]

    interior = []
    border = []
    unprocessed = []

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location =  Location(x, y)
            curr_site = gameMap.getSite(location)
            if curr_site.owner == myID:
                on_border = False
                for d in CARDINALS:
                    neighbor_site = gameMap.getSite(location, d)
                    if neighbor_site.owner != myID and neightbor_site.strength != 255:
                        on_border = True
                        border.append(location)
                        weights[x][y] = 1
                        break
                if on_border == False:
                    unprocessed.append(location)

    set_interior(unprocessed, 1, interior, weights)

    moves = []

    for tile in interior:
        this_site = gameMap.getSite(tile)
        di = 0
        bestVal = -1
        if this_site.strength > this_site.production * 5:
            for d in CARDINALS:
                neighbor = gameMap.getLocation(tile, d)
                if di == 0 or weights[neighbor.x][neighbor.y] < bestval:
                    di = d
                    bestval = weights[neighbor.x][neighbor.y]
        moves.append(Move(tile, di))

    hostile_border = []
    neutral_border = []

    for tile in border:
        hostile = False
        for d in CARDINALS:
            neighbor_site = gameMap.getSite(tile, d)
            if neighbor_site.owner != myID and (neighbor_site.owner != 0 or neighbor_site.strength == 0):
                hostile = True
                break
        if hostile:
            hostile_border.append(tile)
        else:
            neutral_border.append(tile)

    for tile in neutral_border:
        this_site = gameMap.getSite(tile)
        di = 0
        best_prod = -1
        for d in CARDINALS:
            neighbor_site = gameMap.getSite(tile, d)
            if neighbor_site.owner != myID and neighbor_site.strength < this_site.strength and neighbor_site.production > best_prod:
                di = d
                best_prod = neighbor_site.production

        if di == 0 and this_site.strength > this_site.production * 5:
            best_str = 0
            for d in CARDINALS:
                neighbor = gameMap.getLocation(tile, d)
                neighbor_site = gameMap.getSite(neighbor)
                if weights[neighbor.x][neighbor.y] == 1 and neighbor_site.strength > this_site.strength and neighbor_site.strength > best_str:
                    di = d

        moves.append(Move(tile, di))

    for tile in hostile_border:
        this_site = gameMap.getSite(tile)
        di = 0
        best_dmg = 0
        for d in CARDINALS:
            neighbor_site = gameMap.getSite(tile, d)
            if neighbor_site.owner != myID and neighbor_site.owner != 0 and neighbor_site.strength < this_site.strength:
                dmg = 2 + getdamage(gameMap.getLocation(loc, d))
                if dmg > best_dmg:
                    di = d
                    best_dmg = dmg

        moves.append(Move(tile, di))

    sendFrame(moves)
