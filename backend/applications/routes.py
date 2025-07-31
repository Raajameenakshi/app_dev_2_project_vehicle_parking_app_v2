import os
from flask import current_app as app, jsonify, request, abort
from applications.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,JWTManager, jwt_required, get_jwt_identity, get_jwt, current_user
from datetime import datetime, timedelta
from sqlalchemy import func,extract, and_, not_

from celery.result import AsyncResult
from .tasks import daily_booking_reminder, csv_report_for_user, monthly_report

from applications.cache_instance import cache

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    full_name = data.get("full_name")
    address = data.get("address")
    pincode = data.get("pincode")
    password = data.get("password")

    if not email or not password or not full_name or not address or not pincode:
        return jsonify({"error": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    user = User(
        email=email,
        full_name=full_name,
        address=address,
        pincode=pincode
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    cache.delete_memoized(get_users)
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # First try user login
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.email, additional_claims={"role": "user"})
        return jsonify({"access_token": token, "role": "user"}), 200

    # Try admin login (hardcoded user)
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        token = create_access_token(identity=admin.email, additional_claims={"role": "admin"})
        return jsonify({"access_token": token, "role": "admin"}), 200

    return jsonify({"error": "Wrong email or password"}), 401


@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful"}), 200

@app.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    return jsonify({
        "message": "Welcome to Admin Dashboard",}), 200
    
    
@app.route('/api/admin/users')
@jwt_required()
@cache.cached(timeout=300)
def get_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'address': user.address,
            'pincode': user.pincode
        } for user in users
    ])


@app.route("/api/admin/parking-lots", methods=["GET"])
@jwt_required()
def view_parking_lots():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    lots = Parking_lot.query.all()
    return jsonify([
        {
            "id": lot.id,
            "location": lot.location,
            "address": lot.address,
            "pincode": lot.pincode,
            "price": lot.price,
            "max_no_spots": lot.max_no_spots,
            "landmark": lot.landmark
        }
        for lot in lots
    ]), 200



@app.route("/api/admin/new-parking-lot", methods=["POST"])
@jwt_required()
def create_parking_lot():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    data = request.get_json()
    required_fields = ["location", "address", "pincode", "price", "max_no_spots", "landmark"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    existing_lot = Parking_lot.query.filter_by(location=data["location"]).first()
    if existing_lot:
        return jsonify({"error": "Parking lot with this location already exists"}), 400

    lot = Parking_lot(
        location=data["location"],
        address=data["address"],
        pincode=data["pincode"],
        price=data["price"],
        max_no_spots=data["max_no_spots"],
        landmark=data["landmark"]
    )

    db.session.add(lot)
    db.session.commit()

    # Auto-create parking spots after lot is created
    for _ in range(data["max_no_spots"]):
        spot = Parking_spot(parking_lot_id=lot.id)
        db.session.add(spot)

    db.session.commit()

    return jsonify({"message": "Parking lot created with spots"}), 201

@app.route("/api/admin/view-parking-lot/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_parking_lot(lot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    lot = Parking_lot.query.get_or_404(lot_id)
    spots = Parking_spot.query.filter_by(parking_lot_id=lot.id).all()

    return jsonify({
        "lot": {
            "id": lot.id,
            "location": lot.location,
            "address": lot.address,
            "pincode": lot.pincode,
            "price": lot.price,
            "max_no_spots": lot.max_no_spots,
            "landmark": lot.landmark
        },
        "spots": [
            {
                "id": spot.id,
                "is_booked": spot.is_booked,
                "additional_info": spot.additional_info
            } for spot in spots
        ]
    }), 200


@app.route("/api/admin/edit-parking-lot/<int:lot_id>", methods=["PUT"])
@jwt_required()
def update_parking_lot(lot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    lot = Parking_lot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.location = data.get("location", lot.location)
    lot.address = data.get("address", lot.address)
    lot.pincode = data.get("pincode", lot.pincode)
    lot.price = data.get("price", lot.price)
    lot.max_no_spots = data.get("max_no_spots", lot.max_no_spots)
    lot.landmark = data.get("landmark", lot.landmark)

    db.session.commit()
    return jsonify({"message": "Parking lot updated"}), 200


@app.route("/api/admin/del-parking-lot/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_lot(lot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    lot = Parking_lot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Parking lot deleted"}), 200

@app.route("/api/admin/spots/<int:spot_id>", methods=["GET"])
@jwt_required()
def view_spot(spot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    spot = Parking_spot.query.get_or_404(spot_id)
    return jsonify({
        "id": spot.id,
        "is_booked": spot.is_booked,
        "additional_info": spot.additional_info,
        "parking_lot_id": spot.parking_lot_id
    }), 200

@app.route("/api/admin/spots/<int:spot_id>/unavailable", methods=["POST"])
@jwt_required()
def mark_spot_unavailable(spot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    spot = Parking_spot.query.get_or_404(spot_id)

    if spot.is_booked:
        return jsonify({"error": "Cannot mark an occupied spot as unavailable."}), 400

    spot.additional_info = "Unavailable"
    db.session.commit()

    return jsonify({"message": "Spot marked as unavailable."}), 200

@app.route("/api/admin/spots/<int:spot_id>/available", methods=["POST"])
@jwt_required()
def mark_spot_available(spot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    spot = Parking_spot.query.get_or_404(spot_id)

    if spot.additional_info == "Unavailable":
        spot.additional_info = None
        db.session.commit()
        return jsonify({"message": "Spot marked as available."}), 200

    return jsonify({"message": "Spot is already available."}), 200

@app.route("/api/admin/spots/<int:spot_id>/booking", methods=["GET"])
@jwt_required()
def get_spot_booking(spot_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    spot = Parking_spot.query.get_or_404(spot_id)

    booking = Booking.query.filter_by(parking_spot_id=spot.id).order_by(Booking.start_time.desc()).first()
    if not booking:
        return jsonify({"error": "No booking found for this spot."}), 404

    user = User.query.get(booking.user_id)

    return jsonify({
    "booking": {
        "id": booking.id,
        "user_id": booking.user_id,
        "vehicle_number": booking.vehicle_number,
        "start_time": booking.start_time.strftime('%Y-%m-%d %H:%M'),
        "end_time": booking.end_time.strftime('%Y-%m-%d %H:%M'),
        "cost": booking.cost,
        "parking_spot": {
            "id": spot.id,
            "parking_lot_id": spot.parking_lot_id
        }
    },
    "user": {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }
}), 200

@app.route("/api/admin/bookings", methods=["GET"])
@jwt_required()
def admin_all_bookings():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    bookings = Booking.query.all()
    result = []
    for b in bookings:
        spot = b.parking_spot
        lot = spot.parking_lot
        result.append({
            "booking_id": b.id,
            "user": f"{b.user.full_name} (ID: {b.user.id})",
            "lot": lot.location,
            "spot_id": spot.id,
            "vehicle_number": b.vehicle_number,
            "start": b.start_time.strftime("%d-%m-%Y %H:%M"),
            "end": b.end_time.strftime("%d-%m-%Y %H:%M"),
            "cost": b.cost
        })

    return jsonify(result), 200

@app.route("/api/admin/summary", methods=["GET"])
@jwt_required()
def analytics_dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    # Revenue data
    revenue_data = (
        db.session.query(Parking_lot.location, func.sum(Booking.cost))
        .join(Parking_spot, Parking_lot.id == Parking_spot.parking_lot_id)
        .join(Booking, Parking_spot.id == Booking.parking_spot_id)
        .group_by(Parking_lot.location)
        .all()
    )
    revenue = [{ "location": loc, "revenue": rev or 0 } for loc, rev in revenue_data]

    # Occupancy data
    lots = Parking_lot.query.all()
    occupancy = []
    for lot in lots:
        total_spots = lot.parking_spots
        booked = sum(1 for spot in total_spots if spot.is_booked)
        unavailable = sum(1 for spot in total_spots if spot.additional_info == "Unavailable")
        available = len(total_spots) - booked - unavailable
        occupancy.append({
            "location": lot.location,
            "available": available,
            "booked": booked,
            "unavailable": unavailable
        })

    return jsonify({
        "revenue": revenue,
        "occupancy": occupancy
    }), 200


@app.route("/api/user/available_lots", methods=["GET"])
@cache.cached(timeout=120, query_string=True)
@jwt_required()
def available_lots():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    lots = Parking_lot.query.all()
    result = []
    for lot in lots:
        total = lot.max_no_spots
        free = Parking_spot.query.filter_by(parking_lot_id=lot.id, is_booked=False).filter((Parking_spot.additional_info != 'Unavailable') | (Parking_spot.additional_info.is_(None))).count()
        result.append({
          "id": lot.id,
          "location": lot.location,
          "address": lot.address,
          "price": lot.price,
          "spots_free": free
        })
    return jsonify(result), 200

@app.route("/api/user/bookings", methods=["GET"])
@jwt_required()
def user_bookings():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    user = get_jwt_identity()
    uid = User.query.filter_by(email=user).first_or_404().id
    bks = Booking.query.filter_by(user_id=uid).order_by(Booking.start_time.desc()).all()
    def is_active(b: Booking) -> bool:
        # compare only up to seconds
        return b.start_time.replace(microsecond=0) == b.end_time.replace(microsecond=0)
    
    return jsonify([{
      "id": b.id,
      "spot_id": b.parking_spot_id,
      "vehicle_number": b.vehicle_number,
      "start_time": b.start_time.isoformat(),
      "end_time": b.end_time.isoformat() if b.end_time else None,
      "cost": b.cost,
      "is_active": is_active(b)
    } for b in bks]), 200

@app.route("/api/user/lot/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_lot(lot_id):
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    lot = Parking_lot.query.get_or_404(lot_id)
    return jsonify({ "id": lot.id, "location": lot.location, "price":lot.price }), 200

@app.route("/api/user/lot/<int:lot_id>/next_spot", methods=["GET"])
@jwt_required()
def next_spot(lot_id):
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    spot = Parking_spot.query.filter_by(parking_lot_id=lot_id, is_booked=False).filter((Parking_spot.additional_info != 'Unavailable') | (Parking_spot.additional_info.is_(None))).first_or_404()
    return jsonify({ "next_spot": spot.id }), 200

@app.route("/api/user/spot/<int:spot_id>", methods=["GET"])
@jwt_required()
def get_spot_details(spot_id):
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    spot = Parking_spot.query.get_or_404(spot_id)
    return jsonify({ "parking_lot_id": spot.parking_lot_id }), 200


@app.route("/api/user/reserve", methods=["POST"])
@jwt_required()
def reserve_spot():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    payload = request.json
    lot_id = payload["lot_id"]
    vehicle = payload["vehicle_number"]
    userid = get_jwt_identity()
    user_id = User.query.filter_by(email=userid).first_or_404().id
    spot = Parking_spot.query.filter_by(parking_lot_id=lot_id, is_booked=False).filter((Parking_spot.additional_info != 'Unavailable') | (Parking_spot.additional_info.is_(None))).first_or_404()
    spot.is_booked = True
    booking = Booking(
      user_id=user_id,
      parking_spot_id=spot.id,
      vehicle_number=vehicle,
      start_time=datetime.now(),
      end_time=datetime.now(),
      cost=0
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({ "booking_id": booking.id }), 201

@app.route("/api/user/booking/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    b = Booking.query.get_or_404(booking_id)
    def is_active(b: Booking) -> bool:
        # compare only up to seconds
        return b.start_time.replace(microsecond=0) == b.end_time.replace(microsecond=0)
    return jsonify({
      "id": b.id,
      "spot_id": b.parking_spot_id,
      "vehicle_number": b.vehicle_number,
      "start_time": b.start_time.isoformat(),
      "end_time": b.end_time.isoformat() if b.end_time else '',
      "cost": b.cost,
      "is_active": is_active(b)
    }), 200

@app.route("/api/user/booking/<int:booking_id>/release", methods=["POST"])
@jwt_required()
def release_booking(booking_id):
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    b = Booking.query.get_or_404(booking_id)
    spot = Parking_spot.query.get_or_404(b.parking_spot_id)
    if b.start_time.replace(microsecond=0) != b.end_time.replace(microsecond=0):
        return jsonify({ "message": "Already released" }), 400

    now = datetime.now()
    b.end_time = now
    duration_h = (now - b.start_time).total_seconds() / 3600
    lot = Parking_lot.query.get(spot.parking_lot_id)
    b.cost = int(duration_h * lot.price)
    spot.is_booked = False
    db.session.commit()
    return jsonify({ "cost": b.cost }), 200



@app.route("/api/user/summary", methods=["GET"])
@jwt_required()
def user_parking_summary():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "User only"}), 403
    user = get_jwt_identity()
    user_id = User.query.filter_by(email=user).first_or_404().id

    # Total cost (same)
    total_spent = db.session.query(func.coalesce(func.sum(Booking.cost), 0)) \
        .filter(Booking.user_id == user_id).scalar()

    # Monthly cost: group by year and month for unique months
    monthly_cost = db.session.query(
        extract('year', Booking.start_time).label('year'),
        extract('month', Booking.start_time).label('month'),
        func.sum(Booking.cost).label('cost')
    ).filter(Booking.user_id == user_id) \
     .group_by('year', 'month') \
     .order_by('year', 'month').all()

    # Format month as "YYYY-MM" or full month name with year
    monthly = [
        {
            "month": f"{int(m.year)}-{int(m.month):02d}",
            "cost": float(m.cost)
        } for m in monthly_cost
    ]

    # Cost by lot
    cost_by_lot = db.session.query(
        Parking_lot.location,
        func.sum(Booking.cost).label('cost')
    ).join(Parking_spot, Parking_spot.id == Booking.parking_spot_id) \
     .join(Parking_lot, Parking_lot.id == Parking_spot.parking_lot_id) \
     .filter(Booking.user_id == user_id) \
     .group_by(Parking_lot.location).all()

    by_lot = [{"location": l, "cost": float(c)} for l, c in cost_by_lot]

    return jsonify({
        "total": float(total_spent),
        "monthly": monthly,
        "by_lot": by_lot
    })



@app.route("/api/admin/send-test-reminder", methods=["POST"])
@jwt_required()
def trigger_test_reminder():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    # Subquery: users who have a booking today
    booked_user_ids = db.session.query(Booking.user_id).filter(
        and_(
            Booking.start_time >= today_start,
            Booking.start_time <= today_end
        )
    ).distinct()

    # Query users who are NOT in that list
    users = User.query.filter(~User.id.in_(booked_user_ids)).with_entities(
        User.id, User.full_name, User.email
    ).all()

    user_data = [
        {"id": u.id, "full_name": u.full_name, "email": u.email}
        for u in users
    ]

    daily_booking_reminder.delay(user_data)

    return jsonify({
        "status": "Task triggered",
        "users_not_booked": len(user_data)
    }), 200

@app.route("/api/export-csv", methods=["POST"])
@jwt_required()
def trigger_csv_export():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "Users only"}), 403

    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first_or_404()

    bookings = db.session.query(
        Booking.id.label("booking_id"),
        Booking.parking_spot_id.label("spot_id"),
        Parking_spot.parking_lot_id.label("slot_id"),
        Booking.start_time,
        Booking.end_time,
        Booking.cost
    ).join(Parking_spot, Parking_spot.id == Booking.parking_spot_id) \
     .filter(Booking.user_id == user.id).all()

    booking_data = [{
        "booking_id": b.booking_id,
        "spot_id": b.spot_id,
        "slot_id": b.slot_id,
        "start_time": b.start_time.strftime("%Y-%m-%d %H:%M"),
        "end_time": b.end_time.strftime("%Y-%m-%d %H:%M") if b.end_time else "",
        "cost": b.cost,
        "remarks": ""
    } for b in bookings]

    task = csv_report_for_user.delay(user.full_name, booking_data)

    return jsonify({
        "message": "CSV export job started.",
        "task_id": task.id
    }), 202


from flask import send_from_directory

@app.route("/api/csv_result/<task_id>", methods=["GET"])
@jwt_required()
def download_csv_result(task_id):
    result = AsyncResult(task_id)

    if result.state == "SUCCESS":
        filename = result.result
        return send_from_directory("static", filename, as_attachment=True)
    elif result.state == "FAILURE":
        return jsonify({"status": "FAILURE", "error": str(result.result)}), 500
    else:
        return jsonify({"status": result.state}), 202
    

@app.route("/api/send-monthly-report", methods=["GET"])
def send_monthly_report():
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    month_end = datetime(now.year, now.month, now.day, 23, 59, 59)  # Today end

    user_reports = []

    users = User.query.all()
    for user in users:
        bookings = Booking.query.filter(
            Booking.user_id == user.id,
            Booking.start_time >= month_start,
            Booking.end_time <= month_end
        ).all()

        if not bookings:
            continue

        total_spent = sum(b.cost for b in bookings)
        lot_counts = {}
        for b in bookings:
            lot = b.parking_spot.parking_lot
            lot_counts[lot.location] = lot_counts.get(lot.location, 0) + 1

        most_used_lot = max(lot_counts, key=lot_counts.get)

        user_reports.append({
            "username": user.full_name,
            "email": user.email,
            "month": month_start.strftime('%B %Y'),
            "total_bookings": len(bookings),
            "total_spent": total_spent,
            "most_used_lot": most_used_lot
        })

    print(f"[DEBUG] user_reports: {user_reports}")  # optional debug output

    monthly_report.delay(user_reports)

    return jsonify({"status": "Monthly reports sent.", "data": user_reports})

import time

@app.route('/api/test_cache')
@cache.cached(timeout=30)  # Cache for 30 seconds
def test_cache():
    print("[DEBUG] Cache MISS - regenerating response")
    return jsonify({
        "message": "This response is cached for 30 seconds.",
        "timestamp": time.time()
    })