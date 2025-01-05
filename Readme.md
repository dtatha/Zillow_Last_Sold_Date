# Zillow Data Fetching Script Documentation

## Objective

The purpose of this script is to:
1. Fetch property-specific pricing data from Zillow using the RapidAPI platform.
2. Retrieve the three most recent price points (date and price) for each property.
3. Save the results, including property addresses, ZPIDs (Zillow Property IDs), and pricing data, in a CSV file for further analysis or reporting.

---

## Overview of the Script

This script:
- Retrieves the **ZPID** (Zillow Property ID) for a given property address.
- Fetches the price history for the ZPID.
- Extracts and processes the three most recent price points based on timestamps.
- Converts timestamps into human-readable date strings.
- Writes the address, ZPID, and the three most recent price data into a CSV file.
- Securely reads the API key from a local file named `API_Key.txt`.

---

## Code Flow

### Imports and Dependencies
- `requests`: Used to make HTTP requests to the RapidAPI endpoint.
- `csv`: Used to create and write data into the CSV file.
- `datetime`: Used to convert timestamps into human-readable dates.
- `os`: Used to handle file-related operations.

---

### Functions

#### `read_api_key(file_name="API_Key.txt")`
- **Objective**: Securely read the API key from a local file.
- **Input**:
  - `file_name`: Name of the file containing the API key (default is `API_Key.txt`).
- **Output**: Returns the API key as a string.
- **Process**:
  1. Opens the `API_Key.txt` file and reads its content.
  2. Trims any extra spaces or newline characters.
  3. Handles errors if the file is not found or unreadable.

#### `get_zpid(address, api_key, api_host)`
- **Objective**: Retrieve the ZPID for a given property address.
- **Input**:
  - `address`: Property address (e.g., "2300 Arbor Vista Dr, Charlotte, NC 28262").
  - `api_key`: API key retrieved from `API_Key.txt`.
  - `api_host`: RapidAPI host for Zillow.
- **Output**: Returns the ZPID if found, otherwise `None`.
- **Process**:
  1. Sends an HTTP GET request to the `locationSuggestions` endpoint.
  2. Parses the response to extract the ZPID.
  3. Handles errors if the API call fails.

#### `get_price_history(zpid, api_key, api_host)`
- **Objective**: Retrieve the price history for a given ZPID.
- **Input**:
  - `zpid`: Zillow Property ID.
  - `api_key`: API key retrieved from `API_Key.txt`.
  - `api_host`: RapidAPI host for Zillow.
- **Output**: Returns a list of the three most recent price points (`[date, price]` pairs).
- **Process**:
  1. Sends an HTTP GET request to the `valueHistory/listingPrices` endpoint.
  2. Parses the `chartData` section of the response to extract price points.
  3. Sorts the data by timestamp in descending order.
  4. Converts timestamps into human-readable dates.
  5. Handles errors if the API call fails.

---

### Main Script

- Defines a list of addresses to process (e.g., `"2300 Arbor Vista Dr, Charlotte, NC 28262"`).
- Reads the API key from the `API_Key.txt` file.
- Creates and writes the CSV file with the following columns:
  - `Address`
  - `ZPID`
  - `Date 1`, `Price 1`
  - `Date 2`, `Price 2`
  - `Date 3`, `Price 3`
- Iterates over each address to:
  1. Retrieve the ZPID.
  2. Fetch and process price history.
  3. Handle cases where data is unavailable by writing `"No data"` to the CSV.

---

## API Endpoints

### Location Suggestions API
- **Endpoint**: `https://zillow-com1.p.rapidapi.com/locationSuggestions`
- **Purpose**: Retrieve the ZPID for a given address.
- **Parameters**:
  - `q`: The address query (e.g., `"2300 Arbor Vista Dr, Charlotte, NC 28262"`).

### Price History API
- **Endpoint**: `https://zillow-com1.p.rapidapi.com/valueHistory/listingPrices`
- **Purpose**: Retrieve price history for a given ZPID.

---

## File Requirements

1. **API_Key.txt**:
   - A text file containing the RapidAPI key.
   - Must be stored in the same directory as the script.
   - Should contain only the API key with no additional spaces or lines.

   **Example (Do not include real API key)**: