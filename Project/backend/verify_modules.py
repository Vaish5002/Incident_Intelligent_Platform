"""
Module Verification Script
Checks Module 1 & Module 2 completion status
"""
import os
import sys
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} missing: {filepath}")
        return False

def check_file_content(filepath, required_items, description):
    """Check if file contains required content"""
    if not Path(filepath).exists():
        print_error(f"{description} file not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for item in required_items:
        if item not in content:
            missing.append(item)
    
    if not missing:
        print_success(f"{description}: All required items present")
        return True
    else:
        print_error(f"{description}: Missing items: {', '.join(missing)}")
        return False

def verify_module_1():
    """Verify Module 1: Groq Integration"""
    print_header("Module 1: Groq Integration")
    
    results = []
    
    # Check groq_service.py
    print(f"\n{BOLD}1. Checking groq_service.py{RESET}")
    results.append(check_file_exists("ai/groq_service.py", "Service file"))
    
    if Path("ai/groq_service.py").exists():
        required_classes = [
            "class GroqService",
            "def generate_rca",
            "def generate_quick_rca",
            "def generate_recommendations",
            "def analyze_similar_incidents",
            "def generate_prevention_strategy"
        ]
        results.append(check_file_content(
            "ai/groq_service.py",
            required_classes,
            "Required methods"
        ))
    
    # Check config.py
    print(f"\n{BOLD}2. Checking config.py{RESET}")
    results.append(check_file_exists("ai/config.py", "Config file"))
    
    if Path("ai/config.py").exists():
        required_config = [
            "GROQ_API_KEY",
            "GROQ_MODEL",
            "TEMPERATURE",
            "MAX_TOKENS"
        ]
        results.append(check_file_content(
            "ai/config.py",
            required_config,
            "Required config items"
        ))
    
    # Check API routes
    print(f"\n{BOLD}3. Checking rca_routes.py{RESET}")
    results.append(check_file_exists("api/rca_routes.py", "Routes file"))
    
    if Path("api/rca_routes.py").exists():
        required_endpoints = [
            "@router.post(\"/generate-rca\"",
            "@router.post(\"/quick-rca\"",
            "@router.post(\"/recommendations\"",
            "@router.get(\"/health\""
        ]
        results.append(check_file_content(
            "api/rca_routes.py",
            required_endpoints,
            "Required endpoints"
        ))
    
    # Check schemas
    print(f"\n{BOLD}4. Checking schemas/rca.py{RESET}")
    results.append(check_file_exists("schemas/rca.py", "Schemas file"))
    
    if Path("schemas/rca.py").exists():
        required_schemas = [
            "class RCARequest",
            "class RCAResponse",
            "class QuickRCARequest",
            "class RecommendationRequest"
        ]
        results.append(check_file_content(
            "schemas/rca.py",
            required_schemas,
            "Required schemas"
        ))
    
    # Check main.py
    print(f"\n{BOLD}5. Checking main.py{RESET}")
    results.append(check_file_exists("main.py", "Main app file"))
    
    # Check test file
    print(f"\n{BOLD}6. Checking test_groq.py{RESET}")
    results.append(check_file_exists("test_groq.py", "Test file"))
    
    # Check requirements.txt
    print(f"\n{BOLD}7. Checking requirements.txt{RESET}")
    results.append(check_file_exists("requirements.txt", "Requirements file"))
    
    if Path("requirements.txt").exists():
        required_deps = [
            "fastapi",
            "groq",
            "pydantic",
            "uvicorn"
        ]
        results.append(check_file_content(
            "requirements.txt",
            required_deps,
            "Required dependencies"
        ))
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n{BOLD}Module 1 Summary:{RESET}")
    if passed == total:
        print_success(f"All checks passed ({passed}/{total})")
        print_success("Module 1: Groq Integration is COMPLETE ✅")
        return True
    else:
        print_warning(f"Some checks failed ({passed}/{total})")
        return False

def verify_module_2():
    """Verify Module 2: RCA Prompt Engineering"""
    print_header("Module 2: RCA Prompt Engineering")
    
    results = []
    
    # Check prompts.py
    print(f"\n{BOLD}1. Checking prompts.py{RESET}")
    results.append(check_file_exists("ai/prompts.py", "Prompts file"))
    
    if Path("ai/prompts.py").exists():
        required_prompts = [
            "RCA_GENERATION_PROMPT",
            "QUICK_RCA_PROMPT",
            "RECOMMENDATION_PROMPT",
            "SIMILAR_INCIDENT_ANALYSIS_PROMPT",
            "PREVENTION_STRATEGY_PROMPT"
        ]
        results.append(check_file_content(
            "ai/prompts.py",
            required_prompts,
            "Required prompt templates"
        ))
        
        # Check RCA format sections
        print(f"\n{BOLD}2. Checking RCA format structure{RESET}")
        required_sections = [
            "Executive Summary",
            "Root Cause",
            "Contributing Factors",
            "Impact Assessment",
            "Timeline Narrative",
            "Immediate Actions",
            "Recommendations",
            "Prevention Measures",
            "Lessons Learned"
        ]
        results.append(check_file_content(
            "ai/prompts.py",
            required_sections,
            "Required RCA sections"
        ))
        
        # Check helper functions
        print(f"\n{BOLD}3. Checking helper functions{RESET}")
        required_helpers = [
            "def build_rca_prompt",
            "def build_quick_rca_prompt"
        ]
        results.append(check_file_content(
            "ai/prompts.py",
            required_helpers,
            "Required helper functions"
        ))
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n{BOLD}Module 2 Summary:{RESET}")
    if passed == total:
        print_success(f"All checks passed ({passed}/{total})")
        print_success("Module 2: RCA Prompt Engineering is COMPLETE ✅")
        return True
    else:
        print_warning(f"Some checks failed ({passed}/{total})")
        return False

def check_environment():
    """Check environment setup"""
    print_header("Environment Setup Check")
    
    results = []
    
    print(f"\n{BOLD}1. Checking .env configuration{RESET}")
    if Path(".env").exists():
        print_success(".env file exists")
        results.append(True)
        
        # Check if API key is set
        with open(".env", 'r') as f:
            content = f.read()
            if "GROQ_API_KEY" in content and "your_groq_api_key_here" not in content:
                print_success("GROQ_API_KEY appears to be configured")
                results.append(True)
            else:
                print_warning("GROQ_API_KEY not configured yet")
                print_info("Update .env with your Groq API key to run tests")
                results.append(False)
    else:
        print_warning(".env file not found")
        print_info("Copy .env.example to .env and add your API key")
        results.append(False)
    
    print(f"\n{BOLD}2. Checking Python environment{RESET}")
    python_version = sys.version.split()[0]
    print_info(f"Python version: {python_version}")
    
    if sys.version_info >= (3, 10):
        print_success("Python version is 3.10 or higher")
        results.append(True)
    else:
        print_warning("Python 3.10+ recommended")
        results.append(False)
    
    print(f"\n{BOLD}3. Checking virtual environment{RESET}")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_success("Running in virtual environment")
        results.append(True)
    else:
        print_warning("Not running in virtual environment")
        print_info("Consider using: python -m venv venv")
        results.append(False)
    
    return all(results)

def main():
    """Main verification function"""
    print(f"\n{BOLD}{GREEN}{'=' * 70}{RESET}")
    print(f"{BOLD}{GREEN}{'SmartOps AI - Module Verification'.center(70)}{RESET}")
    print(f"{BOLD}{GREEN}{'Member 3: AI & RCA Engine'.center(70)}{RESET}")
    print(f"{BOLD}{GREEN}{'=' * 70}{RESET}\n")
    
    # Change to backend directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check environment
    env_ok = check_environment()
    
    # Verify modules
    module1_ok = verify_module_1()
    module2_ok = verify_module_2()
    
    # Final summary
    print_header("Final Summary")
    
    print(f"\n{BOLD}Module Status:{RESET}")
    if module1_ok:
        print_success("Module 1: Groq Integration - COMPLETE")
    else:
        print_error("Module 1: Groq Integration - INCOMPLETE")
    
    if module2_ok:
        print_success("Module 2: RCA Prompt Engineering - COMPLETE")
    else:
        print_error("Module 2: RCA Prompt Engineering - INCOMPLETE")
    
    print(f"\n{BOLD}Environment Status:{RESET}")
    if env_ok:
        print_success("Environment properly configured")
    else:
        print_warning("Environment needs configuration")
    
    # Next steps
    print_header("Next Steps")
    
    if module1_ok and module2_ok:
        print_success("✅ Modules 1 & 2 are COMPLETE!")
        print()
        print(f"{BOLD}Ready to test:{RESET}")
        print("1. Ensure GROQ_API_KEY is set in .env")
        print("2. Run: python test_groq.py")
        print("3. Run: python -m backend.main")
        print("4. Visit: http://localhost:8002/docs")
        print()
        print(f"{BOLD}Ready to build:{RESET}")
        print("🔄 Module 3: RAG System (Similar incident retrieval)")
        print("🔄 Module 4: Risk Engine (Risk scoring)")
        print("🔄 Module 5: PDF Generation (Downloadable reports)")
        print("🔄 Module 6: AI Copilot (Interactive Q&A)")
    else:
        print_warning("Some modules need attention. Check errors above.")
    
    print(f"\n{BOLD}{GREEN}{'=' * 70}{RESET}\n")

if __name__ == "__main__":
    main()
