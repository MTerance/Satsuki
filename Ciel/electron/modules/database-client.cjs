const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class DatabaseClient {
  constructor() {
    this.db = null;
  }

  // Initialize database connection
  initialize(dbPath = null) {
    return new Promise((resolve, reject) => {
      // Use provided path or default to parent directory
      const finalDbPath = dbPath || path.join(__dirname, '..', '..', 'database.db');
      
      this.db = new sqlite3.Database(finalDbPath, (err) => {
        if (err) {
          console.error('Error opening database:', err.message);
          reject(err);
        } else {
          console.log('Connected to SQLite database at:', finalDbPath);
          
          // Create example table if it doesn't exist
          this.db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )`, (err) => {
            if (err) {
              console.error('Error creating table:', err.message);
              reject(err);
            } else {
              console.log('Users table ready');
              resolve();
            }
          });
        }
      });
    });
  }

  // Add a new user
  addUser(userData) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const { name, email } = userData;
      this.db.run('INSERT INTO users (name, email) VALUES (?, ?)', [name, email], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, name, email });
        }
      });
    });
  }

  // Get all users
  getUsers() {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      this.db.all('SELECT * FROM users ORDER BY created_at DESC', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Delete a user
  deleteUser(userId) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      this.db.run('DELETE FROM users WHERE id = ?', [userId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ deletedId: userId, changes: this.changes });
        }
      });
    });
  }

  // Get user by ID
  getUserById(userId) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      this.db.get('SELECT * FROM users WHERE id = ?', [userId], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row || null);
        }
      });
    });
  }

  // Update user
  updateUser(userId, userData) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const { name, email } = userData;
      this.db.run('UPDATE users SET name = ?, email = ? WHERE id = ?', [name, email, userId], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: userId, changes: this.changes });
        }
      });
    });
  }

  // Close database connection
  close() {
    return new Promise((resolve, reject) => {
      if (this.db) {
        this.db.close((err) => {
          if (err) {
            console.error('Error closing database:', err.message);
            reject(err);
          } else {
            console.log('Database connection closed');
            this.db = null;
            resolve();
          }
        });
      } else {
        resolve();
      }
    });
  }

  // Check if database is connected
  isConnected() {
    return this.db !== null;
  }

  // Get database instance (for advanced usage)
  getDatabase() {
    return this.db;
  }
}

// Export singleton instance
module.exports = new DatabaseClient();
