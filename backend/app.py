from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv 
from database import Database

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize database
db = Database()

# Serve the frontend
@app.route('/')
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'billing_tracker.html')

# ============================================================================
# FACILITY GROUPS
# ============================================================================

@app.route('/api/facility-groups', methods=['GET'])
def get_facility_groups():
    """Get all facility groups with their facilities"""
    try:
        groups = db.get_facility_groups()
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facility-groups', methods=['POST'])
def create_facility_group():
    """Create a new facility group"""
    try:
        data = request.json
        group_id = db.create_facility_group(data)
        return jsonify({'id': group_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facility-groups/<int:group_id>', methods=['PUT'])
def update_facility_group(group_id):
    """Update a facility group"""
    try:
        data = request.json
        db.update_facility_group(group_id, data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facility-groups/<int:group_id>', methods=['DELETE'])
def delete_facility_group(group_id):
    """Delete a facility group"""
    try:
        db.delete_facility_group(group_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# FACILITIES
# ============================================================================

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    """Get all facilities"""
    try:
        facilities = db.get_facilities()
        return jsonify(facilities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facilities', methods=['POST'])
def create_facility():
    """Create a new facility"""
    try:
        data = request.json
        facility_id = db.create_facility(data)
        return jsonify({'id': facility_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facilities/<int:facility_id>', methods=['DELETE'])
def delete_facility(facility_id):
    """Delete a facility"""
    try:
        db.delete_facility(facility_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# BILLING RECORDS
# ============================================================================

@app.route('/api/billing-records', methods=['GET'])
def get_billing_records():
    """Get all billing records"""
    try:
        records = db.get_billing_records()
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/billing-records', methods=['POST'])
def save_billing_record():
    """Create or update a billing record"""
    try:
        data = request.json
        db.save_billing_record(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# CUSTOM DATES
# ============================================================================

@app.route('/api/custom-dates/<int:group_id>', methods=['GET'])
def get_custom_dates(group_id):
    """Get custom dates for a group"""
    try:
        dates = db.get_custom_dates(group_id)
        return jsonify(dates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/custom-dates', methods=['POST'])
def save_custom_dates():
    """Save custom dates for a group"""
    try:
        data = request.json
        group_id = data.get('groupId')
        dates = data.get('customDates', [])
        db.save_custom_dates(group_id, dates)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# SETTINGS
# ============================================================================

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get application settings"""
    try:
        settings = db.get_settings()
        return jsonify(settings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Save application settings"""
    try:
        data = request.json
        db.save_settings(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'database': 'connected'})
# ============================================================================
# STATUS GROUPS
# ============================================================================

@app.route('/api/status-groups', methods=['GET'])
def get_status_groups():
    """Get all status groups with their statuses"""
    try:
        groups = db.get_status_groups()
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status-groups', methods=['POST'])
def create_status_group():
    """Create a new status group"""
    try:
        data = request.json
        group_id = db.create_status_group(data)
        return jsonify({'id': group_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# BILLING STATUSES
# ============================================================================

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    """Get all statuses"""
    try:
        statuses = db.get_all_statuses()
        return jsonify(statuses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/billing-statuses/group/<int:group_id>', methods=['GET'])
def get_statuses_by_group(group_id):
    """Get statuses for a specific group"""
    try:
        statuses = db.get_statuses_by_group(group_id)
        return jsonify(statuses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statuses', methods=['POST'])
def create_status():
    """Create a new status"""
    try:
        data = request.json
        status_id = db.create_status(data)
        return jsonify({'id': status_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statuses/<int:status_id>', methods=['PUT'])
def update_status(status_id):
    """Update a status"""
    try:
        data = request.json
        db.update_status(status_id, data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statuses/<int:status_id>', methods=['DELETE'])
def delete_status(status_id):
    """Delete a status"""
    try:
        db.delete_status(status_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        
# API Version: 1.1 - Added group-specific status management
from flask import Flask, jsonify, request, send_from_directory

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Railway sets PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
 
