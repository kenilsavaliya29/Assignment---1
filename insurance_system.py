import uuid
from datetime import datetime, timedelta
import json
import os


policyholders = {}  
claims = {} 


POLICY_TYPES = ["Health", "Vehicle", "Life"]
CLAIM_STATUSES = ["Pending", "Approved", "Rejected"]


def save_data():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    with open(os.path.join(data_dir, "policyholders.json"), "w") as f:
        json.dump(policyholders, f, indent=4)
    
    with open(os.path.join(data_dir, "claims.json"), "w") as f:
        json.dump(claims, f, indent=4)

def load_data():
   
    global policyholders, claims
    data_dir = "data"
    
    try:
        if os.path.exists(os.path.join(data_dir, "policyholders.json")):
            with open(os.path.join(data_dir, "policyholders.json"), "r") as f:
                policyholders = json.load(f)
        
        if os.path.exists(os.path.join(data_dir, "claims.json")):
            with open(os.path.join(data_dir, "claims.json"), "r") as f:
                claims = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        # Initialize with empty dictionaries if loading fails
        policyholders = {}
        claims = {}

class PolicyholderManager:

    
    @staticmethod
    def register_policyholder(name, age, policy_type, sum_insured):

        try:

            if not name or not name.strip():
                return {"success": False, "message": "Name is required"}
            
            try:
                age = int(age)
                if age <= 0 or age > 120:  
                    return {"success": False, "message": "Age must be a positive number between 1 and 120"}
            except ValueError:
                return {"success": False, "message": "Age must be a valid number"}
            
            if policy_type not in POLICY_TYPES:
                return {"success": False, "message": f"Policy type must be one of: {', '.join(POLICY_TYPES)}"}
            
            try:
                sum_insured = float(sum_insured)
                if sum_insured <= 0:
                    return {"success": False, "message": "Sum insured must be a positive number"}
            except ValueError:
                return {"success": False, "message": "Sum insured must be a valid number"}
            
            # Generate unique ID and create policyholder
            policyholder_id = str(uuid.uuid4())
            policyholders[policyholder_id] = {
                "id": policyholder_id,
                "name": name.strip(),
                "age": age,
                "policy_type": policy_type,
                "sum_insured": sum_insured,
                "registration_date": datetime.now().strftime("%Y-%m-%d")
            }
            save_data()
            return {"success": True, "policyholder_id": policyholder_id}
        
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    @staticmethod
    def get_all_policyholders():
        """Get all policyholders"""
        return list(policyholders.values())
    
    @staticmethod
    def get_policyholder(policyholder_id):
        """Get a specific policyholder by ID"""
        return policyholders.get(policyholder_id)
    
    @staticmethod
    def update_policyholder(policyholder_id, **kwargs):
        """Update policyholder information"""
        if policyholder_id not in policyholders:
            return {"success": False, "message": "Policyholder not found"}
        
        valid_fields = {"name", "age", "policy_type", "sum_insured"}
        
        for key, value in kwargs.items():
            if key in valid_fields:
                # Validate based on field type
                if key == "age":
                    try:
                        value = int(value)
                        if value <= 0 or value > 120:
                            return {"success": False, "message": "Age must be a positive number between 1 and 120"}
                    except ValueError:
                        return {"success": False, "message": "Age must be a valid number"}
                
                elif key == "policy_type" and value not in POLICY_TYPES:
                    return {"success": False, "message": f"Policy type must be one of: {', '.join(POLICY_TYPES)}"}
                
                elif key == "sum_insured":
                    try:
                        value = float(value)
                        if value <= 0:
                            return {"success": False, "message": "Sum insured must be a positive number"}
                    except ValueError:
                        return {"success": False, "message": "Sum insured must be a valid number"}
                
                policyholders[policyholder_id][key] = value
        
        save_data()
        return {"success": True, "message": "Policyholder updated successfully"}

class ClaimManager:
    """Handles all operations related to claims"""
    
    @staticmethod
    def add_claim(policyholder_id, claim_amount, reason, claim_date=None, status="Pending"):
        """
        Add a new claim
        
        Parameters:
        - policyholder_id: ID of the policyholder filing the claim
        - claim_amount: Amount being claimed
        - reason: Reason for the claim
        - claim_date: Date of the claim (defaults to current date)
        - status: Claim status (Pending, Approved, Rejected)
        
        Returns:
        - Dictionary with success status and message/ID
        """
        try:
            # Input validation
            if policyholder_id not in policyholders:
                return {"success": False, "message": "Policyholder not found"}
            
            try:
                claim_amount = float(claim_amount)
                if claim_amount <= 0:
                    return {"success": False, "message": "Claim amount must be a positive number"}
            except ValueError:
                return {"success": False, "message": "Claim amount must be a valid number"}
            
            if not reason or not reason.strip():
                return {"success": False, "message": "Claim reason is required"}
            
            if status not in CLAIM_STATUSES:
                return {"success": False, "message": f"Status must be one of: {', '.join(CLAIM_STATUSES)}"}
            
            # Use current date if not provided
            if not claim_date:
                claim_date = datetime.now().strftime("%Y-%m-%d")
            
            # Generate unique ID and create claim
            claim_id = str(uuid.uuid4())
            claims[claim_id] = {
                "id": claim_id,
                "policyholder_id": policyholder_id,
                "claim_amount": claim_amount,
                "reason": reason.strip(),
                "status": status,
                "claim_date": claim_date
            }
            save_data()
            return {"success": True, "claim_id": claim_id}
        
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    @staticmethod
    def get_all_claims():
        """Get all claims"""
        return list(claims.values())
    
    @staticmethod
    def get_claim(claim_id):
        """Get a specific claim by ID"""
        return claims.get(claim_id)
    
    @staticmethod
    def update_claim_status(claim_id, new_status):
        """Update the status of a claim"""
        if claim_id not in claims:
            return {"success": False, "message": "Claim not found"}
        
        if new_status not in CLAIM_STATUSES:
            return {"success": False, "message": f"Status must be one of: {', '.join(CLAIM_STATUSES)}"}
        
        # Prevent approval if claim amount exceeds sum insured
        if new_status == "Approved":
            claim = claims[claim_id]
            policyholder_id = claim["policyholder_id"]
            if policyholder_id not in policyholders:
                
                return {"success": False, "message": "Associated policyholder not found"}
            
            claim_amount = claim["claim_amount"]
            sum_insured = policyholders[policyholder_id]["sum_insured"]

            if claim_amount > sum_insured:
                return {"success": False, "message": f"Claim amount (₹{claim_amount:,.2f}) exceeds sum insured (₹{sum_insured:,.2f}). Cannot approve claim."}

        claims[claim_id]["status"] = new_status
        save_data()
        return {"success": True, "message": "Claim status updated successfully"}
    
    @staticmethod
    def get_policyholder_claims(policyholder_id): 
    
        """Get all claims for a specific policyholder"""
        return [claim for claim in claims.values() if claim["policyholder_id"] == policyholder_id]

class RiskAnalyzer: 
    """Analyzes risk based on claim patterns and history"""
    
    @staticmethod
    def calculate_claim_frequency(policyholder_id, months=12):
        """
        Calculate how many claims a policyholder has made in the given period
        
        Parameters:
        - policyholder_id: ID of the policyholder
        - months: Number of months to look back (default: 12)
        
        Returns:
        - Number of claims in the period
        """
        if policyholder_id not in policyholders:
            return {"success": False, "message": "Policyholder not found"}
        
        # Calculate date threshold
        today = datetime.now()
        threshold_date = (today - timedelta(days=30*months)).strftime("%Y-%m-%d")
        
        # Count claims within period
        policyholder_claims = ClaimManager.get_policyholder_claims(policyholder_id)
        recent_claims = [claim for claim in policyholder_claims if claim["claim_date"] >= threshold_date]
        
        return len(recent_claims)
    
    @staticmethod
    def calculate_claim_ratio(policyholder_id):
        """
        Calculate the ratio of total claim amount to sum insured
        
        Parameters:
        - policyholder_id: ID of the policyholder
        
        Returns:
        - Claim ratio as a percentage
        """
        if policyholder_id not in policyholders:
            return {"success": False, "message": "Policyholder not found"}
        
        policyholder = policyholders[policyholder_id]
        sum_insured = policyholder["sum_insured"]
        
        # Calculate total claim amount
        policyholder_claims = ClaimManager.get_policyholder_claims(policyholder_id)
        
        total_claim_amount = sum(claim["claim_amount"] for claim in policyholder_claims)
        
        # Calculate and return the ratio
        if sum_insured > 0:
            return (total_claim_amount / sum_insured) * 100
        else:
            return 0
    
    @staticmethod
    def identify_high_risk_policyholders():
        """
        Identify high-risk policyholders based on:
        - More than 3 claims in the last year
        - Claim ratio > 80%
        
        Returns:
        - List of high-risk policyholder IDs with risk reasons
        """
        high_risk = []
        
        for policyholder_id in policyholders:
            risk_factors = []
            
            # Check claim frequency
            claim_frequency = RiskAnalyzer.calculate_claim_frequency(policyholder_id)
            if claim_frequency > 3:
                risk_factors.append(f"High claim frequency: {claim_frequency} claims in the last year")
            
            # Check claim ratio
            claim_ratio = RiskAnalyzer.calculate_claim_ratio(policyholder_id)
            if claim_ratio > 80:
                risk_factors.append(f"High claim ratio: {claim_ratio:.2f}% of sum insured")
            
            if risk_factors:
                high_risk.append({
                    "policyholder_id": policyholder_id,
                    "name": policyholders[policyholder_id]["name"],
                    "risk_factors": risk_factors
                })
        
        return high_risk
    
    @staticmethod
    def claims_by_policy_type():
        """
        Aggregate and analyze claims by policy type
        
        Returns:
        - Dictionary with policy types as keys and claim statistics as values
        """
        policy_type_stats = {policy_type: {
            "total_claims": 0,
            "total_amount": 0,
            "approved_claims": 0,
            "approved_amount": 0,
            "pending_claims": 0,
            "rejected_claims": 0
        } for policy_type in POLICY_TYPES}
        
        for claim in claims.values():
            policyholder_id = claim["policyholder_id"]
            
            # Skip if policyholder doesn't exist
            if policyholder_id not in policyholders:
                continue
                
            policy_type = policyholders[policyholder_id]["policy_type"]
            claim_amount = claim["claim_amount"]
            status = claim["status"]
            
            # Update statistics
            policy_type_stats[policy_type]["total_claims"] += 1
            policy_type_stats[policy_type]["total_amount"] += claim_amount
            
            if status == "Approved":
                policy_type_stats[policy_type]["approved_claims"] += 1
                policy_type_stats[policy_type]["approved_amount"] += claim_amount
            elif status == "Pending":
                policy_type_stats[policy_type]["pending_claims"] += 1
            elif status == "Rejected":
                policy_type_stats[policy_type]["rejected_claims"] += 1
        
        return policy_type_stats

class ReportGenerator:
    """Generates various reports and statistics"""
    
    @staticmethod
    def total_claims_per_month(months=12):
        """
        Calculate total claims per month for the given period
        
        Parameters:
        - months: Number of months to look back (default: 12)
        
        Returns:
        - Dictionary with month-year as keys and claim counts as values
        """
        monthly_claims = {}
        
        # Generate all month-year combinations for the period
        today = datetime.now()
        for i in range(months):
            month_date = today - timedelta(days=30*i)
            month_key = month_date.strftime("%Y-%m")
            monthly_claims[month_key] = {"count": 0, "amount": 0}
        
        # Count claims by month
        for claim in claims.values():
            claim_date = datetime.strptime(claim["claim_date"], "%Y-%m-%d")
            month_key = claim_date.strftime("%Y-%m")
            
            if month_key in monthly_claims:
                monthly_claims[month_key]["count"] += 1
                monthly_claims[month_key]["amount"] += claim["claim_amount"]
        
        return monthly_claims
    
    @staticmethod
    def average_claim_amount_by_policy_type():
        """
        Calculate average claim amount by policy type
        
        Returns:
        - Dictionary with policy types as keys and average claim amounts as values
        """
        policy_claims = {policy_type: {"total_amount": 0, "count": 0} for policy_type in POLICY_TYPES}
        
        for claim in claims.values():
            policyholder_id = claim["policyholder_id"]
            
            # Skip if policyholder doesn't exist
            if policyholder_id not in policyholders:
                continue
                
            policy_type = policyholders[policyholder_id]["policy_type"]
            claim_amount = claim["claim_amount"]
            
            policy_claims[policy_type]["total_amount"] += claim_amount
            policy_claims[policy_type]["count"] += 1
        
        # Calculate averages
        averages = {}
        for policy_type, data in policy_claims.items():
            if data["count"] > 0:
                averages[policy_type] = data["total_amount"] / data["count"]
            else:
                averages[policy_type] = 0
        
        return averages
    
    @staticmethod
    def highest_claim():
        """
        Find the highest claim filed
        
        Returns:
        - Claim object with policyholder information
        """
        if not claims:
            return None
        
        highest_amount = 0
        highest_claim = None
        
        for claim in claims.values():
            if claim["claim_amount"] > highest_amount:
                highest_amount = claim["claim_amount"]
                highest_claim = claim
        
        if highest_claim and highest_claim["policyholder_id"] in policyholders:
            # Add policyholder information to claim
            highest_claim_with_info = highest_claim.copy()
            highest_claim_with_info["policyholder_name"] = policyholders[highest_claim["policyholder_id"]]["name"]
            highest_claim_with_info["policy_type"] = policyholders[highest_claim["policyholder_id"]]["policy_type"]
            return highest_claim_with_info
        
        return highest_claim
    
    @staticmethod
    def policyholders_with_pending_claims():
        """
        List policyholders with pending claims
        
        Returns:
        - List of policyholder objects with their pending claims
        """
        pending_claims_holders = {}
        
        for claim in claims.values():
            if claim["status"] == "Pending":
                policyholder_id = claim["policyholder_id"]
                
                if policyholder_id not in policyholders:
                    continue
                
                if policyholder_id not in pending_claims_holders:
                    policyholder = policyholders[policyholder_id].copy()
                    policyholder["pending_claims"] = []
                    pending_claims_holders[policyholder_id] = policyholder
                
                pending_claims_holders[policyholder_id]["pending_claims"].append(claim)
        
        return list(pending_claims_holders.values())

load_data()
