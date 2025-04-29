from models.database import get_connection
import uuid

class PaymentModel:
	def close_conn(self):
		self.conn.close()

	def save_payment(self, customer_name, customer_email, card_info, total_cost, user_id, show_id, seats):
		conn = get_connection()
		cur = conn.cursor()

		booking_ref = str(uuid.uuid4())[:8]  # 8 UUID to generate booking reference

		cur.execute(
			"""
			INSERT INTO bookings (booking_ref, customer_name, customer_email, card_info, total_cost, booking_status, user_id, show_id)
			VALUES (?, ?, ?, ?, ?, 'confirmed', ?, ?)
			""", (booking_ref, customer_name, customer_email, card_info, total_cost, user_id, show_id))

		booking_id = cur.lastrowid

		for seat_id in seats:
			cur.execute("""
                INSERT INTO booking_seat (booking_id, seat_id)
                VALUES (?, ?)
            """, (booking_id, seat_id))

		conn.commit()
		conn.close()
		return booking_id
	
	def get_booking(self, booking_id):
		conn = get_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			SELECT * from bookings where id = ?
			""", (booking_id,))
		details = cur.fetchone()

		conn.commit()
		conn.close()
		return details