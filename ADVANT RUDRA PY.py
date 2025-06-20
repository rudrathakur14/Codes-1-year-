import time
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self, vehicle_number, vehicle_type):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.now()

class ParkingSlot:
    def __init__(self, slot_id, slot_type):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self.is_occupied = False
        self.vehicle = None

    def assign_vehicle(self, vehicle):
        self.is_occupied = True
        self.vehicle = vehicle

    def remove_vehicle(self):
        vehicle = self.vehicle
        self.vehicle = None
        self.is_occupied = False
        return vehicle

class ParkingLevel:
    def __init__(self, level_id, num_car_slots, num_bike_slots, num_truck_slots):
        self.level_id = level_id
        self.slots = []
        self.create_slots('Car', num_car_slots)
        self.create_slots('Bike', num_bike_slots)
        self.create_slots('Truck', num_truck_slots)

    def create_slots(self, slot_type, count):
        for i in range(count):
            slot_id = f"{self.level_id}-{slot_type[0]}-{i+1}"
            self.slots.append(ParkingSlot(slot_id, slot_type))

    def find_available_slot(self, vehicle_type):
        for slot in self.slots:
            if not slot.is_occupied and slot.slot_type == vehicle_type:
                return slot
        return None

    def display_available_slots(self):
        print(f"Level {self.level_id}:")
        for slot in self.slots:
            status = "Free" if not slot.is_occupied else f"Occupied by {slot.vehicle.vehicle_number}"
            print(f"  Slot {slot.slot_id} ({slot.slot_type}): {status}")

class ParkingLot:
    def __init__(self, levels_config):
        self.levels = []
        for config in levels_config:
            level = ParkingLevel(*config)
            self.levels.append(level)
        self.vehicle_map = {}

    def park_vehicle(self, vehicle):
        for level in self.levels:
            slot = level.find_available_slot(vehicle.vehicle_type)
            if slot:
                slot.assign_vehicle(vehicle)
                self.vehicle_map[vehicle.vehicle_number] = slot
                print(f"Vehicle {vehicle.vehicle_number} parked at slot {slot.slot_id}")
                return
        print("Parking Full for", vehicle.vehicle_type)

    def unpark_vehicle(self, vehicle_number):
        slot = self.vehicle_map.get(vehicle_number)
        if not slot:
            print("Vehicle not found!")
            return
        vehicle = slot.remove_vehicle()
        duration = datetime.now() - vehicle.entry_time
        fee = self.calculate_fee(vehicle.vehicle_type, duration)
        print(f"Vehicle {vehicle_number} unparked from slot {slot.slot_id}")
        print(f"Duration: {str(duration)} | Parking Fee: ${fee}")
        del self.vehicle_map[vehicle_number]

    def calculate_fee(self, vehicle_type, duration):
        base_rate = {'Car': 20, 'Bike': 10, 'Truck': 30}
        hours = max(1, duration.seconds // 3600)
        return base_rate.get(vehicle_type, 15) * hours

    def display_parking_lot(self):
        print("=== Parking Lot Status ===")
        for level in self.levels:
            level.display_available_slots()

# --- Main Execution ---
def main():
    # Level config: (level_id, num_car_slots, num_bike_slots, num_truck_slots)
    levels_config = [
        ('L1', 3, 2, 1),
        ('L2', 2, 3, 1)
    ]
    parking_lot = ParkingLot(levels_config)

    while True:
        print("\n1. Park Vehicle\n2. Unpark Vehicle\n3. Display Parking Lot\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            vnum = input("Enter vehicle number: ")
            vtype = input("Enter vehicle type (Car/Bike/Truck): ").capitalize()
            if vtype not in ['Car', 'Bike', 'Truck']:
                print("Invalid vehicle type.")
                continue
            vehicle = Vehicle(vnum, vtype)
            parking_lot.park_vehicle(vehicle)

        elif choice == '2':
            vnum = input("Enter vehicle number to unpark: ")
            parking_lot.unpark_vehicle(vnum)

        elif choice == '3':
            parking_lot.display_parking_lot()

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

