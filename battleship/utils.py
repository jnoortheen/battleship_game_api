import msgs

yAxis = "ABCDEFGHIJ"


def getAShip(notation, length):
    """
        return a ship notation
    Args:
        notation (str): a string of size three each character specifying y-axis, x-axis positions and alignment
        length (int): number of squares that the ship will cover

    Returns:
        str: ship notation

    Examples:
        >>> getAShip('A0H', 4)
        'A0A1A2A3'
        >>> getAShip('A0V', 4)
        'A0B0C0D0'
    """
    return getShipDenotation(notation[0], notation[1], length, notation[2])


def getShipDenotation(pos_y, pos_x, length=1, align='H'):
    """
        to deal with square positions on a 10x10 grid. It would fill up in top to down('V') or left to right('H') order.
    Args:
        pos_y (str):  anything from [A-J]
        pos_x (str):  anything from [0-9]
        length (int): length of the ship that the ship will be occupying
        align (str):  alignment one of 'V', 'H'
    Returns:
        str: return the ships occupied squares
    Raises:
        ValueError: when one of the arguments given doesn't meet the requirements
    Examples:
        >>> getShipDenotation('A', '0', 4, 'H')
        'A0A1A2A3'
        >>> getShipDenotation('A', '0', 4, 'V')
        'A0B0C0D0'
        >>> getShipDenotation('C', '0', 3, 'V')
        'C0D0E0'
    """

    pos_x = int(pos_x)

    if pos_y < 'A' or pos_y > 'J' or pos_x < 0 or pos_x > 9:
        raise ValueError('Check given start point! It should be inside grid')
    if length < 1 or length > 5:
        raise ValueError('Check given length of the ship! It must lie between 1 and 5')
    if align not in ('H', 'V'):
        raise ValueError('Check given alignment! It must be one of "H" or "V"')

    ship = ""
    for i in range(length):
        if not pos_y or pos_x > 10:
            raise ValueError('Ship must fit within grids')
        ship += (str(pos_y) + str(pos_x))

        if align == 'H':
            pos_x += 1
        else:
            pos_y = nextCharInYAxis(pos_y)
    return ship


def checkSquarePos(x, y):
    """
        Check whether the given position is a valid point on the grid

    Args:
        x (str): from [0-9]
        y (str): from [A-J]

    Returns:
        None: when the point is valid

    Raises:
        ValueError: when the given point is not valid
    """
    x = int(x)
    if y < 'A' or y > 'J' or x < 0 or x > 9:
        raise ValueError('Check given square position! It should be inside grid')


def reflectAShot(fleets, shots, newShot):
    """
        utility function to record a new guess
    Args:
        fleets (str): fleets
        shots (str): shots that are already have been fired
        newShot (str): new shot

    Returns:
        str: one of 'HIT' or 'MISS' or 'SUNK' or 'SUNK ALL'

    Examples:
        >>> reflectAShot('I0I1I2|J0J1|J8J9|H4', '', 'I0')
        'HIT'
        >>> reflectAShot('I0I1I2|J0J1|J8J9|H4', '', 'H4')
        'SUNK'
        >>> reflectAShot('I0I1I2|J0J1|J8J9|H4', 'J8', 'J9')
        'SUNK'
        >>> reflectAShot('I0I1I2|J0J1|J8J9|H4', 'I0I1I2J8', 'J9')
        'SUNK'
        >>> reflectAShot('I0I1I2|J0J1|J8J9|H4', 'I0I1I2J0J1J8J9', 'H4')
        'SUNK_ALL'
    """
    ships = getShipsFromNotation(fleets)
    shots = {shots[i:i + 2] for i in range(0, len(shots), 2)}
    ret = msgs.ShootResult.MISS
    shipsGotHit = 0
    # filter out the ships which aren't sunk already
    for ship in ships:
        hits = 0
        hitAShip = False
        for pos in ship:
            if pos in shots:
                hits += 1
                continue
            elif newShot == pos:
                hitAShip = True
                ret = msgs.ShootResult.HIT
                hits += 1

        if len(ship) == hits:
            shipsGotHit += 1
            if hitAShip:
                ret = msgs.ShootResult.SUNK

    if shipsGotHit == len(ships):
        ret = msgs.ShootResult.SUNK_ALL

    return str(ret)


def getShipsFromNotation(fleets):
    """
        return ships as a list of sets
    Args:
        fleets (str): ships notation separated by pipe symbol

    Returns:
        list: list of sets (each represents a ship)

    Examples:
        >>> getShipsFromNotation('I0I1I2|J0J1|J8J9|H4')
        [set(['I1', 'I0', 'I2']), set(['J0', 'J1']), set(['J8', 'J9']), set(['H4'])]
        >>> getShipsFromNotation('I0I1I2J0J1J8J9H4')
        [set(['J8', 'J9', 'I1', 'I0', 'I2', 'J0', 'J1', 'H4'])]
    """
    return [{ship[x:(x + 2)] for x in range(0, len(ship), 2)} for ship in fleets.split('|')]


def nextCharInYAxis(aChar):
    """
        return the character next to the current one in the y-axis
    Args:
        aChar (str): a single chanracter

    Returns:
        str:
    Examples:
        >>> nextCharInYAxis('A')
        'B'
        >>> nextCharInYAxis('B')
        'C'
    """
    idx = yAxis.find(aChar)
    if idx != -1 and idx < (len(yAxis) - 1):
        return yAxis[idx + 1]


def shipPtToNotation(pt):
    """
        return self's point notation, convert x's range to start from 0 instead of 1
    Args:
        pt (msgs.ShipPoint):
    Returns:
        str: converted notation of self like A0H, B5V etc
    """
    if pt.x > 10 or pt.x < 1:
        raise ValueError('x Position must fit within 1 to 10')
    return str(pt.y) + str(int(pt.x) - 1) + str(pt.align)
