import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.

"""
    Before running this code, create mileage.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);
"""

# Create database
def create_database():
    conn = sqlite3.connect(db_url)
    c = conn.cursor()

    # Table Setup
    c.execute("""CREATE TABLE IF NOT EXISTS miles (
    vehicle TEXT, total_miles FLOAT)""")

    conn.commit()
    conn.close()

class MileageError(Exception):
    pass

def add_miles(vehicle, new_miles):
    '''If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise MileageError
    '''

    if not vehicle:
        raise MileageError('Provide a vehicle name')
    if not isinstance(new_miles, (int, float))  or new_miles < 0:
        raise MileageError('Provide a positive number for new miles')

    vehicle = uppercase_vehicle(vehicle)

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE miles SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO miles VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()

    print("""
        Database updated
    """)

def uppercase_vehicle(vehicle):
    return(vehicle.upper())

def search(vehicle):
    try:
        vehicle = uppercase_vehicle(vehicle)
        vehicle_info = get_vehicle_info(vehicle)
        if vehicle_info != None:
            return vehicle_info[1]
    except sqlite3.Error:
        print("Error: database not found")

def get_vehicle_info(vehicle):
    with sqlite3.connect(db_url) as database:
        c = database.cursor()
        c.execute('SELECT * FROM miles WHERE vehicle = ?', (vehicle,))
        return c.fetchone()


def main():
    create_database()
    while True:
        vehicle = input('Enter vehicle name or enter to quit: ')
        if not vehicle:
            print("Goodbye")
            break
        current_mileage = search(vehicle)
        if current_mileage != None:
            print("Current Mileage: {:.2f} miles".format(current_mileage))
        try:
            miles = float(input('Enter new miles for %s: ' % vehicle))
            add_miles(vehicle, miles)
        except ValueError:
            print("Error: please enter numeric mileage without ,")


if __name__ == '__main__':
    main()