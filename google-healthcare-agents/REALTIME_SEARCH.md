# Real-Time Healthcare Provider Search

## 🌐 Overview

The Healthcare Multi-Agent System now supports **real-time web-based provider search** in addition to the static sample data. This allows you to find actual healthcare facilities dynamically based on any location.

## 🆕 What's New

### Real-Time Provider Locator
- **Dynamic web search** for healthcare providers
- **Location-based** queries (city, state, ZIP, coordinates)
- **Automatic parsing** of search results
- **Smart extraction** of provider details (name, address, phone, ratings)
- **Fallback mechanism** to sample data if web search fails
- **Result caching** for improved performance

## 📊 Comparison: Static vs Real-Time

| Feature | Static Data | Real-Time Search |
|---------|-------------|------------------|
| **Data Source** | Hardcoded sample facilities | Live web search |
| **Locations** | Limited to NYC area | Any location worldwide |
| **Accuracy** | Sample/demonstration data | Current, real information |
| **Performance** | Instant | 2-5 seconds |
| **Offline Support** | ✅ Yes | ❌ No (falls back to static) |
| **Up-to-date** | ❌ Fixed | ✅ Always current |
| **Use Case** | Testing, demos, offline use | Production, real searches |

## 🚀 How to Use

### Option 1: Use Example Script

```bash
python examples/example_realtime_provider_search.py
```

This demonstrates:
- Searching by city/state
- Different specializations
- Emergency services
- Coordinate-based search
- Result parsing and formatting

### Option 2: Import and Use Directly

```python
from agents.provider_locator_realtime import RealTimeProviderLocator

# Create real-time locator
locator = RealTimeProviderLocator()

# Search for providers
response = locator.process_request(
    "Find diabetes specialists in Baltimore, MD",
    context={}
)

# Display results
for facility in response['facilities']:
    print(locator.format_facility_info(facility))
```

### Option 3: Integrate with Main System

Update `main.py`:

```python
# Replace this:
from agents.provider_locator_agent import HealthcareProviderLocator

# With this:
from agents.provider_locator_realtime import RealTimeProviderLocator

# In _initialize_agents():
agents = [
    # ... other agents ...
    RealTimeProviderLocator(),  # Use real-time version
    # ... other agents ...
]
```

## 🔍 Search Capabilities

### Supported Location Formats

1. **City, State**
   ```python
   "Find hospitals in Baltimore, MD"
   "diabetes centers near New York, NY"
   ```

2. **ZIP Code**
   ```python
   "Find clinics in 21201"
   "healthcare providers zip code 10001"
   ```

3. **Coordinates** (via context)
   ```python
   context = {
       'user_location': {'lat': 39.2904, 'lon': -76.6122}
   }
   ```

4. **Neighborhood/Area**
   ```python
   "Find doctors in Downtown Chicago"
   "hospitals near Times Square"
   ```

### Search Filters

- **Specialization**: diabetes, nutrition, cardiology, pediatrics, etc.
- **Facility Type**: hospital, clinic, medical center, urgent care
- **Emergency Services**: 24/7 availability
- **Ratings**: Extracted from search results

### Example Queries

```python
# Specialization search
"Find diabetes specialists in Baltimore"

# Facility type search
"Show me hospitals in Boston"

# Combined search
"Find diabetes clinics with emergency services in Chicago"

# Nutritionist search
"Where can I find a nutritionist near San Francisco?"

# Emergency care
"Urgent care centers open now in Miami"
```

## 🛠️ How It Works

### Search Process Flow

```
1. User Query
   ↓
2. Extract Location & Criteria
   ↓
3. Build Optimized Search Query
   ↓
4. Perform Web Search
   ↓
5. Parse Search Results
   ↓
6. Extract Provider Information:
   • Name
   • Address
   • Phone
   • Website
   • Rating
   • Specializations
   • Hours
   ↓
7. Format & Return Results
```

### Information Extraction

The system intelligently extracts:

**Provider Name**
- Looks for healthcare-related keywords
- Identifies organization names
- Handles various formats

**Address**
- Parses street addresses
- Extracts city, state, ZIP
- Handles P.O. boxes and suites

**Phone Numbers**
- Recognizes multiple formats:
  - (555) 123-4567
  - 555-123-4567
  - 555.123.4567
- Formats consistently

**Ratings**
- Extracts star ratings (out of 5)
- Handles various formats:
  - "4.5 stars"
  - "4.5 out of 5"
  - "4.5/5"

**Specializations**
- Detects medical specialties from text
- Maps keywords to specializations
- Supports multiple specialties per provider

## 📦 Fallback Mechanism

If web search fails or returns no results:

1. **Automatic Fallback**: System uses simulated data
2. **User Notification**: Indicates results are from fallback
3. **Graceful Degradation**: System continues to function
4. **Cache Utilization**: Uses cached results if available

```python
# Fallback is automatic:
locator = RealTimeProviderLocator()

# Even if web search fails, you get results:
response = locator.process_request("Find diabetes centers")

# Check the source:
print(response['search_mode'])  # 'real_time_web_search' or 'simulation'
```

## ⚙️ Configuration

### Enable/Disable Web Search

```python
# Create with web search enabled (default)
locator = RealTimeProviderLocator()

# Or provide custom search function
def my_search_function(query):
    # Your search implementation
    return search_results

locator = RealTimeProviderLocator(web_search_function=my_search_function)
```

### Caching

Results are automatically cached:

```python
# First search - performs web search
response1 = locator.process_request("Find hospitals in Baltimore")

# Second search with same criteria - uses cache
response2 = locator.process_request("Find hospitals in Baltimore")
```

Cache key includes:
- Location
- Specialization
- Facility type
- Emergency services flag

### Result Limits

```python
# Configure in the code:
response = locator.search_web_for_providers(
    location="Baltimore, MD",
    specialization="diabetes",
    max_results=10  # Adjust as needed
)
```

## 🔌 Integration with Search APIs

### Using Google Custom Search API

```python
import requests

def google_search(query):
    api_key = "YOUR_API_KEY"
    cx = "YOUR_CX_ID"
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query
    }
    response = requests.get(url, params=params)
    results = response.json()

    # Combine result snippets
    text = "\n\n".join([
        f"{item['title']}\n{item['snippet']}"
        for item in results.get('items', [])
    ])
    return text

# Use with locator
locator = RealTimeProviderLocator(web_search_function=google_search)
```

### Using Built-in WebSearch Tool

If you're running in an environment with WebSearch tool:

```python
from agents.provider_locator_realtime import RealTimeProviderLocator

def web_search_wrapper(query):
    # Use the WebSearch tool
    # This would be provided by the environment
    result = WebSearch(query=query)
    return result['text']

locator = RealTimeProviderLocator(web_search_function=web_search_wrapper)
```

## 📈 Performance Optimization

### Tips for Better Performance

1. **Cache Aggressively**
   - Common searches are cached
   - Reduces API calls
   - Faster response times

2. **Optimize Queries**
   - Specific location helps
   - Include relevant keywords
   - Avoid overly broad searches

3. **Limit Results**
   - Request only what you need
   - Default: top 10 results
   - Adjust based on use case

4. **Handle Errors Gracefully**
   - Always have fallback data
   - Inform user of limitations
   - Retry with backoff if needed

## 🧪 Testing

### Test with Example Script

```bash
# Run the full demo
python examples/example_realtime_provider_search.py
```

### Test Individual Components

```python
from agents.provider_locator_realtime import RealTimeProviderLocator

locator = RealTimeProviderLocator()

# Test query building
query = locator.build_search_query(
    location="Baltimore, MD",
    specialization="diabetes",
    facility_type="hospital"
)
print(f"Search query: {query}")

# Test location extraction
location = locator.extract_location_from_text(
    "Find diabetes centers in Baltimore, MD"
)
print(f"Extracted location: {location}")

# Test parsing
sample_text = """
Johns Hopkins Diabetes Center
1234 Medical Drive, Baltimore, MD 21287
Phone: (410) 555-0100
Rating: 4.8 stars
"""
providers = locator.parse_search_results(sample_text)
print(f"Parsed providers: {providers}")
```

## 🎯 Use Cases

### 1. Patient Looking for Care
```python
"I need to find a diabetes specialist near me in Chicago"
→ Returns real diabetes centers in Chicago with current info
```

### 2. Emergency Situations
```python
"Find emergency diabetes care in Boston now"
→ Returns hospitals with emergency services
```

### 3. Insurance-Specific Search
```python
"Find diabetes doctors accepting Blue Cross in Baltimore"
→ Can be enhanced to filter by insurance
```

### 4. Travel Planning
```python
"I'm traveling to Miami, find diabetes care providers there"
→ Returns providers in Miami for travel planning
```

## 🚨 Important Notes

### Disclaimers

- **Verify Information**: Always call provider to confirm details
- **Not Emergency Service**: For emergencies, call 911
- **Insurance**: Confirm insurance acceptance before visiting
- **Hours**: Verify current hours of operation
- **Ratings**: Ratings may not be current

### Data Sources

- Results from web search are parsed and may not be 100% accurate
- Always verify critical information (phone, address, hours)
- Use official provider websites when possible
- Check reviews from multiple sources

### Privacy

- No patient data sent in search queries
- Location information used only for search
- No tracking of search history
- Results not stored long-term

## 🔄 Migration Guide

### Switching from Static to Real-Time

**Step 1**: Test with example script
```bash
python examples/example_realtime_provider_search.py
```

**Step 2**: Update your imports
```python
# Old
from agents.provider_locator_agent import HealthcareProviderLocator

# New
from agents.provider_locator_realtime import RealTimeProviderLocator
```

**Step 3**: Update initialization
```python
# Old
locator = HealthcareProviderLocator()

# New
locator = RealTimeProviderLocator()
```

**Step 4**: Update queries (if needed)
```python
# Now you can use any location!
response = locator.process_request(
    "Find diabetes centers in Seattle, WA"  # Any city works
)
```

### Hybrid Approach

Keep both for different use cases:

```python
# Real-time for production
realtime_locator = RealTimeProviderLocator()

# Static for testing/offline
static_locator = HealthcareProviderLocator()

# Choose based on context
if online_mode:
    locator = realtime_locator
else:
    locator = static_locator
```

## 📚 Additional Resources

### Files Added

- `agents/provider_locator_realtime.py` - Main real-time locator
- `agents/provider_locator_agent_websearch.py` - Alternate implementation
- `examples/example_realtime_provider_search.py` - Demo script
- `REALTIME_SEARCH.md` - This documentation

### Related Documentation

- `README.md` - Main system documentation
- `PROJECT_OVERVIEW.md` - Architecture details
- `QUICKSTART.md` - Getting started guide

## 💡 Future Enhancements

Planned improvements:

1. **Insurance Integration**
   - Filter by insurance plans
   - Check network participation

2. **Availability Check**
   - Real-time appointment availability
   - Online booking integration

3. **Reviews Integration**
   - Pull recent patient reviews
   - Aggregate ratings from multiple sources

4. **Distance Calculation**
   - Calculate actual driving distance
   - Provide directions

5. **Hours Verification**
   - Check if currently open
   - Holiday hours

6. **Multi-Language**
   - Search in multiple languages
   - Translate results

## ❓ FAQ

**Q: Does this work offline?**
A: Yes, it automatically falls back to sample data if web search is unavailable.

**Q: How often is data updated?**
A: Data is fetched in real-time for each search, so it's always current.

**Q: Can I search internationally?**
A: Yes, it works for any location where web search returns results.

**Q: Is this production-ready?**
A: The parsing logic is robust, but always verify critical information.

**Q: How do I add my own search API?**
A: Pass your search function to `RealTimeProviderLocator(web_search_function=your_function)`

**Q: Does this use my real location?**
A: No, you specify the location in your query or context.

---

**Ready to try it?**

```bash
python examples/example_realtime_provider_search.py
```

**Need help?** Check the example script or README.md for more details.
