from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
import pandas as pd
import zipfile
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
            wedding_id = file.filename[:-5] #remove ".xlsx" ending
            #check if wedding_id is already in the database (must be unique)
            if GuestModel.query.filter_by(wedding_id=wedding_id, user_id=current_user).first():
                abort(400, message="A guest list with this wedding ID for this user already exists.")
            try:
                df = pd.read_excel(file, engine="openpyxl") #output is a pandas DataFrame object
                expected_columns = ["name", "number", "email", "wedding_id"]
                if not set(expected_columns).issubset(df.columns) or len(df.columns) != len(expected_columns):
                    #abort() statements inside a try() block won't be executed there,
                    #they raise a HTTP exception that must be handled outside, or use a return()
                    return {"message": "Excel format is not correct."}, 400
                for index, row in df.iterrows():
                    guest = GuestModel(name=row["name"],
                                       number=row["number"],
                                       email=row["email"],
                                       user_id=current_user,
                                       wedding_id=wedding_id)
                    guest.save_to_db()
                return {"message": "Guests added to database succesfully."}, 201
            except zipfile.BadZipfile:
                abort(400, message="Uploaded file is not a valid Excel file. Please check file is not empty")
            except Exception as e:
                abort(500, message=f"Internal server error: {e}")
        else:
            abort(400, message="Only Excel files (.xlsx) are allowed")