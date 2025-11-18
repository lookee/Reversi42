#!/bin/bash
# Cleanup script for Reversi42
# Removes build artifacts, old distributions, and temporary files after PyPI release
# Usage: ./scripts/cleanup.sh [--keep-versions=N] [--dry-run]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Default options
KEEP_VERSIONS=3  # Keep last N versions in dist/
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-versions=*)
            KEEP_VERSIONS="${1#*=}"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --keep-versions=N    Keep last N versions in dist/ (default: 3)"
            echo "  --dry-run            Show what would be deleted without actually deleting"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🧹 Reversi42 Cleanup Script${NC}"
echo "======================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}⚠️  DRY RUN MODE - No files will be deleted${NC}"
    echo ""
fi

# Function to safely remove files/directories
remove() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY RUN] Would remove: $1${NC}"
    else
        if [ -e "$1" ]; then
            rm -rf "$1"
            echo -e "${GREEN}✅ Removed: $1${NC}"
        fi
    fi
}

# Function to get size before cleanup
get_size() {
    if [ -d "$1" ]; then
        du -sh "$1" 2>/dev/null | cut -f1 || echo "0"
    else
        echo "0"
    fi
}

# Track total space saved
TOTAL_SIZE_BEFORE=0
TOTAL_SIZE_AFTER=0

# 1. Clean old distribution files
echo -e "${BLUE}→ Cleaning old distribution files...${NC}"
if [ -d "dist" ]; then
    DIST_SIZE_BEFORE=$(du -sb dist 2>/dev/null | cut -f1 || echo 0)
    TOTAL_SIZE_BEFORE=$((TOTAL_SIZE_BEFORE + DIST_SIZE_BEFORE))
    
    # Get current version from pyproject.toml
    CURRENT_VERSION=$(awk -F'"' '/^[[:space:]]*version[[:space:]]*=/ {print $2; exit}' pyproject.toml 2>/dev/null || echo "")
    
    if [ -n "$CURRENT_VERSION" ]; then
        echo "   Current version: $CURRENT_VERSION"
        echo "   Keeping last $KEEP_VERSIONS versions"
        
        # Get all unique versions from dist files
        VERSIONS=$(cd dist && ls -1 *.whl *.tar.gz 2>/dev/null | \
            sed -E 's/reversi42-([0-9]+\.[0-9]+\.[0-9]+[^[:space:]]*).*/\1/' | \
            sort -V -u | tail -n "$KEEP_VERSIONS" || echo "")
        
        # Remove files not in the keep list
        cd dist
        for file in *.whl *.tar.gz; do
            [ ! -f "$file" ] && continue
            FILE_VERSION=$(echo "$file" | sed -E 's/reversi42-([0-9]+\.[0-9]+\.[0-9]+[^[:space:]]*).*/\1/')
            KEEP=false
            for keep_version in $VERSIONS; do
                if [ "$FILE_VERSION" = "$keep_version" ]; then
                    KEEP=true
                    break
                fi
            done
            
            if [ "$KEEP" = false ]; then
                remove "../dist/$file"
            else
                echo "   Keeping: $file"
            fi
        done 2>/dev/null || true
        cd ..
    else
        echo -e "${YELLOW}⚠️  Could not determine current version, skipping dist cleanup${NC}"
    fi
    
    DIST_SIZE_AFTER=$(du -sb dist 2>/dev/null | cut -f1 || echo 0)
    TOTAL_SIZE_AFTER=$((TOTAL_SIZE_AFTER + DIST_SIZE_AFTER))
    DIST_SAVED=$((DIST_SIZE_BEFORE - DIST_SIZE_AFTER))
    if [ $DIST_SAVED -gt 0 ]; then
        if command -v numfmt >/dev/null 2>&1; then
            SAVED_SIZE=$(numfmt --to=iec-i --suffix=B $DIST_SAVED)
        else
            SAVED_SIZE=$(awk "BEGIN {printf \"%.1fMB\", $DIST_SAVED/1024/1024}")
        fi
        echo -e "${GREEN}   Saved: $SAVED_SIZE${NC}"
    fi
else
    echo "   No dist/ directory found"
fi
echo ""

# 2. Clean Python cache files
echo -e "${BLUE}→ Cleaning Python cache files (__pycache__)...${NC}"
CACHE_COUNT=0
while IFS= read -r cache_dir; do
    [ -z "$cache_dir" ] && continue
    remove "$cache_dir"
    CACHE_COUNT=$((CACHE_COUNT + 1))
done < <(find . -type d -name "__pycache__" 2>/dev/null)
if [ $CACHE_COUNT -eq 0 ]; then
    echo "   No __pycache__ directories found"
else
    echo "   Removed $CACHE_COUNT __pycache__ directories"
fi
echo ""

# 3. Clean .pyc files
echo -e "${BLUE}→ Cleaning compiled Python files (.pyc, .pyo)...${NC}"
PYC_COUNT=0
while IFS= read -r pyc_file; do
    [ -z "$pyc_file" ] && continue
    remove "$pyc_file"
    PYC_COUNT=$((PYC_COUNT + 1))
done < <(find . -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) 2>/dev/null)
if [ $PYC_COUNT -eq 0 ]; then
    echo "   No .pyc/.pyo files found"
else
    echo "   Removed $PYC_COUNT compiled Python files"
fi
echo ""

# 4. Clean egg-info directories
echo -e "${BLUE}→ Cleaning egg-info directories...${NC}"
EGG_COUNT=0
while IFS= read -r egg_dir; do
    [ -z "$egg_dir" ] && continue
    remove "$egg_dir"
    EGG_COUNT=$((EGG_COUNT + 1))
done < <(find . -type d -name "*.egg-info" 2>/dev/null)
if [ $EGG_COUNT -eq 0 ]; then
    echo "   No .egg-info directories found"
else
    echo "   Removed $EGG_COUNT .egg-info directories"
fi
echo ""

# 5. Clean build directory
echo -e "${BLUE}→ Cleaning build directory...${NC}"
if [ -d "build" ]; then
    BUILD_SIZE=$(du -sb build 2>/dev/null | cut -f1 || echo 0)
    TOTAL_SIZE_BEFORE=$((TOTAL_SIZE_BEFORE + BUILD_SIZE))
    remove "build"
    TOTAL_SIZE_AFTER=$((TOTAL_SIZE_AFTER + 0))
else
    echo "   No build/ directory found"
fi
echo ""

# 6. Clean coverage files
echo -e "${BLUE}→ Cleaning coverage files...${NC}"
COVERAGE_FILES=(
    ".coverage"
    ".coverage.*"
    "coverage.xml"
    "htmlcov"
    ".pytest_cache"
    ".cache"
)
COVERAGE_COUNT=0
for pattern in "${COVERAGE_FILES[@]}"; do
    for file in $pattern; do
        if [ -e "$file" ]; then
            remove "$file"
            COVERAGE_COUNT=$((COVERAGE_COUNT + 1))
        fi
    done
done
if [ $COVERAGE_COUNT -eq 0 ]; then
    echo "   No coverage files found"
else
    echo "   Removed $COVERAGE_COUNT coverage files/directories"
fi
echo ""

# 7. Clean temporary files
echo -e "${BLUE}→ Cleaning temporary files...${NC}"
TEMP_PATTERNS=(
    "*.tmp"
    "*.bak"
    "*.old"
    "*.swp"
    "*.swo"
    "*~"
    ".DS_Store"
)
TEMP_COUNT=0
for pattern in "${TEMP_PATTERNS[@]}"; do
    while IFS= read -r temp_file; do
        [ -z "$temp_file" ] && continue
        remove "$temp_file"
        TEMP_COUNT=$((TEMP_COUNT + 1))
    done < <(find . -type f -name "$pattern" 2>/dev/null)
done
if [ $TEMP_COUNT -eq 0 ]; then
    echo "   No temporary files found"
else
    echo "   Removed $TEMP_COUNT temporary files"
fi
echo ""

# 8. Clean mypy cache
echo -e "${BLUE}→ Cleaning mypy cache...${NC}"
if [ -d ".mypy_cache" ]; then
    remove ".mypy_cache"
else
    echo "   No .mypy_cache directory found"
fi
echo ""

# Summary
echo "======================================"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}📊 DRY RUN SUMMARY${NC}"
    echo "   (No files were actually deleted)"
else
    TOTAL_SAVED=$((TOTAL_SIZE_BEFORE - TOTAL_SIZE_AFTER))
    if [ $TOTAL_SAVED -gt 0 ]; then
        if command -v numfmt >/dev/null 2>&1; then
            SAVED_SIZE=$(numfmt --to=iec-i --suffix=B $TOTAL_SAVED)
        else
            SAVED_SIZE=$(awk "BEGIN {printf \"%.1fMB\", $TOTAL_SAVED/1024/1024}")
        fi
        echo -e "${GREEN}✅ Cleanup completed!${NC}"
        echo -e "${GREEN}   Total space saved: $SAVED_SIZE${NC}"
    else
        echo -e "${GREEN}✅ Cleanup completed!${NC}"
        echo "   (No significant space was freed)"
    fi
fi
echo ""
echo "Remaining files in dist/:"
if [ -d "dist" ] && [ "$(ls -A dist 2>/dev/null)" ]; then
    ls -lh dist/ | tail -n +2 | awk '{print "   " $9 " (" $5 ")"}'
else
    echo "   (empty)"
fi
echo ""

