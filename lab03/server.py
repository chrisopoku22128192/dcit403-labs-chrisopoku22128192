import os
import csv
from datetime import date
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pharmacy-stock")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pharmacy_stock.csv")


def load():
    with open(DATA, newline="") as f:
        return list(csv.DictReader(f))


@mcp.tool()
def check_stock(item: str, strength: str = "") -> list[dict]:
    """Check stock for one medicine. Returns rows whose item name contains `item`
    (and whose strength contains `strength`, if given), with form, quantity,
    unit_price_ghs and expiry_date. Use for availability, quantity, price or expiry
    of a named medicine, e.g. item="amoxicillin", strength="500mg"."""
    rows = [r for r in load() if item.lower() in r["item"].lower()]
    if strength:
        rows = [r for r in rows if strength.lower() in r["strength"].lower()]
    return rows


@mcp.tool()
def search_items(query: str) -> list[dict]:
    """Search all stock by a keyword that may appear in the item name, strength or
    form, e.g. "syrup", "tablets" or "para". Use when the exact medicine name is not
    known or the user asks what kinds of an item are available."""
    q = query.lower()
    return [r for r in load()
            if q in r["item"].lower() or q in r["strength"].lower() or q in r["form"].lower()]


@mcp.tool()
def list_expiring(days: int) -> list[dict]:
    """List items that expire within the next `days` days (or have already expired),
    soonest first. Each row includes days_left; a negative value means expired."""
    today = date.today()
    out = []
    for r in load():
        left = (date.fromisoformat(r["expiry_date"]) - today).days
        if left <= days:
            out.append({**r, "days_left": left})
    return sorted(out, key=lambda r: r["days_left"])


if __name__ == "__main__":
    mcp.run()