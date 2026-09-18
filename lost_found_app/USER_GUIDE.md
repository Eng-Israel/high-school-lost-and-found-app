# 👨‍💼 Visual User Guide - Step by Step

## 🎯 Using the Lost & Found System

This guide shows exactly what you'll see and do when using the application.

---

## 🔐 ADMIN WORKFLOW

### Step 1: First Visit - Setup Page
```
┌─────────────────────────────────────────┐
│    🔧 INITIAL SETUP                     │
│                                         │
│  Welcome to Lost & Found System         │
│  First-time setup detected              │
│                                         │
│  Create Your Admin Account:             │
│  ┌──────────────────────────────────┐  │
│  │ Admin Username:  [__________]    │  │
│  │ Password:        [__________]    │  │
│  │ Confirm Password:[__________]    │  │
│  │                                  │  │
│  │        [✓ Create Admin Account]  │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Step 2: Login Page
```
┌──────────────────────────┐
│  🔐 Admin Login          │
│                          │
│  ┌──────────────────────┐
│  │ Username: [______]   │
│  │ Password: [______]   │
│  │           [Login]    │
│  └──────────────────────┘
│                          │
│  User Portal Start->     │
└──────────────────────────┘
```

### Step 3: Admin Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 Lost & Found Manager                    🚪 Logout          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STATISTICS                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ 📦 Total     │ │ ✅ Available │ │ ⏳ Claimed   │            │
│  │    Items: 27 │ │     Items: 19│ │    Items: 8  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐                                               │
│  │ 📋 Pending   │                                               │
│  │ Reports: 5   │                                               │
│  └──────────────┘                                               │
│                                                                  │
│  RECENT ACTIVITIES                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Found Items (Recent)        │ Reports (Recent)          │   │
│  ├────────────────────────────┼──────────────────────────┤   │
│  │ Blue Trouser (Shelf A3)    │ John - Lost Phone       │   │
│  │ Red Book (Box 1)           │ Sarah - Missing Card    │   │
│  │ Black Wallet (Shelf B1)    │ Mike - Lost Bag         │   │
│  └────────────────────────────┴──────────────────────────┘   │
│                                                                  │
│  QUICK ACTIONS                                                   │
│  [+ Add Found Item] [📦 Manage Items] [📋 Lost Reports]        │
└─────────────────────────────────────────────────────────────────┘
```

### Step 4: Add Found Item Page
```
┌─────────────────────────────────────────┐
│ ➕ Add Found Item                        │
├─────────────────────────────────────────┤
│                                         │
│ Item Type: [▼ Select Item Type]         │
│            └─ Trouser                   │
│            └─ Card                      │
│            └─ Phone                     │
│                                         │
│ (After selecting Trouser:)              │
│ Size:      [Large ▼]                   │
│ Color:     [Blue    ]                  │
│                                         │
│ Shelf Location: [Shelf A3        ]     │
│                 (Where items are      │
│                  stored for retrieval)│
│                                         │
│ Date Found: [2026-04-18]                │
│                                         │
│ Notes: [Nice condition, has ID inside] │
│                                         │
│           [💾 Add Item] [Cancel]       │
└─────────────────────────────────────────┘
```

### Step 5: Manage Items (Search & Filter)
```
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 Search & Filter Items                                        │
├─────────────────────────────────────────────────────────────────┤
│ Item Type [▼ All]  Size [______]  Color [______]               │
│ Location [______]  Status [▼ All]  [🔍 Search]                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ FOUND ITEMS LIST (19 Available)                                │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ ID │ Type  │ Description      │ Location │ Status │ Action │ │
│ ├────┼───────┼──────────────────┼──────────┼────────┼────────┤ │
│ │ 1  │Trouser│Blue, Size L      │ Shelf A3 │ ✅ Avail│ Claim │ │
│ │ 2  │ Card  │ID: AC123, Red    │ Box 1    │ ✅ Avail│ Claim │ │
│ │ 3  │Phone  │iPhone 12, Silver │ Shelf B1 │ ⏳ Claimed│ Delete│ │
│ │ 4  │Wallet │Black, Contents   │ Shelf A1 │ ✅ Avail│ Claim │ │
│ └────┴───────┴──────────────────┴──────────┴────────┴────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Step 6: Claim Item (Modal)
```
┌──────────────────────────────────────┐
│ 📝 Claim Found Item                  │
├──────────────────────────────────────┤
│                                      │
│ Item: Blue Trouser (Shelf A3)        │
│                                      │
│ Student Admission Number:            │
│ [________________]                   │
│                                      │
│        [✓ Confirm] [Cancel]         │
│                                      │
│ (Updates system: Item marked as     │
│  Claimed by Student AC2024)         │
└──────────────────────────────────────┘
```

### Step 7: Manage Reports (Lost Reports List)
```
┌─────────────────────────────────────────────────────────────────┐
│ 📋 Lost Item Reports (5 Pending)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ REPORTS TABLE                                                    │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ ID │Student│Admission│Item │Desc │Date Lost│Status│Action│ │
│ ├────┼───────┼─────────┼─────┼─────┼─────────┼──────┼──────┤ │
│ │1   │John   │AC2024-1 │Phone│Brand│04-15   │⏳ Pend│Match │ │
│ │2   │Sarah  │AC2024-2 │Card │Type │04-16   │⏳ Pend│Match │ │
│ │3   │Mike   │AC2024-3 │Bag  │Color│04-17   │⏳ Pend│Match │ │
│ └────┴───────┴─────────┴─────┴─────┴─────────┴──────┴──────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Step 8: Match Items (Modal)
```
┌──────────────────────────────────────────────┐
│ 🔗 Match with Found Item                     │
├──────────────────────────────────────────────┤
│                                              │
│ Lost Report: John's Phone                    │
│ (Brand: iPhone, Model: 12)                   │
│                                              │
│ Available Found Items:                       │
│ [▼ Select Found Item]                        │
│  └─ #3 - Phone at Shelf B1                   │
│  └─ #7 - Phone at Box 2                      │
│  └─ #12- Phone at Shelf C3                   │
│                                              │
│ Item Details:                                │
│ - Brand: iPhone                              │
│ - Model: 12                                  │
│ - Location: Shelf B1                         │
│ - Date Found: 2026-04-16                     │
│                                              │
│     [✓ Match Items] [Cancel]                │
└──────────────────────────────────────────────┘
```

---

## 👤 USER/STUDENT WORKFLOW

### Step 1: Landing Page
```
┌─────────────────────────────────────────┐
│ 🔍 Lost & Found                         │
│ Lost an item? Need help finding it?     │
│                                         │
│ QUICK OPTIONS                           │
│ [🔍 Search Found Items]                │
│ [📋 Report Lost Item]                  │
│ [🔐 Admin Login]                       │
│                                         │
│ We help reunite lost items with their   │
│ owners. Search our database or file a   │
│ report. Our admin team will help match! │
└─────────────────────────────────────────┘
```

### Step 2: Search Found Items
```
┌─────────────────────────────────────────┐
│ 🔍 Search Found Items                  │
│                                         │
│ Looking for something?                  │
│                                         │
│ Select Item Type:                       │
│ [▼ -- Select Item Type --]              │
│  └─ Trouser                             │
│  └─ Card                                │
│  └─ Book                                │
│  └─ Phone                               │
│  └─ Wallet                              │
│  └─ Bag                                 │
│  └─ Shoe                                │
│  └─ Uniform                             │
│  └─ Accessories                         │
│  └─ Keys                                │
│                                         │
│         [🔍 Search] [Report Lost] [Back]│
│                                         │
│ Hint: Select your item type and        │
│ click search to see all available items │
└─────────────────────────────────────────┘
```

### Step 3: Search Results
```
┌─────────────────────────────────────────────┐
│ 📦 Found Items (3 Results)                 │
├─────────────────────────────────────────────┤
│                                             │
│ ┌────────────────────────────────────────┐ │
│ │ 👖 TROUSER                             │ │
│ │                                        │ │
│ │ Size: Large                            │ │
│ │ Color: Blue                            │ │
│ │                                        │ │
│ │ 📍 Location: Shelf A3                  │ │
│ │ 📅 Date Found: 2026-04-16              │ │
│ │                                        │ │
│ │ [Is this yours? Report it!]            │ │
│ └────────────────────────────────────────┘ │
│                                             │
│ ┌────────────────────────────────────────┐ │
│ │ 👔 UNIFORM                             │ │
│ │                                        │ │
│ │ Size: Medium                           │ │
│ │ Color: White with Blue trim            │ │
│ │                                        │ │
│ │ 📍 Location: Shelf B2                  │ │
│ │ 📅 Date Found: 2026-04-17              │ │
│ │                                        │ │
│ │ [Is this yours? Report it!]            │ │
│ └────────────────────────────────────────┘ │
│                                             │
│ [◄ Back to Search]                         │
└─────────────────────────────────────────────┘
```

### Step 4: Report Lost Item
```
┌─────────────────────────────────────────┐
│ 📋 Report Lost Item                     │
│                                         │
│ ┌───────────────────────────────────┐   │
│ │ Student Name: [____________]      │   │
│ │ Admission No: [____________]      │   │
│ │                                   │   │
│ │ Item Type:    [▼ Select...]      │   │
│ │               └─ Trouser         │   │
│ │               └─ Card            │   │
│ │               └─ Phone           │   │
│ │                                   │   │
│ │ (After selecting Trouser:)       │   │
│ │ Size:  [Large ▼]                │   │
│ │ Color: [Blue    ]                │   │
│ │                                   │   │
│ │ Date Lost:    [2026-04-15]        │   │
│ │ Location Lost: [Classroom A12  ]  │   │
│ │ Contact Info:  [+27-123-4567  ]  │   │
│ │                                   │   │
│ │    [📤 Submit Report] [Cancel]   │   │
│ │                                   │   │
│ │ (Admin will check for matches)   │   │
│ └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Step 5: Report Submitted
```
┌─────────────────────────────────────────┐
│ ✅ SUCCESS!                             │
│                                         │
│ Your lost item report has been         │
│ submitted successfully!                │
│                                         │
│ Report ID: #42                         │
│ Date Submitted: 2026-04-18             │
│                                         │
│ 📌 Next Steps:                         │
│ 1. Our admin team will review your     │
│    report                              │
│ 2. We will search for matching items   │
│ 3. If found, we'll contact you at:    │
│    +27-123-4567                        │
│                                         │
│ 💡 Tip: Check back in a few days or   │
│ give us a call!                        │
│                                         │
│ [🏠 Back to Home]                     │
└─────────────────────────────────────────┘
```

---

## 🎯 Key Interactions Explained

### Dynamic Item Fields
```
Step 1: Select Item Type
User chooses "Trouser" from dropdown
         ↓
Step 2: Form Updates Automatically
New fields appear: Size & Color
         ↓
Step 3: User Enters Values
Size: "Large"
Color: "Blue"
         ↓
Step 4: System Stores as JSON
description: {"size": "Large", "color": "Blue"}
```

### Search & Match Flow
```
User Reports Lost Item
         ↓
Admin Sees Report
         ↓
Admin Clicks "Match"
         ↓
System Shows Similar Found Items
         ↓
Admin Selects Match
         ↓
System Links Records
         ↓
Status Updates Automatically
Item: "Returned" | Report: "Resolved"
         ↓
Student Can Retrieve Item
```

---

## 💬 Common User Scenarios

### Scenario 1: Student Lost a Trouser
1. Visits `/user/search`
2. Selects "Trouser" → Clicks Search
3. Sees "Blue Size L Trouser at Shelf A3"
4. Goes to Shelf A3 → Finds trouser
5. Takes it to admin to confirm
6. **Problem Solved!** ✅

### Scenario 2: Found Item, No Match Yet
1. Admin adds "Red Wallet" to system
2. Shelf location: "Shelf B1"
3. Student reports lost wallet
4. Admin sees report → Clicks Match
5. Selects the "Red Wallet" (#15)
6. System links them
7. **Match Made!** ✅ Student retrieves wallet

### Scenario 3: Wrong Size Found
1. Student lost "Blue Size L Trouser"
2. Found item is "Blue Size M Trouser"
3. Admin doesn't match them
4. Still visible in search (different size)
5. **Students can decide** if it's similar enough

---

## 🎨 Color-Coded Status Indicators

```
✅ AVAILABLE  (Green)     - Item ready to claim
⏳ CLAIMED    (Yellow)    - Student claimed it
✔️  RETURNED   (Blue)     - Item returned/resolved
📌 PENDING    (Red)       - Report waiting for match
🔗 FOUND      (Green)     - Match found between report & item
```

---

**This visual guide shows you exactly what to expect!** 🎯
