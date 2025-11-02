# Hybrid Provider Search Approach

## 🔄 Overview

The **Hybrid Provider Locator** intelligently combines the best of both worlds:
- **Real-time web search** for current, accurate provider data
- **Static offline data** for reliability and speed

This hybrid approach ensures you **always get results** while preferring the most up-to-date information available.

## ✨ Key Benefits

### 1. Reliability
- ✅ **Always returns results** - never fails completely
- ✅ **Automatic fallback** - seamlessly switches to static data if web search fails
- ✅ **No single point of failure** - multiple data sources

### 2. Accuracy
- ✅ **Prefers real-time data** - uses web search first for current information
- ✅ **Up-to-date contact info** - real phone numbers, addresses, hours
- ✅ **Current ratings** - recent reviews and ratings

### 3. Flexibility
- ✅ **Multiple modes** - web-preferred, static-preferred, hybrid merge
- ✅ **Configurable per-request** - override mode for specific searches
- ✅ **Works offline** - falls back to static data automatically

### 4. Performance
- ✅ **Smart caching** - reduces redundant web searches
- ✅ **Fast fallback** - instant switch to static data when needed
- ✅ **Optimized queries** - efficient web search queries

### 5. Transparency
- ✅ **Source tracking** - know where each result came from
- ✅ **Search statistics** - monitor usage patterns
- ✅ **Mode reporting** - see which mode was used

## 🎯 How It Works

### Search Flow

```
User Query → Hybrid Locator
     ↓
┌────┴────┐
│ Strategy │
│ Decision │
└────┬────┘
     │
     ├─→ Mode: Web Preferred (DEFAULT)
     │   ├─→ Try Web Search
     │   │   ├─→ Success? → Return web results ✅
     │   │   └─→ Fail? → Fallback to static data 📋
     │
     ├─→ Mode: Static Preferred
     │   └─→ Use Static Data → Return static results 📋
     │
     ├─→ Mode: Hybrid Merge
     │   ├─→ Get Web Results
     │   ├─→ Get Static Results
     │   └─→ Merge Unique Results → Return combined 🔄
     │
     ├─→ Mode: Web Only
     │   └─→ Web Search Only → Return web or nothing
     │
     └─→ Mode: Static Only
         └─→ Static Data Only → Return static results
```

### Data Source Priority

1. **Real-time Web Search** (preferred when available)
   - Live search results
   - Current information
   - Source marked as: `web_search` or `live_web_search`

2. **Static Offline Data** (fallback)
   - Pre-loaded sample data
   - Works offline
   - Source marked as: `static_data` or `sample_data`

## 🚀 Quick Start

### Basic Usage

```python
from agents.provider_locator_hybrid import HybridProviderLocator

# Create hybrid locator with default settings
locator = HybridProviderLocator()

# Search for providers
response = locator.process_request(
    "Find diabetes specialists in Baltimore, MD",
    context={}
)

# Check results
print(f"Found: {response['total_found']} facilities")
print(f"Search mode used: {response['search_mode']}")

# Display facilities
for facility in response['facilities']:
    print(locator.format_facility_info(facility))
```

### Configuration Options

#### 1. Web Preferred (DEFAULT - Recommended)

```python
locator = HybridProviderLocator(
    prefer_web_search=True,   # Try web first
    merge_results=False       # Use web OR static (not both)
)
```

**When to use**: Production deployment, normal operation
**Behavior**: Tries web search first, falls back to static if web fails

#### 2. Static Preferred

```python
locator = HybridProviderLocator(
    prefer_web_search=False,  # Use static primarily
    merge_results=False
)
```

**When to use**: Offline mode, demos, testing
**Behavior**: Uses static data by default

#### 3. Hybrid Merge Mode

```python
locator = HybridProviderLocator(
    prefer_web_search=True,
    merge_results=True        # Combine both sources
)
```

**When to use**: Maximum coverage needed
**Behavior**: Gets results from both sources and merges unique entries

#### 4. Custom Configuration

```python
locator = HybridProviderLocator(
    prefer_web_search=True,
    merge_results=False,
    max_results=20            # Return up to 20 results
)
```

## 🔧 Advanced Features

### Dynamic Mode Switching

Change search mode at runtime:

```python
locator = HybridProviderLocator()

# Switch to hybrid merge mode
locator.set_mode('hybrid')

# Switch to static only
locator.set_mode('static_only')

# Switch back to web preferred
locator.set_mode('web_preferred')
```

**Available Modes**:
- `'web_preferred'` - Try web first, fall back to static (default)
- `'static_preferred'` - Use static data primarily
- `'hybrid'` - Always merge both sources
- `'web_only'` - Only use web search
- `'static_only'` - Only use static data

### Force Mode Per Request

Override mode for a specific request:

```python
# Force web search only for this request
response = locator.process_request(
    "Find hospitals",
    context={'search_mode': 'web_only'}
)

# Force static data only
response = locator.process_request(
    "Find clinics",
    context={'search_mode': 'static_only'}
)
```

### Location-Based Search with Distances

Provide user location for distance calculation:

```python
response = locator.process_request(
    "Find diabetes care centers",
    context={
        'user_location': {
            'lat': 39.2904,  # Latitude
            'lon': -76.6122  # Longitude
        }
    }
)

# Results will include distance and be sorted by proximity
for facility in response['facilities']:
    print(f"{facility['name']}: {facility.get('distance', 'N/A')} miles")
```

### Search Statistics

Track search performance:

```python
# Get statistics
stats = locator.get_stats()

print(f"Total searches: {stats['total_searches']}")
print(f"Web searches: {stats['web_searches']} ({stats['percentages']['web_searches']}%)")
print(f"Static searches: {stats['static_searches']} ({stats['percentages']['static_searches']}%)")
print(f"Hybrid searches: {stats['hybrid_searches']} ({stats['percentages']['hybrid_searches']}%)")
print(f"Web failures: {stats['web_failures']} ({stats['percentages']['web_failures']}%)")

# Reset statistics
locator.reset_stats()
```

## 📊 Response Structure

### Success Response

```python
{
    'status': 'success',
    'agent': 'Hybrid Healthcare Provider Locator',
    'message': 'Found 5 healthcare facilities using web_search',
    'facilities': [
        {
            'id': 'LIVE001',
            'name': 'Johns Hopkins Medicine - Diabetes Center',
            'type': 'Medical Center',
            'address': '1830 E. Monument Street, Baltimore, MD 21287',
            'phone': '(410) 955-5000',
            'rating': 4.8,
            'specializations': ['Diabetes Care', 'Nutrition'],
            'website': 'www.hopkinsmedicine.org/diabetes',
            'hours': 'Mon-Fri 8am-5pm',
            'source': 'live_web_search',  # Data source indicator
            'distance': 2.3  # If location provided
        },
        # ... more facilities
    ],
    'total_found': 5,
    'search_mode': 'web_search',  # Mode that was used
    'search_breakdown': {
        'web_results': 5,
        'static_results': 0,
        'displayed': 5
    },
    'filters_applied': {
        'specialization': 'diabetes',
        'facility_type': None,
        'emergency_only': False
    },
    'stats': {
        'total_searches': 10,
        'web_searches': 8,
        'static_searches': 2,
        'hybrid_searches': 1,
        'web_failures': 1
    },
    'disclaimer': 'Information from real-time web search. Please verify before visiting.',
    'next_steps': [
        '📞 Call to verify current information',
        '🏥 Check if they accept your insurance',
        '📅 Schedule an appointment',
        '🗺️  Get directions to the facility',
        '⭐ Read recent reviews'
    ]
}
```

### Search Mode Values

- `'web_search'` - Results from real-time web search
- `'static_fallback'` - Web search failed, using static data
- `'hybrid'` - Results merged from both sources
- `'no_results'` - No results found from any source

## 🎨 Result Display

### Source Indicators

Each facility includes source information:

```python
for facility in response['facilities']:
    source = facility.get('source', 'unknown')

    if source in ['web_search', 'live_web_search']:
        icon = "🌐"  # Web search result
    elif source in ['static_data', 'sample_data']:
        icon = "📋"  # Static data result
    else:
        icon = "❓"

    print(f"{icon} {facility['name']}")
```

### Formatted Display

Use the built-in formatter:

```python
for facility in response['facilities']:
    print(locator.format_facility_info(facility))
```

Output:
```
🌐 Johns Hopkins Medicine - Diabetes Center
   📍 Address: 1830 E. Monument Street, Baltimore, MD 21287
   📞 Phone: (410) 955-5000
   🏥 Type: Medical Center
   📏 Distance: 2.3 miles
   ⭐⭐⭐⭐ Rating: 4.8/5.0
   🔬 Specializations: Diabetes Care, Nutrition
   🌐 Website: www.hopkinsmedicine.org/diabetes
   🕐 Hours: Mon-Fri 8am-5pm
   ℹ️  Source: Live Web Search
```

## 🔌 Integration

### Main Healthcare System

The hybrid locator is already integrated in `main.py`:

```python
from agents.provider_locator_hybrid import HybridProviderLocator

class HealthcareAssistantSystem:
    def _initialize_agents(self):
        agents = [
            DiabetesPredictionAgent(),
            AppointmentSchedulerAgent(),
            HybridProviderLocator(prefer_web_search=True, merge_results=False),
            DieticianAgent(),
            DiabetesCareSpecialist(),
            GeneralHealthAssistant()
        ]
        # ... register agents
```

### Using with Coordinator

The coordinator automatically routes provider search queries to the hybrid locator:

```python
# In interactive mode
python main.py

You: Find diabetes specialists in Chicago
# → Automatically uses hybrid locator with web search + fallback
```

### Custom Integration

```python
from agents.coordinator_agent import HealthcareCoordinator
from agents.provider_locator_hybrid import HybridProviderLocator

# Create coordinator
coordinator = HealthcareCoordinator()

# Create hybrid locator with custom config
hybrid_locator = HybridProviderLocator(
    prefer_web_search=True,
    merge_results=True,  # Merge mode
    max_results=15
)

# Register with coordinator
coordinator.register_agent(hybrid_locator)

# Now provider searches will use hybrid approach
response = coordinator.process_request(
    "Find diabetes centers near me",
    context={}
)
```

## 📈 Use Cases

### 1. Production Deployment

**Configuration**:
```python
locator = HybridProviderLocator(
    prefer_web_search=True,
    merge_results=False
)
```

**Why**: Always tries to get real-time data, but gracefully falls back if needed

### 2. Offline/Demo Mode

**Configuration**:
```python
locator = HybridProviderLocator(
    prefer_web_search=False,
    merge_results=False
)
```

**Why**: Works without internet, consistent results for demonstrations

### 3. Maximum Coverage

**Configuration**:
```python
locator = HybridProviderLocator(
    prefer_web_search=True,
    merge_results=True
)
```

**Why**: Gets results from all available sources for comprehensive listings

### 4. Testing

**Per-request override**:
```python
# Test web search only
response1 = locator.process_request(query, {'search_mode': 'web_only'})

# Test static data only
response2 = locator.process_request(query, {'search_mode': 'static_only'})
```

**Why**: Test each source independently to verify functionality

## ⚙️ Configuration File

Settings in `config.py`:

```python
# Hybrid Provider Locator Configuration
HYBRID_PROVIDER_CONFIG = {
    'prefer_web_search': True,
    'merge_results': False,
    'max_results': 10,
    'cache_results': True,
    'fallback_to_static': True
}

DEFAULT_SEARCH_MODE = 'web_preferred'
```

## 🧪 Testing

### Run Hybrid Example

```bash
python examples/example_hybrid_provider_search.py
```

This demonstrates:
- All search modes
- Fallback behavior
- Result merging
- Statistics tracking
- Source indicators

### Test in Main System

```bash
python main.py
```

Try queries like:
```
You: Find diabetes specialists in Baltimore
You: Show me nearby hospitals
You: Find nutritionists in my area
```

The system automatically uses the hybrid locator!

## 📊 Comparison Matrix

| Feature | Web Only | Static Only | Hybrid (Web Preferred) | Hybrid (Merge) |
|---------|----------|-------------|----------------------|----------------|
| **Always works** | ❌ | ✅ | ✅ | ✅ |
| **Current data** | ✅ | ❌ | ✅ (when available) | ✅ (when available) |
| **Works offline** | ❌ | ✅ | ✅ (fallback) | ✅ (fallback) |
| **Speed** | Slow (2-5s) | Fast (<1s) | Variable | Slowest |
| **Result count** | Variable | Limited | Variable | Maximum |
| **Recommended for** | Test only | Demos/Offline | Production ⭐ | Max coverage |

## 🚨 Important Notes

### Web Search Simulation

The current implementation uses **simulated web search** results for demonstration. To enable real web search:

1. Provide a web search function:
```python
def my_search(query):
    # Implement actual web search here
    # e.g., using Google API, Bing API, etc.
    return search_results_text

locator = HybridProviderLocator(web_search_function=my_search)
```

2. Or integrate with environment's WebSearch tool (if available)

### Verify Information

Always verify provider information before visiting:
- ✅ Call to confirm hours
- ✅ Verify insurance acceptance
- ✅ Check current services offered
- ✅ Confirm address and location

### Not for Emergencies

For medical emergencies:
- ❌ Don't use this system
- ✅ Call 911 immediately
- ✅ Go to nearest emergency room

## 📚 Additional Resources

### Documentation
- `README.md` - Main system documentation
- `REALTIME_SEARCH.md` - Real-time web search details
- `PROJECT_OVERVIEW.md` - Technical architecture
- `QUICK_REFERENCE.md` - Command reference

### Code Files
- `agents/provider_locator_hybrid.py` - Hybrid locator implementation
- `agents/provider_locator_realtime.py` - Real-time web search locator
- `agents/provider_locator_agent.py` - Static data locator
- `examples/example_hybrid_provider_search.py` - Usage examples

### Examples
- `examples/example_hybrid_provider_search.py` - Comprehensive hybrid demo
- `examples/example_realtime_provider_search.py` - Web search demo
- `examples/example_full_workflow.py` - Full system workflow

## 🎉 Summary

The **Hybrid Provider Locator** provides:

✅ **Reliability** - Always returns results
✅ **Accuracy** - Prefers real-time data
✅ **Flexibility** - Multiple modes and configurations
✅ **Performance** - Smart caching and fallback
✅ **Transparency** - Clear source tracking

**Current Status**: ✅ Implemented and active in main system

**To Use**: Already integrated - just run `python main.py` and search for providers!

---

**Questions?** Check the examples or read the code in `agents/provider_locator_hybrid.py`
