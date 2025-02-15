from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import time
import enum
from bson.objectid import ObjectId

# Importing the rating functions
from ratings import competitor_analysis, oppurtunity_rating, sectoral_analysis, relative_prosperity, ease_of_business, transaction_analysis

app = FastAPI()

MONGODB_URL = "mongodb://localhost:27017"
client = pymongo.MongoClient(MONGODB_URL)
db = client['hackathon']

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BorrowerModel(BaseModel):
    name: str
    mobileNumber: str
    typeOfBusiness: str
    businessAddress: str
    businessState: str
    businessDistrict: str
    businessPinCode: str
    amountApplied: int
    amountApproved: Optional[int] = 0
    consentId: Optional[str] = None
    sessionId: Optional[str] = None
    applicationStatus: int

class ApplicationStatus(enum.Enum):
    newApplication = 0
    accepted = 1
    halted = 2
    rejected = 3

@app.get('/')
def index():
    return {'msg': 'API working. Check /docs for more'}
@app.post('/addborrower')
def add_borrower(borrower: dict = Body(...)):
    borrower = jsonable_encoder(borrower)
    borrower['businessState'] = borrower['businessState'].lower()
    borrower['businessDistrict'] = borrower['businessDistrict'].lower()

    result = db["borrowers"].insert_one(borrower)
    userid = str(result.inserted_id)  # Convert ObjectId to string

    print("*" * 10, userid, "*" * 10)

    # Simulate consent ID
    consentId = f"consent-{userid}"
    db["borrowers"].update_one({"_id": ObjectId(userid)}, {"$set": {"consentId": consentId}})
    
    return {'msg': 'Borrower added successfully', 'userId': userid, 'consentId': consentId}
@app.get('/all')
def get_all_application():
    borrowers = db["borrowers"].find()
    borrowersList = []
    for borrower in borrowers:
        userId = str(borrower['_id'])
        name = borrower['name']
        mobileNumber = borrower['mobileNumber']
        applicationDate = borrower['_id'].generation_time
        applicationStatus = borrower['applicationStatus']

        obj = {
            'userId': userId,
            'name': name,
            'mobileNumber': mobileNumber,
            'applicationDate': applicationDate,
            'applicationStatus': applicationStatus
        }

        borrowersList.append(obj)

    return borrowersList

@app.get('/getdatasession')
def get_data_session(userid: str):
    # Simulate fetching data session
    time.sleep(2)  # Simulate delay
    mock_data = {
        "accountDetails": {
            "maskedAccNumber": "1234-5678-1234",
            "type": "Savings",
            "holders": {
                "holder": [
                    {
                        "email": "holder@example.com",
                        "pan": "ABCDE1234F"
                    }
                ]
            }
        }
    }
    
    # Simulate saving the fetched data
    db['financialData'].insert_one({"userid": userid, "accountDetails": mock_data})
    
    return {"msg": "Successfully fetched and saved data", "data": mock_data}

@app.get('/userinfo')
def fetch_user_info(userid: str):
    borrower = db['borrowers'].find_one({'_id': ObjectId(userid)}, {'_id': False, 'consentId': False, 'sessionId': False})
    financialDetails = db['financialData'].find_one({'userid': userid})

    if not financialDetails:
        return JSONResponse(status_code=404, content={"msg": "Financial details not found."})

    accountDetails = financialDetails.get('accountDetails', {})
    
    # Check if 'holders' key exists
    holders = accountDetails.get('holders', {}).get('holder', [])
    if not holders:
        accountEmail = 'NA'
        pan = 'NA'
    else:
        accountEmail = holders[0].get('email', 'NA')
        pan = holders[0].get('pan', 'NA')

    pincode = borrower['businessPinCode']
    typeOfBusiness = borrower['typeOfBusiness']
    state = borrower['businessState']
    district = borrower['businessDistrict']
    amountApplied = borrower['amountApplied']

    # Call the analysis functions
    competitorAnalysis = competitor_analysis(pincode, typeOfBusiness)
    oppurtunityRating = oppurtunity_rating(state, district)
    sectoralAnalysis = sectoral_analysis(typeOfBusiness.lower())
    relativeProsperity = relative_prosperity(state, district)
    easeOfBusiness = ease_of_business(pincode, state)
    transactionAnalysis = transaction_analysis(userid)

    score = (competitorAnalysis['rating'] + oppurtunityRating['rating'] + sectoralAnalysis['rating'] + relativeProsperity['rating'] + easeOfBusiness['rating'])
    allowedCredit = int((score / 500) * amountApplied)

    obj = {
        'userFormSubmittedInfo': {
            'Name': borrower['name'],
            'Phone': borrower['mobileNumber'],
            'Business Type': borrower['typeOfBusiness'],
            'Business Address': borrower['businessAddress'],
            'Amount Applied': borrower['amountApplied']
        },
        'score': score,
        'allowedCredit': allowedCredit,
        'accountDetails': {
            'Account Number': accountDetails.get('maskedAccNumber', 'NA'),
            'Account Type': accountDetails.get('type', 'NA'),
            'Account Email': accountEmail,
            'PAN': pan
        },
        'indicators': [
            competitorAnalysis,
            oppurtunityRating,
            sectoralAnalysis,
            relativeProsperity,
            easeOfBusiness,
        ],
        'transactionalAnalysis': transactionAnalysis
    }

    return obj

@app.get('/updateuser')
@app.get('/updateuser')
def update_user(userid: str, updateType: str, approvedAmount: Optional[int] = 0):
    ApplicationStatusValue = None
    if updateType == 'new':
        ApplicationStatusValue = ApplicationStatus.newApplication.value
    elif updateType == 'accept':
        ApplicationStatusValue = ApplicationStatus.accepted.value
    elif updateType == 'reject':
        ApplicationStatusValue = ApplicationStatus.rejected.value
    elif updateType == 'halt':
        ApplicationStatusValue = ApplicationStatus.halted.value

    db["borrowers"].update_one({"_id": ObjectId(userid)}, {"$set": {"applicationStatus": ApplicationStatusValue, "approvedAmount": approvedAmount}})

    return {'msg': f'Value of user Application Status updated to {ApplicationStatusValue}'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)