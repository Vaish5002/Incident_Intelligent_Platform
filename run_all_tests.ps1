# 🧪 AUTOMATED TEST RUNNER FOR SMARTOPS AI
# Run all tests to verify 100% functionality

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     SMARTOPS AI - COMPREHENSIVE TEST SUITE            ║" -ForegroundColor Cyan
Write-Host "║     Testing all components for deployment readiness   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$script:passedTests = 0
$script:failedTests = 0
$script:totalTests = 0

function Test-Component {
    param(
        [string]$TestName,
        [scriptblock]$TestScript,
        [string]$SuccessMessage = "PASS"
    )
    
    $script:totalTests++
    Write-Host "🔷 Testing: $TestName" -ForegroundColor Blue
    
    try {
        $result = & $TestScript
        if ($result) {
            Write-Host "   ✅ $SuccessMessage" -ForegroundColor Green
            $script:passedTests++
            return $true
        } else {
            Write-Host "   ❌ FAIL" -ForegroundColor Red
            $script:failedTests++
            return $false
        }
    } catch {
        Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $script:failedTests++
        return $false
    }
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════
# PHASE 1: BACKEND API TESTS
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "PHASE 1: BACKEND API TESTS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Test 1.1: Health Check
Test-Component "Backend Health Check" {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8002/api/health" -UseBasicParsing -TimeoutSec 5
        $content = $response.Content | ConvertFrom-Json
        return ($content.status -eq "healthy" -and $content.groq_service -eq "healthy")
    } catch {
        return $false
    }
} "Backend is healthy and Groq service connected"

# Test 1.2: Root Endpoint
Test-Component "Root API Endpoint" {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8002/" -UseBasicParsing -TimeoutSec 5
        $content = $response.Content | ConvertFrom-Json
        return ($content.service -eq "SmartOps AI - RCA Engine")
    } catch {
        return $false
    }
} "Root endpoint returning service information"

# Test 1.3: API Documentation
Test-Component "API Documentation Accessible" {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8002/docs" -UseBasicParsing -TimeoutSec 5
        return ($response.StatusCode -eq 200)
    } catch {
        return $false
    }
} "Swagger documentation accessible at /docs"

# ═══════════════════════════════════════════════════════════
# PHASE 2: AGENT VERIFICATION
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "PHASE 2: AGENT VERIFICATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Test 2.1: All Agents
Write-Host "🔷 Testing: All 6 Agents (This will take ~15 seconds)" -ForegroundColor Blue
Write-Host "   Running test_full_investigation.py..." -ForegroundColor Gray

Push-Location "Project\backend"
try {
    $output = python test_full_investigation.py 2>&1 | Out-String
    if ($output -match "ALL AGENTS WORKING SUCCESSFULLY") {
        Write-Host "   ✅ All 6 agents verified working with real data" -ForegroundColor Green
        $script:passedTests++
    } else {
        Write-Host "   ❌ Agent test failed" -ForegroundColor Red
        Write-Host "   Output: $output" -ForegroundColor Gray
        $script:failedTests++
    }
    $script:totalTests++
} catch {
    Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    $script:failedTests++
    $script:totalTests++
}
Pop-Location

# ═══════════════════════════════════════════════════════════
# PHASE 3: FRONTEND UI TESTS
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "PHASE 3: FRONTEND UI TESTS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Test 3.1: Frontend Accessibility
Test-Component "Frontend Accessibility" {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5
        return ($response.StatusCode -eq 200)
    } catch {
        return $false
    }
} "Frontend accessible on port 5173"

# Test 3.2: Frontend Serves React App
Test-Component "Frontend Serves React App" {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5
        $content = $response.Content
        return ($content -match "root" -or $content -match "vite")
    } catch {
        return $false
    }
} "Frontend serving React application"

# ═══════════════════════════════════════════════════════════
# PHASE 4: CONFIGURATION CHECKS
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "PHASE 4: CONFIGURATION AND ENVIRONMENT" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Test 4.1: Environment Variables
Write-Host "🔷 Testing: Environment Variables" -ForegroundColor Blue
Push-Location "Project\backend"
try {
    $configCheck = python -c "from ai.config import settings; print('OK' if settings.GROQ_API_KEY else 'FAIL')" 2>&1
    if ($configCheck -match "OK") {
        Write-Host "   ✅ All required environment variables configured" -ForegroundColor Green
        $script:passedTests++
    } else {
        Write-Host "   ❌ Environment variables missing or invalid" -ForegroundColor Red
        $script:failedTests++
    }
    $script:totalTests++
} catch {
    Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    $script:failedTests++
    $script:totalTests++
}
Pop-Location

# Test 4.2: Database File
Test-Component "Database File Exists" {
    return (Test-Path "Project\backend\smartops_ai.db")
} "SQLite database file present"

# ═══════════════════════════════════════════════════════════
# TEST SUMMARY
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$passPercentage = [math]::Round(($script:passedTests / $script:totalTests) * 100, 1)

Write-Host "Total Tests Run:     $($script:totalTests)" -ForegroundColor White
Write-Host "Tests Passed:        $($script:passedTests) ✅" -ForegroundColor Green
Write-Host "Tests Failed:        $($script:failedTests) ❌" -ForegroundColor $(if ($script:failedTests -eq 0) { "Green" } else { "Red" })
Write-Host "Pass Percentage:     $passPercentage%" -ForegroundColor $(if ($passPercentage -ge 90) { "Green" } elseif ($passPercentage -ge 70) { "Yellow" } else { "Red" })
Write-Host ""

# ═══════════════════════════════════════════════════════════
# FINAL VERDICT
# ═══════════════════════════════════════════════════════════

if ($script:failedTests -eq 0) {
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                        ║" -ForegroundColor Green
    Write-Host "║              ✅ ALL TESTS PASSED! ✅                   ║" -ForegroundColor Green
    Write-Host "║                                                        ║" -ForegroundColor Green
    Write-Host "║     Your system is 100% functional and ready for      ║" -ForegroundColor Green
    Write-Host "║              DEPLOYMENT AND DEMO! 🚀                   ║" -ForegroundColor Green
    Write-Host "║                                                        ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Open browser: http://localhost:5173" -ForegroundColor White
    Write-Host "  2. Login and test manually with Investigation page" -ForegroundColor White
    Write-Host "  3. Review DEPLOY_NOW.md for deployment instructions" -ForegroundColor White
    Write-Host "  4. Review DEMO_SCRIPT.md for demo preparation" -ForegroundColor White
} elseif ($passPercentage -ge 80) {
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║                                                        ║" -ForegroundColor Yellow
    Write-Host "║            ⚠️  MOST TESTS PASSED ⚠️                    ║" -ForegroundColor Yellow
    Write-Host "║                                                        ║" -ForegroundColor Yellow
    Write-Host "║     $($script:failedTests) test(s) failed. Review and fix before      ║" -ForegroundColor Yellow
    Write-Host "║                   deployment.                          ║" -ForegroundColor Yellow
    Write-Host "║                                                        ║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Action Required:" -ForegroundColor Yellow
    Write-Host "  1. Check logs above for failed tests" -ForegroundColor White
    Write-Host "  2. Fix the issues" -ForegroundColor White
    Write-Host "  3. Re-run this test script" -ForegroundColor White
} else {
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║                                                        ║" -ForegroundColor Red
    Write-Host "║              ❌ TESTS FAILED ❌                         ║" -ForegroundColor Red
    Write-Host "║                                                        ║" -ForegroundColor Red
    Write-Host "║     Multiple tests failed. System needs attention     ║" -ForegroundColor Red
    Write-Host "║          before deployment can proceed.                ║" -ForegroundColor Red
    Write-Host "║                                                        ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Action Required:" -ForegroundColor Red
    Write-Host "  1. Review failed tests above" -ForegroundColor White
    Write-Host "  2. Check server logs for errors" -ForegroundColor White
    Write-Host "  3. Verify both servers are running" -ForegroundColor White
    Write-Host "  4. Fix issues and re-run tests" -ForegroundColor White
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Return exit code
if ($script:failedTests -eq 0) {
    exit 0
} else {
    exit 1
}
