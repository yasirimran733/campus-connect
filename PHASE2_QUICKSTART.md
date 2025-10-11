# 🚀 Phase 2 Quick Start Guide

## ✅ Prerequisites

Make sure Phase 1 is complete:
- ✅ Server is running
- ✅ Database migrations applied
- ✅ Superuser created
- ✅ At least one verified user exists

---

## 🎯 Quick Test Flow

### **1. Create a Verified User (If Needed)**

```powershell
# In Django shell
python manage.py shell
```

```python
from users.models import User

# Create verified user
user = User.objects.create_user(
    username='testuser',
    email='test@pucit.edu.pk',
    password='test123',
    first_name='Test',
    last_name='User',
    is_verified=True  # Important!
)
print(f"Created: {user.username}")
exit()
```

### **2. Login as Verified User**

1. Go to: http://127.0.0.1:8000/users/login/
2. Login with verified user credentials
3. You should see "✓ Verified" in navigation

### **3. Post Your First Item**

**Option A: Via Dashboard**
1. Go to Dashboard
2. Click "Post New Item" button

**Option B: Direct URL**
1. Go to: http://127.0.0.1:8000/items/create/

**Fill the Form:**
- **Item Type:** Lost or Found
- **Title:** "Black iPhone 13 Pro"
- **Category:** Electronics
- **Description:** "Lost near library, has a blue case"
- **Location:** "Library 2nd Floor"
- **Date:** Select today's date
- **Image:** Upload a photo (optional)
- **Contact:** Your phone/email (optional)
- Click "Post Item"

### **4. Approve Item (Admin)**

1. Go to: http://127.0.0.1:8000/admin/
2. Login as superuser
3. Click "Lost & Found Items" → "Items"
4. Find your item
5. Check the "is_approved" checkbox
6. Click "Save"

### **5. View Public Item**

1. Go to: http://127.0.0.1:8000/items/
2. You should see your approved item
3. Click on it to view details

---

## 🌐 Key URLs

| Page | URL | Access |
|------|-----|--------|
| Browse Items | `/items/` | Public |
| Lost Items | `/items/lost/` | Public |
| Found Items | `/items/found/` | Public |
| Item Detail | `/items/<id>/` | Public |
| Post Item | `/items/create/` | Verified Users |
| My Items | `/items/my-items/` | Verified Users |
| Edit Item | `/items/<id>/edit/` | Owner Only |
| Admin Panel | `/admin/` | Admin Only |

---

## 🎨 Features to Test

### **1. Browse & Search**
- ✅ Go to `/items/`
- ✅ Use search box
- ✅ Filter by type (Lost/Found)
- ✅ Filter by category
- ✅ Filter by date range

### **2. Item Details**
- ✅ Click any item
- ✅ View full details
- ✅ See contact info (verified users only)
- ✅ Check view counter
- ✅ View related items

### **3. My Items Management**
- ✅ Go to "My Items"
- ✅ View statistics
- ✅ Edit your items
- ✅ Update item status
- ✅ Delete items

### **4. Admin Approval**
- ✅ Login to admin panel
- ✅ View pending items
- ✅ Approve multiple items (bulk action)
- ✅ Filter by status
- ✅ Search items

### **5. Dashboard Integration**
- ✅ View items statistics
- ✅ See recent items feed
- ✅ Quick action buttons

---

## 🧪 Test Scenarios

### **Scenario 1: Lost Item Workflow**

1. **User posts lost item**
   - Login as verified user
   - Post lost iPhone
   - See "Pending Approval" status

2. **Admin approves**
   - Login to admin
   - Approve the item
   - Item becomes public

3. **Someone finds it**
   - Another user views the item
   - Contacts owner via email/phone
   - Owner marks as "Claimed"

### **Scenario 2: Found Item Workflow**

1. **User finds item**
   - Post found wallet
   - Add location and date
   - Upload photo

2. **Owner searches**
   - Browse found items
   - Search by keyword "wallet"
   - Find their item

3. **Contact & Return**
   - Owner contacts finder
   - Item marked as "Returned"

### **Scenario 3: Reward System**

1. **Post with reward**
   - Check "Reward Offered"
   - Enter amount (e.g., 500 PKR)
   - Item shows reward badge

2. **Browse rewards**
   - Filter items with rewards
   - View reward amount

---

## 🐛 Troubleshooting

### **Issue: Can't post items**
**Solution:** Make sure user is verified
```python
# Check user status
python manage.py shell
from users.models import User
user = User.objects.get(username='youruser')
print(f"Verified: {user.is_verified}")

# Verify user if needed
user.is_verified = True
user.save()
```

### **Issue: Items not showing**
**Solution:** Items need admin approval
- Check `is_approved` field in admin panel
- Approve the item

### **Issue: Can't upload images**
**Solution:** Check media settings
- Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured
- Check file permissions
- Verify image size (max 5MB)

### **Issue: Search not working**
**Solution:** 
- Make sure items are approved
- Check search query syntax
- Try filtering by category first

---

## 📊 Sample Data

### **Create Sample Items (Optional)**

```python
python manage.py shell
```

```python
from items.models import Item
from users.models import User
from datetime import date

user = User.objects.get(username='testuser')

# Lost items
Item.objects.create(
    title='Lost Blue Backpack',
    description='Blue Nike backpack with laptop inside',
    item_type='lost',
    category='bags',
    location='Cafeteria',
    date_lost_found=date.today(),
    user=user,
    is_approved=True  # Auto-approve for testing
)

Item.objects.create(
    title='Lost Student ID Card',
    description='PUCIT student ID, name: Ali Ahmed',
    item_type='lost',
    category='documents',
    location='Library Entrance',
    date_lost_found=date.today(),
    user=user,
    is_approved=True
)

# Found items
Item.objects.create(
    title='Found Keys',
    description='Set of 3 keys with Honda keychain',
    item_type='found',
    category='keys',
    location='Parking Lot',
    date_lost_found=date.today(),
    user=user,
    is_approved=True,
    reward_offered=True,
    reward_amount=200
)

print("Sample items created!")
```

---

## 🎯 Success Criteria

Phase 2 is working correctly if:

- ✅ Verified users can post items
- ✅ Items require admin approval
- ✅ Approved items appear in public listing
- ✅ Search and filters work
- ✅ Image upload works
- ✅ Users can manage their items
- ✅ Status updates work
- ✅ Dashboard shows statistics
- ✅ Contact info visible to verified users only

---

## 📝 Next Steps

After testing Phase 2:

1. **Populate with real data**
   - Add more items
   - Test different categories
   - Upload various images

2. **Test edge cases**
   - Very long descriptions
   - Items without images
   - Multiple items per user

3. **Prepare for Phase 3**
   - Chat system planning
   - WebSocket setup
   - Real-time messaging

---

## 🆘 Need Help?

Check these files:
- `PHASE2_COMPLETE.md` - Full documentation
- `SETUP_GUIDE.md` - Setup instructions
- `README.md` - Project overview
- `context.md` - Project specifications

---

**Happy Testing! 🚀**

*Phase 2 is now ready for production use!*
