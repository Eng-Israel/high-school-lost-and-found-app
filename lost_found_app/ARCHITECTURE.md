# Lost & Found System - Architecture & Features Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WEB BROWSER                               │
│         (Admin Dashboard / User Interface)                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP/HTTPS
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              FLASK WEB SERVER (app.py)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Route Handlers & Business Logic                       │ │
│  │  - Authentication & Sessions                          │ │
│  │  - Item Management                                    │ │
│  │  - Report Processing                                 │ │
│  │  - Matching Algorithm                                │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ SQL Queries
                   │
┌──────────────────▼──────────────────────────────────────────┐
│         SQLAlchemy ORM & SQLite Database                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Tables:                                              │ │
│  │  - Admin (User Accounts)                             │ │
│  │  - ItemType (Type Definitions)                       │ │
│  │  - FoundItem (Items Reported Found)                  │ │
│  │  - LostReport (Student Loss Reports)                 │ │
│  └────────────────────────────────────────────────────────┘ │
│  File: lost_found.db                                       │
└──────────────────────────────────────────────────────────────┘
```

## 👥 User Flows

### Admin Flow
```
┌─────────────────┐
│   Admin Login   │
└────────┬────────┘
         │
    ┌────▼────┐
    │Dashboard │
    └────┬────┘
         │
    ┌────┴─────────────────────┬──────────────┐
    │                          │              │
    ▼                          ▼              ▼
┌─────────────┐         ┌──────────────┐  ┌─────────────┐
│ Add Items   │         │ Manage Found │  │Lost Reports │
│ - Intake    │         │    Items     │  │             │
│ - Location  │         │ - Search     │  │ - View      │
│ - Describe  │         │ - Filter     │  │ - Match     │
│             │         │ - Claim      │  │ - Link      │
└─────────────┘         └──────────────┘  └─────────────┘
```

### User/Student Flow
```
┌──────────────────────────────────────┐
│   User Lands on Homepage             │
└─────────┬──────────────────────────┬─┘
          │                          │
    ┌─────▼──────┐             ┌─────▼──────────┐
    │Search Items │             │Report Lost Item│
    │- Browse by  │             │- Input Details │
    │  Type       │             │- Submit Report │
    │- View Found │             │- Get Contacted │
    └─────────────┘             └─────────────────┘
          │
    ┌─────▼──────────────┐
    │View Item Details   │
    │- Description       │
    │- Shelf Location    │
    │- Date Found        │
    └────────────────────┘
```

## 📊 Data Model

### Item Type
```
ItemType {
  id: int (primary key)
  name: string ("Trouser", "Card", "Phone", etc.)
  fields: json ["size", "color"] or ["id_number", "type"]
}
```

### Found Item
```
FoundItem {
  id: int (primary key)
  item_type_id: int (foreign key)
  description: json {size: "L", color: "Blue"}
  location: string "Shelf A3"
  date_found: datetime
  date_added: datetime
  is_claimed: boolean
  claimed_by_admission_no: string
  claim_date: datetime
  status: string ("Available", "Claimed", "Returned")
  notes: text
}
```

### Lost Report
```
LostReport {
  id: int (primary key)
  student_admission_no: string
  student_name: string
  item_type_id: int (foreign key)
  description: json
  date_lost: datetime
  date_reported: datetime
  location_lost: string
  contact_info: string
  status: string ("Pending", "Found", "Resolved")
  matched_found_item_id: int (foreign key)
}
```

## 🔄 Item Lifecycle

```
FOUND ITEM:
New Item → Available → Claimed (by student) → Returned/Archived

Lost Report:
Lost → Reported → Pending → Found Match → Resolved

MATCHING PROCESS:
Admin views Lost Report
      ↓
Admin clicks "Match" 
      ↓
Selects Corresponding Found Item
      ↓
System Updates Both Records
      ↓
Status Changes: Item "Returned", Report "Resolved"
      ↓
Student Notified (can be expanded with email/SMS)
```

## 🎯 Key Features Breakdown

### 1. Dynamic Item Descriptions
```
Item Type Selected → System Fetches Required Fields
                          ↓
                  Form Updates with Specific Inputs
                          ↓
                  Admin Provides Values
                          ↓
                  Stored as JSON in Database
```

### 2. Search & Filter
```
User Input (Type, Size, Color, Location)
        ↓
Query Builder Filters Database
        ↓
Results Displayed with Details
        ↓
User Can Search Again or View Details
```

### 3. Matching Algorithm
```
Lost Report Details
        ↓
    Find Similar Found Items
        ↓
Display Available Found Items
        ↓
Admin Selects Match
        ↓
Link Records & Update Status
```

## 🔐 Security Features

- Session-based admin authentication
- Database validation for all inputs
- CSRF protection (can be enhanced)
- Password-protected admin area
- Admission number tracking

## 📈 Workflow Statistics

**Dashboard Shows:**
- Total Found Items
- Available Items Count
- Claimed Items Count
- Pending Lost Reports

## 🌐 API Endpoints Summary

| Method | Endpoint | Function |
|--------|----------|----------|
| GET | `/` | Home redirect |
| GET/POST | `/login` | Admin authentication |
| GET | `/admin/dashboard` | Admin dashboard |
| GET/POST | `/admin/add-item` | Add found item |
| GET | `/admin/items` | List/manage items |
| POST | `/admin/items/search` | Search items |
| POST | `/admin/item/<id>/claim` | Claim item |
| GET | `/admin/reports` | Lost reports list |
| POST | `/admin/report/<id>/match` | Match items |
| GET | `/user/search` | User search page |
| POST | `/user/search-found-items` | Search results |
| GET/POST | `/user/report-lost` | Report lost item |
| GET | `/api/item-types` | Get item types (JSON) |
| GET | `/api/found-items` | Get found items (JSON) |

## 🎨 UI Components

### Admin Interface
- Login form with validation
- Dashboard with statistics cards
- Multi-field search form
- Interactive tables with actions
- Modals for claim/match operations

### User Interface
- Clean search interface
- Item type selector
- Found items card layout
- Lost report form with dynamic fields
- Item details display

### Styling
- Bootstrap 5 framework
- Custom gradient backgrounds
- Responsive design
- Smooth animations
- Accessibility features

## 🚀 Performance Notes

- SQLite database (suitable for small to medium systems)
- Efficient JSON field storage for item descriptions
- Indexed queries for frequent searches
- Session management for authentication

---

This architecture provides a scalable, maintainable system perfect for high school environments!
