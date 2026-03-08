import argparse
import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from .client import EG4Client, AsyncEG4Client

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="EG4 Monitor CLI")
    parser.add_argument("--username", help="EG4 Username", default=os.getenv("EG4_USERNAME"))
    parser.add_argument("--password", help="EG4 Password", default=os.getenv("EG4_PASSWORD"))
    parser.add_argument("--serial", help="Inverter Serial Number", default=os.getenv("EG4_SERIAL_NUM"))
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--async-mode", action="store_true", help="Use async client")
    
    args = parser.parse_args()

    if not all([args.username, args.password, args.serial]):
        parser.error("Username, password, and serial number are required (via args or environment variables).")

    if args.async_mode:
        asyncio.run(run_async(args))
    else:
        run_sync(args)

def run_sync(args):
    client = EG4Client(args.username, args.password, args.serial)
    try:
        data = client.get_inverter_data()
        print_data(data, args.json)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

async def run_async(args):
    async with AsyncEG4Client(args.username, args.password, args.serial) as client:
        try:
            data = await client.get_inverter_data()
            print_data(data, args.json)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

def print_data(data, as_json):
    if as_json:
        print(data.model_dump_json(indent=2))
    else:
        print(f"Inverter: {data.serial_num} ({data.status_text})")
        print(f"Solar:    {data.ppv} W")
        print(f"Battery:  {data.soc}% ({data.v_bat_v} V)")
        print(f"Charge:   {data.p_charge} W")
        print(f"Discharge: {data.p_discharge} W")
        print(f"Load:     {data.peps} W")

if __name__ == "__main__":
    main()
