#!/bin/bash
# Create a new release for Reversi42
# Usage: ./scripts/release.sh <version>

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 3.2.0"
    exit 1
fi

VERSION=$1
TAG="v${VERSION}"

echo -e "${BLUE}🚀 Creating Release: ${TAG}${NC}"
echo "======================================"

# Pre-flight checks
echo -e "\n${BLUE}→ Running pre-flight checks...${NC}"

# 1. Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}❌ Working directory not clean${NC}"
    echo "Please commit or stash changes before releasing"
    exit 1
fi
echo -e "${GREEN}✅ Working directory clean${NC}"

# 2. Check on master branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "master" ]; then
    echo -e "${YELLOW}⚠️  Not on master branch (currently on: $CURRENT_BRANCH)${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 3. Pull latest changes
echo -e "\n${BLUE}→ Pulling latest changes...${NC}"
git pull origin master

# 4. Check version in files
echo -e "\n${BLUE}→ Checking version consistency...${NC}"

# Check pyproject.toml
if grep -q "version = \"${VERSION}\"" pyproject.toml; then
    echo -e "${GREEN}✅ pyproject.toml version: ${VERSION}${NC}"
else
    echo -e "${RED}❌ pyproject.toml version mismatch${NC}"
    echo "Please update version in pyproject.toml to ${VERSION}"
    exit 1
fi

# Check setup.py
if grep -q "version=\"${VERSION}\"" setup.py; then
    echo -e "${GREEN}✅ setup.py version: ${VERSION}${NC}"
else
    echo -e "${YELLOW}⚠️  setup.py version mismatch (updating...)${NC}"
    sed -i.bak "s/version=\"[^\"]*\"/version=\"${VERSION}\"/" setup.py
    rm setup.py.bak
fi

# 5. Run tests
echo -e "\n${BLUE}→ Running tests...${NC}"
./scripts/run_tests.sh --fast || {
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
}
echo -e "${GREEN}✅ Tests passed${NC}"

# 6. Run quality checks
echo -e "\n${BLUE}→ Running quality checks...${NC}"
./scripts/check_quality.sh || {
    echo -e "${YELLOW}⚠️  Quality checks have warnings${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
}

# 7. Check CHANGELOG
echo -e "\n${BLUE}→ Checking CHANGELOG...${NC}"
if grep -q "## \[${VERSION}\]" CHANGELOG.md; then
    echo -e "${GREEN}✅ CHANGELOG has entry for ${VERSION}${NC}"
else
    echo -e "${RED}❌ CHANGELOG missing entry for ${VERSION}${NC}"
    echo "Please add release notes to CHANGELOG.md"
    exit 1
fi

# 8. Build package
echo -e "\n${BLUE}→ Building package...${NC}"
python -m build
echo -e "${GREEN}✅ Package built${NC}"

# 9. Check package
echo -e "\n${BLUE}→ Checking package...${NC}"
twine check dist/*
echo -e "${GREEN}✅ Package valid${NC}"

# Ready to release
echo -e "\n======================================"
echo -e "${YELLOW}Ready to create release ${TAG}${NC}"
echo -e "\nThis will:"
echo "  1. Create git tag: ${TAG}"
echo "  2. Push tag to origin"
echo "  3. Trigger GitHub Actions release workflow"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Release cancelled"
    exit 0
fi

# Create and push tag
echo -e "\n${BLUE}→ Creating git tag...${NC}"
git tag -a "${TAG}" -m "Release ${VERSION}"
echo -e "${GREEN}✅ Tag created: ${TAG}${NC}"

echo -e "\n${BLUE}→ Pushing tag...${NC}"
git push origin "${TAG}"
echo -e "${GREEN}✅ Tag pushed${NC}"

echo -e "\n======================================"
echo -e "${GREEN}🎉 Release ${TAG} initiated!${NC}"
echo ""
echo "Next steps:"
echo "  1. GitHub Actions will build artifacts"
echo "  2. GitHub Release will be created automatically"
echo "  3. Package will be published to PyPI"
echo "  4. Monitor progress at:"
echo "     https://github.com/lookee/Reversi42/actions"
echo ""
echo -e "${BLUE}Release URL (when ready):${NC}"
echo "https://github.com/lookee/Reversi42/releases/tag/${TAG}"
echo ""
echo -e "${YELLOW}💡 Tip: After PyPI publication succeeds, run cleanup:${NC}"
echo "   ./scripts/cleanup.sh --keep-versions=3"

