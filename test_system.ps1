# SmartOps AI - Quick Test Script
# Tests essential components for deployment readiness

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host " SMARTOPS AI - SYSTEM TEST SUITE" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""

$passed = 0
$failed = 0

# Test 1: Backend Health
Write-Host "[1/6] Testing Backend Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8002/api/health" -UseBasicParsing -TimeoutSec 5
    $content = $response.Content | ConvertFrom-Json
    if ($content.status -eq "healthy") {
        Write-Host "      PASS - Backend is healthy" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "      FAIL - Backend unhealthy" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "      FAIL - Cannot connect to backend" -ForegroundColor Red
    $failed++
}

# Test 2: API Documentation
Write-Host "[2/6] Testing API Documentation..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8002/docs" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "      PASS - API docs accessible" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "      FAIL - API docs not accessible" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "      FAIL - Cannot access API docs" -ForegroundColor Red
    $failed++
}

# Test 3: Frontend Accessibility
Write-Host "[3/6] Testing Frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "      PASS - Frontend is accessible" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "      FAIL - Frontend not accessible" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "      FAIL - Cannot connect to frontend" -ForegroundColor Red
    $failed++
}

# Test 4: Environment Configuration
Write-Host "[4/6] Testing Configuration..." -ForegroundColor Yellow
Push-Location "Project\backend"
try {
    $configCheck = python -c "from ai.config import settings; print('OK' if settings.GROQ_API_KEY else 'FAIL')" 2>&1
    if ($configCheck -match "OK") {
        Write-Host "      PASS - Configuration valid" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "      FAIL - Configuration invalid" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "      FAIL - Cannot check configuration" -ForegroundColor Red
    $failed++
}
Pop-Location

# Test 5: Database File
Write-Host "[5/6] Testing Database..." -ForegroundColor Yellow
if (Test-Path "Project\backend\smartops_ai.db") {
    Write-Host "      PASS - Database file exists" -ForegroundColor Green
    $passed++
} else {
    Write-Host "      FAIL - Database file missing" -ForegroundColor Red
    $failed++
}

# Test 6: All Agents
Write-Host "[6/6] Testing All Agents (this takes ~15 seconds)..." -ForegroundColor Yellow
Push-Location "Project\backend"
try {
    $output = python test_full_investigation.py 2>&1 | Out-String
    if ($output -match "ALL AGENTS WORKING SUCCESSFULLY") {
        Write-Host "      PASS - All 6 agents working" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "      FAIL - Agent test failed" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "      FAIL - Cannot run agent test" -ForegroundColor Red
    $failed++
}
Pop-Location

# Summary
Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host " TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests Passed: $passed/6" -ForegroundColor $(if ($passed -eq 6) { "Green" } else { "Yellow" })
Write-Host "Tests Failed: $failed/6" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host ""

# Final verdict
if ($failed -eq 0) {
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host " SUCCESS - ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host " System is 100% functional and ready for deployment" -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Open browser: http://localhost:5173" -ForegroundColor White
    Write-Host "  2. Test manually with an investigation" -ForegroundColor White
    Write-Host "  3. Review DEPLOY_NOW.md for deployment" -ForegroundColor White
    exit 0
} else {
    Write-Host "=========================================================" -ForegroundColor Red
    Write-Host " TESTS FAILED - $failed issue(s) found" -ForegroundColor Red
    Write-Host "=========================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Action Required:" -ForegroundColor Yellow
    Write-Host "  1. Check failed tests above" -ForegroundColor White
    Write-Host "  2. Verify both servers are running" -ForegroundColor White
    Write-Host "  3. Check logs for errors" -ForegroundColor White
    Write-Host "  4. Fix issues and re-run tests" -ForegroundColor White
    exit 1
}
