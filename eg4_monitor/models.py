from typing import List, Optional
from pydantic import BaseModel, Field

class BatteryInfo(BaseModel):
    """Detailed info for an individual battery module."""
    battery_key: str = Field(alias="batteryKey")
    battery_sn: str = Field(alias="batterySn")
    battery_type: str = Field(alias="batteryType")
    last_update_time: str = Field(alias="lastUpdateTime")
    total_voltage: int = Field(alias="totalVoltage")  # In 0.01V units
    current: int  # In 0.1A units
    soc: int
    soh: int
    remain_capacity: int = Field(alias="currentRemainCapacity")  # Ah
    full_capacity: int = Field(alias="currentFullCapacity")  # Ah
    max_charge: int = Field(alias="maxBatteryCharge")  # Ah
    max_cell_temp: int = Field(alias="batMaxCellTemp")
    min_cell_temp: int = Field(alias="batMinCellTemp")
    max_cell_voltage: int = Field(alias="batMaxCellVoltage")
    min_cell_voltage: int = Field(alias="batMinCellVoltage")
    charge_max_cur: int = Field(alias="batChargeMaxCur")
    charge_volt_ref: int = Field(alias="batChargeVoltRef")
    cycle_cnt: int = Field(alias="cycleCnt")
    fw_version: str = Field(alias="fwVersionText")

    @property
    def total_voltage_v(self) -> float:
        return self.total_voltage / 100.0

    @property
    def current_a(self) -> float:
        return self.current / 10.0

class InverterData(BaseModel):
    """The main inverter and system status data."""
    success: bool
    serial_num: str = Field(alias="serialNum")
    status_text: str = Field(alias="statusText")
    ppv: int  # Solar Power in Watts
    p_charge: int = Field(alias="pCharge")  # Charge Power in Watts
    p_discharge: int = Field(alias="pDisCharge")  # Discharge Power in Watts
    peps: int = Field(alias="peps")  # EPS/Load Power in Watts?
    pinv: int = Field(alias="pinv")  # Inverter Power in Watts?
    prec: int = Field(alias="prec")  # Rectifier Power in Watts?
    bat_status: str = Field(alias="batStatus")
    soc: int
    v_bat: int = Field(alias="vBat")  # Battery Voltage in 0.1V units
    remain_capacity: int = Field(alias="remainCapacity")
    full_capacity: int = Field(alias="fullCapacity")
    capacity_percent: int = Field(alias="capacityPercent")
    battery_array: List[BatteryInfo] = Field(alias="batteryArray")
    
    # Global/System-wide cell details
    global_max_cell_temp: int = Field(alias="globalMaxCellTemp")
    global_min_cell_temp: int = Field(alias="globalMinCellTemp")
    global_max_cell_voltage: int = Field(alias="globalMaxCellVoltage")
    global_min_cell_voltage: int = Field(alias="globalMinCellVoltage")
    
    # Extra convenience fields
    current_text: str = Field(alias="currentText")
    current_type: str = Field(alias="currentType")
    total_voltage_text: str = Field(alias="totalVoltageText")

    @property
    def v_bat_v(self) -> float:
        return self.v_bat / 10.0
