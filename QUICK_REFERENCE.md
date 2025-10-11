# 🚀 Campus Connect - Quick Reference Card

**Last Updated:** October 11, 2025, 23:14 PKT

---

## 🎯 Quick Start Commands

### **Start Development Server**
```powershell
cd "C:\Users\User\Desktop\Campus Connect"
venv\Scripts\python.exe manage.py runserver
```
**URL:** http://127.0.0.1:8000/

### **Run Tests**
```powershell
# All tests
python manage.py test

# Items tests only
python manage.py test items

# Verbose output
python manage.py test items -v 2
```

### **Database Commands**
```powershell
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

---

## 🌐 Important URLs

| Page | URL | Access Level |
|------|-----|--------------|
| **Home** | `/` | Public |
| **Register** | `/users/register/` | Public |
| **Login** | `/users/login/` | Public |
| **Dashboard** | `/users/dashboard/` | Authenticated |
| **Profile** | `/users/profile/` | Authenticated |
| **Browse Items** | `/items/` | Public |
| **Lost Items** | `/items/lost/` | Public |
| **Found Items** | `/items/found/` | Public |
| **Post Item** | `/items/create/` | Verified Users |
| **My Items** | `/items/my-items/` | Verified Users |
| **Admin Panel** | `/admin/` | Admin Only |

---

## 👤 User Roles & Permissions

### **Unverified User** (is_verified=False)
- ✅ Can login
- ✅ Can view dashboard
- ✅ Can view profile
- ✅ Can browse items
- ❌ Cannot post items
- ❌ Cannot see contact info

### **Verified User** (is_verified=True)
- ✅ All unverified permissions
- ✅ Can post items
- ✅ Can edit/delete own items
- ✅ Can see contact information
- ✅ Can manage item status

### **Admin/Superuser**
- ✅ All verified permissions
- ✅ Can approve users
- ✅ Can approve items
- ✅ Can edit any item
- ✅ Can delete any item
- ✅ Full admin panel access

---

## 📝 Quick Workflows

### **Register New User**
1. Go to `/users/register/`
2. Use @pucit.edu.pk email
3. Fill all fields
4. Submit → Account created (unverified)

### **Verify User (Admin)**
1. Login to `/admin/`
2. Users → Find user
3. Check `is_verified`
4. Save

### **Post Item**
1. Login as verified user
2. Go to `/items/create/`
3. Fill form + upload image
4. Submit → Item pending approval

### **Approve Item (Admin)**
1. Login to `/admin/`
2. Items → Find item
3. Check `is_approved`
4. Save → Item now public

### **Search Items**
1. Go to `/items/`
2. Use search box
3. Apply filters
4. Click item to view

---

## 🎨 Item Categories

1. **Electronics** - Phones, laptops, chargers
2. **Documents** - IDs, certificates, papers
3. **Books** - Textbooks, notebooks
4. **Bags** - Backpacks, purses
5. **Keys** - All types of keys
6. **Clothing** - Jackets, scarves, etc.
7. **Accessories** - Watches, jewelry
8. **Sports** - Sports equipment
9. **Other** - Everything else

---

## 🔄 Item Status Types

- **Active** - Still lost/found, visible
- **Claimed** - Someone claimed it
- **Returned** - Returned to owner
- **Closed** - Case closed, hidden

---

## 🛠️ Common Tasks

### **Create Sample Item (Shell)**
```python
python manage.py shell

from items.models import Item
from users.models import User
from datetime import date

user = User.objects.get(username='youruser')

Item.objects.create(
    title='Lost iPhone',
    description='Black iPhone 13 Pro',
    item_type='lost',
    category='electronics',
    location='Library',
    date_lost_found=date.today(),
    user=user,
    is_approved=True  # Auto-approve for testing
)
```

### **Verify User (Shell)**
```python
python manage.py shell

from users.models import User

user = User.objects.get(username='youruser')
user.is_verified = True
user.save()
print(f"{user.username} is now verified!")
```

### **Check Statistics (Shell)**
```python
python manage.py shell

from items.models import Item
from users.models import User

print(f"Total Users: {User.objects.count()}")
print(f"Verified Users: {User.objects.filter(is_verified=True).count()}")
print(f"Total Items: {Item.objects.count()}")
print(f"Approved Items: {Item.objects.filter(is_approved=True).count()}")
print(f"Lost Items: {Item.objects.filter(item_type='lost').count()}")
print(f"Found Items: {Item.objects.filter(item_type='found').count()}")
```

---

## 🐛 Troubleshooting

### **Server won't start**
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F

# Try different port
python manage.py runserver 8080
```

### **Can't post items**
- Check user is verified: `user.is_verified = True`
- Check user is logged in
- Check form validation errors

### **Items not showing**
- Check item is approved: `item.is_approved = True`
- Check item status is 'active'
- Clear browser cache

### **Image upload fails**
- Check file size < 5MB
- Check file format (JPG, PNG, GIF, WebP)
- Check media folder permissions

### **Database errors**
```powershell
# Reset database (WARNING: Deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📊 File Locations

### **Important Files**
- **Settings:** `campus_connect/settings.py`
- **Main URLs:** `campus_connect/urls.py`
- **User Models:** `users/models.py`
- **Item Models:** `items/models.py`
- **Database:** `db.sqlite3`
- **Environment:** `.env`

### **Templates**
- **Base:** `templates/base.html`
- **Home:** `templates/home.html`
- **Users:** `templates/users/`
- **Items:** `templates/items/`

### **Media Files**
- **Uploaded Images:** `media/items/`

---

## 🔐 Security Checklist

- [x] CSRF protection enabled
- [x] Password hashing enabled
- [x] Email validation (@pucit.edu.pk)
- [x] User verification required
- [x] Image validation (size, format)
- [x] Permission-based access
- [ ] HTTPS/SSL (production)
- [ ] Rate limiting (production)
- [ ] Email verification (future)

---

## 📚 Documentation Files

1. **README.md** - Project overview
2. **SETUP_GUIDE.md** - Detailed setup
3. **QUICK_START.md** - Quick start
4. **PHASE2_COMPLETE.md** - Phase 2 docs
5. **PHASE2_QUICKSTART.md** - Phase 2 testing
6. **PROJECT_SUMMARY.md** - Overall status
7. **TESTING_CHECKLIST.md** - Testing guide
8. **QUICK_REFERENCE.md** - This file

---

## 🎯 Testing Checklist (Quick)

- [ ] Register with PUCIT email
- [ ] Login successfully
- [ ] View dashboard
- [ ] Browse items
- [ ] Post new item (verified user)
- [ ] Approve item (admin)
- [ ] Search items
- [ ] Edit own item
- [ ] Update item status
- [ ] Delete item

---

## 💡 Pro Tips

1. **Use Django Shell** for quick database operations
2. **Check Admin Panel** for easy data management
3. **Read Error Messages** carefully - they're helpful
4. **Use Browser DevTools** to debug frontend issues
5. **Check Terminal Output** for backend errors
6. **Test with Multiple Users** to verify permissions
7. **Use Sample Data** for realistic testing
8. **Keep Documentation Updated** as you add features

---

## 🚀 Next Phase Preview

### **Phase 3: Real-Time Chat**
- Django Channels
- WebSocket connections
- Real-time messaging
- Chat history
- Online status

**Estimated Time:** 2-3 weeks

---

## 📞 Quick Help

**Issue?** Check in this order:
1. Terminal for errors
2. Browser console for JS errors
3. Django admin for data issues
4. Documentation files
5. Test with different user roles

---

## ✅ Current Status

**Phase 1:** ✅ Complete (Authentication)  
**Phase 2:** ✅ Complete (Items Module)  
**Phase 3:** 🔄 Pending (Chat System)  
**Tests Passing:** ✅ 12/12 (100%)  
**Server Status:** 🟢 Running

---

**Last Test Run:** October 11, 2025, 23:14 PKT  
**Result:** ✅ All tests passed  
**Ready for:** Production testing & Phase 3 planning

---

*Keep this file handy for quick reference during development!*
