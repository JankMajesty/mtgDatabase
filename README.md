# MTG Card Database - Advanced Search

A modern web application for searching Magic: The Gathering cards from Urza's Block through Invasion Block, featuring a vanilla JavaScript frontend with Flask backend API.

## 🃏 Features

- **🔍 Advanced Search Interface**: Build complex queries using a user-friendly interface that mimics SQL SELECT statements
- **🎯 Multiple Filter Options**: Search by card name, set, color, rarity, card type, subtype, artist, and more
- **📊 Range Filters**: Filter by converted mana cost, power, and toughness with min/max ranges
- **⚡ Real-time Results**: See search results instantly with card images and detailed information
- **💻 SQL Preview**: View the generated SQL query for educational purposes
- **📱 Responsive Design**: Modern UI that works on desktop and mobile devices
- **🎨 Beautiful Card Display**: Card grid with hover effects and detailed card information

## 🚀 Quick Start

### Prerequisites
- Python 3.11+

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd mtgDatabase
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
# OR using uv:
uv sync
```

### Running the Application

1. **Start the Flask application:**
```bash
python3 app.py
# OR using uv:
uv run python app.py
```
The application will be available at `http://localhost:8001`

2. **Open your browser and navigate to `http://localhost:8001`**

## 🗄️ Database Coverage

The database includes cards from these MTG sets:
- **Urza's Block**: Urza's Saga, Urza's Legacy, Urza's Destiny
- **Masques Block**: Mercadian Masques, Nemesis, Prophecy  
- **Invasion Block**: Invasion, Planeshift, Apocalypse

**Total**: ~1,908 cards with complete metadata

## 🔍 Search Capabilities

### Text Search
- **Card Name**: Partial matching (e.g., "Lightning" finds "Lightning Bolt")

### Multi-Select Filters
- **Sets**: Filter by specific MTG sets
- **Colors**: White, Blue, Black, Red, Green
- **Rarities**: Common, Uncommon, Rare
- **Card Types**: Creature, Instant, Sorcery, Enchantment, Artifact, Land
- **Subtypes**: Goblin, Elf, Dragon, etc.
- **Artists**: Filter by card artist

### Range Filters
- **Converted Mana Cost**: Min/max mana cost
- **Power**: Min/max power for creatures
- **Toughness**: Min/max toughness for creatures

### Advanced Features
- **Combined Queries**: Mix any combination of filters
- **SQL Preview**: See the actual database query being executed
- **Result Limits**: Control number of results returned

## 🏗️ Architecture

### Backend (Flask)
- **API Endpoints**: RESTful API for card data and filtering
- **Database Layer**: SQLite with optimized queries
- **CORS Support**: Enables frontend-backend communication

### Frontend (Vanilla JavaScript)
- **Modern JavaScript**: ES6+ features with async/await
- **Responsive UI**: CSS Grid and Flexbox layouts
- **Modular Structure**: Organized functions for search and display
- **Dynamic DOM**: Real-time filter population and results rendering

### Database Schema
```sql
Card              - Main card information
├── Artist        - Card artists  
├── CardSet       - MTG sets and release info
├── Rarity        - Card rarities
├── Color         - Card colors (WUBRG)
├── CardType      - Types (Creature, Instant, etc.)
└── SubType       - Subtypes (Goblin, Elf, etc.)
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/filters` | Get all available filter options |
| `POST` | `/api/search` | Search cards with filters |
| `GET` | `/api/card/<id>` | Get detailed card information |

### Example API Usage

**Search for red creatures from Urza's Saga:**
```bash
curl -X POST http://localhost:8001/api/search \
  -H "Content-Type: application/json" \
  -d '{"sets": [1], "colors": [5], "card_types": [2]}'
```

## 🛠️ Technology Stack

- **Backend**: Flask, SQLite, Python 3.11+
- **Frontend**: Vanilla JavaScript ES6+, HTML5, CSS3
- **Styling**: Modern CSS3 with gradients and animations
- **Icons**: Font Awesome icon library
- **HTTP Client**: Native Fetch API

## 📁 Project Structure

```
mtgDatabase/
├── app.py                 # Flask backend server
├── main.py               # Database population script
├── mtg_database.db        # SQLite database
├── mtgSchema.sql         # Database schema
├── requirements.txt       # Python dependencies
├── templates/            # Frontend templates
│   ├── index.html        # Main HTML page
│   ├── css/
│   │   └── styles.css    # Application styles
│   └── js/
│       └── main.js       # Frontend JavaScript
├── Procfile              # Deployment configuration
└── README.md             # This file
```

## 🚀 Development

### Adding New Features
1. **Backend**: Add new API endpoints in `app.py`
2. **Frontend**: Modify `templates/js/main.js` for new functionality
3. **Database**: Use `update_schema.py` for schema changes

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use modern ES6+ syntax with async/await
- **HTML/CSS**: Semantic markup with responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed.

---

**Built with ❤️ for Magic: The Gathering enthusiasts**