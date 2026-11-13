def _to_int(text):
    """Strict non-negative integer parser (ASCII digits only). Returns None if invalid."""
    if not isinstance(text, str) or not text.isascii() or not text.isdigit():
        return None
    return int(text)


def parse_ticket_id(ticket_id):
    """Return (PREFIX, year, serial) or None if the ticket ID is invalid."""
    if not isinstance(ticket_id, str):
        return None
    parts = ticket_id.split('-')
    if len(parts) != 3:
        return None
    prefix, year, serial = parts
    year, serial = _to_int(year), _to_int(serial)
    if not prefix or year is None or serial is None:
        return None
    return prefix.upper(), year, serial


def total_fines(amounts_csv):
    """Return total fines capped at 10000, or None if input is invalid."""
    if not isinstance(amounts_csv, str):
        return None
    amounts = [_to_int(a.strip()) for a in amounts_csv.split(',')]
    if any(a is None for a in amounts):
        return None
    total = sum(amounts)
    if total > 10000:
        total = 10000
    return total


def speed_excess(reading):
    """Return percent over the limit, or None if the reading is invalid."""
    if not isinstance(reading, str):
        return None
    parts = reading.split('/')
    if len(parts) != 2:
        return None
    speed, limit = _to_int(parts[0].strip()), _to_int(parts[1].strip())
    if speed is None or limit is None or limit == 0:
        return None
    return (speed - limit) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    if result is None:
        print("Invalid ticket ID")
    else:
        print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    if result is None:
        print("Invalid fine amounts")
    else:
        print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    if result is None:
        print("Invalid speed/limit reading")
    else:
        print("Percent Over Limit:", result)


if __name__ == "__main__":
    main()