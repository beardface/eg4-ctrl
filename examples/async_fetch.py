import os
import asyncio
from dotenv import load_dotenv
from eg4_monitor.client import AsyncEG4Client

async def main():
    # Load credentials from .env
    load_dotenv()
    
    username = os.getenv("EG4_USERNAME")
    password = os.getenv("EG4_PASSWORD")
    serial_num = os.getenv("EG4_SERIAL_NUM")

    if not all([username, password, serial_num]):
        print("Error: Please set EG4_USERNAME, EG4_PASSWORD, and EG4_SERIAL_NUM in .env")
        return

    # Initialize the client
    async with AsyncEG4Client(username, password, serial_num, session_file="session_async.json") as client:
        try:
            # Fetch data
            data = await client.get_inverter_data()
            
            print(f"--- Inverter Status (Async) ---")
            print(f"Status: {data.status_text}")
            print(f"Solar Power: {data.ppv} W")
            print(f"Battery SoC: {data.soc}%")
            print(f"Battery Voltage: {data.v_bat_v} V")
            
            print(f"\n--- Individual Batteries ---")
            for batt in data.battery_array:
                print(f"- {batt.battery_sn}: {batt.soc}% SoC, {batt.total_voltage_v:.2f} V")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
