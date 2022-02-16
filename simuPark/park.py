from math import gamma
from random import choice
from typing import Callable
from simuPark.person import Person, Archetype
from simuPark.constants import ACTIVITIES, ARCHETYPES, ATTRACTIONS
import numpy as np


class Queue:
    def __init__(self, type: str = "NORMAL") -> None:
        self.type: str = type
        self.waitTime: int = 0
        self.topWaitTime: int = 0
        self.inQueue: list[Person] = []

    def serve(self, name: str, nPeople: int, duration: int):
        # In this scenario, the number of people in queue is less or the same as the
        # service rate of the attraction, everyone on the queue is served.
        if nPeople > len(self.inQueue):
            nPeople = len(self.inQueue)

        for _i in range(nPeople):
            person: Person = self.inQueue.pop(0)
            person.rideAttraction(name=name, duration=duration)

    def addToQueue(self, person: Person):
        self.inQueue.append(person)

    def _updateWaitTime(self, serviceRate: int):
        newWaitTime = 5 * round((len(self.inQueue) / (serviceRate / 60)) / 5)
        self.topWaitTime = max(newWaitTime, self.waitTime)
        self.waitTime = newWaitTime


class Activity:
    def __init__(self, name: str, popularity: int, duration: int) -> None:
        self.name: str = name
        self.duration: int = duration
        self.popularity: int = popularity


class Attraction(Activity):
    def __init__(
        self,
        name: str,
        popularity: int,
        duration: int,
        serviceRate: int,
        altQueue: str = None,
    ) -> None:
        super().__init__(name, popularity, duration)
        self.serviceRate: int = serviceRate
        self.fakeWaitTime: int = 0
        self.queue: Queue = Queue()
        if altQueue in ["DFP", "SFP"]:
            self.altQueue: Queue = Queue(type=altQueue)

    def serve(self):
        # We calculate the amount of people the attraction can serve each minute
        nPeopleToServe = int(np.floor(self.serviceRate / 60))
        # We tell out Queue to serve the amount of people given
        # And the duration of the ride
        self.queue.serve(name=self.name, nPeople=nPeopleToServe, duration=self.duration)

    def addToQueue(self, person: Person, queue: str):
        if queue == "NORMAL":
            self.queue.addToQueue(person)
        else:  # queue in ["DFP", "SFP"]
            self.altQueue.addToQueue(person)

    def serveWithFastPass(self):
        pass

    def updateWaitTime(self):
        pass

    def updateFakeWaitTime(self):
        pass


class Park:
    def __init__(
        self,
        attrDict: dict[str, dict] = ATTRACTIONS,
        activitiesDict: dict[str, dict] = ACTIVITIES,
        archetypeDict: dict[str, dict] = ARCHETYPES,
        function: Callable = lambda x, k: np.power(k, x) * np.exp(-k) / gamma(x + 1),
        altQ: str = None,
        hoursOpen: int = 11,
    ) -> None:
        self.currentTime: int = 0
        self.closingTime: int = 60 * hoursOpen
        self.attractions: list[Attraction] = self._handleAttractions(attrDict, altQ)
        self.activities: list[Activity] = self._handleActivities(activitiesDict)
        self.guestArchetypes: list[Archetype] = self._handleArchetypes(archetypeDict)
        self.guests: list[Person] = []
        self.function: Callable[[int], float] = function

    def startDayBase(self, totalGuests: int) -> None:
        # Day starts, time starts running minute pero minute depending in the
        # hours open
        for minute in range(self.closingTime):
            # ✌Every minute, the park receives guests
            self._receiveGuests(totalGuests=totalGuests, time=minute)

            # Every 5 minutes, all queue times update for the guests to check
            if minute % 5 == 0:
                self._updateWaitTimes()

            for guest in self.guests:
                # print(f"Guest id : {guest.id}")
                guest.checkLeavePark(minute)
                # This case is the 'left the park' state, they're skipped
                if guest.timeLeftInActivity == -2:
                    # print("left park")
                    continue

                # In this case, the guest is in a queue, they're are skipped
                # as they're not able to change selections. TotalWaitTime increases.
                elif guest.timeLeftInActivity == -1:
                    # print("On queue")
                    guest.totalWaitTime += 1

                # On this case, the guest is currently doing an activity
                # or riding an attraction. Time passes.
                elif guest.timeLeftInActivity > 0:
                    # print("Doing activity")
                    guest.timeLeftInActivity -= 1

                # In this scenario, they're looking for something to do
                # They're free to choose based on their archetype
                elif guest.timeLeftInActivity == 0:
                    selection = guest.chooseWhatToDo(self.activities, self.attractions)
                    if isinstance(selection, Attraction):
                        guest.checkAttraction(selection)
                        # guest.doActivity(selection.name, selection.duration)
                        # print("Chose attraction")
                    elif isinstance(selection, Activity):
                        # print("Chose activity")
                        guest.doActivity(selection.name, selection.duration)

                    guest.choicesMade += 1
                # print(f"Choices made: {guest.choicesMade}")
                # print("")

            self._serveGuests()

    def _handleArchetypes(self, archetypeDict: dict[str, dict]) -> list[Archetype]:
        # setArchetypes handles the creation of the archetypes
        # to be used during the simulation.

        if not bool(archetypeDict):
            raise IndexError("Dictionary is Empty") from None

        archetypeList: list[Archetype] = []

        for name, details in archetypeDict.items():
            archetype: Archetype = Archetype(
                name=name,
                attractionChance=details.get("AttractionPercentage"),
                maxStay=details.get("MaxStayTime"),
                minStay=details.get("MinStayTime"),
                maxWaitTime=details.get("MaxWaitTime"),
                minWaitTime=details.get("MinWaitTime"),
            )
            archetypeList.append(archetype)

        return archetypeList

    def _handleActivities(self, activityDict: dict[str, dict]) -> list[Activity]:
        if not bool(activityDict):
            raise IndexError("Dictionary is Empty") from None

        activityList: list[Archetype] = []

        for name, details in activityDict.items():
            activity: Activity = Activity(
                name=name,
                duration=details.get("Duration"),
                popularity=details.get("Popularity"),
            )
            activityList.append(activity)

        return activityList

    def _handleAttractions(
        self, attractionDict: dict[str, dict], atlQueue: str = None
    ) -> list[Attraction]:
        if not bool(attractionDict):
            raise IndexError("Dictionary is Empty") from None

        attractionList: list[Archetype] = []

        for name, details in attractionDict.items():
            attraction: Attraction = Attraction(
                name=name,
                duration=details.get("Duration"),
                popularity=details.get("Popularity"),
                serviceRate=details.get("ServiceRate"),
                altQueue=atlQueue,
            )
            attractionList.append(attraction)

        return attractionList

    def _receiveGuests(self, totalGuests: int, time: int) -> None:
        # This function is executed everytime a minute passes
        # It handles the creation of each person that visits the park
        randNum = np.random.uniform(low=0, high=1)
        nGuests = int(np.floor(totalGuests / self.closingTime))

        if randNum <= float(self.function(time / 60, 3)):
            for _i in range(nGuests):
                archetype: Archetype = choice(self.guestArchetypes)
                newGuest: Person = Person(len(self.guests), time, archetype)
                self.guests.append(newGuest)

    def _updateWaitTimes(self):
        for attraction in self.attractions:
            attraction.queue._updateWaitTime(serviceRate=attraction.serviceRate)

    def _serveGuests(self):
        for attraction in self.attractions:
            attraction.serve()
