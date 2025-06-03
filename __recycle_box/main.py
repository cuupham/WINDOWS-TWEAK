import subprocess
import os


network_services = (
    "LanmanServer",
    "LanmanWorkstation",
    "NetTcpPortSharing",
    "RemoteAccess",
    "RemoteRegistry",
)

virtualization_services = (
    "HvHost",
    "vmicguestinterface",
    "vmicheartbeat",
    "vmickvpexchange",
    "vmicrdv",
    "vmicshutdown",
    "vmictimesync",
    "vmicvmsession",
    "vmicvss",
)

printing_services = ("PrintNotify", "Spooler")

security_services = ("DiagTrack", "SCardSvr", "SCPolicySvc", "WbioSrvc", "wlidsvc")

system_maintenance_services = ("SysMain", "wbengine", "tzautoupdate", "UevAgentService")

user_experience_services = (
    "Themes",
    "XblAuthManager",
    "XblGameSave",
    "XboxGipSvc",
    "XboxNetApiSvc",
)

sensor_services = ("SensorDataService", "SensorService", "SensrSvc")

miscellaneous_services = (
    "AppVClient",
    "BDESVC",
    "diagnosticshub.standardcollector.service",
    "DiagTrack",
    "DialogBlockingService",
    "fhsvc",
    "GameInputSvc",
    "LPlatSvc",
    "LxpSvc",
    "MapsBroker",
    "MsKeyboardFilter",
    "PhoneSvc",
    "RetailDemo",
    "SEMgrSvc",
    "SessionEnv",
    "shpamsvc",
    "ssh-agent",
    "TapiSrv",
    "TermService",
    "UmRdpService",
    "wisvc",
    "WMPNetworkSvc",
    "WSearch",
    "BcastDVRUserService",
    "cbdhsvc",
    "OneSyncSvc",
    "PimIndexMaintenanceSvc",
    "UnistoreSvc",
)

performance_services = ("NDU",)

services = (
    *network_services,
    *virtualization_services,
    *printing_services,
    *security_services,
    *system_maintenance_services,
    *user_experience_services,
    *sensor_services,
    *miscellaneous_services,
    *performance_services,
)

services_without_print = tuple(
    srv for srv in services if srv not in (*printing_services, *network_services[:2])
)


def is_service_exist(service_name: str) -> bool:
    result = subprocess.run(
        ["sc", "query", service_name], capture_output=True, text=True
    )
    return result.returncode == 0


def disable_service(service_name: str):
    try:
        subprocess.run(
            ["sc", "config", service_name, "start=", "disabled"],
            check=True,
            stdout=subprocess.DEVNULL,  # Không in thông báo khi thành công
            stderr=subprocess.PIPE,  # Bắt lỗi nếu có
            text=True,  # Để nhận kết quả dưới dạng chuỗi thay vì bytes
        )
        print(f"{service_name} has been disabled successfully")
    except subprocess.CalledProcessError as err:
        print(f"Failed to disable {service_name}: {err}")


if __name__ == "__main__":
    srv_collection = None
    print(
        """Disable services with:
1. Full list
2. Services without print
"""
    )
    choice = input("Enter your choice: ")
    if choice == "1":
        srv_collection = services
    elif choice == "2":
        srv_collection = services_without_print
    else:
        print("\nHas Error!!\n")
        os.system("pause")

    if srv_collection:
        try:
            for service in srv_collection:
                disable_service(service) if is_service_exist(service) else print(
                    f"Service {service} does not exist"
                )
        except Exception as e:
            print(f"[ERROR]: {e}")

        finally:
            os.system("pause")
