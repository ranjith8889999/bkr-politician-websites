# 🔴 CRITICAL: Database Getting Cleared on Every Deployment

## The Problem:

Your database is cleared after every deployment because:

1. **`.gitignore` excludes `*.db` files** - Database is NOT in Git
2. **EasyPanel ephemeral filesystem** - Files not in Git are deleted on redeploy
3. **start.sh creates new DB** if missing - So you get fresh sample data each time

---

## ✅ SOLUTION 1: Use Persistent Volume (RECOMMENDED)

### In EasyPanel:

1. **Go to your app settings**
2. **Add a Persistent Volume/Mount:**
   ```
   Mount Path: /app/backend/data
   Size: 1GB
   ```

3. **Update Environment Variable:**
   ```
   DATABASE_PATH=/app/backend/data/bkr_database.db
   ```

4. **Redeploy once** - Database will now persist across deployments

---

## ✅ SOLUTION 2: Use External Database (Production Best Practice)

### Option A: PostgreSQL/MySQL on EasyPanel

1. **Create a separate database service** in EasyPanel
2. **Update backend to use PostgreSQL** instead of SQLite
3. **Connection string in environment variables**

### Option B: Use Environment Variables for Data

Store critical data in environment variables (not ideal for large datasets)

---

## ✅ SOLUTION 3: Commit Database to Git (Quick Fix, NOT RECOMMENDED)

**Only for development/testing:**

```bash
# Remove *.db from .gitignore
# Then commit the database
git add backend/bkr_database.db
git commit -m "Add database file"
git push
```

⚠️ **Problems with this approach:**
- Database grows with every commit
- Merge conflicts when multiple people update
- Not suitable for production

---

## 📝 Implementation: Persistent Volume (BEST SOLUTION)

### Step 1: Update backend/app.py to use data directory

```python
# Check if DATABASE_PATH is set, otherwise use data directory
import os
DB_DIR = '/app/backend/data' if os.path.exists('/app/backend/data') else '.'
DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(DB_DIR, 'bkr_database.db'))
```

### Step 2: Update start.sh to create data directory

```bash
# Create data directory if it doesn't exist
mkdir -p data
cd data

# Check if database exists
if [ ! -f "bkr_database.db" ]; then
    echo "📦 Creating database..."
    cd ..
    python migrate_data.py --sample
    mv bkr_database.db data/
    cd data
fi

cd ..
```

### Step 3: Configure EasyPanel

**Mounts/Volumes:**
- Path: `/app/backend/data`
- Size: 1GB (adjust as needed)

**Environment Variables:**
```
DATABASE_PATH=/app/backend/data/bkr_database.db
```

---

## 🔍 Current Database Flow:

```
Deploy → start.sh runs → Check if bkr_database.db exists
   ↓                              ↓
   No database              Database missing (deleted on deploy)
   ↓                              ↓
Run migrate_data.py --sample  Creates fresh DB with 3 sample camps
   ↓
✅ App starts with new empty database each time
```

## ✅ With Persistent Volume:

```
Deploy → start.sh runs → Check if /app/backend/data/bkr_database.db exists
   ↓                              ↓
   Volume persists           Database EXISTS (in persistent volume)
   ↓                              ↓
Skip migration             Use existing database with all data
   ↓
✅ App starts with EXISTING database preserved
```

---

## 🚀 Quick Fix Implementation:

I'll update the code to support persistent volumes now.
