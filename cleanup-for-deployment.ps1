# ================================================
# SmartOps AI - Deployment Cleanup Script
# ================================================
# This script removes test files, cache, and development artifacts
# to prepare the project for production deployment.
# ================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   SmartOps AI - Deployment Cleanup Script                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot
$backendPath = Join-Path $rootPath "Project\backend"
$frontendPath = Join-Path $rootPath "Project\frontend"

$filesRemoved = 0
$dirsRemoved = 0
$errors = 0

# ================================================
# BACKEND CLEANUP
# ================================================
Write-Host "🔧 BACKEND CLEANUP" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Test files to remove
$backendTestFiles = @(
    "demo_database.py",
    "quick_test.py",
    "show_database.py",
    "test_api_endpoints.py",
    "test_api_key.py",
    "test_full_investigation.py",
    "test_github_commit_display.py",
    "test_groq.py",
    "test_module3_4.py",
    "test_module5_6.py",
    "test_module7_8.py",
    "test_module9.py",
    "test_module10.py",
    "test_module11_e2e.py",
    "verify_modules.py"
)

Write-Host "  → Removing test files..." -ForegroundColor Gray
foreach ($file in $backendTestFiles) {
    $filePath = Join-Path $backendPath $file
    if (Test-Path $filePath) {
        try {
            Remove-Item -Path $filePath -Force
            Write-Host "    ✓ Removed: $file" -ForegroundColor Green
            $filesRemoved++
        } catch {
            Write-Host "    ✗ Failed to remove: $file" -ForegroundColor Red
            $errors++
        }
    }
}

# Cache directories to remove
$backendCacheDirs = @(
    "__pycache__",
    "agents\__pycache__",
    "ai\__pycache__",
    "api\__pycache__",
    "database\__pycache__",
    "schemas\__pycache__",
    "test_output"
)

Write-Host ""
Write-Host "  → Removing cache directories..." -ForegroundColor Gray
foreach ($dir in $backendCacheDirs) {
    $dirPath = Join-Path $backendPath $dir
    if (Test-Path $dirPath) {
        try {
            Remove-Item -Path $dirPath -Recurse -Force
            Write-Host "    ✓ Removed: $dir" -ForegroundColor Green
            $dirsRemoved++
        } catch {
            Write-Host "    ✗ Failed to remove: $dir" -ForegroundColor Red
            $errors++
        }
    }
}

# Development database
Write-Host ""
Write-Host "  → Removing development database..." -ForegroundColor Gray
$dbPath = Join-Path $backendPath "smartops_ai.db"
if (Test-Path $dbPath) {
    try {
        Remove-Item -Path $dbPath -Force
        Write-Host "    ✓ Removed: smartops_ai.db" -ForegroundColor Green
        $filesRemoved++
    } catch {
        Write-Host "    ✗ Failed to remove: smartops_ai.db" -ForegroundColor Red
        $errors++
    }
}

# Optional: Remove unused routes
Write-Host ""
Write-Host "  → Checking for unused routes (optional)..." -ForegroundColor Gray
$unusedRoutes = @(
    "api\demo_investigate_routes.py",
    "api\simple_investigation_routes.py"
)
foreach ($route in $unusedRoutes) {
    $routePath = Join-Path $backendPath $route
    if (Test-Path $routePath) {
        $response = Read-Host "    Remove $route? (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            try {
                Remove-Item -Path $routePath -Force
                Write-Host "    ✓ Removed: $route" -ForegroundColor Green
                $filesRemoved++
            } catch {
                Write-Host "    ✗ Failed to remove: $route" -ForegroundColor Red
                $errors++
            }
        } else {
            Write-Host "    ○ Kept: $route" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "✅ Backend cleanup complete!" -ForegroundColor Green
Write-Host ""

# ================================================
# FRONTEND CLEANUP
# ================================================
Write-Host "🎨 FRONTEND CLEANUP" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Test directory
Write-Host "  → Removing test files..." -ForegroundColor Gray
$testDir = Join-Path $frontendPath "tests"
if (Test-Path $testDir) {
    try {
        Remove-Item -Path $testDir -Recurse -Force
        Write-Host "    ✓ Removed: tests/" -ForegroundColor Green
        $dirsRemoved++
    } catch {
        Write-Host "    ✗ Failed to remove: tests/" -ForegroundColor Red
        $errors++
    }
}

$vitestConfig = Join-Path $frontendPath "vitest.config.js"
if (Test-Path $vitestConfig) {
    try {
        Remove-Item -Path $vitestConfig -Force
        Write-Host "    ✓ Removed: vitest.config.js" -ForegroundColor Green
        $filesRemoved++
    } catch {
        Write-Host "    ✗ Failed to remove: vitest.config.js" -ForegroundColor Red
        $errors++
    }
}

# Build artifacts
Write-Host ""
Write-Host "  → Removing build artifacts..." -ForegroundColor Gray
$frontendBuildDirs = @(
    "dist",
    "node_modules"
)
foreach ($dir in $frontendBuildDirs) {
    $dirPath = Join-Path $frontendPath $dir
    if (Test-Path $dirPath) {
        $response = Read-Host "    Remove $dir? (will be regenerated) (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            try {
                Write-Host "    ⏳ Removing $dir (this may take a moment)..." -ForegroundColor Gray
                Remove-Item -Path $dirPath -Recurse -Force
                Write-Host "    ✓ Removed: $dir" -ForegroundColor Green
                $dirsRemoved++
            } catch {
                Write-Host "    ✗ Failed to remove: $dir" -ForegroundColor Red
                $errors++
            }
        } else {
            Write-Host "    ○ Kept: $dir" -ForegroundColor Yellow
        }
    }
}

# .env file (keep .env.example)
Write-Host ""
Write-Host "  → Checking .env file..." -ForegroundColor Gray
$envFile = Join-Path $frontendPath ".env"
if (Test-Path $envFile) {
    $response = Read-Host "    Remove .env? (keep .env.example) (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        try {
            Remove-Item -Path $envFile -Force
            Write-Host "    ✓ Removed: .env" -ForegroundColor Green
            $filesRemoved++
        } catch {
            Write-Host "    ✗ Failed to remove: .env" -ForegroundColor Red
            $errors++
        }
    } else {
        Write-Host "    ○ Kept: .env" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Frontend cleanup complete!" -ForegroundColor Green
Write-Host ""

# ================================================
# ROOT CLEANUP (Optional)
# ================================================
Write-Host "📄 ROOT DOCUMENTATION CLEANUP (Optional)" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

$optionalDocs = @(
    "COMPLETE_TEST_CASES.md",
    "COMPREHENSIVE_TESTING_PLAN.md",
    "DATABASE_DEMO_CHEATSHEET.md",
    "HOW_TO_DEMO_DATABASE.md",
    "LIVE_DEMO_TESTING_GUIDE.md",
    "PROGRESS_TRACKER_FIX_SUMMARY.md",
    "GITHUB_COMMIT_DISPLAY_FIX.md",
    "COMMIT_DISPLAY_FIX_SUMMARY.md",
    "CODE_SNIPPET_DISPLAY_ENHANCEMENT.md",
    "VISUAL_DEMO_CODE_DISPLAY.md"
)

Write-Host "  The following documentation files are for testing/development:" -ForegroundColor Gray
Write-Host "  You may want to keep them for reference or remove to reduce clutter." -ForegroundColor Gray
Write-Host ""

$response = Read-Host "  Remove verbose testing/development documentation? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    foreach ($doc in $optionalDocs) {
        $docPath = Join-Path $rootPath $doc
        if (Test-Path $docPath) {
            try {
                Remove-Item -Path $docPath -Force
                Write-Host "    ✓ Removed: $doc" -ForegroundColor Green
                $filesRemoved++
            } catch {
                Write-Host "    ✗ Failed to remove: $doc" -ForegroundColor Red
                $errors++
            }
        }
    }
} else {
    Write-Host "    ○ Kept all documentation files" -ForegroundColor Yellow
}

# ================================================
# SUMMARY
# ================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   CLEANUP SUMMARY                                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Files removed:       $filesRemoved" -ForegroundColor Green
Write-Host "  Directories removed: $dirsRemoved" -ForegroundColor Green
Write-Host "  Errors:              $errors" -ForegroundColor $(if ($errors -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($errors -eq 0) {
    Write-Host "🎉 SUCCESS! Project is clean and ready for deployment." -ForegroundColor Green
} else {
    Write-Host "⚠️  Cleanup completed with $errors error(s). Please review." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review remaining files in Project/backend and Project/frontend" -ForegroundColor White
Write-Host "  2. Update .env.example files with required variables" -ForegroundColor White
Write-Host "  3. Test locally before deploying:" -ForegroundColor White
Write-Host "     Backend:  cd Project/backend && python run_server.py" -ForegroundColor Gray
Write-Host "     Frontend: cd Project/frontend && npm run build && npm run preview" -ForegroundColor Gray
Write-Host "  4. Deploy to your chosen platform (Render, Vercel, Docker, etc.)" -ForegroundColor White
Write-Host ""
Write-Host "📚 See DEPLOYMENT_CLEANUP.md for detailed deployment instructions." -ForegroundColor Cyan
Write-Host ""

# ================================================
# VERIFICATION
# ================================================
Write-Host "🔍 VERIFICATION" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

Write-Host "Essential files check:" -ForegroundColor Gray
$essentialFiles = @{
    "Backend main.py" = (Join-Path $backendPath "main.py")
    "Backend requirements.txt" = (Join-Path $backendPath "requirements.txt")
    "Backend .env.example" = (Join-Path $backendPath ".env.example")
    "Frontend package.json" = (Join-Path $frontendPath "package.json")
    "Frontend index.html" = (Join-Path $frontendPath "index.html")
    "Frontend .env.example" = (Join-Path $frontendPath ".env.example")
}

$allEssentialPresent = $true
foreach ($file in $essentialFiles.GetEnumerator()) {
    if (Test-Path $file.Value) {
        Write-Host "  ✓ $($file.Key)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $($file.Key) - MISSING!" -ForegroundColor Red
        $allEssentialPresent = $false
    }
}

Write-Host ""
if ($allEssentialPresent) {
    Write-Host "✅ All essential files present!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some essential files are missing. Please check!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
