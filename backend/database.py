import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json

class Database:
    def __init__(self):
        """Initialize database connection"""
        self.db_url = os.environ.get('DATABASE_URL')
        if not self.db_url:
            raise Exception("DATABASE_URL environment variable not set")
        
        # Railway provides DATABASE_URL in the correct format
        self.conn = psycopg2.connect(self.db_url)
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        with self.conn.cursor() as cur:
            # Status Groups table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS status_groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    is_default BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Billing Statuses table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS billing_statuses (
                    id SERIAL PRIMARY KEY,
                    status_group_id INTEGER REFERENCES status_groups(id) ON DELETE CASCADE,
                    name VARCHAR(100) NOT NULL,
                    color VARCHAR(20) NOT NULL,
                    sort_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Facility Groups table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS facility_groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    billing_type VARCHAR(50) NOT NULL,
                    billing_day INTEGER,
                    status_group_id INTEGER REFERENCES status_groups(id) DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Facilities table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS facilities (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    group_id INTEGER REFERENCES facility_groups(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Billing Records table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS billing_records (
                    id SERIAL PRIMARY KEY,
                    facility_id INTEGER REFERENCES facilities(id) ON DELETE CASCADE,
                    cycle INTEGER NOT NULL,
                    billing_date VARCHAR(8),
                    from_date VARCHAR(8),
                    through_date VARCHAR(8),
                    billed_amount VARCHAR(50),
                    status_id INTEGER REFERENCES billing_statuses(id),
                    paid_amount VARCHAR(50),
                    paid_date VARCHAR(8),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(facility_id, cycle)
                )
            ''')
            
            # Custom Dates table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS custom_dates (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER REFERENCES facility_groups(id) ON DELETE CASCADE,
                    date VARCHAR(8) NOT NULL,
                    frequency VARCHAR(50),
                    custom_from VARCHAR(10),
                    custom_through VARCHAR(10),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Settings table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id SERIAL PRIMARY KEY,
                    key VARCHAR(100) UNIQUE NOT NULL,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            
            self.conn.commit()
            
           # Insert default data if tables are empty
            self._insert_default_data()
            
           # Run migrations for existing tables
            self._run_migrations()
            

            
    def _run_migrations(self):
        """Run database migrations for schema updates"""
        with self.conn.cursor() as cur:
            try:
                # Insert status group first if it doesn't exist
                cur.execute('''
                    INSERT INTO status_groups (id, name, is_default)
                    VALUES (1, 'Default', true)
                    ON CONFLICT (id) DO NOTHING
                ''')
                
                # Insert default statuses if they don't exist
                cur.execute('''
                    INSERT INTO billing_statuses (status_group_id, name, color, sort_order)
                    VALUES 
                        (1, 'Not Billed', '#93C5FD', 1),
                        (1, 'Billed', '#FDE047', 2),
                        (1, 'Pending', '#C4B5FD', 3),
                        (1, 'Approved', '#86EFAC', 4),
                        (1, 'Paid', '#22C55E', 5)
                    ON CONFLICT DO NOTHING
                ''')
                
                # Now add columns (without foreign key constraints to avoid errors)
                cur.execute('''
                    ALTER TABLE facility_groups 
                    ADD COLUMN IF NOT EXISTS status_group_id INTEGER DEFAULT 1
                ''')
                
                cur.execute('''
                    ALTER TABLE billing_records 
                    ADD COLUMN IF NOT EXISTS billed_amount VARCHAR(50)
                ''')
                
                cur.execute('''
                    ALTER TABLE billing_records 
                    ADD COLUMN IF NOT EXISTS status_id INTEGER
                ''')
                
                self.conn.commit()
                print("Migration completed successfully")
            except Exception as e:
                self.conn.rollback()
                print(f"Migration error: {e}")
                
                
    
    def _insert_default_data(self):
        """Insert default data if database is empty"""
        with self.conn.cursor() as cur:
            # Check if we have any groups
            cur.execute('SELECT COUNT(*) FROM facility_groups')
            count = cur.fetchone()[0]
            
            if count == 0:
                # Insert default status group
                cur.execute('''
                    INSERT INTO status_groups (id, name, is_default)
                    VALUES (1, 'Default', true)
                    ON CONFLICT (id) DO NOTHING
                ''')

                # Insert default statuses
                cur.execute('''
                    INSERT INTO billing_statuses (status_group_id, name, color, sort_order)
                    VALUES 
                        (1, 'Not Billed', '#93C5FD', 1),
                        (1, 'Billed', '#FDE047', 2),
                        (1, 'Pending', '#C4B5FD', 3),
                        (1, 'Approved', '#86EFAC', 4),
                        (1, 'Paid', '#22C55E', 5)
                    ON CONFLICT DO NOTHING
                ''')
                # Insert default groups
                cur.execute('''
                    INSERT INTO facility_groups (id, name, billing_type, billing_day)
                    VALUES 
                        (1, 'Alabama Facilities', 'monthly', 1),
                        (2, 'Weekly Facilities', 'weekly', 5)
                ''')
                
                # Insert default facilities
                cur.execute('''
                    INSERT INTO facilities (id, name, group_id)
                    VALUES 
                        (1, 'Birmingham Care Center', 1),
                        (2, 'Montgomery Health', 1),
                        (3, 'Phoenix Center', 2),
                        (4, 'Sunrise Health', 2)
                ''')
                
                self.conn.commit()
    
    # ========================================================================
    # FACILITY GROUPS
    # ========================================================================
    
    def get_facility_groups(self):
        """Get all facility groups with their facilities and custom dates"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT id, name, billing_type, billing_day
                FROM facility_groups
                ORDER BY id
            ''')
            groups = cur.fetchall()
            
            # Get facilities and custom dates for each group
            for group in groups:
                # Get facilities
                cur.execute('''
                    SELECT id, name
                    FROM facilities
                    WHERE group_id = %s
                    ORDER BY id
                ''', (group['id'],))
                group['facilities'] = cur.fetchall()
            
            #Get statuses for this facility group
            cur.execute('''
                SELECT id, name, color, sort_order
                FROM billing_statuses
                WHERE group_id = %s
                ORDER BY sort_order
            ''', (group['id'],))
            group['statuses'] = cur.fetchall()
                
                # Get custom dates
                cur.execute('''
                    SELECT date, frequency, custom_from, custom_through
                    FROM custom_dates
                    WHERE group_id = %s
                    ORDER BY date DESC
                ''', (group['id'],))
                custom_dates = cur.fetchall()
                
                # Convert to format expected by frontend
                group['customDates'] = []
                for cd in custom_dates:
                    date_obj = {'date': cd['date'], 'frequency': cd['frequency']}
                    if cd['custom_from']:
                        date_obj['customFrom'] = cd['custom_from']
                    if cd['custom_through']:
                        date_obj['customThrough'] = cd['custom_through']
                    group['customDates'].append(date_obj)
                
                # Convert snake_case to camelCase for frontend
                group['billingType'] = group.pop('billing_type')
                group['billingDay'] = group.pop('billing_day')
            
            return groups
    
    def create_facility_group(self, data):
        """Create a new facility group"""
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO facility_groups (name, billing_type, billing_day)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (data['name'], data['billingType'], data.get('billingDay')))
            group_id = cur.fetchone()[0]
            self.conn.commit()
            return group_id
    
    def update_facility_group(self, group_id, data):
        """Update a facility group"""
        with self.conn.cursor() as cur:
            cur.execute('''
                UPDATE facility_groups
                SET name = %s, billing_type = %s, billing_day = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (data['name'], data['billingType'], data.get('billingDay'), group_id))
            self.conn.commit()
    
    def delete_facility_group(self, group_id):
        """Delete a facility group (cascades to facilities and records)"""
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM facility_groups WHERE id = %s', (group_id,))
            self.conn.commit()
    
    # ========================================================================
    # FACILITIES
    # ========================================================================
    
    def get_facilities(self):
        """Get all facilities"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT id, name, group_id
                FROM facilities
                ORDER BY id
            ''')
            facilities = cur.fetchall()
            
            # Convert snake_case to camelCase
            for f in facilities:
                f['groupId'] = f.pop('group_id')
            
            return facilities
    
    def create_facility(self, data):
        """Create a new facility"""
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO facilities (name, group_id)
                VALUES (%s, %s)
                RETURNING id
            ''', (data['name'], data['groupId']))
            facility_id = cur.fetchone()[0]
            self.conn.commit()
            return facility_id
    
    def delete_facility(self, facility_id):
        """Delete a facility (cascades to billing records)"""
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM facilities WHERE id = %s', (facility_id,))
            self.conn.commit()
    
    # ========================================================================
    # BILLING RECORDS
    # ========================================================================
    
    def get_billing_records(self):
        """Get all billing records"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT 
                    facility_id, cycle, billing_date, from_date, through_date,
                    billed_amount, paid_amount, paid_date, status_id
                FROM billing_records
            ''')
            records = cur.fetchall()
            
            # Convert to format expected by frontend (keyed by facility_id-cycle)
            records_dict = {}
            for r in records:
                key = f"{r['facility_id']}-{r['cycle']}"
                records_dict[key] = {
                    'facilityId': r['facility_id'],
                    'cycle': r['cycle'],
                    'billingDate': r['billing_date'],
                    'fromDate': r['from_date'],
                    'throughDate': r['through_date'],
                    'billedAmount': r['billed_amount'] or '',
                    'paidAmount': r['paid_amount'] or '',
                    'paidDate': r['paid_date'] or '',
                    'statusId': r['status_id']
                }
            
            return records_dict
    
    def save_billing_record(self, data):
        """Create or update a billing record"""
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO billing_records 
                    (facility_id, cycle, billing_date, from_date, through_date, 
                     billed_amount, paid_amount, paid_date, status_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (facility_id, cycle) 
                DO UPDATE SET
                    billing_date = EXCLUDED.billing_date,
                    from_date = EXCLUDED.from_date,
                    through_date = EXCLUDED.through_date,
                    billed_amount = EXCLUDED.billed_amount,
                    paid_amount = EXCLUDED.paid_amount,
                    paid_date = EXCLUDED.paid_date,
                    status_id = EXCLUDED.status_id,
                    updated_at = CURRENT_TIMESTAMP
            ''', (
                data['facilityId'],
                data['cycle'],
                data.get('billingDate'),
                data.get('fromDate'),
                data.get('throughDate'),
                data.get('billedAmount', ''),
                data.get('paidAmount', ''),
                data.get('paidDate', ''),
                data.get('statusId')
            ))
            self.conn.commit()
    
    # ========================================================================
    # CUSTOM DATES
    # ========================================================================
    
    def get_custom_dates(self, group_id):
        """Get custom dates for a group"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT date, frequency, custom_from, custom_through
                FROM custom_dates
                WHERE group_id = %s
                ORDER BY date DESC
            ''', (group_id,))
            return cur.fetchall()
    
    def save_custom_dates(self, group_id, dates):
        """Save custom dates for a group (replaces all existing)"""
        with self.conn.cursor() as cur:
            # Delete existing
            cur.execute('DELETE FROM custom_dates WHERE group_id = %s', (group_id,))
            
            # Insert new dates
            for date_obj in dates:
                cur.execute('''
                    INSERT INTO custom_dates (group_id, date, frequency, custom_from, custom_through)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    group_id,
                    date_obj['date'],
                    date_obj.get('frequency', 'monthly'),
                    date_obj.get('customFrom'),
                    date_obj.get('customThrough')
                ))
            
            self.conn.commit()
    
    # ========================================================================
    # SETTINGS
    # ========================================================================
    
    def get_settings(self):
        """Get all settings"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT key, value FROM settings')
            settings = cur.fetchall()
            
            # Convert to dict
            settings_dict = {}
            for s in settings:
                settings_dict[s['key']] = s['value']
            
            return settings_dict
    
    def save_settings(self, settings):
        """Save settings"""
        with self.conn.cursor() as cur:
            for key, value in settings.items():
                cur.execute('''
                    INSERT INTO settings (key, value)
                    VALUES (%s, %s)
                    ON CONFLICT (key)
                    DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
                ''', (key, value))
            
            self.conn.commit()
            
# ========================================================================
    # STATUS GROUPS
    # ========================================================================
    
    def get_status_groups(self):
        """Get all status groups with their statuses"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT id, name, is_default
                FROM status_groups
                ORDER BY is_default DESC, name
            ''')
            groups = cur.fetchall()
            
            # Get statuses for each group
            for group in groups:
                cur.execute('''
                    SELECT id, name, color, sort_order
                    FROM billing_statuses
                    WHERE status_group_id = %s
                    ORDER BY sort_order
                ''', (group['id'],))
                group['statuses'] = cur.fetchall()
                
                # Convert snake_case to camelCase for frontend
                group['isDefault'] = group.pop('is_default')
            
            return groups
    
    def create_status_group(self, data):
        """Create a new status group"""
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO status_groups (name, is_default)
                VALUES (%s, %s)
                RETURNING id
            ''', (data['name'], data.get('isDefault', False)))
            group_id = cur.fetchone()[0]
            self.conn.commit()
            return group_id
    
    # ========================================================================
    # BILLING STATUSES
    # ========================================================================
    
    def get_all_statuses(self):
        """Get all statuses across all groups"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT bs.id, bs.name, bs.color, bs.sort_order, bs.status_group_id,
                       sg.name as group_name
                FROM billing_statuses bs
                JOIN status_groups sg ON bs.status_group_id = sg.id
                ORDER BY sg.is_default DESC, bs.sort_order
            ''')
            statuses = cur.fetchall()
            
            # Convert to camelCase
            for s in statuses:
                s['sortOrder'] = s.pop('sort_order')
                s['statusGroupId'] = s.pop('status_group_id')
                s['groupName'] = s.pop('group_name')
            
            return statuses
    
    def get_statuses_by_group(self, group_id):
        """Get statuses for a specific group"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                SELECT id, name, color, sort_order
                FROM billing_statuses
                WHERE group_id = %s
                ORDER BY sort_order
            ''', (group_id,))
            statuses = cur.fetchall()
            
            # Convert to camelCase
            for s in statuses:
                s['sortOrder'] = s.pop('sort_order')
            
            return statuses
    
    def create_status(self, data):
        """Create a new status"""
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO billing_statuses (status_group_id, name, color, sort_order)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            ''', (
                data['group_id'],
                data['name'],
                data['color'],
                data.get('sortOrder', 0)
            ))
            status_id = cur.fetchone()[0]
            self.conn.commit()
            return status_id
    
    def update_status(self, status_id, data):
        """Update a status"""
        with self.conn.cursor() as cur:
            cur.execute('''
                UPDATE billing_statuses
                SET name = %s, color = %s, sort_order = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
                data['name'],
                data['color'],
                data.get('sortOrder', 0),
                status_id
            ))
            self.conn.commit()
    
    def delete_status(self, status_id):
        """Delete a status"""
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM billing_statuses WHERE id = %s', (status_id,))
            self.conn.commit()
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()
