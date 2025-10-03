def create_appointment_legacy(data):
    import sqlite3
    from datetime import datetime
    def send_email(addr, msg):
        pass 

    conn = sqlite3.connect('auto.db')
    now = datetime.now()
    if 'client_id' not in data:
        raise ValueError('missing client_id')
    if 'description' not in data:
        raise ValueError('missing description')

    try:
        conn.execute('BEGIN')
        cur = conn.execute("INSERT INTO appointments(client_id, when_ts, description, status) VALUES (?,?,?,?)",
                           (data['client_id'], now.isoformat(), data['description'], 'scheduled'))
        if data.get('send_email', True):
            send_email(data.get('email',''), 'Cita creada')
        if data.get('amount', 0) > 0:
            conn.execute("INSERT INTO invoices(appointment_id, amount, issued_at) VALUES (?,?,?)",
                         (cur.lastrowid, float(data['amount']), now.isoformat()))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
