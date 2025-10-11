# Campus Connect - Quick Setup Script
# Run this script to set up the project automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Campus Connect - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if virtual environment exists
Write-Host "Step 1: Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 2: Activate virtual environment and install dependencies
Write-Host "Step 2: Installing dependencies..." -ForegroundColor Yellow
Write-Host "Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"
Write-Host "Installing packages from requirements.txt..." -ForegroundColor Gray
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 3: Run migrations
Write-Host "Step 3: Setting up database..." -ForegroundColor Yellow
Write-Host "Creating migrations..." -ForegroundColor Gray
python manage.py makemigrations
Write-Host "Applying migrations..." -ForegroundColor Gray
python manage.py migrate
Write-Host "✓ Database setup complete" -ForegroundColor Green
Write-Host ""

# Step 4: Create superuser
Write-Host "Step 4: Create admin account..." -ForegroundColor Yellow
Write-Host "Please enter admin credentials:" -ForegroundColor Gray
python manage.py createsuperuser
Write-Host ""

# Step 5: Collect static files
Write-Host "Step 5: Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "✓ Static files collected" -ForegroundColor Green
Write-Host ""

# Final message
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then visit:" -ForegroundColor Yellow
Write-Host "  Home: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
