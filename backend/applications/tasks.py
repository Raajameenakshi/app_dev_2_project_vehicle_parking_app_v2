from celery import shared_task
import requests
import os
from datetime import datetime
from flask import current_app
from applications.models import *
import csv
from jinja2 import Template
from applications.mail import send_email
from sqlalchemy import and_

GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAhlSOBgU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=6O1TqxFo3Z23EDm3RFlJ64mDsUKnsxQr9MHgVrhcXJY"

# @shared_task(name="daily_reminder_google_chat", ignore_results = False)
# def daily_booking_reminder(users):
#     for user in users:
#         message = {
#             "text": f"👋 Hey {user['full_name']}, you haven’t booked a parking spot today. Don’t miss out!"
#         }

#         try:
#             res = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)
#             if res.status_code == 200:
#                 print(f"✅ Reminder sent to {user['email']}")
#             else:
#                 print(f"❌ Failed for {user['email']}: {res.text}")
#         except Exception as e:
#             print(f"❗ Error sending to {user['email']}: {str(e)}")

#     return "Reminder task complete"


@shared_task(name="daily_reminder_google_chat", ignore_results=False)
def daily_booking_reminder():
    with current_app.app_context():
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        booked_user_ids = db.session.query(Booking.user_id).filter(
            and_(
                Booking.start_time >= today_start,
                Booking.start_time <= today_end
            )
        ).distinct()

        users = User.query.filter(~User.id.in_(booked_user_ids)).with_entities(
            User.id, User.full_name, User.email
        ).all()

        for user in users:
            message = {
                "text": f"👋 Hey {user.full_name}, you haven’t booked a parking spot today. Don’t miss out!"
            }

            try:
                res = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)
                if res.status_code == 200:
                    print(f"✅ Reminder sent to {user.email}")
                else:
                    print(f"❌ Failed for {user.email}: {res.text}")
            except Exception as e:
                print(f"❗ Error sending to {user.email}: {str(e)}")

    return f"Sent reminders to {len(users)} users"


@shared_task(name="csv_report_for_user",ignore_results = False)
def csv_report_for_user(full_name, booking_data):

    filename = f"{full_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("static", filename)

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["booking_id", "spot_id", "slot_id", "start_time", "end_time", "cost", "remarks"])
        writer.writeheader()
        for row in booking_data:
            writer.writerow(row)

    return filename  # just filename, not full path


PARKING_REPORT_TEMPLATE = """
<h3>Dear {{ user_data.username }},</h3>
<p>Please find your parking summary for the month of {{ user_data.month }}:</p>

<ul>
  <li><strong>Total bookings:</strong> {{ user_data.total_bookings }}</li>
  <li><strong>Total amount spent:</strong> ₹{{ user_data.total_spent }}</li>
  <li><strong>Most used parking lot:</strong> {{ user_data.most_used_lot }}</li>
</ul>

<p>Visit your dashboard for more info: <a href="http://127.0.0.1:5173">Vehicle Parking Dashboard</a></p>

<br><br>
<h5>Regards,<br>
Vehicle-Park Team<br>
MAD II Project</h5>
"""

# @shared_task(ignore_results=False, name="monthly_report")
# def monthly_report(user_reports):
#     for user_data in user_reports:
#         html_body = Template(PARKING_REPORT_TEMPLATE).render(user_data=user_data)
#         send_email(
#             to_address=user_data["email"],
#             subject=f"Your Monthly Parking Report - {user_data['month']}",
#             message=html_body,
#             content="html"
#         )
#     return "Monthly reports sent."

@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    month_end = datetime(now.year, now.month, now.day, 23, 59, 59)  # Today end

    users = User.query.all()
    reports_sent = 0

    for user in users:
        bookings = Booking.query.filter(
            and_(
                Booking.user_id == user.id,
                Booking.start_time >= month_start,
                Booking.end_time <= month_end
            )
        ).all()

        if not bookings:
            continue

        total_spent = sum(b.cost for b in bookings)
        lot_counts = {}
        for b in bookings:
            lot = b.parking_spot.parking_lot
            lot_counts[lot.location] = lot_counts.get(lot.location, 0) + 1

        most_used_lot = max(lot_counts, key=lot_counts.get)

        user_data = {
            "username": user.full_name,
            "email": user.email,
            "month": month_start.strftime('%B %Y'),
            "total_bookings": len(bookings),
            "total_spent": total_spent,
            "most_used_lot": most_used_lot
        }

        html_body = Template(PARKING_REPORT_TEMPLATE).render(user_data=user_data)
        send_email(
            to_address=user.email,
            subject=f"Your Monthly Parking Report - {user_data['month']}",
            message=html_body,
            content="html"
        )
        reports_sent += 1

    return f"Monthly reports sent to {reports_sent} users."
