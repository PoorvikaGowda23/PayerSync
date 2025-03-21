from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, PayerGroup, Payer, PayerDetail
from mapping import process_excel_data
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
db.init_app(app)

# Forms (unchanged)
class MappingForm(FlaskForm):
    detail_id = SelectField('Payer Detail', coerce=int, validators=[DataRequired()])
    payer_id = SelectField('Map to Payer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Map')

class PrettyNameForm(FlaskForm):
    payer_id = SelectField('Payer', coerce=int, validators=[DataRequired()])
    display_name = StringField('Display Name', validators=[DataRequired()])
    submit = SubmitField('Update Display Name')

class HierarchyForm(FlaskForm):
    payer_id = SelectField('Payer', coerce=int, validators=[DataRequired()])
    group_id = SelectField('Payer Group', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Group')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payer-groups')
def payer_groups():
    groups = PayerGroup.query.all()
    return render_template('payer_groups.html', groups=groups)

@app.route('/payer/<int:payer_id>')
def payer_details(payer_id):
    payer = Payer.query.get_or_404(payer_id)
    return render_template('payer_details.html', payer=payer)

@app.route('/admin/mapping', methods=['GET', 'POST'])
def admin_mapping():
    form = MappingForm()
    form.detail_id.choices = [(d.id, f"{d.raw_name} ({d.source})") for d in PayerDetail.query.all()]
    form.payer_id.choices = [(p.id, p.canonical_name) for p in Payer.query.all()]
    
    if form.validate_on_submit():
        detail = PayerDetail.query.get(form.detail_id.data)
        detail.payer_id = form.payer_id.data
        db.session.commit()
        flash('Mapping updated successfully!', 'success')
        return redirect(url_for('admin_mapping'))
    
    return render_template('admin_mapping.html', form=form)

@app.route('/admin/pretty_names', methods=['GET', 'POST'])
def admin_pretty_names():
    form = PrettyNameForm()
    form.payer_id.choices = [(p.id, p.canonical_name) for p in Payer.query.all()]
    
    if form.validate_on_submit():
        payer = Payer.query.get(form.payer_id.data)
        payer.display_name = form.display_name.data
        db.session.commit()
        flash('Display name updated successfully!', 'success')
        return redirect(url_for('admin_pretty_names'))
    
    return render_template('admin_pretty_names.html', form=form)

@app.route('/admin/hierarchy', methods=['GET', 'POST'])
def admin_hierarchy():
    form = HierarchyForm()
    form.payer_id.choices = [(p.id, p.canonical_name) for p in Payer.query.all()]
    form.group_id.choices = [(g.id, g.name) for g in PayerGroup.query.all()]
    
    if form.validate_on_submit():
        payer = Payer.query.get(form.payer_id.data)
        payer.group_id = form.group_id.data
        db.session.commit()
        flash('Payer group updated successfully!', 'success')
        return redirect(url_for('admin_hierarchy'))
    
    return render_template('admin_hierarchy.html', form=form)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file_path = 'uploaded_data.xlsx'
    file.save(file_path)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        map_payers = process_excel_data(file_path)
        map_payers()
    
    flash('File processed successfully!', 'success')
    return redirect(url_for('payer_groups'))  # Redirect to new page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)