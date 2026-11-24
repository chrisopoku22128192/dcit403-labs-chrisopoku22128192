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
    """Check stock for one medicine. Stock uses full generic names (e.g. "Amoxicillin",
    "Oral Rehydration Salts"), so convert brand names and abbreviations to the generic
    name first: Amoxil -> amoxicillin, ORS -> oral rehydration salts. Returns rows whose
    item name contains `item` (and whose strength contains `strength`, if given), with form,
    quantity, unit_price_ghs and expiry_date. If no rows are found, try search_items with a
    shorter keyword before saying the item is out of stock."""
    rows = [r for r in load() if item.lower() in r["item"].lower()]
    if strength:
        rows = [r for r in rows if strength.lower() in r["strength"].lower()]
    return rows


@mcp.tool()
def search_items(query: str) -> list[dict]:
    """Search all stock by a keyword that may appear in the item name, strength or
    form, e.g. "syrup", "tablets" or "rehydration". Item names are full generic names,
    so search with words from the generic name, not abbreviations or brand names.
    Use when the exact medicine name is not known or the user asks what kinds of an
    item are available."""
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


def save(rows):
    with open(DATA, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


@mcp.tool()
def record_sale(item: str, strength: str, qty: int) -> dict:
    """ACTION: record a sale and reduce stock in the stock file. This changes real data.
    Only use when the user clearly says an item was sold or wants to sell it.
    item: medicine name, e.g. "paracetamol". strength: exact strength, e.g. "500mg".
    qty: number of packs sold, a whole number greater than 0.
    The sale is refused if qty is not positive, the item is not found, the item and
    strength match more than one product, the item has expired, or there is not enough stock."""
    if qty <= 0:
        return {"ok": False, "message": f"Sale refused: quantity must be at least 1 (got {qty})."}
    rows = load()
    matches = [r for r in rows
               if item.lower() in r["item"].lower() and strength.lower() == r["strength"].lower()]
    if not matches:
        return {"ok": False, "message": f"Sale refused: no stock found for {item} {strength}."}
    if len(matches) > 1:
        names = ", ".join(f'{r["item"]} {r["strength"]} ({r["form"]})' for r in matches)
        return {"ok": False, "message": f"Sale refused: more than one product matches: {names}. Be more specific."}
    row = matches[0]
    if date.fromisoformat(row["expiry_date"]) < date.today():
        return {"ok": False, "message": (f"Sale refused: {row['item']} {row['strength']} expired on "
                                         f"{row['expiry_date']} and must not be sold.")}
    available = int(row["quantity"])
    if qty > available:
        return {"ok": False, "message": (f"Sale refused: only {available} packs of {row['item']} "
                                         f"{row['strength']} in stock; cannot sell {qty}.")}
    row["quantity"] = str(available - qty)
    save(rows)
    total = qty * float(row["unit_price_ghs"])
    return {"ok": True, "message": (f"Sold {qty} x {row['item']} {row['strength']} for GHS {total:.2f}. "
                                    f"Stock left: {row['quantity']}."),
            "item": row["item"], "strength": row["strength"], "sold": qty,
            "total_ghs": round(total, 2), "stock_left": int(row["quantity"])}


if __name__ == "__main__":
    mcp.run()