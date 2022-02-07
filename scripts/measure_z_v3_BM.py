
# Version for Black Pill programmed with Rust and String-Actuator configuration

#from javax.script import ScriptEngineManager
import time

# print "guguss"
# print('dir machine {}'.format(dir(machine)))
# print('dir machine.actuators {}'.format(dir(machine.actuators)))
# print('locals: {}'.format(locals()))

# print('locals.actuateBoolean: {}'.format(locals()['actuateBoolean']))

#for ite in machine.actuators:
#    print ite.read()
#machine.actuators[2].read()

#for symbol, value in locals().items():
#    print symbol,

def read():
    print('read() called')
    return 1

def actuate(val):
    print('actuate() called')
    print val

# machine.actuators[2].read = read


############## BOILER PLATE #################
# boiler plate to get access to psypnp modules, outside scripts/ dir
import os.path
import sys
python_scripts_folder = os.path.join(scripting.getScriptsDirectory().toString(),
                                      '..', 'lib')
sys.path.append(python_scripts_folder)

# setup globals for modules
import psypnp.globals
psypnp.globals.setup(machine, config, scripting, gui)

############## /BOILER PLATE #################
from org.openpnp.model import LengthUnit, Location
from org.openpnp.model import Length
#Length(22, LengthUnit.Millimeters)
#from org.openpnp.model import LengthUnit

import psypnp

def main():
    #set_feeder_heigth_test()
    #set_hight_test()
    set_stripe_feeder_height("Strips")
    #nozzle = machine.defaultHead.getNozzleByName('N2')
    #position = Location(LengthUnit.Millimeters,100,100,0,0)
    #measure_height(nozzle, position)
    pass

def set_allfeeder_heigt():
    pass

def measureHeithByStepSize(nozzle, hightActuator, zStartTest, stepsize, position):
    # read a one to reset, if there is one pending, just in case
    hightActuator.read()

    for pos in range(0,2000):
        nextTestheightMeasureLoc = Location(position.getUnits(),
                                            position.getX(),
                                            position.getY(),
                                            float(zStartTest-(pos*stepsize)),
                                            0)
        nozzle.moveTo(nextTestheightMeasureLoc)
        # add test if surface hit by sensor
        #time.sleep(0.1)
        val = int(hightActuator.read())
        print "hightActuator val: ", val, type(val)
        if val == 1:
            nozzle.moveTo(position)
            hightActuator.actuate(False)
            return zStartTest-(pos*stepsize)

def measure_height(nozzle, position):
    print "measure_height() called"
    # hightActuator = nozzle.getHead().getActuatorByName('3dTouch') # ('Z-Probe')
    hightActuator = nozzle.getHead().getActuatorByName('3dTouch_BM') # ('Z-Probe')
    # print hightActuator.name
    # hightActuator = machine.getActuatorByName('Z-Probe')
    if hightActuator == None:
        print "invalied actuator name"
    else:
        print hightActuator.name
    hightActuator.actuate(True)
    #time.sleep(2)
    #hightActuator.actuate(False)
    print dir(hightActuator), hightActuator.valueType
    #time.sleep(2)
    #hightActuator.actuate(True)
    #time.sleep(2)
    zStartTest = position.getZ()
    # Test with 1mm steps
    heightOfMeasurement = measureHeithByStepSize(nozzle, hightActuator, zStartTest, 1, position)
    posNow = position.getZ()
    print "heightOfMeasurement", heightOfMeasurement, "posNow", posNow

    nextTestheightMeasureLoc = Location(position.getUnits(),
                                            position.getX(),
                                            position.getY(),
                                            float(heightOfMeasurement + 2.0),
                                            0)
    # move up 2 mm
    nozzle.moveTo(nextTestheightMeasureLoc)
    zStartTest = nextTestheightMeasureLoc.getZ()
    hightActuator.actuate(False)
    time.sleep(0.2)
    hightActuator.actuate(True)

    # measure with 0.01mm precistion
    heightOfMeasurement = measureHeithByStepSize(nozzle, hightActuator, zStartTest, 0.01, position)

    return heightOfMeasurement
    # for pos in range(0,2000):
    #     nextTestheightMeasureLoc = Location(position.getUnits(),
    #                                         position.getX(),
    #                                         position.getY(),
    #                                         float(zStartTest-(pos*0.05)),
    #                                         0)
    #     nozzle.moveTo(nextTestheightMeasureLoc)
    #     # add test if surface hit by sensor
    #     val = int(hightActuator.read())
    #     print "hightActuator val: ", val, type(val)
    #     if val == 1:
    #         nozzle.moveTo(position)
    #         hightActuator.actuate(False)
    #         return zStartTest-(pos*0.05)
    #     #if pos == 1000:
    #     #    return zStartTest-(pos*0.05)


def measure_feeder_height(afeeder):
    print "measure_feeder_height() called"
    picLocation = afeeder.getPickLocation()
    xloc = picLocation.getX()
    yloc = picLocation.getY()
    heightMeasureLoc = Location(picLocation.getUnits(), xloc, yloc, -25, 0)
    # Position sensor over pick location
    machine.defaultHead.moveToSafeZ()
    print "Nozzles", machine.defaultHead.getNozzles()
    # machine.defaultHead.defaultNozzle.moveTo(heightMeasureLoc)
    # nozzle2 = machine.defaultHead.getNozzle('N1')
    # nozzle2 = machine.defaultHead.getNozzles()[1]
    nozzle2 = machine.defaultHead.getNozzleByName('N2')
    print nozzle2.id, nozzle2.name
    nozzle2.moveTo(heightMeasureLoc)

    # run height detection
    height_measured = measure_height(nozzle2, heightMeasureLoc)
    print "measrued height:", height_measured
    # return measured height
    return height_measured

def set_stripe_feeder_height(name):
    print "###############################################3"
    for afeeder in machine.getFeeders():
        # print afeeder.getClass().__name__
        if afeeder.getClass().__name__ == 'ReferenceStripFeeder' and afeeder.isEnabled(): #'org.openpnp.machine.reference.feeder.ReferenceStripFeeder':
            print afeeder.getName()
            print dir(afeeder)
            if afeeder.getName().find(name) >= 0:
                print afeeder.getName()
                feeder_height = measure_feeder_height(afeeder)
                # time.sleep(2)
                refHole = afeeder.getReferenceHoleLocation()
                nextHole = afeeder.getLastHoleLocation()
                if feeder_height > 0:
                    print "Error wrong hight greater than -5"
                    return
                afeederhight = float(feeder_height)
                afeederHeightLength = Length(afeederhight, LengthUnit.Millimeters)
                if refHole is None or not refHole:
                    print("A feed has no reference hole... hum")
                else:
                    newLoc = Location(refHole.getUnits(),
                                        refHole.getX(),
                                        refHole.getY(),
                                        afeederhight,
                                        refHole.getRotation())
                    afeeder.setReferenceHoleLocation(newLoc)

                if nextHole is None or not nextHole:
                    print("A feed has no reference hole... hum")
                else:
                    newLoc = Location(refHole.getUnits(),
                                        nextHole.getX(),
                                        nextHole.getY(),
                                        afeederhight,
                                        refHole.getRotation())
                    afeeder.setLastHoleLocation(newLoc)
        else:
            continue



def set_feeder_heigth_test():
    print "machine", dir(machine)
    print "machine.getHeads", machine.getHeads()
    print "Nozzles", machine.getHeads()[0].getNozzles()
    print machine.getFeeders()
    for feeder in machine.getFeeders():
        print feeder

    for el in dir(machine.getFeeders()[0]):
        print el

    print "location", machine.getFeeders()[0].getLocation()
    print type(machine.getFeeders()[0].getLocation())
    loc = machine.getFeeders()[0].getLocation()
    print type(loc.z)
    # getPickLocation() returns x, y, z, rotation along y increase = 180°
    print "Picklocation", machine.getFeeders()[0].getPickLocation()
    print "Picklocation_var", machine.getFeeders()[0].pickLocation

    # newloc = Location(LengthUnit.Millimeters, 20, 30, -11.0, 270.0);
    # machine.getFeeders()[0].setLocation(newloc)
    # print "location", machine.getFeeders()[0].getLocation()
    #machine.getFeeders()[0].prepareForJob(True)
    # getPickLocation() returns x, y, z, rotation along y increase = 180°
    print "Picklocation", machine.getFeeders()[0].getPickLocation()
    print "Picklocation_var", machine.getFeeders()[0].pickLocation
    #machine.getFeeders()[0].pickLocation = newloc

    afeeder = machine.getFeeders()[1]
    if afeeder.isEnabled():
        refHole = afeeder.getReferenceHoleLocation()
        nextHole = afeeder.getLastHoleLocation()
        afeederhight = float(-12)
        afeederHeightLength = Length(afeederhight, LengthUnit.Millimeters)
        if refHole is None or not refHole:
            print("A feed has no reference hole... hum")
        else:
            newX = refHole.getX()
            newY = refHole.getY()
            newLoc = Location(refHole.getUnits(), newX, newY, afeederhight, refHole.getRotation())
            afeeder.setReferenceHoleLocation(newLoc)

        if nextHole is None or not nextHole:
            print("A feed has no reference hole... hum")
        else:
            newXnext = nextHole.getX()
            newYnext = nextHole.getY()
            newLoc = Location(refHole.getUnits(), newXnext, newYnext, afeederhight, refHole.getRotation())
            afeeder.setLastHoleLocation(newLoc)
        print "afeeder Picklocation", afeeder.getPickLocation()
        print "afeeder location", afeeder.getLocation()
        print "afeeder getHolePitch()", afeeder.getHolePitch()
        print "afeeder getLastHoleLocation() ", afeeder.getLastHoleLocation()
        print "afeeder getPartPitch() ", afeeder.getPartPitch()
        print "afeeder getReferenceHoleLocation() ", afeeder.getReferenceHoleLocation()
        print "afeeder getReferenceHoleToPartLinear() ", afeeder.getReferenceHoleToPartLinear()
        print "afeeder getIdealLineLocations()", afeeder.getIdealLineLocations()
        print "afeeder canTakeBackPart()", afeeder.canTakeBackPart()

    gui.getFeedersTab().repaint()

def set_hight_test():
    heightval = float(0.6)
    height = Length(heightval, LengthUnit.Millimeters)
    print "Parts", config.getParts()
    allParts = config.getParts()
    for part in allParts:
        print part.id
        print part.name
        print part.height
        part.height = height
        # or
        part.setHeight(height)
        print part.getPackage()


main()
