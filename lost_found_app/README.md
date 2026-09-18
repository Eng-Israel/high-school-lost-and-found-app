# Lost & Found Management System

A comprehensive web-based Lost and Found management system designed for high schools. The system allows admins to manage found items and helps students find their lost belongings.

## Features

### Admin Features
- **Dashboard**: Overview of all found items and lost reports
- **Add Found Items**: Register found items with detailed descriptions
  - Dynamic item type fields (e.g., size & color for trousers, ID number for cards)
  - Specify shelf location for easy retrieval
  - Track item status (Available, Claimed, Returned)
  
- **Manage Items**: Search and filter found items by:
  - Item type
  - Size
  - Color
  - Location
  - Status
  
- **Claim Items**: Mark items as claimed to a specific student (admission number)

- **Lost Reports**: View student reports about lost items
- **Match Items**: Link lost reports with found items

- **Advanced Search Interface**: Exhaustive search and selection capabilities

### User Features
- **Search Found Items**: Browse available found items by type
- **Report Lost Items**: Submit lost item reports with detailed descriptions
  - Dynamic fields based on item type
  - Location where item was lost
  - Contact information for follow-up
  
- **Easy Discovery**: View found items with complete descriptions and shelf locations

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd lost_found_app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Open your web browser
   - Go to `http://localhost:5000`
   - First time? You'll be prompted to create an admin account
   - Use the admin credentials to access the admin dashboard

## Usage

### First Time Setup
1. Visit `http://localhost:5000`
2. You'll be directed to the setup page
3. Create your admin account with a username and password
4. The system will automatically create default item types

### Admin Dashboard

**Login:**
- Navigate to `http://localhost:5000/login`
- Enter your admin credentials

**Add Found Items:**
1. Click "Add Found Item" from the dashboard
2. Select the item type (Trouser, Card, Book, Phone, Wallet, Bag, Shoe, Uniform, Accessories, Keys)
3. Fill in dynamic fields based on item type
4. Specify the shelf location for easy retrieval
5. Enter the date found and any additional notes
6. Submit to register the item

**Manage Items:**
1. Click "Manage Items"
2. Use the search and filter panel to find specific items
3. Filter by: Item Type, Size, Color, Location, Status
4. Click "Claim" to mark an item as claimed to a student
5. Click "Delete" to remove items (use for duplicates or returned items)

**Lost Reports:**
1. Click "Lost Reports"
2. View all student lost reports
3. Click "Match" to link a lost report with a found item
4. System will automatically update both the report and item status

### User Section

**Search for Lost Items:**
1. Go to `http://localhost:5000/user/search`
2. Select your item type
3. Click "Search" to see all available found items
4. View details including shelf location, date found, and description

**Report a Lost Item:**
1. Click "Report Lost Item" from the user menu
2. Enter your student information (name and admission number)
3. Select the item type you lost
4. Fill in the item description (dynamic fields based on type)
5. Enter where and when you lost it
6. Provide contact information
7. Submit the report
8. Admin will check for matches and contact you

## Item Types and Fields

The system supports the following item types with their respective fields:

| Item Type | Fields |
|-----------|--------|
| Trouser | Size, Color |
| Card | ID Number, Type |
| Book | Title, Author |
| Phone | Brand, Model |
| Wallet | Color, Contents |
| Bag | Color, Brand |
| Shoe | Size, Color, Brand |
| Uniform | Size, Color |
| Accessories | Type, Color |
| Keys | Description |

## Database

The system uses SQLite database (`lost_found.db`) that is automatically created on first run.

### Database Tables:
- **Admin**: Admin user accounts
- **ItemType**: Available item types and their dynamic fields
- **FoundItem**: Items reported as found
- **LostReport**: Student reports of lost items

## Technical Details

### Technology Stack
- **Backend**: Flask (Python Web Framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentication**: Session-based admin authentication

### File Structure
```
lost_found_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── login.html
│   ├── admin_setup.html
│   ├── admin_dashboard.html
│   ├── add_found_item.html
│   ├── manage_items.html
│   ├── manage_reports.html
│   ├── user_search.html
│   ├── report_lost.html
│   ├── found_items_list.html
│   ├── 404.html
│   └── 500.html
├── static/
│   └── css/
│       └── style.css      # Application styling
└── lost_found.db         # SQLite database (auto-created)
```

## API Endpoints

- `GET /` - Home page
- `GET/POST /login` - Admin login
- `GET /logout` - Admin logout
- `GET /admin/dashboard` - Admin dashboard
- `GET/POST /admin/add-item` - Add found item
- `GET /admin/items` - Manage found items
- `POST /admin/items/search` - Search items
- `POST /admin/item/<id>/claim` - Claim item
- `POST /admin/item/<id>/delete` - Delete item
- `GET /admin/reports` - Manage lost reports
- `POST /admin/report/<id>/match` - Match report with item
- `GET /user/search` - User search page
- `POST /user/search-found-items` - Display found items
- `GET/POST /user/report-lost` - Report lost item
- `GET /api/item-types` - Get all item types (JSON)
- `GET /api/item-type/<id>` - Get item type details (JSON)
- `GET /api/found-items` - Get all available found items (JSON)

## Security Considerations

- Admin accounts are protected with password-based authentication
- Sessions are used to maintain user state
- Admission numbers are stored for item claims
- Database includes timestamps for audit trails

## Future Enhancements

- Email notifications when items are found or matched
- Photo upload for items
- Student account creation and history tracking
- Advanced analytics and reports
- SMS notifications
- Multi-location support
- Barcode/QR code generation for items
- Admin role management (super admin, staff)
- Export reports to CSV/PDF

## Troubleshooting

**Issue: "Address already in use" error**
- The port 5000 is already in use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Issue: Database error**
- Delete `lost_found.db` and restart the application
- The database will be recreated automatically

**Issue: Module not found**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Support

For issues or questions, contact your system administrator.

---

**Version**: 1.0.0  
**Last Updated**: 2026  
**System**: High School Lost & Found Management System
