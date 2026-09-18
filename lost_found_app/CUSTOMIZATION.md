# Configuration & Customization Guide

## System Customization

### Adding Custom Item Types

To add new item types beyond the defaults, you can:

**Option 1: Edit in Database (Advanced)**
1. Stop the application
2. Use a SQLite viewer to edit `lost_found.db`
3. Add to `item_type` table with JSON fields array

**Option 2: Add via Code**
Edit `app.py` in the `create_first_admin()` function and add:
```python
ItemType(name='YourItemType', fields=['field1', 'field2'])
```

### Default Item Types
The following are created automatically:
- Trouser (Size, Color)
- Card (ID Number, Type)
- Book (Title, Author)
- Phone (Brand, Model)
- Wallet (Color, Contents)
- Bag (Color, Brand)
- Shoe (Size, Color, Brand)
- Uniform (Size, Color)
- Accessories (Type, Color)
- Keys (Description)

## Application Settings

### Change Port
In `app.py`, modify the last line:
```python
app.run(debug=True, port=5001)  # Change 5000 to desired port
```

### Database Location
By default, database is at: `lost_found.db` in the app directory

To change:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/your/database.db'
```

### Debug Mode
In `app.py`:
- `debug=True` - Development mode (auto-reload, detailed errors)
- `debug=False` - Production mode (safer, no auto-reload)

## UI Customization

### Brand Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    --danger-color: #dc3545;
    /* Add more as needed */
}
```

### Logo/Title
In template files, change:
- `{{ url_for('dashboard') }}` links
- Navbar branding text "🔐 Admin Login" or "Lost & Found"

### Application Title
In each HTML template `<title>` tag

## Advanced Customization

### Add Email Notifications
1. Install: `pip install Flask-Mail`
2. Configure email settings in `app.py`
3. Add email sending in routes

### Add Image Upload for Items
1. Install: `pip install Werkzeug`
2. Create uploads folder
3. Add file handling in `add_found_item` route

### Export Reports
1. Install: `pip install openpyxl python-dateutil`
2. Create export endpoint returning CSV/Excel

### SMS Notifications
1. Use Twilio API
2. Add SMS sending on item match

## Database Backup

### Manual Backup
```bash
# Copy the database file
cp lost_found.db lost_found_backup.db
```

### Automated Backup (Optional)
Add to `app.py`:
```python
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('lost_found.db', f'backups/lost_found_{timestamp}.db')
```

## Performance Tips

1. **Database Cleanup**: Periodically delete old resolved reports
2. **Search Optimization**: Add database indexes for frequently searched fields
3. **Caching**: Implement item type caching to reduce database hits
4. **Pagination**: Add pagination to item lists for large datasets

## Security Enhancements

### Password Hashing (Recommended)
Replace plain text passwords with hashed ones:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# When creating admin:
admin.password = generate_password_hash(password)

# When checking password:
if check_password_hash(admin.password, provided_password):
    # Login successful
```

### Session Security
In `app.py`:
```python
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
```

### CSRF Protection
Install: `pip install Flask-WTF`

## Troubleshooting Customizations

**Issue: Changes not reflecting**
- Clear browser cache (Ctrl+F5)
- Restart Flask server
- Check for syntax errors in edited files

**Issue: Database issues after changes**
- Delete `lost_found.db` 
- Restart application to recreate with new schema

**Issue: Templates not updating**
- Flask auto-reloads templates (if debug=True)
- Restart server if still not working

## Production Deployment

### Before Going Live:
1. Set `debug=False`
2. Use strong SECRET_KEY
3. Implement password hashing
4. Use production database (PostgreSQL recommended)
5. Set up HTTPS
6. Configure proper logging
7. Regular database backups

### Environment Variables
Create `.env` file:
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@localhost/lostfound
SECRET_KEY=your-secret-key-here
```

### Recommended Hosting
- Heroku (easy deployment)
- AWS/Google Cloud
- DigitalOcean
- PythonAnywhere

## Support for Customization

For complex customizations, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.1/

---
Happy customizing!
