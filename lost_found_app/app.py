from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps
import webbrowser
from threading import Timer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_found.db'
app.config['SECRET_KEY'] = 'lost_found_secret_key_2026'
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelf_number = db.Column(db.String(50), unique=True, nullable=False)  # e.g., "A1", "B2", "C3"
    location = db.Column(db.String(200))  # e.g., "First Floor - Main Office"
    capacity = db.Column(db.Integer, default=20)
    
    def __repr__(self):
        return f'<Shelf {self.shelf_number}>'

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # e.g., "Trouser", "Card", "Book"
    fields = db.Column(db.JSON)  # e.g., {"Trouser": ["size", "color"], "Card": ["id_number"]}
    icon = db.Column(db.String(50), default='📦')  # Emoji icon for display
    
    def __repr__(self):
        return f'<ItemType {self.name}>'

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'), nullable=False)
    item_type = db.relationship('ItemType')
    
    description = db.Column(db.JSON)  # Dynamic fields based on item type
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'))
    shelf = db.relationship('Shelf')
    location = db.Column(db.String(200), nullable=False)  # Shelf location or custom location
    date_found = db.Column(db.DateTime, default=datetime.now)
    date_added = db.Column(db.DateTime, default=datetime.now)
    
    is_claimed = db.Column(db.Boolean, default=False)
    claimed_by_admission_no = db.Column(db.String(50))
    claim_date = db.Column(db.DateTime)
    
    status = db.Column(db.String(50), default='Available')  # Available, Claimed, Returned
    notes = db.Column(db.Text)
    photo_url = db.Column(db.String(300))  # URL to photo of item
    
    def __repr__(self):
        return f'<FoundItem {self.id}>'

class LostReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_admission_no = db.Column(db.String(50))  # Made optional
    student_name = db.Column(db.String(100), nullable=False)
    
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'), nullable=False)
    item_type = db.relationship('ItemType')
    
    description = db.Column(db.JSON)  # Dynamic fields based on item type
    date_lost = db.Column(db.DateTime, nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.now)
    
    location_lost = db.Column(db.String(200))  # Where they lost it
    contact_info = db.Column(db.String(100))  # Phone/email
    
    status = db.Column(db.String(50), default='Pending')  # Pending, Found, Resolved
    matched_found_item_id = db.Column(db.Integer, db.ForeignKey('found_item.id'))
    
    def __repr__(self):
        return f'<LostReport {self.id}>'

# ==================== AUTO MATCHING SYSTEM ====================

def auto_match_lost_report(lost_report):
    """
    Automatically match a lost report with available found items based on:
    1. Item type matching
    2. Admission number matching (if provided)
    3. Description similarity
    """
    # Find available items of the same type
    found_items = FoundItem.query.filter_by(
        item_type_id=lost_report.item_type_id,
        status='Available'
    ).all()
    
    best_match = None
    best_score = 0
    
    for found_item in found_items:
        score = 0
        
        # Item type match (high priority)
        score += 50
        
        # Admission number match (very high priority if provided)
        if lost_report.student_admission_no and found_item.description:
            lost_admission = lost_report.student_admission_no.lower().strip()
            found_admission = found_item.description.get('student_id', '').lower().strip()
            if found_admission and lost_admission == found_admission:
                score += 100  # Perfect match
        
        # Description field matching
        if lost_report.description and found_item.description:
            for key, lost_value in lost_report.description.items():
                found_value = found_item.description.get(key, '')
                if found_value and lost_value:
                    # Case-insensitive string matching
                    if isinstance(lost_value, str) and isinstance(found_value, str):
                        if lost_value.lower().strip() == found_value.lower().strip():
                            score += 20
                        elif lost_value.lower().strip() in found_value.lower().strip() or \
                             found_value.lower().strip() in lost_value.lower().strip():
                            score += 10
        
        # Size matching (important for uniforms)
        lost_size = lost_report.description.get('size', '').lower().strip() if lost_report.description else ''
        found_size = found_item.description.get('size', '').lower().strip() if found_item.description else ''
        if lost_size and found_size and lost_size == found_size:
            score += 15
        
        # Color matching
        lost_color = lost_report.description.get('color', '').lower().strip() if lost_report.description else ''
        found_color = found_item.description.get('color', '').lower().strip() if found_item.description else ''
        if lost_color and found_color and lost_color == found_color:
            score += 10
        
        # Update best match if this score is higher
        if score > best_score and score >= 60:  # Minimum threshold for suggestion
            best_score = score
            best_match = found_item
    
    if best_match:
        return {
            'found_item_id': best_match.id,
            'item_type': best_match.item_type.name,
            'description': best_match.description,
            'location': best_match.location,
            'date_found': best_match.date_found.strftime('%Y-%m-%d') if best_match.date_found else None,
            'confidence_score': best_score,
            'match_reason': get_match_reason(best_score, lost_report, best_match)
        }
    
    return None

def get_match_reason(score, lost_report, found_item):
    """Generate a human-readable reason for the match"""
    reasons = []
    
    if score >= 100:
        reasons.append("Perfect admission number match")
    
    if lost_report.description and found_item.description:
        matching_fields = []
        for key in lost_report.description.keys():
            if key in found_item.description and \
               str(lost_report.description[key]).lower().strip() == str(found_item.description[key]).lower().strip():
                matching_fields.append(key.title())
        
        if matching_fields:
            reasons.append(f"Matching {', '.join(matching_fields)}")
    
    if not reasons:
        reasons.append("Similar item characteristics")
    
    return " and ".join(reasons)

# ==================== AUTHENTICATION ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES ====================

@app.route('/')
def index():
    # Check if admin exists
    admin_count = Admin.query.count()
    has_admin = admin_count > 0
    return render_template('landing.html', has_admin=has_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if Admin.query.count() == 0:
        return redirect(url_for('admin_setup'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            return redirect(url_for('dashboard'))
        else:
            # Check if this is a request from the landing page
            referer = request.headers.get('Referer', '')
            if 'login' not in referer and '/' in referer:
                # Came from landing page, redirect back with error
                return redirect(url_for('index') + '?login_error=1')
            else:
                # Came from login page
                return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== ADMIN DASHBOARD ====================

@app.route('/admin/dashboard')
@login_required
def dashboard():
    total_items = FoundItem.query.count()
    available_items = FoundItem.query.filter_by(status='Available').count()
    claimed_items = FoundItem.query.filter_by(status='Claimed').count()
    lost_reports = LostReport.query.count()
    pending_reports = LostReport.query.filter_by(status='Pending').count()
    
    recent_items = FoundItem.query.order_by(FoundItem.date_added.desc()).limit(5).all()
    recent_reports = LostReport.query.order_by(LostReport.date_reported.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_items=total_items,
                         available_items=available_items,
                         claimed_items=claimed_items,
                         lost_reports=lost_reports,
                         pending_reports=pending_reports,
                         recent_items=recent_items,
                         recent_reports=recent_reports)

# ==================== ADD FOUND ITEM ====================

@app.route('/admin/add-item', methods=['GET', 'POST'])
@login_required
def add_found_item():
    item_types = ItemType.query.all()
    shelves = Shelf.query.all()
    
    # Convert ItemType objects to dictionaries for JSON serialization
    item_types_data = []
    for item_type in item_types:
        item_types_data.append({
            'id': item_type.id,
            'name': item_type.name,
            'fields': item_type.fields,
            'icon': item_type.icon
        })
    
    if request.method == 'POST':
        item_type_id = request.form.get('item_type_id')
        location = request.form.get('location')
        shelf_id = request.form.get('shelf_id')
        date_found = request.form.get('date_found')
        notes = request.form.get('notes')
        photo_url = request.form.get('photo_url')
        
        # Get dynamic description fields
        description = {}
        item_type = ItemType.query.get(item_type_id)
        if item_type and item_type.fields:
            for field in item_type.fields:
                description[field] = request.form.get(f'desc_{field}')
        
        found_item = FoundItem(
            item_type_id=item_type_id,
            description=description,
            location=location,
            shelf_id=shelf_id if shelf_id else None,
            date_found=datetime.strptime(date_found, '%Y-%m-%d'),
            notes=notes,
            photo_url=photo_url
        )
        
        db.session.add(found_item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Item added successfully', 'item_id': found_item.id})
    
    return render_template('add_found_item.html', item_types=item_types, shelves=shelves, item_types_data=item_types_data)

# ==================== MANAGE FOUND ITEMS ====================

@app.route('/admin/items')
@login_required
def manage_items():
    items = FoundItem.query.order_by(FoundItem.date_added.desc()).all()
    item_types = ItemType.query.all()
    return render_template('manage_items.html', items=items, item_types=item_types)

@app.route('/admin/item-types')
@login_required
def manage_item_types():
    item_types = ItemType.query.order_by(ItemType.name).all()
    item_counts = {item_type.id: FoundItem.query.filter_by(item_type_id=item_type.id).count() for item_type in item_types}
    return render_template('admin_item_types.html', item_types=item_types, item_counts=item_counts)

@app.route('/admin/item-type/create', methods=['POST'])
@login_required
def create_item_type():
    name = request.form.get('name', '').strip()
    icon = request.form.get('icon', '📦').strip() or '📦'
    fields_raw = request.form.get('fields', '').strip()

    if not name:
        return jsonify({'success': False, 'message': 'Item type name is required'})

    if ItemType.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': 'An item type with that name already exists'})

    fields = [field.strip() for field in fields_raw.split(',') if field.strip()]
    item_type = ItemType(name=name, icon=icon, fields=fields)
    db.session.add(item_type)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item type added successfully'})

@app.route('/admin/item-type/<int:type_id>/delete', methods=['POST'])
@login_required
def delete_item_type(type_id):
    item_type = ItemType.query.get(type_id)
    if not item_type:
        return jsonify({'success': False, 'message': 'Item type not found'})

    linked_items = FoundItem.query.filter_by(item_type_id=type_id).count()
    if linked_items > 0:
        return jsonify({'success': False, 'message': 'Cannot delete item type because found items still use it'})

    db.session.delete(item_type)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item type deleted successfully'})

@app.route('/admin/items/search', methods=['POST'])
@login_required
def search_items():
    item_type_id = request.form.get('item_type_id')
    size = request.form.get('size')
    color = request.form.get('color')
    status = request.form.get('status')
    location = request.form.get('location')
    
    query = FoundItem.query
    
    if item_type_id:
        query = query.filter_by(item_type_id=item_type_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if location:
        query = query.filter(FoundItem.location.ilike(f'%{location}%'))
    
    items = query.all()
    
    # Filter by size and color if needed (from JSON description)
    if size or color:
        filtered_items = []
        for item in items:
            if size and item.description.get('size') != size:
                continue
            if color and item.description.get('color', '').lower() != color.lower():
                continue
            filtered_items.append(item)
        items = filtered_items
    
    return render_template('manage_items.html', items=items, item_types=ItemType.query.all())

@app.route('/admin/item/<int:item_id>/claim', methods=['POST'])
@login_required
def claim_item(item_id):
    data = request.get_json()
    admission_no = data.get('admission_no')
    
    item = FoundItem.query.get(item_id)
    if item:
        item.is_claimed = True
        item.claimed_by_admission_no = admission_no
        item.claim_date = datetime.now()
        item.status = 'Claimed'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item claimed successfully'})
    
    return jsonify({'success': False, 'message': 'Item not found'})

@app.route('/admin/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = FoundItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item deleted successfully'})
    
    return jsonify({'success': False, 'message': 'Item not found'})

# ==================== MANAGE LOST REPORTS ====================

@app.route('/admin/reports')
@login_required
def manage_reports():
    reports = LostReport.query.order_by(LostReport.date_reported.desc()).all()
    return render_template('manage_reports.html', reports=reports)

@app.route('/admin/report/<int:report_id>/match', methods=['POST'])
@login_required
def match_report(report_id):
    data = request.get_json()
    found_item_id = data.get('found_item_id')
    
    report = LostReport.query.get(report_id)
    found_item = FoundItem.query.get(found_item_id)
    
    if report and found_item:
        report.matched_found_item_id = found_item_id
        report.status = 'Found'
        found_item.status = 'Returned'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Report matched with found item'})
    
    return jsonify({'success': False, 'message': 'Invalid report or item'})

@app.route('/admin/reset-system', methods=['POST'])
@login_required
def reset_system():
    try:
        # Remove all records in the right order to avoid foreign key issues.
        LostReport.query.delete()
        FoundItem.query.delete()
        db.session.commit()

        Admin.query.delete()
        Shelf.query.delete()
        ItemType.query.delete()
        db.session.commit()

        session.clear()
        return jsonify({
            'success': True,
            'message': 'System reset complete. The database is now empty and admin login has been cleared.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Reset failed: {str(e)}'}), 500

# ==================== ADMIN PROFILE MANAGEMENT ====================

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    admin = Admin.query.get(session['admin_id'])
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if admin.password != current_password:
            return render_template('admin_profile.html', admin=admin, error='Current password is incorrect')
        
        # Check if new password matches confirmation
        if new_password != confirm_password:
            return render_template('admin_profile.html', admin=admin, error='New passwords do not match')
        
        # Check if username is already taken (if changed)
        if new_username != admin.username:
            existing_admin = Admin.query.filter_by(username=new_username).first()
            if existing_admin:
                return render_template('admin_profile.html', admin=admin, error='Username already exists')
            admin.username = new_username
        
        # Update password if provided
        if new_password:
            admin.password = new_password
        
        db.session.commit()
        session['admin_username'] = admin.username
        
        return render_template('admin_profile.html', admin=admin, success='Profile updated successfully')
    
    return render_template('admin_profile.html', admin=admin)

# ==================== USER SECTION ====================

@app.route('/user/search')
def user_search():
    item_types = ItemType.query.all()
    return render_template('user_search.html', item_types=item_types)

@app.route('/user/report-lost', methods=['GET', 'POST'])
def report_lost():
    item_types = ItemType.query.all()
    
    # Convert ItemType objects to dictionaries for JSON serialization
    item_types_data = []
    for item_type in item_types:
        item_types_data.append({
            'id': item_type.id,
            'name': item_type.name,
            'fields': item_type.fields,
            'icon': item_type.icon
        })
    
    if request.method == 'POST':
        student_admission_no = request.form.get('admission_no')
        student_name = request.form.get('student_name')
        item_type_id = request.form.get('item_type_id')
        date_lost = request.form.get('date_lost')
        location_lost = request.form.get('location_lost')
        contact_info = request.form.get('contact_info')
        
        # Get dynamic description fields
        description = {}
        item_type = ItemType.query.get(item_type_id)
        if item_type and item_type.fields:
            for field in item_type.fields:
                description[field] = request.form.get(f'desc_{field}')
        
        lost_report = LostReport(
            student_admission_no=student_admission_no,
            student_name=student_name,
            item_type_id=item_type_id,
            description=description,
            date_lost=datetime.strptime(date_lost, '%Y-%m-%d'),
            location_lost=location_lost,
            contact_info=contact_info
        )
        
        db.session.add(lost_report)
        db.session.commit()
        
        # Auto-match with found items
        auto_match_result = auto_match_lost_report(lost_report)
        
        response_data = {'success': True, 'message': 'Lost report submitted successfully'}
        if auto_match_result:
            response_data['match_suggestion'] = auto_match_result
        
        return jsonify(response_data)
    
    return render_template('report_lost.html', item_types=item_types, item_types_data=item_types_data)

@app.route('/user/search-found-items', methods=['POST'])
def search_found_items():
    item_type_id = request.form.get('item_type_id')
    
    query = FoundItem.query.filter_by(status='Available')
    
    if item_type_id:
        query = query.filter_by(item_type_id=item_type_id)
    
    items = query.all()
    
    return render_template('found_items_list.html', items=items)

# ==================== ADMIN SETUP ====================

@app.route('/admin/setup')
def admin_setup():
    # Check if admin exists
    admin_count = Admin.query.count()
    if admin_count == 0:
        return render_template('admin_setup.html')
    return redirect(url_for('login'))

@app.route('/admin/setup/create', methods=['POST'])
def create_first_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    
    if Admin.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'})
    
    admin = Admin(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
    
    # Create shelves
    shelves = [
        Shelf(shelf_number='A1', location='Main Office - First Shelf'),
        Shelf(shelf_number='A2', location='Main Office - Second Shelf'),
        Shelf(shelf_number='B1', location='Library - First Shelf'),
        Shelf(shelf_number='B2', location='Library - Second Shelf'),
        Shelf(shelf_number='C1', location='Security Office - First Shelf'),
        Shelf(shelf_number='C2', location='Security Office - Second Shelf'),
    ]
    
    for shelf in shelves:
        if not Shelf.query.filter_by(shelf_number=shelf.shelf_number).first():
            db.session.add(shelf)
    
    db.session.commit()
    
    # Create 20+ default item types with detailed fields
    default_types = [
        ItemType(name='School Uniform', fields=['size', 'color', 'condition', 'school_grade'], icon='👕'),
        ItemType(name='School Shirt', fields=['size', 'color', 'condition', 'school_grade', 'sleeve_type'], icon='👕'),
        ItemType(name='School Trouser', fields=['size', 'color', 'condition', 'school_grade', 'material'], icon='👖'),
        ItemType(name='School Skirt', fields=['size', 'color', 'condition', 'school_grade', 'length'], icon='👗'),
        ItemType(name='School Blazer', fields=['size', 'color', 'condition', 'school_grade'], icon='🧥'),
        ItemType(name='School Tie', fields=['color', 'pattern', 'condition', 'school_grade'], icon='👔'),
        ItemType(name='School Belt', fields=['size', 'color', 'condition', 'buckle_type'], icon='🪢'),
        ItemType(name='PE Uniform', fields=['size', 'color', 'condition', 'school_grade'], icon='🏃'),
        ItemType(name='Textbook', fields=['title', 'subject', 'grade', 'author', 'condition'], icon='📚'),
        ItemType(name='Exercise Book', fields=['subject', 'grade', 'color', 'size'], icon='📓'),
        ItemType(name='ID Card', fields=['student_id', 'full_name', 'grade', 'card_color'], icon='🆔'),
        ItemType(name='Mobile Phone', fields=['brand', 'model', 'color', 'condition'], icon='📱'),
        ItemType(name='Laptop/Computer', fields=['brand', 'model', 'color', 'serial_number'], icon='💻'),
        ItemType(name='Tablet', fields=['brand', 'model', 'color', 'size'], icon='📱'),
        ItemType(name='Wallet', fields=['color', 'brand', 'contents_detail', 'material'], icon='👛'),
        ItemType(name='Keys', fields=['number_of_keys', 'description', 'key_color'], icon='🔑'),
        ItemType(name='Shoes', fields=['size', 'brand', 'color', 'condition', 'type'], icon='👟'),
        ItemType(name='Bag/Backpack', fields=['color', 'brand', 'size', 'type', 'condition'], icon='🎒'),
        ItemType(name='Glasses/Sunglasses', fields=['frame_color', 'brand', 'lens_color', 'condition'], icon='👓'),
        ItemType(name='Watch', fields=['brand', 'color', 'type', 'condition'], icon='⌚'),
        ItemType(name='Jewelry', fields=['type', 'metal', 'color', 'stones', 'condition'], icon='💍'),
        ItemType(name='Sports Equipment', fields=['sport_type', 'equipment_name', 'brand', 'color', 'size'], icon='⚽'),
        ItemType(name='Musical Instrument', fields=['instrument_type', 'brand', 'color', 'condition'], icon='🎸'),
        ItemType(name='Art Supplies', fields=['supply_type', 'brand', 'quantity', 'color'], icon='🎨'),
        ItemType(name='Lab Coat', fields=['size', 'color', 'school_department', 'condition'], icon='🥼'),
        ItemType(name='Sweater/Cardigan', fields=['size', 'color', 'brand', 'condition'], icon='🧶'),
        ItemType(name='Scarf/Hat', fields=['type', 'color', 'size', 'material'], icon='🧣'),
        ItemType(name='Umbrella', fields=['color', 'brand', 'type', 'condition'], icon='☂️'),
        ItemType(name='Water Bottle', fields=['brand', 'capacity', 'color', 'material'], icon='🧴'),
        ItemType(name='Lunch Box', fields=['color', 'size', 'material', 'contents'], icon='🍱'),
        ItemType(name='Headphones', fields=['brand', 'model', 'color', 'type', 'condition'], icon='🎧'),
        ItemType(name='Charger/Cable', fields=['type', 'brand', 'connector_type', 'condition'], icon='🔌'),
    ]
    
    for item_type in default_types:
        if not ItemType.query.filter_by(name=item_type.name).first():
            db.session.add(item_type)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Admin created successfully'})

@app.route('/api/item-types')
def get_item_types():
    types = ItemType.query.all()
    return jsonify([{'id': t.id, 'name': t.name, 'fields': t.fields, 'icon': t.icon} for t in types])

@app.route('/api/item-type/<int:type_id>')
def get_item_type_detail(type_id):
    item_type = ItemType.query.get(type_id)
    if item_type:
        return jsonify({'id': item_type.id, 'name': item_type.name, 'fields': item_type.fields, 'icon': item_type.icon})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/found-items')
def get_found_items():
    items = FoundItem.query.filter_by(status='Available').all()
    return jsonify([{
        'id': item.id,
        'item_type': item.item_type.name,
        'item_icon': item.item_type.icon,
        'description': item.description,
        'location': item.location,
        'shelf': item.shelf.shelf_number if item.shelf else 'Not Assigned',
        'date_found': item.date_found.strftime('%Y-%m-%d'),
        'notes': item.notes
    } for item in items])

# ==================== PUBLIC DISPLAY ROUTES ====================

@app.route('/display')
def display():
    """Beautiful scrolling display for found items - TV mode"""
    items = FoundItem.query.filter_by(status='Available').order_by(FoundItem.date_added.desc()).all()
    return render_template('display.html', items=items)

@app.route('/api/display-items')
def api_display_items():
    """API endpoint for live updating of display items"""
    items = FoundItem.query.filter_by(status='Available').order_by(FoundItem.date_added.desc()).all()
    return jsonify([{
        'id': item.id,
        'item_type': item.item_type.name,
        'icon': item.item_type.icon,
        'description': item.description,
        'location': item.location,
        'shelf': item.shelf.shelf_number if item.shelf else 'Not Assigned',
        'date_found': item.date_found.strftime('%B %d, %Y'),
        'notes': item.notes,
        'photo_url': item.photo_url
    } for item in items])

@app.route('/items-public')
def items_public():
    """Public display of found items with shelf information - accessible from same IP"""
    items = FoundItem.query.filter_by(status='Available').order_by(FoundItem.date_added.desc()).all()
    shelves = Shelf.query.all()
    return render_template('items_public.html', items=items, shelves=shelves)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ==================== CREATE TABLES ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Open browser automatically
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')
    
    # Delay opening browser by 1 second to let Flask start
    Timer(1.0, open_browser).start()
    
    app.run(debug=True, port=5000)
