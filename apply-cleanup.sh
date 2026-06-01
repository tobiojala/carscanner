#!/bin/bash
# run from your project root: bash apply-cleanup.sh
# safe to re-run — copies files, does not delete originals until you confirm

set -e
FRONTEND="./frontend"
CLEANUP="./frontend-cleanup"

echo "=== Applying frontend cleanup ==="

# 1. Nav — replace
echo "→ Updating app-nav.tsx"
cp "$CLEANUP/components/app-nav.tsx" "$FRONTEND/components/app-nav.tsx"

# 2. Deals page — replace (merges pipeline into deals)
echo "→ Updating deals/page.tsx"
cp "$CLEANUP/app/deals/page.tsx" "$FRONTEND/app/deals/page.tsx"

# 3. DealsTable — new file in correct location
echo "→ Adding components/deals-table.tsx"
cp "$CLEANUP/components/deals-table.tsx" "$FRONTEND/components/deals-table.tsx"

# 4. Rename csv-tools → listing-import-csv
echo "→ Renaming csv-tools.tsx → listing-import-csv.tsx"
cp "$FRONTEND/components/csv-tools.tsx" "$FRONTEND/components/listing-import-csv.tsx"
# Original kept until you verify builds — delete manually after

# 5. Rename actual-outcome-form → deal-outcome-form
echo "→ Renaming actual-outcome-form.tsx → deal-outcome-form.tsx"
cp "$FRONTEND/components/actual-outcome-form.tsx" "$FRONTEND/components/deal-outcome-form.tsx"
# Update export name inside the file manually (see deal-outcome-form.tsx notes)

# 6. Delete link-intake page
echo "→ Removing link-intake page"
rm -rf "$FRONTEND/app/link-intake"

# 7. Remove pipeline as standalone page (now merged into deals)
echo "→ Removing pipeline page"
rm -rf "$FRONTEND/app/pipeline"

echo ""
echo "=== Done. Next steps ==="
echo ""
echo "1. Open components/deals-table.tsx and verify the CompareDealItem import path"
echo "   matches your actual api.ts type export."
echo ""
echo "2. Open components/deal-outcome-form.tsx and rename the export function:"
echo "   ActualOutcomeForm → DealOutcomeForm"
echo "   Then run: grep -r 'ActualOutcomeForm' frontend/ to find all usages."
echo ""
echo "3. In deals/page.tsx the CsvTools import now points to listing-import-csv."
echo "   Confirm no other file still imports from csv-tools."
echo "   Run: grep -r 'csv-tools' frontend/"
echo ""
echo "4. In components/compare/ you still have DealsTableWithCompare.tsx."
echo "   Once deals-table.tsx is confirmed working, delete it:"
echo "   rm frontend/components/compare/DealsTableWithCompare.tsx"
echo ""
echo "5. Rebuild:"
echo "   FRONTEND_PORT=5173 BACKEND_PORT=8010 POSTGRES_PORT=55432 docker compose up --build"
