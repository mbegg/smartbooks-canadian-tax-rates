"""
Example script demonstrating how to fetch and import tax rates from the GitHub repository.

This would be integrated into SmartBooks as the TaxRateUpdateService.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen

logger = logging.getLogger(__name__)

# GitHub repository configuration
GITHUB_REPO = "smartbooks/canadian-tax-rates"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def fetch_latest_release_info() -> Dict:
    """
    Fetch information about the latest release from GitHub API.
    
    Returns:
        Dict with 'tag_name', 'published_at', 'commit_sha', etc.
    """
    try:
        with urlopen(GITHUB_API_URL) as response:
            return json.loads(response.read())
    except Exception as e:
        logger.error(f"Failed to fetch release info: {e}")
        raise


def fetch_rate_file(year: int, province: str) -> Dict:
    """
    Fetch a specific province rate file from GitHub.
    
    Args:
        year: Tax year (e.g., 2025)
        province: Province code (e.g., 'ON', 'BC') or 'federal'
    
    Returns:
        Parsed JSON rate data
    """
    if province.upper() == 'FEDERAL':
        url = f"{GITHUB_RAW_URL}/rates/{year}/federal.json"
    else:
        url = f"{GITHUB_RAW_URL}/rates/{year}/provinces/{province.upper()}.json"
    
    try:
        with urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        logger.error(f"Failed to fetch {province} rates for {year}: {e}")
        raise


def fetch_all_provinces(year: int = 2025) -> Dict[str, Dict]:
    """
    Fetch all provincial rate files for a given year.
    
    Args:
        year: Tax year (default: 2025)
    
    Returns:
        Dict mapping province codes to rate data
    """
    provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    
    rates = {}
    for province in provinces:
        try:
            rates[province] = fetch_rate_file(year, province)
            logger.info(f"Fetched rates for {province}")
        except Exception as e:
            logger.warning(f"Skipping {province}: {e}")
    
    return rates


def import_rates_to_database(rates_data: Dict[str, Dict], db_connection):
    """
    Import fetched rates into the SmartBooks database.
    
    Args:
        rates_data: Dict mapping province codes to rate data
        db_connection: Database connection (from SmartBooks.models.database)
    """
    cursor = db_connection.cursor()
    
    inserted = 0
    updated = 0
    
    for province, data in rates_data.items():
        for rate in data.get('rates', []):
            # Check if rate already exists
            cursor.execute("""
                SELECT RateID FROM ProvincialTaxRates 
                WHERE RateID = ?
            """, (rate['rate_id'],))
            
            exists = cursor.fetchone()
            
            if exists:
                # Update existing rate
                cursor.execute("""
                    UPDATE ProvincialTaxRates
                    SET Rate = ?, 
                        EffectiveFrom = ?, 
                        EffectiveTo = ?,
                        Description = ?,
                        SourceURL = ?,
                        Notes = ?,
                        UpdatedAt = CURRENT_TIMESTAMP
                    WHERE RateID = ?
                """, (
                    rate['rate'],
                    rate['effective_from'],
                    rate.get('effective_to'),
                    rate.get('description'),
                    rate.get('source_url'),
                    rate.get('notes'),
                    rate['rate_id']
                ))
                updated += 1
            else:
                # Insert new rate
                cursor.execute("""
                    INSERT INTO ProvincialTaxRates (
                        RateID, Province, TaxType, Rate, EffectiveFrom, EffectiveTo,
                        Component, Description, Source, SourceURL, Notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rate['rate_id'],
                    province,
                    rate['tax_type'],
                    rate['rate'],
                    rate['effective_from'],
                    rate.get('effective_to'),
                    rate.get('component'),
                    rate.get('description'),
                    'GitHub',
                    rate.get('source_url'),
                    rate.get('notes')
                ))
                inserted += 1
    
    db_connection.commit()
    logger.info(f"Import complete: {inserted} inserted, {updated} updated")
    
    return inserted, updated


def record_update_history(db_connection, release_info: Dict, inserted: int, updated: int):
    """
    Record the update in TaxRateUpdates table for audit trail.
    
    Args:
        db_connection: Database connection
        release_info: GitHub release information
        inserted: Number of rates inserted
        updated: Number of rates updated
    """
    import uuid
    
    update_id = str(uuid.uuid4())
    cursor = db_connection.cursor()
    
    cursor.execute("""
        INSERT INTO TaxRateUpdates (
            UpdateID, SourceVersion, SourceURL, UpdateType,
            ChangeSummary, Status, AppliedAt, AppliedBy
        ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
    """, (
        update_id,
        release_info.get('tag_name', 'unknown'),
        release_info.get('html_url', ''),
        'Automatic',
        f"GitHub import: {inserted} inserted, {updated} updated",
        'Applied',
        'system'
    ))
    
    db_connection.commit()
    logger.info(f"Recorded update {update_id}")


def check_for_updates(current_version: Optional[str] = None) -> bool:
    """
    Check if there are new tax rate updates available on GitHub.
    
    Args:
        current_version: Currently installed version tag (e.g., 'v2025.1')
    
    Returns:
        True if updates available, False otherwise
    """
    try:
        release_info = fetch_latest_release_info()
        latest_version = release_info.get('tag_name')
        
        if not current_version:
            logger.info(f"No current version, latest is {latest_version}")
            return True
        
        if latest_version != current_version:
            logger.info(f"Update available: {current_version} → {latest_version}")
            return True
        
        logger.info(f"Already at latest version: {current_version}")
        return False
        
    except Exception as e:
        logger.error(f"Failed to check for updates: {e}")
        return False


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Check for updates
    has_updates = check_for_updates(current_version='v2025.0')
    
    if has_updates:
        # Fetch all provincial rates for 2025
        logger.info("Fetching 2025 tax rates from GitHub...")
        rates = fetch_all_provinces(2025)
        
        # Display summary
        logger.info(f"\nFetched rates for {len(rates)} provinces:")
        for prov, data in sorted(rates.items()):
            rate_count = len(data.get('rates', []))
            logger.info(f"  {prov}: {rate_count} rate(s)")
        
        # In SmartBooks, this would import to database:
        # from SmartBooks.models.database import get_connection
        # with get_connection() as conn:
        #     inserted, updated = import_rates_to_database(rates, conn)
        #     release_info = fetch_latest_release_info()
        #     record_update_history(conn, release_info, inserted, updated)
