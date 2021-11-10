from typing import Any
import falcon
import sqlite3

def node(hostname, onem, fivem, fifteenm, cpu_usage, mem_usage):
    return {
        "hostname": hostname,
        "1m": onem,
        "5m": fivem,
        "15m": fifteenm,
        "cpu": cpu_usage,
        "mem": mem_usage
    }

class Database:
    def __init__(self) -> None:
        self.cur = sqlite3.connect("database/database.db")
    
    def get_all(self) -> Any:
        to_return = []
        for r in self.cur.execute("SELECT * FROM report"):
            to_return.append(node(r[0], r[1], r[2], r[3], r[4], r[5]))
        return to_return

db = Database()

class StatusResource:
    def on_get(self, req, resp):
        resp.media = db.get_all()

api = falcon.API()
api.add_route('/reports', StatusResource())