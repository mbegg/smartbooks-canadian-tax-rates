# SmartBooks Canadian Tax Rates Repository - Setup Guide

## Repository Created

A complete GitHub repository structure has been created at:
`tax-rates-repo/`

This repository is ready to be pushed to GitHub and will serve as the centralized source for Canadian tax rate updates.

## Contents

### Core Files
- **README.md** - Complete documentation for the repository
- **CHANGELOG.md** - Version history and rate changes
- **.gitignore** - Standard Python/Git ignore patterns

### Schema
- **schema/rate-schema.json** - JSON schema for validating rate files

### Rate Files (2025)
- **rates/2025/federal.json** - Federal GST (5%)
- **rates/2025/provinces/** - Individual files for all 13 provinces/territories:
  - AB.json (Alberta - GST only)
  - BC.json (British Columbia - GST + PST)
  - MB.json (Manitoba - GST + PST)
  - NB.json (New Brunswick - HST 15%)
  - NL.json (Newfoundland and Labrador - HST 15%)
  - NS.json (Nova Scotia - HST 15%)
  - NT.json (Northwest Territories - GST only)
  - NU.json (Nunavut - GST only)
  - ON.json (Ontario - HST 13%)
  - PE.json (Prince Edward Island - HST 15%)
  - QC.json (Quebec - GST + QST compounded)
  - SK.json (Saskatchewan - GST + PST)
  - YT.json (Yukon - GST only)

### Example Code
- **example_import.py** - Python script demonstrating how to:
  - Check for updates via GitHub API
  - Fetch rate files
  - Import into SmartBooks database
  - Record update history

## Next Steps

### 1. Create GitHub Repository

```bash
cd tax-rates-repo
git init
git add .
git commit -m "Initial commit: 2025 Canadian provincial tax rates"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/smartbooks-canadian-tax-rates.git
git branch -M main
git push -u origin main
```

### 2. Create Release Tag

```bash
git tag -a v2025.1 -m "2025 Canadian Tax Rates - Initial Release"
git push origin v2025.1
```

### 3. Integrate into SmartBooks

The next phase is to create `TaxRateUpdateService` in SmartBooks that:

1. **Check for Updates** (Tools → Tax Rates Manager)
   - Query GitHub API for latest release
   - Compare with last imported version (stored in TaxRateUpdates table)
   - Show notification if updates available

2. **Preview Changes**
   - Fetch new rate files from GitHub
   - Compare with current database rates
   - Show user a diff of what will change

3. **Apply Updates**
   - Download JSON files
   - Import to ProvincialTaxRates table
   - Record update in TaxRateUpdates table with commit SHA
   - Show confirmation with summary

4. **Rollback Support**
   - Keep previous versions in TaxRateUpdates
   - Allow rollback to previous version if needed

5. **Auto-Update Option**
   - Setting: "Check for tax rate updates on startup"
   - Background check with notification

## Rate File Format Example

```json
{
  "province": "ON",
  "province_name": "Ontario",
  "effective_from": "2025-01-01",
  "rates": [
    {
      "rate_id": "ON-HST-2025",
      "tax_type": "HST",
      "rate": 0.13,
      "component": "COMBINED",
      "description": "Ontario Harmonized Sales Tax",
      "effective_from": "2025-01-01",
      "effective_to": null,
      "source_url": "https://www.canada.ca/...",
      "notes": "Combined federal (5%) and provincial (8%)"
    }
  ]
}
```

## Validation

All rate files conform to `schema/rate-schema.json` and can be validated using:

```bash
# Using jsonschema validator (if installed)
pip install jsonschema
python -m jsonschema -i rates/2025/provinces/ON.json schema/rate-schema.json
```

## Testing

The repository includes all data needed for comprehensive testing:
- ✅ All 13 provinces/territories
- ✅ All tax types (GST, HST, PST, QST)
- ✅ Compounding calculation (Quebec)
- ✅ Combined vs separate rates
- ✅ Official government source URLs
- ✅ Historical effective dates

## SmartBooks Integration Architecture

```
SmartBooks Application
    ↓
TaxRateUpdateService
    ↓ (GitHub API)
GitHub Repository (smartbooks-canadian-tax-rates)
    ↓ (JSON files)
ProvincialTaxRates Table
    ↓
TaxCalculationService
    ↓
Invoices / Expenses
```

## Benefits

1. **Centralized Management** - Single source of truth for all tax rates
2. **Version Control** - Full history of rate changes via Git
3. **Transparency** - Open source, auditable by accountants/users
4. **Easy Updates** - Push updates to GitHub, all SmartBooks instances can pull
5. **Compliance** - Official government sources documented
6. **Rollback** - Can revert to previous versions if needed
7. **Multi-Client** - One repository serves all SmartBooks installations

## Maintenance

When tax rates change:
1. Update the relevant JSON file(s) in `rates/YEAR/`
2. Update `CHANGELOG.md` with the change details
3. Commit and push to GitHub
4. Create a new release tag (e.g., v2025.2)
5. SmartBooks installations will see update notification

## Future Enhancements

- **Automated Testing** - CI/CD pipeline to validate JSON schema
- **Historical Rates** - Archive for previous years (2024, 2023, etc.)
- **Rate Calculator API** - Optional REST API for real-time rate queries
- **Notification Service** - Email alerts when rates change
- **Multi-Country** - Expand to support US state taxes, etc.
