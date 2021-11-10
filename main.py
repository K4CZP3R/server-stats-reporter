import sqlite3
import psutil
import os
from time import sleep

class Database:
    def __init__(self) -> None:
        self.cur = sqlite3.connect("database/database.db")
        self.__check_table()

    def __check_table(self) -> bool:
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS report (hostname text, onem integer, fivem integer, fifteenm integer, cpu_usage integer, mem_usage_percent integer)')

    def check_if_hostname_exists(self, hostname):
        found = 0
        for row in self.cur.execute(f"SELECT hostname FROM report WHERE hostname=:hostname", {"hostname": hostname}):
            found += 1
        return found > 0


    def insert_report(self, hostname: str, onem: int, fivem: int, fifteenm: int, cpu_usage: int, mem_usage_percent: int):
        exists = self.check_if_hostname_exists(hostname)
        if exists:
            self.cur.execute(f"UPDATE report SET onem=:onem, fivem=:fivem, fifteenm=:fifteenm, cpu_usage=:cpu_usage, mem_usage_percent=:mem_usage_percent WHERE hostname=:hostname", {
                "onem": onem,
                "fivem": fivem,
                "fifteenm": fifteenm,
                "cpu_usage": cpu_usage,
                "hostname": hostname,
                "mem_usage_percent": mem_usage_percent
            })
        else:
            self.cur.execute("INSERT INTO report VALUES (?,?,?,?,?,?)", (hostname, onem, fivem, fifteenm, cpu_usage, mem_usage_percent))
        self.cur.commit()
        

def report():
    l1,l5,l15= psutil.getloadavg()
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    return [l1,l5,l15, cpu_percent, mem_percent]


db = Database()

hostname = os.environ['NODENAME']
# hostname = "Test"

while True:
    r = report()
    db.insert_report(hostname, r[0], r[1], r[2], r[3], r[4])
    sleep(5)
