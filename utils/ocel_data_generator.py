import datetime
import json
import random
from dataclasses import dataclass

from faker import Faker


@dataclass
class OCELGenerator:
    """
    A class used to generate synthetic flights data and save it in an OCEL log
    """

    ocel_filename: str
    number_of_events: int = 100

    def generate_flights_data(self) -> dict:
        """
        Generates synthetic flights data.

        Returns:
            A dictionary representing flights events in OCEL format.
        """

        plane_types = ["Boeing 737", "Airbus A320", "Boeing 747", "Airbus A380"]
        airports = ["JFK", "LAX", "SFO", "ATL", "LHR"]
        delay_probability = 0.2  # probability of a "delayed" event
        faker = Faker()

        flights_data = {
            "ocel:global-event": {"ocel:activity": "__INVALID__"},
            "ocel:global-object": {"ocel:type": "__INVALID__"},
            "ocel:global-log": {
                "ocel:attribute-names": [],
                "ocel:object-types": ["plane", "airport"],
                "ocel:version": "1.0",
                "ocel:ordering": "timestamp"
            },
            "ocel:events": {},
            "ocel:objects": {},
        }

        timestamp = datetime.datetime.now()

        for i in range(self.number_of_events):
            plane = random.choice(plane_types)
            airport = random.choice(airports)
            passenger = faker.name()

            sequence_of_events = ["boarding"]

            if random.random() < delay_probability:
                sequence_of_events.append("delayed")

            sequence_of_events.extend(["departure", "in-flight", "arrival"])

            for event in sequence_of_events:
                event_id = f'e{i+1}'
                timestamp += datetime.timedelta(minutes=random.randint(1, 60))
                flights_data['ocel:events'][event_id] = {
                    "ocel:activity": event,
                    "ocel:timestamp": timestamp.isoformat(),
                    "ocel:omap": [f'p{i+1}', f'a{i+1}'],  # maps to the plane and airport objects
                    "ocel:vmap": {"passenger": passenger}
                }

            # Generate object maps for each plane and airport per event
            flights_data['ocel:objects'][f'p{i+1}'] = {"ocel:type": "plane", "ocel:ovmap": {"model": plane}}
            flights_data['ocel:objects'][f'a{i+1}'] = {"ocel:type": "airport", "ocel:ovmap": {"location": airport}}

        return flights_data

    def save_ocel_log(self, ocel_log: dict, filename: str) -> None:
        """
        Saves an OCEL log to a JSONOCEL file
        """

        with open(filename + ".jsonocel", 'w') as f:
            json.dump(ocel_log, f, indent=4)


    def generate(self) -> None:
        """
        Generates synthetic flights data and saves it in an OCEL log.
        """

        flights_data = self.generate_flights_data()
        self.save_ocel_log(flights_data, self.ocel_filename)
