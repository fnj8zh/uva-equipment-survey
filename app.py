from datetime import datetime, timezone
import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from models import EquipmentSurvey
from storage import append_record, load_all_records

app = Flask(__name__, static_folder="static", template_folder="templates")

IMAGE_DIR = "data/images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit_survey():
    data = request.form.to_dict()

    data["needs_maintenance"] = "needs_maintenance" in data

    if data.get("return_date") == "":
        data["return_date"] = None

    # ------------- HANDLE OTHER FIELDS -------------
    if data.get("item_rented") == "Other":
        typed = data.get("item_rented_other", "").strip()
        if typed:
            data["item_rented"] = typed
        data.pop("item_rented_other", None)

    if data.get("usage_purpose") == "Other":
        typed = data.get("usage_purpose_other", "").strip()
        if typed:
            data["usage_purpose"] = typed
        data.pop("usage_purpose_other", None)

    # ------------- HANDLE FILE UPLOAD -------------
    uploaded_file = request.files.get("item_image")
    image_filename = None

    if uploaded_file and uploaded_file.filename:
        safe_filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + uploaded_file.filename
        image_path = os.path.join(IMAGE_DIR, safe_filename)
        uploaded_file.save(image_path)
        image_filename = safe_filename

    data["image_filename"] = image_filename

    try:
        survey = EquipmentSurvey(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    record = survey.dict()

    # Ensure return_date is ISO before saving
    if record.get("return_date"):
        record["return_date"] = record["return_date"].isoformat()

    append_record(record)
    return jsonify({"status": "saved"}), 200


@app.get("/surveys")
def list_surveys():
    records = load_all_records()
    return jsonify(records), 200


@app.get("/time")
def get_time():
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    return jsonify({
        "utc_iso": now_utc.isoformat(),
        "local_iso": now_local.isoformat()
    })


@app.get("/ping")
def ping():
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })


@app.get("/images/<filename>")
def serve_image(filename):
    return send_from_directory("data/images", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
