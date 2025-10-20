#!/bin/bash
# Run all code quality checks
# Usage: ./scripts/check_quality.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 Code Quality Checks${NC}"
echo "======================================"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Track overall status
ALL_PASSED=true

# 1. Black formatting check
echo -e "\n${BLUE}→ Checking code formatting (Black)...${NC}"
if black --check src/ tests/ 2>&1; then
    echo -e "${GREEN}✅ Black: Formatting OK${NC}"
else
    echo -e "${RED}❌ Black: Formatting issues found${NC}"
    echo -e "${YELLOW}Run: black src/ tests/${NC}"
    ALL_PASSED=false
fi

# 2. Import sorting check
echo -e "\n${BLUE}→ Checking import sorting (isort)...${NC}"
if isort --check-only src/ tests/ 2>&1; then
    echo -e "${GREEN}✅ isort: Imports OK${NC}"
else
    echo -e "${RED}❌ isort: Import issues found${NC}"
    echo -e "${YELLOW}Run: isort src/ tests/${NC}"
    ALL_PASSED=false
fi

# 3. Pylint
echo -e "\n${BLUE}→ Running linter (Pylint)...${NC}"
if pylint src/ --fail-under=7.0 --output-format=colorized 2>&1; then
    echo -e "${GREEN}✅ Pylint: Score >= 7.0${NC}"
else
    echo -e "${YELLOW}⚠️  Pylint: Score < 7.0 (warning)${NC}"
    # Don't fail on pylint, just warn
fi

# 4. Type checking
echo -e "\n${BLUE}→ Type checking (mypy)...${NC}"
if mypy src/ --ignore-missing-imports 2>&1; then
    echo -e "${GREEN}✅ mypy: No type errors${NC}"
else
    echo -e "${YELLOW}⚠️  mypy: Type errors found (warning)${NC}"
    # Don't fail on mypy in CI, just warn
fi

# 5. Security check
echo -e "\n${BLUE}→ Security check (Bandit)...${NC}"
if bandit -r src/ -ll 2>&1; then
    echo -e "${GREEN}✅ Bandit: No security issues${NC}"
else
    echo -e "${YELLOW}⚠️  Bandit: Potential security issues (review manually)${NC}"
fi

# Summary
echo -e "\n======================================"
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}✅ All critical quality checks passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some quality checks failed${NC}"
    echo -e "${YELLOW}Please fix the issues and run again${NC}"
    exit 1
fi

