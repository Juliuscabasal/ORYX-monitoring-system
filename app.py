import os
import json
import pandas as pd
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oryx_secret_key_123' 

# Connection & Upload Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:/oryx_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# --- LOGIN MANAGER ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- MODELS ---

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(500), nullable=False)
    author_name = db.Column(db.String(100), nullable=True) 

class POMonitoring(db.Model):
    __tablename__ = 'po_monitoring'
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.String(100), nullable=False)
    po_no = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    received_by = db.Column(db.String(100), nullable=False)
    dr_no = db.Column(db.String(100), nullable=True)
    si_no = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default="Pending")
    status_note = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.String(100), nullable=True) 
    files = db.relationship('POFile', backref='po', cascade="all, delete-orphan", lazy=True)
    items = db.relationship('POItem', backref='po', cascade="all, delete-orphan", lazy=True)

class POItem(db.Model):
    __tablename__ = 'po_item'
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer, db.ForeignKey('po_monitoring.id'), nullable=False)
    pr_checked = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default="Pending")
    remarks = db.Column(db.String(255), nullable=True)

class POFile(db.Model):
    __tablename__ = 'po_file'
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer, db.ForeignKey('po_monitoring.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

class UATMonitoring(db.Model):
    __tablename__ = 'uat_monitoring'
    id = db.Column(db.Integer, primary_key=True)
    uat_no = db.Column(db.String(100), nullable=False)
    ccr = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    accepting_personnel = db.Column(db.String(100), nullable=False)
    it_incharge = db.Column(db.String(100), nullable=False)
    date_start = db.Column(db.String(50), nullable=True)
    date_end = db.Column(db.String(50), nullable=True)
    hr_per_day = db.Column(db.String(50), nullable=True)
    total_cost = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="Pending")
    created_by = db.Column(db.String(100), nullable=True) 
    files = db.relationship('UATFile', backref='uat', cascade="all, delete-orphan", lazy=True)

class UATFile(db.Model):
    __tablename__ = 'uat_file'
    id = db.Column(db.Integer, primary_key=True)
    uat_id = db.Column(db.Integer, db.ForeignKey('uat_monitoring.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

class PRMonitoring(db.Model):
    __tablename__ = 'pr_monitoring'
    id = db.Column(db.Integer, primary_key=True)
    purchase_no = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(500), nullable=True) # PR Comment
    status = db.Column(db.String(50), default="Pending")
    urgent_reason = db.Column(db.String(500), nullable=True) 
    po_no = db.Column(db.String(100), nullable=True)
    doc_date = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(100), nullable=True)
    files = db.relationship('PRFile', backref='pr', cascade="all, delete-orphan", lazy=True)
    items = db.relationship('PRItem', backref='pr', cascade="all, delete-orphan", lazy=True)

# NEW ITEM MODEL FOR PR
class PRItem(db.Model):
    __tablename__ = 'pr_item'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey('pr_monitoring.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    qty = db.Column(db.Integer, default=1)

class PRFile(db.Model):
    __tablename__ = 'pr_file'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey('pr_monitoring.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# --- AUTH ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Invalid Username or Password"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            return "Username already taken"
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, full_name=full_name)
        db.session.add(new_user)
        db.session.commit() 
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- DASHBOARD & GENERAL ROUTES ---

@app.route('/')
@login_required
def dashboard():
    try:
        all_reminders = Reminder.query.all() 
        return render_template('index.html', reminders=all_reminders)
    except Exception as e:
        return render_template('index.html', reminders=[], error=str(e))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- REMINDERS API ---

@app.route('/api/save_reminder', methods=['POST'])
@login_required
def save_reminder():
    try:
        data = request.get_json()
        rem_id = data.get('id')
        note_content = data.get('note')
        if rem_id:
            rem = Reminder.query.get(rem_id)
            if rem:
                rem.note = note_content
                rem.author_name = current_user.full_name
        else:
            db.session.add(Reminder(note=note_content, author_name=current_user.full_name))
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/delete_reminder/<int:id>', methods=['DELETE'])
@login_required
def delete_reminder(id):
    try:
        rem = Reminder.query.get(id)
        if rem:
            db.session.delete(rem)
            db.session.commit()
            return jsonify({"success": True})
        return jsonify({"success": False}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- PO MONITORING ROUTES ---

@app.route('/po-monitoring')
@login_required
def po_monitoring_page():
    all_pos = POMonitoring.query.order_by(POMonitoring.id.desc()).all()
    summary = {
        "pending": POMonitoring.query.filter_by(status='Pending').count(),
        "revision": POMonitoring.query.filter_by(status='For Revision').count()
    }
    return render_template('po.html', pos=all_pos, summary=summary)

@app.route('/api/get_po/<int:id>')
@login_required
def get_po(id):
    po = POMonitoring.query.get(id)
    if not po: return jsonify({"success": False}), 404
    file_list = [{"id": f.id, "filename": f.filename} for f in (po.files or [])]
    item_list = [{"pr_checked": i.pr_checked, "description": i.description, "qty": i.qty, "status": i.status, "remarks": i.remarks} for i in (po.items or [])]
    return jsonify({"id": po.id, "date_received": po.date_received, "po_no": po.po_no, "dept": po.dept, "received_by": po.received_by, "dr_no": po.dr_no, "si_no": po.si_no, "status": po.status, "status_note": po.status_note, "files": file_list, "items": item_list})

@app.route('/api/save_po', methods=['POST'])
@login_required
def save_po():
    try:
        po_id = request.form.get('po_id')
        data = {
            "date_received": request.form.get('date_delivered'), 
            "po_no": request.form.get('po_no'), 
            "dept": request.form.get('dept'), 
            "received_by": request.form.get('rec_by'), 
            "dr_no": request.form.get('dr_no'), 
            "si_no": request.form.get('si_no'), 
            "status": request.form.get('status'), 
            "status_note": request.form.get('status_note'),
            "created_by": current_user.full_name
        }
        if po_id and po_id != "":
            po = POMonitoring.query.get(po_id)
            for key, val in data.items(): setattr(po, key, val)
            POItem.query.filter_by(po_id=po.id).delete()
        else:
            po = POMonitoring(**data)
            db.session.add(po)
        db.session.commit()
        
        items_json = request.form.get('items_json')
        if items_json:
            for item in json.loads(items_json):
                db.session.add(POItem(po_id=po.id, pr_checked=bool(item.get('pr_checked')), description=item.get('description',''), qty=int(item.get('qty',1)), status=item.get('status','Pending'), remarks=item.get('remarks','')))
            db.session.commit()
        
        if 'attachments' in request.files:
            for file in request.files.getlist('attachments'):
                if file.filename:
                    fname = secure_filename(f"PO_{po.id}_{file.filename}")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                    db.session.add(POFile(po_id=po.id, filename=fname))
            db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/delete_po/<int:id>', methods=['DELETE'])
@login_required
def delete_po(id):
    po = POMonitoring.query.get(id)
    if po:
        db.session.delete(po)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@app.route('/api/delete_po_file/<int:file_id>', methods=['DELETE'])
@login_required
def delete_po_file(file_id):
    f = POFile.query.get(file_id)
    if f:
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        if os.path.exists(path): os.remove(path)
        db.session.delete(f)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@app.route('/api/export_po_excel')
@login_required
def export_po_excel():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    query = POMonitoring.query
    if start_date and end_date:
        query = query.filter(POMonitoring.date_received.between(start_date, end_date))
    pos = query.all()
    if not pos:
        return jsonify({"success": False, "message": "No data found"}), 404
    data = []
    for p in pos:
        data.append({
            "Date Received": p.date_received, "PO Number": p.po_no,
            "Department": p.dept, "Received By": p.received_by,
            "DR Number": p.dr_no, "SI Number": p.si_no,
            "Status": p.status, "Note": p.status_note, "Entry Created By": p.created_by
        })
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='PO Report')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name="PO_Report.xlsx")

# --- UAT MONITORING ROUTES ---

@app.route('/uat-monitoring')
@login_required
def uat_monitoring_page():
    all_uats = UATMonitoring.query.order_by(UATMonitoring.id.desc()).all()
    summary = {
        "signature": UATMonitoring.query.filter_by(status='For Signature').count(),
        "billing": UATMonitoring.query.filter_by(status='For Billing').count()
    }
    return render_template('uat_monitoring.html', uats=all_uats, summary=summary)

@app.route('/api/get_uat/<int:id>')
@login_required
def get_uat(id):
    uat = UATMonitoring.query.get(id)
    if not uat: return jsonify({"success": False}), 404
    file_list = [{"id": f.id, "filename": f.filename} for f in (uat.files or [])]
    return jsonify({"id": uat.id, "uat_no": uat.uat_no, "ccr": uat.ccr, "dept": uat.dept, "accepting_personnel": uat.accepting_personnel, "it_incharge": uat.it_incharge, "hr_per_day": uat.hr_per_day, "date_start": uat.date_start, "date_end": uat.date_end, "total_cost": uat.total_cost, "status": uat.status, "files": file_list})

@app.route('/api/save_uat', methods=['POST'])
@login_required
def save_uat():
    try:
        uat_id = request.form.get('uat_id')
        data = {
            "uat_no": request.form.get('uat_no'), "ccr": request.form.get('ccr'), 
            "dept": request.form.get('dept'), "accepting_personnel": request.form.get('accepting_personnel'), 
            "it_incharge": request.form.get('it_incharge'), "date_start": request.form.get('date_start'), 
            "date_end": request.form.get('date_end'), "hr_per_day": request.form.get('hr_per_day'), 
            "total_cost": request.form.get('total_cost'), "status": request.form.get('status'),
            "created_by": current_user.full_name
        }
        if uat_id and uat_id != "":
            uat = UATMonitoring.query.get(uat_id)
            for key, val in data.items(): setattr(uat, key, val)
        else:
            uat = UATMonitoring(**data)
            db.session.add(uat)
        db.session.commit()
        if 'attachments' in request.files:
            for file in request.files.getlist('attachments'):
                if file.filename:
                    fname = secure_filename(f"UAT_{uat.id}_{file.filename}")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                    db.session.add(UATFile(uat_id=uat.id, filename=fname))
            db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/delete_uat/<int:id>', methods=['DELETE'])
@login_required
def delete_uat(id):
    uat = UATMonitoring.query.get(id)
    if uat:
        db.session.delete(uat)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@app.route('/api/delete_uat_file/<int:file_id>', methods=['DELETE'])
@login_required
def delete_uat_file(file_id):
    f = UATFile.query.get(file_id)
    if f:
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        if os.path.exists(path): os.remove(path)
        db.session.delete(f)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

# --- PR MONITORING ROUTES ---

@app.route('/pr-monitoring')
@login_required
def pr_monitoring_page():
    all_prs = PRMonitoring.query.order_by(PRMonitoring.id.desc()).all()
    urgent_count = PRMonitoring.query.filter_by(status='Others').count()
    summary = {
        "open": PRMonitoring.query.filter_by(status='Open').count(),
        "pending": PRMonitoring.query.filter_by(status='Pending').count(),
        "approved": PRMonitoring.query.filter_by(status='Approved').count(),
        "closed": PRMonitoring.query.filter_by(status='Closed').count(),
        "urgent": urgent_count
    }
    return render_template('pr.html', prs=all_prs, summary=summary)

@app.route('/api/get_pr/<int:id>')
@login_required
def get_pr(id):
    pr = PRMonitoring.query.get(id)
    if not pr: return jsonify({"success": False}), 404
    file_list = [{"id": f.id, "filename": f.filename} for f in pr.files]
    
    # Return items formatted
    item_list = [{"description": i.description, "qty": i.qty} for i in pr.items]
    
    return jsonify({
        "id": pr.id, "purchase_no": pr.purchase_no, "location": pr.location,
        "items": item_list, "remarks": pr.remarks, "status": pr.status,
        "urgent_reason": pr.urgent_reason, "po_no": pr.po_no, "doc_date": pr.doc_date, "files": file_list
    })

@app.route('/api/save_pr', methods=['POST'])
@login_required
def save_pr():
    try:
        pr_id = request.form.get('pr_id')
        data = {
            "purchase_no": request.form.get('purchase_no'),
            "location": request.form.get('location'),
            "remarks": request.form.get('remarks'),
            "status": request.form.get('status'),
            "urgent_reason": request.form.get('urgent_reason'),
            "po_no": request.form.get('po_no'),
            "doc_date": request.form.get('doc_date'),
            "created_by": current_user.full_name
        }
        if pr_id and pr_id != "":
            pr = PRMonitoring.query.get(pr_id)
            for key, val in data.items(): setattr(pr, key, val)
            
            # Delete old items to refresh
            PRItem.query.filter_by(pr_id=pr.id).delete()
        else:
            pr = PRMonitoring(**data)
            db.session.add(pr)
        db.session.commit()

        # Save new items
        items_json = request.form.get('items_json')
        if items_json:
            for item in json.loads(items_json):
                if item.get('description'): # Ensure it's not totally empty
                    db.session.add(PRItem(pr_id=pr.id, description=item.get('description'), qty=int(item.get('qty', 1))))
            db.session.commit()

        if 'attachments' in request.files:
            for file in request.files.getlist('attachments'):
                if file.filename:
                    fname = secure_filename(f"PR_{pr.id}_{file.filename}")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                    db.session.add(PRFile(pr_id=pr.id, filename=fname))
            db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/delete_pr/<int:id>', methods=['DELETE'])
@login_required
def delete_pr(id):
    pr = PRMonitoring.query.get(id)
    if pr:
        db.session.delete(pr)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@app.route('/api/delete_pr_file/<int:file_id>', methods=['DELETE'])
@login_required
def delete_pr_file(file_id):
    f = PRFile.query.get(file_id)
    if f:
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        if os.path.exists(path): os.remove(path)
        db.session.delete(f)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@app.route('/api/export_pr_excel')
@login_required
def export_pr_excel():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    query = PRMonitoring.query
    
    if start_date and end_date:
        query = query.filter(PRMonitoring.doc_date.between(start_date, end_date))
        
    prs = query.all()
    if not prs: 
        return jsonify({"success": False, "message": "No data found for this date range."}), 404
        
    data = []
    for pr in prs:
        # Join the items into a single readable string for the excel cell
        desc_str = ", ".join([f"{i.qty}x {i.description}" for i in pr.items])
        
        data.append({
            "Purchase Number": pr.purchase_no,
            "Location": pr.location,
            "Item/Description": desc_str,
            "Status": pr.status,
            "Urgent Reason": pr.urgent_reason if pr.status == 'Others' else '',
            "PR Comment (Remarks)": pr.remarks,
            "PO Number": pr.po_no,
            "Document Date": pr.doc_date,
            "Entry Created By": pr.created_by
        })
        
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='PR Report')
    
    output.seek(0)
    return send_file(
        output, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        as_attachment=True, 
        download_name="PR_Report.xlsx"
    )

if __name__ == '__main__':
    app.run(debug=True)