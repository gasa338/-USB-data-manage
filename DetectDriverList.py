import json
import subprocess
# from asyncio import sleep
from dataclasses import dataclass
from time import sleep
from typing import Callable, List


@dataclass
class Drive:
    letter: str
    label: str
    drive_type: str

    @property
    def is_removable(self) -> bool:
        return self.drive_type == 'Removable Disk'


def list_drives() -> List[Drive]:
    """
    Prikuplja listu svih diskova pomoću WMI (Windows Management Instrumentation) komande.
    :return: Lista diskova u vidu `Drive` objekata.
    """
    proc = subprocess.run(
        args=[
            'powershell',
            '-noprofile',
            '-command',
            'Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json'
        ],
        text=True,
        stdout=subprocess.PIPE
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print('Failed to enumerate drives')
        return []
    devices = json.loads(proc.stdout)

    drive_types = {
        0: 'Unknown',
        1: 'No Root Directory',
        2: 'Removable Disk',
        3: 'Local Disk',
        4: 'Network Drive',
        5: 'Compact Disc',
        6: 'RAM Disk',
    }
    print(devices)

    return [Drive(
        letter=d['deviceid'],
        label=d['volumename'],
        drive_type=drive_types[d['drivetype']]
    ) for d in devices]

def watch_drives(on_change: Callable[[List[Drive]], None], poll_interval: int = 1):
    """
    Kontinuirano prati promene na diskovima i poziva `on_change` funkciju pri promenama.
    :param on_change: Funkcija koja se poziva pri promeni liste diskova
    :param poll_interval: Interval provere u sekundama
    """
    prev = None
    while True:
        drives = list_drives()
        if prev != drives:
            on_change(drives)
            prev = drives
        sleep(poll_interval)


if __name__ == '__main__':
    watch_drives(on_change=print)