# Changelog

All notable changes to Canadian tax rates will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses calendar versioning (YYYY.N).

## [Unreleased]

## [2025.2] - 2025-11-21

### Changed
- **Nova Scotia**: HST reduced from 15% to 14% effective April 1, 2025
  - Rate ID: `NS-HST-2025-Q1` (15%) valid Jan 1 - Mar 31, 2025
  - Rate ID: `NS-HST-2025-Q2` (14%) valid Apr 1, 2025 onwards
  - Source: https://novascotia.ca/finance/en/home/taxation/tax101/default.aspx
  - Provincial portion reduced from 10% to 9%

### Technical Details
- Added `effective_to` date to Q1 rate (2025-03-31)
- New rate record for Q2 with reduced rate
- SmartBooks will automatically select correct rate based on invoice date
- Backward compatible: existing Q1 invoices unaffected

## [2025.1] - 2025-01-01

### Added
- Initial release of 2025 Canadian provincial tax rates
- Federal GST rate: 5%
- Provincial rates for all 13 provinces and territories:
  - Alberta: GST 5%
  - British Columbia: GST 5% + PST 7%
  - Manitoba: GST 5% + PST 7%
  - New Brunswick: HST 15%
  - Newfoundland and Labrador: HST 15%
  - Northwest Territories: GST 5%
  - Nova Scotia: HST 15%
  - Nunavut: GST 5%
  - Ontario: HST 13%
  - Prince Edward Island: HST 15%
  - Quebec: GST 5% + QST 9.975% (compounded)
  - Saskatchewan: GST 5% + PST 6%
  - Yukon: GST 5%

### Notes
- All rates effective January 1, 2025
- No rate changes from 2024
- Quebec QST remains at 9.975% (compounded calculation)
- HST provinces maintain their combined federal/provincial rates

### Data Sources
- Canada Revenue Agency: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses.html
- Provincial revenue agencies (see individual rate files)

---

## Future Updates

Tax rate changes will be published as they are announced by federal and provincial governments. 
Typical change dates:
- January 1 (new year budget changes)
- July 1 (mid-year adjustments)
- Ad-hoc changes following provincial budgets

Subscribe to releases to be notified of updates.
