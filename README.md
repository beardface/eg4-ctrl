# EG4 Control Library (eg4-ctrl)

A Python library for monitoring EG4 Solar Inverters via the EG4 Monitor website (monitor.eg4electronics.com). This library is specifically useful for remote monitoring of EG4 6000XP inverters and similar models that report to the EG4 web portal.

## Features

- **Synchronous and Asynchronous Clients:** Supports both `requests` and `httpx` for flexible integration.
- **Pydantic Models:** Strongly typed data models for system status and individual battery details.
- **Session Persistence:** Saves session cookies to minimize login requests and avoid account lockout.
- **Unit Conversion:** Convenient properties for converting raw API values to standard units (Volts, Amps, Watts).

## Installation

```bash
pip install eg4-ctrl
```

## Quick Start

### Synchronous Client

```python
from eg4_monitor import EG4Client

client = EG4Client(
    username="your_username",
    password="your_password",
    serial_num="your_inverter_serial",
    session_file="session.json"
)

data = client.get_inverter_data()
print(f"Status: {data.status_text}")
print(f"Solar Power: {data.ppv}W")
print(f"Battery SoC: {data.soc}%")
```

### Asynchronous Client

```python
import asyncio
from eg4_monitor import AsyncEG4Client

async def main():
    async with AsyncEG4Client(
        username="your_username",
        password="your_password",
        serial_num="your_inverter_serial",
        session_file="session.json"
    ) as client:
        data = await client.get_inverter_data()
        print(f"Battery Voltage: {data.v_bat_v}V")

asyncio.run(main())
```

## Data Models

The library uses Pydantic to parse API responses into structured objects.

### `InverterData`
- `status_text`: "normal", "warning", etc.
- `ppv`: Solar production (Watts).
- `p_charge`: Battery charging power (Watts).
- `p_discharge`: Battery discharging power (Watts).
- `soc`: System State of Charge (%).
- `v_bat_v`: Battery voltage (Volts).
- `battery_array`: List of `BatteryInfo` objects.

### `BatteryInfo`
- `battery_sn`: Battery serial number.
- `soc`: Battery State of Charge (%).
- `total_voltage_v`: Battery voltage (Volts).
- `current_a`: Battery current (Amps).
- `cycle_cnt`: Number of charge cycles.

## License

MIT
