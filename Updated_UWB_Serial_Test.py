import serial
from scipy.optimize import minimize
import math
import numpy as np
    
def location_solver(points, distances, x0):
    def objective_func(X):
        x, y = X
        return sum([((x - point[0])**2 + (y - point[1])**2 - d**2)**2 for point, d in zip(points, distances)])
    
    result = minimize(objective_func, x0, method='L-BFGS-B')
    if result.success and result.x[0] >= 0 and result.x[1] >= 0:
        return result.x
    else:
        return x0

if __name__ == "__main__":

    x0 = np.array([0,0])
    points = [(0,0), (10,0), (0,10), (10,10)]
    uwb_distances_dict = {}
    
    
    # Adjust port, baud rate, and timeout as needed
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    except:
        print("Failed to open serial port. Please check the port and try again.")
    else:
        try:
            while True:
                distances = []
                uwb_distances_dict = {}
                for i in range(0,4):
                    # Read data from the serial port
                    data = ser.readline().decode().strip()
                    if data:  # Only print if data is not empty
                        data = data.split(",")
                        anchor_id = int(data[0])
                        distance = float(data[1])
                        uwb_distances_dict[anchor_id] = distance
                        distances.append(distance)
                    # adjust order of points based on the uwb location accordingly
                print("Distances dictionary:", uwb_distances_dict)
                print("Distances count: ",len(distances))
                target_location = location_solver(points, distances, x0)
                print("Target location:", target_location)
                x0 = target_location
                
                    
        except KeyboardInterrupt:
            print("\nExiting due to keyboard interrupt.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            ser.close()  # Ensure the serial port is closed
            print("Serial port closed.")