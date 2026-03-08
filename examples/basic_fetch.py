import os
import json
from dotenv import load_dotenv
from eg4_monitor.client import EG4Client

def main():
    # Load credentials from .env
    load_dotenv()
    
    username = os.getenv("EG4_USERNAME")
    password = os.getenv("EG4_PASSWORD")
    serial_num = os.getenv("EG4_SERIAL_NUM")

    if not all([username, password, serial_num]):
        print("Error: Please set EG4_USERNAME, EG4_PASSWORD, and EG4_SERIAL_NUM in .env")
        return

    # Initialize the client
    client = EG4Client(username, password, serial_num, session_file="session_example.json")

    try:
        # Fetch data
        data = client.get_inverter_data()
        
        print(f"--- Inverter Status ---")
        print(f"Status: {data.status_text}")
        print(f"Solar Power: {data.ppv} W")
        print(f"Battery SoC: {data.soc}%")
        print(f"Battery Voltage: {data.v_bat_v} V")
        print(f"Charge Power: {data.p_charge} W")
        print(f"Discharge Power: {data.p_discharge} W")
        print(f"Remaining Capacity: {data.remain_capacity} Ah")
        
        print(f"\n--- Individual Batteries ---")
        for batt in data.battery_array:
            print(f"- {batt.battery_sn}: {batt.soc}% SoC, {batt.total_voltage_v:.2f} V, {batt.cycle_cnt} cycles")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
