# ✅ Campus Connect - Testing Checklist

Use this checklist to verify all features are working correctly.

---

## 🔐 Phase 1: Authentication Testing

### **User Registration**
- [ ] Navigate to `/users/register/`
- [ ] Try registering with Gmail (@gmail.com) - Should fail
- [ ] Try registering with PUCIT email (@pucit.edu.pk) - Should succeed
- [ ] Verify success message appears
- [ ] Verify user is created with `is_verified=False`
- [ ] Check duplicate email validation

### **User Login**
- [ ] Navigate to `/users/login/`
- [ ] Login with unverified user - Should show warning
- [ ] Login with verified user - Should show success
- [ ] Check "Remember me" functionality
- [ ] Verify redirect to dashboard

### **User Profile**
- [ ] Navigate to `/users/profile/`
- [ ] Verify all user information displays
- [ ] Check verification status badge
- [ ] Verify statistics are correct

### **Admin Approval**
- [ ] Login to `/admin/`
- [ ] Navigate to Users
- [ ] Find unverified user
- [ ] Check `is_verified` checkbox
- [ ] Save and verify user is approved
- [ ] Test bulk approval action

---

## 📦 Phase 2: Items Module Testing

### **Browse Items (Public)**
- [ ] Navigate to `/items/` (without login)
- [ ] Verify only approved items show
- [ ] Test search functionality
- [ ] Test type filter (Lost/Found)
- [ ] Test category filter
- [ ] Test date range filter
- [ ] Check pagination works
- [ ] Verify empty state shows when no results

### **Item Detail (Public)**
- [ ] Click on any item
- [ ] Verify all details display
- [ ] Check image displays (or placeholder)
- [ ] Verify view counter increments
- [ ] Check related items section
- [ ] Verify contact info hidden for non-logged-in users

### **Item Detail (Logged In)**
- [ ] Login as verified user
- [ ] View item detail
- [ ] Verify contact information is visible
- [ ] Check "Contact Owner" button works

### **Post New Item**
- [ ] Login as verified user
- [ ] Navigate to `/items/create/`
- [ ] Fill all required fields
- [ ] Upload image (test with valid image)
- [ ] Try uploading >5MB image - Should fail
- [ ] Try uploading non-image file - Should fail
- [ ] Submit form
- [ ] Verify success message
- [ ] Check item is created with `is_approved=False`

### **My Items**
- [ ] Navigate to `/items/my-items/`
- [ ] Verify statistics cards show correct numbers
- [ ] Check items table displays all user's items
- [ ] Verify status indicators are correct
- [ ] Test "View" button (only for approved items)
- [ ] Test "Edit" button
- [ ] Test "Delete" button

### **Edit Item**
- [ ] Click edit on your item
- [ ] Modify some fields
- [ ] Upload new image
- [ ] Save changes
- [ ] Verify changes are saved
- [ ] Try editing another user's item - Should fail (404)

### **Delete Item**
- [ ] Click delete on your item
- [ ] Verify confirmation dialog shows
- [ ] Cancel deletion
- [ ] Try again and confirm deletion
- [ ] Verify item is deleted

### **Update Item Status**
- [ ] Navigate to status update page
- [ ] Change status to "Claimed"
- [ ] Save and verify status updated
- [ ] Try other statuses (Returned, Closed)

### **Admin Item Approval**
- [ ] Login to admin panel
- [ ] Navigate to Items
- [ ] Find pending item
- [ ] Check `is_approved` checkbox
- [ ] Save and verify item is now public
- [ ] Test bulk approval action
- [ ] Test "Mark as Claimed" bulk action

### **Search & Filter**
- [ ] Test keyword search with various terms
- [ ] Filter by "Lost" items only
- [ ] Filter by "Found" items only
- [ ] Filter by specific category
- [ ] Combine multiple filters
- [ ] Test date range filtering

---

## 🎨 UI/UX Testing

### **Navigation**
- [ ] Verify logo links to home
- [ ] Check all navigation links work
- [ ] Verify "My Items" only shows for verified users
- [ ] Check user info dropdown displays correctly
- [ ] Test logout functionality

### **Dashboard**
- [ ] Verify statistics cards show correct data
- [ ] Check recent items feed displays
- [ ] Verify quick action buttons work
- [ ] Test locked state for unverified users

### **Responsive Design**
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768px)
- [ ] Test on mobile (375px)
- [ ] Verify navigation collapses properly
- [ ] Check images scale correctly

### **Messages/Alerts**
- [ ] Verify success messages appear (green)
- [ ] Verify error messages appear (red)
- [ ] Verify warning messages appear (yellow)
- [ ] Check messages auto-dismiss after 5 seconds

---

## 🔒 Security Testing

### **Access Control**
- [ ] Try accessing `/items/create/` without login - Should redirect
- [ ] Try accessing `/items/create/` as unverified user - Should redirect
- [ ] Try editing another user's item - Should fail (404)
- [ ] Try deleting another user's item - Should fail (404)
- [ ] Verify admin panel requires admin login

### **Email Validation**
- [ ] Try registering with @gmail.com - Should fail
- [ ] Try registering with @yahoo.com - Should fail
- [ ] Try registering with @pu.edu.pk - Should fail
- [ ] Try registering with @PUCIT.EDU.PK (uppercase) - Should work
- [ ] Try duplicate email - Should fail

### **Image Upload**
- [ ] Try uploading 10MB image - Should fail
- [ ] Try uploading .exe file - Should fail
- [ ] Try uploading .pdf file - Should fail
- [ ] Upload valid JPG - Should work
- [ ] Upload valid PNG - Should work

### **Form Validation**
- [ ] Submit empty form - Should show errors
- [ ] Submit with missing required fields - Should show errors
- [ ] Test password strength validation
- [ ] Test email format validation

---

## 📊 Data Integrity Testing

### **User Data**
- [ ] Create user and verify in database
- [ ] Update user and verify changes saved
- [ ] Delete user and verify cascade deletes

### **Item Data**
- [ ] Create item and verify in database
- [ ] Update item and verify changes saved
- [ ] Delete item and verify image file deleted
- [ ] Verify view counter increments correctly

### **Relationships**
- [ ] Verify items link to correct users
- [ ] Delete user and verify their items are deleted
- [ ] Verify related items query works

---

## 🧪 Edge Cases

### **Long Content**
- [ ] Post item with very long title (200 chars)
- [ ] Post item with very long description (5000 chars)
- [ ] Verify truncation works in list view

### **Special Characters**
- [ ] Use special characters in title
- [ ] Use emojis in description
- [ ] Use quotes and apostrophes

### **Empty States**
- [ ] View items list with no items
- [ ] View dashboard with no items
- [ ] View "My Items" with no items
- [ ] Check empty search results

### **Concurrent Actions**
- [ ] Have two users edit same item
- [ ] Have admin approve while user edits
- [ ] Test simultaneous item creation

---

## 🚀 Performance Testing

### **Page Load Times**
- [ ] Home page loads in <2 seconds
- [ ] Items list loads in <3 seconds
- [ ] Item detail loads in <2 seconds
- [ ] Dashboard loads in <2 seconds

### **Image Loading**
- [ ] Images load progressively
- [ ] Placeholder shows while loading
- [ ] Large images are optimized

### **Database Queries**
- [ ] Check query count on items list
- [ ] Verify select_related is used
- [ ] Test pagination performance

---

## 📱 Browser Compatibility

### **Desktop Browsers**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (latest)

### **Mobile Browsers**
- [ ] Chrome Mobile
- [ ] Safari Mobile
- [ ] Samsung Internet

---

## ✅ Final Checks

### **Documentation**
- [ ] README.md is up to date
- [ ] All setup guides are accurate
- [ ] Code comments are clear
- [ ] API documentation exists

### **Code Quality**
- [ ] No console errors in browser
- [ ] No Python errors in terminal
- [ ] All migrations applied
- [ ] No unused imports

### **Deployment Prep**
- [ ] .env.example is complete
- [ ] .gitignore includes sensitive files
- [ ] Requirements.txt is up to date
- [ ] Static files collected

---

## 📝 Test Results

**Date Tested:** _______________  
**Tested By:** _______________  
**Total Tests:** 150+  
**Passed:** _____  
**Failed:** _____  
**Notes:**

---

## 🐛 Bug Report Template

If you find bugs, document them here:

**Bug #:** ___  
**Severity:** Critical / High / Medium / Low  
**Description:**  
**Steps to Reproduce:**  
1. 
2. 
3. 

**Expected Result:**  
**Actual Result:**  
**Screenshots:**  
**Browser/Device:**  

---

**Testing Status:** ⏳ In Progress / ✅ Complete

*Use this checklist systematically to ensure all features work correctly before moving to Phase 3.*
