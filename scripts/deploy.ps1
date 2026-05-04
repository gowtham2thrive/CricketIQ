# Deployment script for CricketIQ
# Requires Google Cloud SDK (gcloud) to be installed and authenticated

Write-Host "Deploying CricketIQ to Google Cloud Run..." -ForegroundColor Cyan

# Deploy to Cloud Run
gcloud run deploy cricketiq --source . --region asia-south1 --allow-unauthenticated

Write-Host "`nSetting environment variables..." -ForegroundColor Cyan

# Note: Replace 'your_api_key_here' with your actual Gemini API key
# Example: .\deploy.ps1 -ApiKey "AIzaSy..."
param(
    [string]$ApiKey = "your_api_key_here"
)

if ($ApiKey -eq "your_api_key_here") {
    Write-Host "WARNING: You did not provide a valid API key. The agent features will not work until you set the GEMINI_API_KEY environment variable in Cloud Run." -ForegroundColor Yellow
    Write-Host "To set it later, run: gcloud run services update cricketiq --update-env-vars GEMINI_API_KEY=your_real_key"
} else {
    gcloud run services update cricketiq --update-env-vars GEMINI_API_KEY=$ApiKey
    Write-Host "API key successfully configured!" -ForegroundColor Green
}

Write-Host "`nDeployment Complete!" -ForegroundColor Green
