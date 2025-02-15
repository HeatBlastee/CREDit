from operator import itemgetter
import pandas as pd
import requests
import random

GEOAPIFY_API_KEY = 'YOUR_GEOAPIFY_API_KEY'  # Replace with your actual API key

def transaction_analysis(userId):
    """
    Simulates transaction analysis for a user.
    """
    online_spends = round(random.uniform(2000, 14000), 2)
    earns = round(random.uniform(40000, 60000), 2)
    cash_withdrawal = round(100000 - (online_spends + earns), 2)
    
    return [
        {'name': 'Online Spends', 'value': online_spends},
        {'name': 'Earns', 'value': earns},
        {'name': 'Cash Withdrawal', 'value': cash_withdrawal}
    ]

def competitor_analysis(pincode, typeOfBusiness):
    """
    Simulates competitor analysis for a given pincode and business type.
    """
    print(f"Simulating competitor analysis for pincode: {pincode} and business type: {typeOfBusiness}")
    
    competitorList = [f'Competitor {chr(65 + i)}' for i in range(random.randint(1, 5))]
    number_of_competitors = len(competitorList)
    competitor_rating = round(random.uniform(50, 100) / number_of_competitors, 2) if number_of_competitors > 0 else 0
    
    return {
        'name': 'Competition Score',
        'rating': competitor_rating,
        'competitors': competitorList,
        'remarks': ''
    }

def oppurtunity_rating(state, businessDistrict):
    """
    Simulates opportunity rating for a given state and district.
    """
    print(f"Simulating opportunity rating for state: {state} and district: {businessDistrict}")
    
    opportunity_rating = round(random.uniform(50, 90), 2)
    
    return {
        'name': 'Opportunity Score',
        'rating': opportunity_rating
    }

def sectoral_analysis(typeOfBusiness):
    """
    Simulates sectoral analysis for a given business type.
    """
    print(f"Simulating sectoral analysis for business type: {typeOfBusiness}")
    
    sector_rating = round(random.uniform(50, 85), 2)
    top_sector_list = random.sample(['Retail', 'Hospitality', 'Technology', 'Agriculture', 'Healthcare'], 3)
    
    return {
        'name': 'Sectoral Score',
        'rating': sector_rating,
        'sectors': top_sector_list,
        'remark': ''
    }

def relative_prosperity(state, district):
    """
    Simulates relative prosperity for a given state and district.
    Includes specific data for Himachal Pradesh (Una) and surrounding regions.
    """
    print(f"Simulating relative prosperity for state: {state} and district: {district}")
    
    # Define prosperity data for Una and nearby districts
    prosperity_data = {
        'Himachal Pradesh': {
            'Una': 85.0,
            'Kangra': 80.0,
            'Shimla': 75.0,
            'Solan': 70.0,
        },
        'Punjab': {
            'Hoshiarpur': 78.0,
            'Rupnagar': 72.0,
            'Patiala': 68.0,
        },
        'Haryana': {
            'Ambala': 76.0,
            'Panchkula': 74.0,
            'Yamunanagar': 70.0,
        },
        'Uttarakhand': {
            'Dehradun': 82.0,
            'Haridwar': 79.0,
            'Nainital': 75.0,
        }
    }
    
    # Get prosperity rating for the given district
    prosperity_rating = prosperity_data.get(state, {}).get(district, round(random.uniform(60, 95), 2))
    
    # Get top 3 districts (excluding the current district)
    all_districts = [d for s in prosperity_data.values() for d in s.keys()]
    top_3_districts = random.sample([d for d in all_districts if d != district], 3)
    
    return {
        'name': 'Prosperity Score',
        'rating': prosperity_rating,
        'moreProsperousAreas': top_3_districts,
        'remark': ''
    }

def ease_of_business(pincode, state):
    """
    Simulates ease of business for a given pincode and state.
    Includes specific data for Himachal Pradesh and surrounding states.
    """
    print(f"Simulating ease of business for pincode: {pincode} and state: {state}")
    
    # Define ease of business data for Una and nearby states
    ease_of_business_data = {
        'Himachal Pradesh': 85.0,
        'Punjab': 80.0,
        'Haryana': 78.0,
        'Uttarakhand': 82.0,
    }
    
    # Get ease of business rating for the given state
    ease_of_business_rating = ease_of_business_data.get(state, round(random.uniform(50, 90), 2))
    
    # Get top 3 states (excluding the current state)
    all_states = list(ease_of_business_data.keys())
    top_3_states = random.sample([s for s in all_states if s != state], 3)
    
    return {
        'name': 'Ease of Business Score',
        'rating': ease_of_business_rating,
        'betterAreas': top_3_states,
        'remark': ''
    }