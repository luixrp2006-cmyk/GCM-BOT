import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    """SQLite Database Handler"""
    
    def __init__(self, db_path="gcm_bot.db"):
        self.db_path = db_path
        self.conn = None
    
    async def initialize(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        try:
            # Timesheet (Ponto)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timesheet (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    check_in TIMESTAMP,
                    check_out TIMESTAMP,
                    status TEXT DEFAULT 'in_progress',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, DATE(check_in))
                )
            ''')
            
            # Vehicles (Viaturas)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate TEXT UNIQUE NOT NULL,
                    model TEXT NOT NULL,
                    status TEXT DEFAULT 'available',
                    last_check_out TIMESTAMP,
                    assigned_to INTEGER,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Incidents (Ocorrências)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    location TEXT,
                    status TEXT DEFAULT 'open',
                    priority TEXT DEFAULT 'normal',
                    reported_by INTEGER NOT NULL,
                    assigned_to INTEGER,
                    vehicle_plate TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    closed_at TIMESTAMP
                )
            ''')
            
            # Incident Updates (Log de Ocorrências)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incident_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
                )
            ''')
            
            self.conn.commit()
            logger.info("✓ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    # ===== TIMESHEET METHODS =====
    
    async def add_check_in(self, user_id: int, username: str):
        """Register check-in"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO timesheet (user_id, username, check_in, status)
            VALUES (?, ?, CURRENT_TIMESTAMP, 'in_progress')
        ''', (user_id, username))
        self.conn.commit()
        return cursor.lastrowid
    
    async def add_check_out(self, user_id: int):
        """Register check-out"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE timesheet 
            SET check_out = CURRENT_TIMESTAMP, status = 'completed'
            WHERE user_id = ? AND status = 'in_progress'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def get_today_timesheet(self, user_id: int):
        """Get today's timesheet"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM timesheet 
            WHERE user_id = ? AND DATE(created_at) = DATE('now')
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        return cursor.fetchone()
    
    # ===== VEHICLE METHODS =====
    
    async def add_vehicle(self, plate: str, model: str, notes: str = None):
        """Add a new vehicle"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vehicles (plate, model, notes)
            VALUES (?, ?, ?)
        ''', (plate.upper(), model, notes))
        self.conn.commit()
        return cursor.lastrowid
    
    async def assign_vehicle(self, plate: str, user_id: int):
        """Assign vehicle to officer"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE vehicles 
            SET assigned_to = ?, status = 'in_use', updated_at = CURRENT_TIMESTAMP
            WHERE plate = ?
        ''', (user_id, plate.upper()))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def return_vehicle(self, plate: str):
        """Return vehicle to available"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE vehicles 
            SET assigned_to = NULL, status = 'available', last_check_out = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE plate = ?
        ''', (plate.upper(),))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def get_vehicle(self, plate: str):
        """Get vehicle info"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vehicles WHERE plate = ?', (plate.upper(),))
        return cursor.fetchone()
    
    async def list_vehicles(self):
        """List all vehicles"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vehicles ORDER BY plate')
        return cursor.fetchall()
    
    # ===== INCIDENT METHODS =====
    
    async def create_incident(self, incident_id: str, title: str, description: str, 
                            location: str, reported_by: int, priority: str = 'normal'):
        """Create a new incident"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO incidents (incident_id, title, description, location, reported_by, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (incident_id, title, description, location, reported_by, priority))
        self.conn.commit()
        return cursor.lastrowid
    
    async def get_incident(self, incident_id: str):
        """Get incident details"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM incidents WHERE incident_id = ?', (incident_id,))
        return cursor.fetchone()
    
    async def assign_incident(self, incident_id: str, user_id: int):
        """Assign incident to officer"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE incidents 
            SET assigned_to = ?, updated_at = CURRENT_TIMESTAMP
            WHERE incident_id = ?
        ''', (user_id, incident_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def update_incident_status(self, incident_id: str, status: str):
        """Update incident status"""
        closed_at = 'CURRENT_TIMESTAMP' if status == 'closed' else 'NULL'
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE incidents 
            SET status = ?, updated_at = CURRENT_TIMESTAMP, closed_at = {closed_at}
            WHERE incident_id = ?
        ''', (status, incident_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    async def add_incident_update(self, incident_id: str, user_id: int, message: str):
        """Add update to incident"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO incident_updates (incident_id, user_id, message)
            VALUES (?, ?, ?)
        ''', (incident_id, user_id, message))
        self.conn.commit()
    
    async def get_incident_updates(self, incident_id: str):
        """Get all updates for incident"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM incident_updates 
            WHERE incident_id = ?
            ORDER BY created_at ASC
        ''', (incident_id,))
        return cursor.fetchall()
    
    async def list_open_incidents(self):
        """List all open incidents"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM incidents 
            WHERE status IN ('open', 'in_progress')
            ORDER BY created_at DESC
        ''')
        return cursor.fetchall()
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
