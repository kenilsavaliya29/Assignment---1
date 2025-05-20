
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from insurance_system import (
    PolicyholderManager, ClaimManager, RiskAnalyzer, ReportGenerator,
    POLICY_TYPES, CLAIM_STATUSES
)

app = Flask(__name__)
app.secret_key = "abc_insurance_secret_key"

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Policyholder routes
@app.route('/policyholders')
def list_policyholders():
    policyholders = PolicyholderManager.get_all_policyholders()
    return render_template('policyholders.html', policyholders=policyholders)

@app.route('/policyholders/add', methods=['GET', 'POST'])
def add_policyholder():
    if request.method == 'POST':
        result = PolicyholderManager.register_policyholder(
            name=request.form['name'],
            age=request.form['age'],
            policy_type=request.form['policy_type'],
            sum_insured=request.form['sum_insured']
        )
        
        if result['success']:
            flash('Policyholder registered successfully!', 'success')
            return redirect(url_for('list_policyholders'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('add_policyholder.html', policy_types=POLICY_TYPES)

@app.route('/policyholders/<policyholder_id>')
def view_policyholder(policyholder_id):
    policyholder = PolicyholderManager.get_policyholder(policyholder_id)
    if not policyholder:
        flash('Policyholder not found', 'danger')
        return redirect(url_for('list_policyholders'))
    
    # Get policyholder claims
    policyholder_claims = ClaimManager.get_policyholder_claims(policyholder_id)
    
    # Get risk metrics
    claim_frequency = RiskAnalyzer.calculate_claim_frequency(policyholder_id)
    claim_ratio = RiskAnalyzer.calculate_claim_ratio(policyholder_id)
    
    return render_template(
        'view_policyholder.html',
        policyholder=policyholder,
        claims=policyholder_claims,
        claim_frequency=claim_frequency,
        claim_ratio=claim_ratio
    )

# Claim routes
@app.route('/claims')
def list_claims():
    claims = ClaimManager.get_all_claims()
    return render_template('claims.html', claims=claims)

@app.route('/claims/add', methods=['GET', 'POST'])
def add_claim():
    if request.method == 'POST':
        result = ClaimManager.add_claim(
            policyholder_id=request.form['policyholder_id'],
            claim_amount=request.form['claim_amount'],
            reason=request.form['reason'],
            status=request.form['status']
        )
        
        if result['success']:
            flash('Claim added successfully!', 'success')
            return redirect(url_for('list_claims'))
        else:
            flash(result['message'], 'danger')
    
    policyholders = PolicyholderManager.get_all_policyholders()
    return render_template(
        'add_claim.html',
        policyholders=policyholders,
        claim_statuses=CLAIM_STATUSES
    )

@app.route('/claims/<claim_id>')
def view_claim(claim_id):
    claim = ClaimManager.get_claim(claim_id)
    if not claim:
        flash('Claim not found', 'danger')
        return redirect(url_for('list_claims'))
    
    # Get policyholder information
    policyholder = PolicyholderManager.get_policyholder(claim['policyholder_id'])
    
    return render_template('view_claim.html', claim=claim, policyholder=policyholder)

@app.route('/claims/<claim_id>/update-status', methods=['POST'])
def update_claim_status(claim_id):
    new_status = request.form['status']
    result = ClaimManager.update_claim_status(claim_id, new_status)
    
    if result['success']:
        flash('Claim status updated successfully!', 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('view_claim', claim_id=claim_id))

# Risk Analysis routes
@app.route('/risk-analysis')
def risk_analysis():
    high_risk_policyholders = RiskAnalyzer.identify_high_risk_policyholders()
    claims_by_policy = RiskAnalyzer.claims_by_policy_type()
    
    return render_template(
        'risk_analysis.html',
        high_risk_policyholders=high_risk_policyholders,
        claims_by_policy=claims_by_policy
    )

# Reports routes
@app.route('/reports')
def reports():
    # Monthly claims
    monthly_claims = ReportGenerator.total_claims_per_month()
    
    # Average claim by policy type
    avg_claims = ReportGenerator.average_claim_amount_by_policy_type()
    
    # Highest claim
    highest_claim = ReportGenerator.highest_claim()
    
    # Policyholders with pending claims
    pending_claims = ReportGenerator.policyholders_with_pending_claims()
    
    return render_template(
        'reports.html',
        monthly_claims=monthly_claims,
        avg_claims=avg_claims,
        highest_claim=highest_claim,
        pending_claims=pending_claims
    )

# API Endpoints for REST interface
@app.route('/api/policyholders', methods=['GET'])
def api_get_policyholders():
    policyholders = PolicyholderManager.get_all_policyholders()
    return jsonify(policyholders)

@app.route('/api/policyholders', methods=['POST'])
def api_add_policyholder():
    data = request.json
    result = PolicyholderManager.register_policyholder(
        name=data.get('name'),
        age=data.get('age'),
        policy_type=data.get('policy_type'),
        sum_insured=data.get('sum_insured')
    )
    return jsonify(result)

@app.route('/api/policyholders/<policyholder_id>', methods=['GET'])
def api_get_policyholder(policyholder_id):
    policyholder = PolicyholderManager.get_policyholder(policyholder_id)
    if policyholder:
        return jsonify(policyholder)
    return jsonify({"success": False, "message": "Policyholder not found"}), 404

@app.route('/api/claims', methods=['GET'])
def api_get_claims():
    claims = ClaimManager.get_all_claims()
    return jsonify(claims)

@app.route('/api/claims', methods=['POST'])
def api_add_claim():
    data = request.json
    result = ClaimManager.add_claim(
        policyholder_id=data.get('policyholder_id'),
        claim_amount=data.get('claim_amount'),
        reason=data.get('reason'),
        status=data.get('status', 'Pending')
    )
    return jsonify(result)

@app.route('/api/risk/high-risk', methods=['GET'])
def api_high_risk():
    high_risk = RiskAnalyzer.identify_high_risk_policyholders()
    return jsonify(high_risk)

@app.route('/api/reports/monthly-claims', methods=['GET'])
def api_monthly_claims():
    months = request.args.get('months', 12, type=int)
    monthly_claims = ReportGenerator.total_claims_per_month(months)
    return jsonify(monthly_claims)

if __name__ == '__main__':
    app.run(debug=True)