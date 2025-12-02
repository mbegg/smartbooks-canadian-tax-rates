# ELK Books Canadian Tax Rates

Centralized repository for Canadian provincial and territorial tax rates used by SmartBooks accounting software.

## Overview

This repository provides authoritative tax rate data for all 13 Canadian provinces and territories, including:
- Goods and Services Tax (GST) - 5% federal
- Harmonized Sales Tax (HST) - 13-15% (combined federal/provincial)
- Provincial Sales Tax (PST) - 6-7%
- Quebec Sales Tax (QST) - 9.975% (compounded)

## Structure

```
tax-rates-repo/
├── rates/
│   └── 2025/
│       ├── federal.json          # Federal GST rate
│       └── provinces/
│           ├── AB.json           # Alberta
│           ├── BC.json           # British Columbia
│           ├── MB.json           # Manitoba
│           ├── NB.json           # New Brunswick
│           ├── NL.json           # Newfoundland and Labrador
│           ├── NS.json           # Nova Scotia
│           ├── NT.json           # Northwest Territories
│           ├── NU.json           # Nunavut
│           ├── ON.json           # Ontario
│           ├── PE.json           # Prince Edward Island
│           ├── QC.json           # Quebec
│           ├── SK.json           # Saskatchewan
│           └── YT.json           # Yukon
├── schema/
│   └── rate-schema.json          # JSON schema for validation
├── CHANGELOG.md                   # Version history
└── README.md                      # This file
```

## Rate File Format

Each province file contains tax rates with the following structure:

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
      "source_url": "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses.html",
      "notes": "Combined federal (5%) and provincial (8%) portions"
    }
  ]
}
```

## Tax Types

- **GST**: Goods and Services Tax (federal, 5%)
- **HST**: Harmonized Sales Tax (combined federal/provincial, 13-15%)
- **PST**: Provincial Sales Tax (provincial only, 6-7%)
- **QST**: Quebec Sales Tax (provincial, 9.975%, compounded on subtotal + GST)

## Provincial Tax Systems

### HST Provinces (Single Combined Rate)
- **Ontario (ON)**: 13%
- **New Brunswick (NB)**: 15%
- **Nova Scotia (NS)**: 15%
- **Prince Edward Island (PE)**: 15%
- **Newfoundland and Labrador (NL)**: 15%

### GST + PST Provinces (Separate Rates)
- **British Columbia (BC)**: GST 5% + PST 7% = 12%
- **Saskatchewan (SK)**: GST 5% + PST 6% = 11%
- **Manitoba (MB)**: GST 5% + PST 7% = 12%

### GST + QST (Compounded)
- **Quebec (QC)**: GST 5% + QST 9.975% (on subtotal + GST) = 14.975% effective

### GST Only (No Provincial Tax)
- **Alberta (AB)**: GST 5%
- **Yukon (YT)**: GST 5%
- **Northwest Territories (NT)**: GST 5%
- **Nunavut (NU)**: GST 5%

## Versioning

This repository uses calendar versioning based on the tax year:
- **v2025.1** - Initial 2025 rates (January 1, 2025)
- **v2025.2** - Mid-year updates (if any rate changes)
- **v2026.1** - 2026 rates

## Data Sources

All rates are sourced from official government agencies:
- [Canada Revenue Agency (CRA)](https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses.html)
- Provincial revenue agencies (see individual rate files for specific URLs)

## Usage in ELK Books

ELK Books automatically checks this repository for tax rate updates:
1. On startup (if enabled in settings)
2. Via Tools → Tax Rates Manager → "Check for Updates"
3. Manual import of specific versions

The app compares the GitHub commit SHA with the last imported version to detect changes.

## Contributing

Tax rate updates are managed by the SmartBooks development team. If you notice an incorrect rate:
1. Open an issue with the province, current rate, correct rate, and source URL
2. Include the effective date of the change
3. Link to official government announcement

## License

Tax rate data is factual information from government sources and is not copyrightable. This repository structure and documentation are provided for use with SmartBooks accounting software.

## Support

For questions about official tax rates:
- Contact the Canada Revenue Agency: 1-800-959-5525
- Visit: https://www.canada.ca/en/revenue-agency.html
