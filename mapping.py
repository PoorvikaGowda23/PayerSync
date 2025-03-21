import pandas as pd
from difflib import SequenceMatcher
from models import db, PayerGroup, Payer, PayerDetail

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def process_excel_data(file_path):
    # Read all sheets
    sheets = {
        'Vyne': pd.read_excel(file_path, sheet_name='Vyne'),
        'Availity': pd.read_excel(file_path, sheet_name='Availity'),
        'Optum dental': pd.read_excel(file_path, sheet_name='Optum dental'),
        'change-claims': pd.read_excel(file_path, sheet_name='change-claims'),
        'change-ERA': pd.read_excel(file_path, sheet_name='change-ERA'),
        'change-EFT': pd.read_excel(file_path, sheet_name='change-EFT'),
        'DxC': pd.read_excel(file_path, sheet_name='DxC'),
        'Optum-all': pd.read_excel(file_path, sheet_name='Optum-all')
    }

    def map_payer_details():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Dictionaries to track existing entities
        existing_groups = {}
        existing_payers = {}

        for sheet_name, df in sheets.items():
            # Find ID and Name columns
            id_col = next((col for col in ['Payer ID', 'ID'] if col in df.columns), None)
            name_col = next((col for col in ['Payer Name', 'Name', 'Payer', 'Payer Identification Information'] 
                           if col in df.columns), None)
            
            if not id_col or not name_col:
                continue

            for _, row in df.iterrows():
                # Get only the required fields
                payer_id = str(row[id_col]) if pd.notna(row[id_col]) else None
                raw_name = str(row[name_col]) if pd.notna(row[name_col]) else f"Unknown_{payer_id}"

                # Extract group name for hierarchy
                group_name_parts = raw_name.split()
                group_name = ' '.join(group_name_parts[:2]) if ' of ' in raw_name else group_name_parts[0]

                # Create or get payer group
                if group_name not in existing_groups:
                    group = PayerGroup(name=group_name, display_name=group_name)
                    db.session.add(group)
                    db.session.flush()
                    existing_groups[group_name] = group.id
                group_id = existing_groups[group_name]

                # Create payer detail entry
                detail = PayerDetail(
                    source=sheet_name,
                    raw_name=raw_name,
                    payer_number=payer_id 
                )
                db.session.add(detail)
                db.session.flush()

                # Semantic matching and deduplication
                payer_key = f"{payer_id}_{raw_name}" if payer_id else raw_name
                
                if payer_key not in existing_payers:
                    # Check for existing similar payers
                    matched_payer_id = None
                    max_similarity = 0.0
                    
                    for existing_payer in Payer.query.filter_by(group_id=group_id).all():
                        # First check payer_id match if available
                        if payer_id and any(d.payer_id == payer_id for d in existing_payer.payer_details):
                            matched_payer_id = existing_payer.id
                            break
                        # Otherwise use semantic matching
                        elif not payer_id:
                            current_similarity = similarity(raw_name, existing_payer.canonical_name)
                            if current_similarity > 0.85 and current_similarity > max_similarity:
                                max_similarity = current_similarity
                                matched_payer_id = existing_payer.id

                    if matched_payer_id:
                        detail.payer_id = matched_payer_id
                    else:
                        # Create new payer if no match found
                        new_payer = Payer(
                            canonical_name=raw_name,
                            display_name=raw_name,
                            group_id=group_id
                        )
                        db.session.add(new_payer)
                        db.session.flush()
                        detail.payer_id = new_payer.id
                        existing_payers[payer_key] = new_payer.id
                else:
                    detail.payer_id = existing_payers[payer_key]

        db.session.commit()

    return map_payer_details
