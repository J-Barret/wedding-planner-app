from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
import pandas as pd
from models.guest import GuestModel

blp = Blueprint("Guests", "guests", description="Operations on guests")

@blp.route("/upload")
class ExcelUpload(MethodView):

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if "file" not in request.files:
            abort(400, message="No file part in the request")
        file = request.files["file"]
        if file.filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(file) #output is a pandas DataFrame object
                expected_columns = ["name", "number", "email"]
                if not all(col in df.columns for col in expected_columns):
                    abort(400, message="Excel format is not correct")
                for index, row in df.iterrows():
                    guest = GuestModel(name=row["name"], number=row["number"], email=row["email"], user_id=current_user)
                    guest.save_to_db()
                return {"message": "Guests added to database succesfully."}, 201
            except Exception as e:
                abort(500, message=f"Internal server error: {e}")
        else:
            abort(400, message="Only Excel files (.xlsx) are allowed")