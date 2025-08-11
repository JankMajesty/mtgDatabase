from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
from typing import Dict, List, Optional, Any
import re
import os

app = Flask(__name__)
CORS(app)

class MTGQueryEngine:
    def __init__(self, db_path: str = "mtg_database.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    
    def get_available_filters(self) -> Dict[str, List[Dict]]:
        """Get all available filter options for the frontend"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        filters = {}
        
        # Get all sets
        cursor.execute("SELECT SetID, SetName, SetCode, ReleaseDate FROM CardSet ORDER BY ReleaseDate")
        filters['sets'] = [dict(row) for row in cursor.fetchall()]
        
        # Get all colors
        cursor.execute("SELECT ColorID, Color FROM Color ORDER BY Color")
        filters['colors'] = [dict(row) for row in cursor.fetchall()]
        
        # Get all rarities
        cursor.execute("SELECT RarityID, RarityName FROM Rarity ORDER BY RarityName")
        filters['rarities'] = [dict(row) for row in cursor.fetchall()]
        
        # Get all card types (excluding "//" type)
        cursor.execute("SELECT CardTypeID, TypeName FROM CardType WHERE TypeName != '//' ORDER BY TypeName")
        filters['card_types'] = [dict(row) for row in cursor.fetchall()]
        
        # Get all subtypes
        cursor.execute("SELECT SubTypeID, SubTypeName FROM SubType ORDER BY SubTypeName")
        filters['subtypes'] = [dict(row) for row in cursor.fetchall()]
        
        # Get all artists
        cursor.execute("SELECT ArtistID, ArtistName FROM Artist ORDER BY ArtistName")
        filters['artists'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return filters
    
    def build_query(self, filters: Dict[str, Any]) -> tuple[str, List[Any]]:
        """Build SQL query from frontend filters"""
        base_query = """
            SELECT DISTINCT 
                c.CardID,
                c.CardName,
                c.ManaCost,
                c.ConvertedManaCost,
                c.Abilities,
                c.FlavorText,
                c.Power,
                c.Toughness,
                c.ImageURL,
                c.Layout,
                c.SuperType,
                a.ArtistName,
                r.RarityName,
                s.SetName,
                s.SetCode,
                s.ReleaseDate,
                GROUP_CONCAT(DISTINCT col.Color) as Colors,
                GROUP_CONCAT(DISTINCT ct.TypeName) as CardTypes,
                GROUP_CONCAT(DISTINCT st.SubTypeName) as SubTypes
            FROM Card c
            JOIN Artist a ON c.ArtistID = a.ArtistID
            JOIN Rarity r ON c.RarityID = r.RarityID
            JOIN CardSet s ON c.SetID = s.SetID
            LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
            LEFT JOIN Color col ON cc.ColorID = col.ColorID
            LEFT JOIN Card_CardType cct ON c.CardID = cct.CardID
            LEFT JOIN CardType ct ON cct.CardTypeID = ct.CardTypeID
            LEFT JOIN Card_SubType cst ON c.CardID = cst.CardID
            LEFT JOIN SubType st ON cst.SubTypeID = st.SubTypeID
        """
        
        where_conditions = []
        params = []
        
        # Card name search
        if filters.get('card_name'):
            where_conditions.append("c.CardName LIKE ?")
            params.append(f"%{filters['card_name']}%")
        
        # Set filter
        if filters.get('sets') and len(filters['sets']) > 0:
            set_ids = [str(sid) for sid in filters['sets']]
            where_conditions.append(f"c.SetID IN ({','.join(['?'] * len(set_ids))})")
            params.extend(set_ids)
        
        # Color filter
        if filters.get('colors') and len(filters['colors']) > 0:
            color_ids = [str(cid) for cid in filters['colors']]
            where_conditions.append(f"cc.ColorID IN ({','.join(['?'] * len(color_ids))})")
            params.extend(color_ids)
        
        # Rarity filter
        if filters.get('rarities') and len(filters['rarities']) > 0:
            rarity_ids = [str(rid) for rid in filters['rarities']]
            where_conditions.append(f"c.RarityID IN ({','.join(['?'] * len(rarity_ids))})")
            params.extend(rarity_ids)
        
        # Card type filter
        if filters.get('card_types') and len(filters['card_types']) > 0:
            type_ids = [str(tid) for tid in filters['card_types']]
            where_conditions.append(f"cct.CardTypeID IN ({','.join(['?'] * len(type_ids))})")
            params.extend(type_ids)
        
        # Subtype filter
        if filters.get('subtypes') and len(filters['subtypes']) > 0:
            subtype_ids = [str(stid) for stid in filters['subtypes']]
            where_conditions.append(f"cst.SubTypeID IN ({','.join(['?'] * len(subtype_ids))})")
            params.extend(subtype_ids)
        
        # Artist filter
        if filters.get('artists') and len(filters['artists']) > 0:
            artist_ids = [str(aid) for aid in filters['artists']]
            where_conditions.append(f"c.ArtistID IN ({','.join(['?'] * len(artist_ids))})")
            params.extend(artist_ids)
        
        # Converted mana cost range
        if filters.get('cmc_min') is not None:
            where_conditions.append("c.ConvertedManaCost >= ?")
            params.append(filters['cmc_min'])
        
        if filters.get('cmc_max') is not None:
            where_conditions.append("c.ConvertedManaCost <= ?")
            params.append(filters['cmc_max'])
        
        # Power/Toughness filters
        if filters.get('power_min') is not None:
            where_conditions.append("CAST(c.Power AS REAL) >= ?")
            params.append(filters['power_min'])
        
        if filters.get('power_max') is not None:
            where_conditions.append("CAST(c.Power AS REAL) <= ?")
            params.append(filters['power_max'])
        
        if filters.get('toughness_min') is not None:
            where_conditions.append("CAST(c.Toughness AS REAL) >= ?")
            params.append(filters['toughness_min'])
        
        if filters.get('toughness_max') is not None:
            where_conditions.append("CAST(c.Toughness AS REAL) <= ?")
            params.append(filters['toughness_max'])
        
        # Add WHERE clause if conditions exist
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        # Add GROUP BY and ORDER BY
        base_query += " GROUP BY c.CardID ORDER BY c.CardName"
        
        # Add LIMIT if specified
        if filters.get('limit'):
            base_query += f" LIMIT {filters['limit']}"
        else:
            base_query += " LIMIT 100"  # Default limit
        
        return base_query, params
    
    def search_cards(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Search cards based on filters"""
        try:
            query, params = self.build_query(filters)
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            
            # Get total count for pagination  
            # Simplified count query - just count the main table with filters
            count_query = """
                SELECT COUNT(DISTINCT c.CardID) as total
                FROM Card c
                JOIN Artist a ON c.ArtistID = a.ArtistID
                JOIN Rarity r ON c.RarityID = r.RarityID
                JOIN CardSet s ON c.SetID = s.SetID
                LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
                LEFT JOIN Color col ON cc.ColorID = col.ColorID
                LEFT JOIN Card_CardType cct ON c.CardID = cct.CardID
                LEFT JOIN CardType ct ON cct.CardTypeID = ct.CardTypeID
                LEFT JOIN Card_SubType cst ON c.CardID = cst.CardID
                LEFT JOIN SubType st ON cst.SubTypeID = st.SubTypeID
            """
            
            # Add the same WHERE conditions as the main query
            where_conditions = []
            count_params = []
            
            # Card name search
            if filters.get('card_name'):
                where_conditions.append("c.CardName LIKE ?")
                count_params.append(f"%{filters['card_name']}%")
            
            # Set filter
            if filters.get('sets') and len(filters['sets']) > 0:
                set_ids = [str(sid) for sid in filters['sets']]
                where_conditions.append(f"c.SetID IN ({','.join(['?'] * len(set_ids))})")
                count_params.extend(set_ids)
            
            # Color filter
            if filters.get('colors') and len(filters['colors']) > 0:
                color_ids = [str(cid) for cid in filters['colors']]
                where_conditions.append(f"cc.ColorID IN ({','.join(['?'] * len(color_ids))})")
                count_params.extend(color_ids)
            
            # Rarity filter
            if filters.get('rarities') and len(filters['rarities']) > 0:
                rarity_ids = [str(rid) for rid in filters['rarities']]
                where_conditions.append(f"c.RarityID IN ({','.join(['?'] * len(rarity_ids))})")
                count_params.extend(rarity_ids)
            
            # Card type filter
            if filters.get('card_types') and len(filters['card_types']) > 0:
                type_ids = [str(tid) for tid in filters['card_types']]
                where_conditions.append(f"cct.CardTypeID IN ({','.join(['?'] * len(type_ids))})")
                count_params.extend(type_ids)
            
            # Subtype filter
            if filters.get('subtypes') and len(filters['subtypes']) > 0:
                subtype_ids = [str(stid) for stid in filters['subtypes']]
                where_conditions.append(f"cst.SubTypeID IN ({','.join(['?'] * len(subtype_ids))})")
                count_params.extend(subtype_ids)
            
            # Artist filter
            if filters.get('artists') and len(filters['artists']) > 0:
                artist_ids = [str(aid) for aid in filters['artists']]
                where_conditions.append(f"c.ArtistID IN ({','.join(['?'] * len(artist_ids))})")
                count_params.extend(artist_ids)
            
            # Converted mana cost range
            if filters.get('cmc_min') is not None:
                where_conditions.append("c.ConvertedManaCost >= ?")
                count_params.append(filters['cmc_min'])
            
            if filters.get('cmc_max') is not None:
                where_conditions.append("c.ConvertedManaCost <= ?")
                count_params.append(filters['cmc_max'])
            
            # Power/Toughness filters
            if filters.get('power_min') is not None:
                where_conditions.append("CAST(c.Power AS REAL) >= ?")
                count_params.append(filters['power_min'])
            
            if filters.get('power_max') is not None:
                where_conditions.append("CAST(c.Power AS REAL) <= ?")
                count_params.append(filters['power_max'])
            
            if filters.get('toughness_min') is not None:
                where_conditions.append("CAST(c.Toughness AS REAL) >= ?")
                count_params.append(filters['toughness_min'])
            
            if filters.get('toughness_max') is not None:
                where_conditions.append("CAST(c.Toughness AS REAL) <= ?")
                count_params.append(filters['toughness_max'])
            
            # Add WHERE clause if conditions exist
            if where_conditions:
                count_query += " WHERE " + " AND ".join(where_conditions)
            
            cursor.execute(count_query, count_params)
            total_count = cursor.fetchone()['total']
            
            conn.close()
            
            return {
                'success': True,
                'cards': results,
                'total': total_count,
                'query': query,  # For debugging
                'params': params  # For debugging
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'cards': [],
                'total': 0
            }

# Initialize the query engine
query_engine = MTGQueryEngine()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/<path:path>')
def serve_react(path):
    """Serve React app routes"""
    return render_template('index.html')

@app.route('/api/filters', methods=['GET'])
def get_filters():
    """Get all available filter options"""
    try:
        filters = query_engine.get_available_filters()
        return jsonify({'success': True, 'filters': filters})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/search', methods=['POST'])
def search_cards():
    """Search cards based on filters"""
    try:
        filters = request.json
        result = query_engine.search_cards(filters)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/card/<int:card_id>', methods=['GET'])
def get_card_details(card_id):
    """Get detailed information for a specific card"""
    try:
        conn = query_engine.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                c.*,
                a.ArtistName,
                r.RarityName,
                s.SetName,
                s.SetCode,
                s.ReleaseDate,
                GROUP_CONCAT(DISTINCT col.Color) as Colors,
                GROUP_CONCAT(DISTINCT ct.TypeName) as CardTypes,
                GROUP_CONCAT(DISTINCT st.SubTypeName) as SubTypes
            FROM Card c
            JOIN Artist a ON c.ArtistID = a.ArtistID
            JOIN Rarity r ON c.RarityID = r.RarityID
            JOIN CardSet s ON c.SetID = s.SetID
            LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
            LEFT JOIN Color col ON cc.ColorID = col.ColorID
            LEFT JOIN Card_CardType cct ON c.CardID = cct.CardID
            LEFT JOIN CardType ct ON cct.CardTypeID = ct.CardTypeID
            LEFT JOIN Card_SubType cst ON c.CardID = cst.CardID
            LEFT JOIN SubType st ON cst.SubTypeID = st.SubTypeID
            WHERE c.CardID = ?
            GROUP BY c.CardID
        """
        
        cursor.execute(query, (card_id,))
        card = cursor.fetchone()
        
        conn.close()
        
        if card:
            return jsonify({'success': True, 'card': dict(card)})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Use environment variable for port (Render requirement)
    port = int(os.environ.get('PORT', 8001))
    app.run(debug=False, host='0.0.0.0', port=port)
