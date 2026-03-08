import pytest
import requests_mock
import respx
from httpx import Response
from eg4_monitor.client import EG4Client, AsyncEG4Client
from eg4_monitor.exceptions import AuthError, APIError

MOCK_LOGIN_URL = "https://monitor.eg4electronics.com/WManage/web/login"
MOCK_API_URL = "https://monitor.eg4electronics.com/WManage/api/battery/getBatteryInfo"
MOCK_DASHBOARD_URL = "https://monitor.eg4electronics.com/WManage/web/monitor/inverter"

MOCK_DATA = {
    "success": True,
    "serialNum": "5223740518",
    "statusText": "normal",
    "ppv": 629,
    "pCharge": 521,
    "pDisCharge": 0,
    "peps": 28,
    "pinv": 0,
    "prec": 0,
    "batStatus": "Charging",
    "soc": 71,
    "vBat": 540,
    "remainCapacity": 198,
    "fullCapacity": 280,
    "capacityPercent": 71,
    "batteryArray": [
        {
            "batteryKey": "5223740518_Battery_ID_01",
            "batterySn": "Battery_ID_01",
            "batteryType": "BATT_default",
            "lastUpdateTime": "2026-03-08 14:55:49",
            "totalVoltage": 5404,
            "current": 92,
            "soc": 71,
            "soh": 100,
            "currentRemainCapacity": 198,
            "currentFullCapacity": 280,
            "maxBatteryCharge": 280,
            "batMaxCellTemp": 60,
            "batMinCellTemp": 60,
            "batMaxCellVoltage": 3380,
            "batMinCellVoltage": 3376,
            "batChargeMaxCur": 1400,
            "batChargeVoltRef": 560,
            "cycleCnt": 28,
            "fwVersionText": "2.04"
        }
    ],
    "globalMaxCellTemp": 60,
    "globalMinCellTemp": 60,
    "globalMaxCellVoltage": 3380,
    "globalMinCellVoltage": 3376,
    "currentText": "9.8",
    "currentType": "charge",
    "totalVoltageText": "54"
}

def test_sync_client_login_success():
    with requests_mock.Mocker() as m:
        # Mock login redirect
        m.post(MOCK_LOGIN_URL, status_code=302, headers={"Location": "/WManage/web/monitor/inverter"})
        m.get(MOCK_DASHBOARD_URL, text="Dashboard")
        client = EG4Client("user", "pass", "123")
        assert client.login() is True

def test_sync_client_login_failure():
    with requests_mock.Mocker() as m:
        # Mock login failing (staying on login page)
        m.post(MOCK_LOGIN_URL, text="Login Page")
        client = EG4Client("user", "pass", "123")
        with pytest.raises(AuthError):
            client.login()

def test_sync_client_get_data():
    with requests_mock.Mocker() as m:
        m.post(MOCK_LOGIN_URL, status_code=302, headers={"Location": "/WManage/web/monitor/inverter"})
        m.get(MOCK_DASHBOARD_URL, text="Dashboard")
        m.post(MOCK_API_URL, json=MOCK_DATA)
        client = EG4Client("user", "pass", "123")
        data = client.get_inverter_data()
        assert data.ppv == 629
        assert data.v_bat_v == 54.0
        assert data.battery_array[0].total_voltage_v == 54.04

@pytest.mark.asyncio
async def test_async_client_get_data():
    with respx.mock:
        respx.post(MOCK_LOGIN_URL).mock(return_value=Response(302, headers={"Location": "/WManage/web/monitor/inverter"}))
        respx.get(MOCK_DASHBOARD_URL).mock(return_value=Response(200, text="Dashboard"))
        respx.post(MOCK_API_URL).mock(return_value=Response(200, json=MOCK_DATA))
        
        async with AsyncEG4Client("user", "pass", "123") as client:
            data = await client.get_inverter_data()
            assert data.ppv == 629
            assert data.v_bat_v == 54.0
            assert data.battery_array[0].total_voltage_v == 54.04
