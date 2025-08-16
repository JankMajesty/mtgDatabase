# Retrieve top 10 cards by toughness
_Exported on 8/15/2025 at 18:55:48 CDT from Cursor (1.4.5)_

---

**User**

I want to write a select statement that pulls cards descending from the highest toughness descending and limit to 10 cards.

---

**Cursor**

I'll help you write a SELECT statement to pull cards with the highest toughness in descending order, limited to 10 cards. First, let me examine the database schema to understand the table structure.


Perfect! I can see the database schema. The `Card` table has a `Toughness` field that stores toughness values. Based on the schema, here's the SELECT statement you need:

```sql
SELECT 
    c.CardName,
    c.Toughness,
    c.Power,
    c.ManaCost,
    c.ConvertedManaCost,
    s.SetName,
    r.RarityName,
    a.ArtistName
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
JOIN Artist a ON c.ArtistID = a.ArtistID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

This query:

1. **Selects key card information** including name, toughness, power, mana cost, converted mana cost, set name, rarity, and artist
2. **Joins related tables** to get meaningful information instead of just IDs
3. **Filters out null/empty toughness values** and special characters like '*' (which some cards use for variable toughness)
4. **Orders by toughness descending** using `CAST(c.Toughness AS INTEGER)` to ensure proper numeric sorting
5. **Limits to 10 results** as requested

**Note**: The `CAST(c.Toughness AS INTEGER)` is necessary because the toughness field is stored as TEXT in your schema (which allows for special values like '*' or '+1/+1' counters), but we want to sort numerically for the highest values.

If you want a simpler version that just shows the card name and toughness, you could use:

```sql
SELECT CardName, Toughness
FROM Card
WHERE Toughness IS NOT NULL 
    AND Toughness != ''
    AND Toughness != '*'
ORDER BY CAST(Toughness AS INTEGER) DESC
LIMIT 10;
```

```sql
SELECT 
    c.CardName,
    c.Toughness,
    c.Power,
    c.ManaCost,
    c.ConvertedManaCost,
    s.SetName,
    r.RarityName,
    a.ArtistName
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
JOIN Artist a ON c.ArtistID = a.ArtistID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

```sql
SELECT CardName, Toughness
FROM Card
WHERE Toughness IS NOT NULL 
    AND Toughness != ''
    AND Toughness != '*'
ORDER BY CAST(Toughness AS INTEGER) DESC
LIMIT 10;
```

---

**User**

Can we import the columns "CardName" as "Card Name", "Toughness" as "Toughness", "Power" as "Power", "ManaCost" as "Mana Cost", "ConvertedManaCost" as "CMC", "SetName" as Set Name", and "RarityName" as "Rarity". I don't need "ArtistName" column.

---

**Cursor**

Absolutely! Here's the updated SELECT statement with the column aliases you requested:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.Toughness AS "Toughness",
    c.Power AS "Power",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    s.SetName AS "Set Name",
    r.RarityName AS "Rarity"
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

This query now:
- **Removes the ArtistName column** as requested
- **Uses the exact column aliases** you specified:
  - `CardName` → `"Card Name"`
  - `Toughness` → `"Toughness"`
  - `Power` → `"Power"`
  - `ManaCost` → `"Mana Cost"`
  - `ConvertedManaCost` → `"CMC"`
  - `SetName` → `"Set Name"`
  - `RarityName` → `"Rarity"`
- **Maintains the same logic** for filtering and sorting by highest toughness
- **Still limits to 10 results** as originally requested

The double quotes around the aliases ensure that spaces in column names are preserved correctly in the output.

```sql
SELECT 
    c.CardName AS "Card Name",
    c.Toughness AS "Toughness",
    c.Power AS "Power",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    s.SetName AS "Set Name",
    r.RarityName AS "Rarity"
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

---

**User**

can we add a column for "Abilities" as "Abilities" and "FlavorText" as "Flavor Text"

---

**Cursor**

Absolutely! Here's the updated SELECT statement with the additional columns for Abilities and Flavor Text:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.Toughness AS "Toughness",
    c.Power AS "Power",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    c.Abilities AS "Abilities",
    c.FlavorText AS "Flavor Text",
    s.SetName AS "Set Name",
    r.RarityName AS "Rarity"
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

Now the query includes:
- **All the previous columns** with their aliases
- **`c.Abilities AS "Abilities"`** - displays the card's abilities
- **`c.FlavorText AS "Flavor Text"`** - displays the flavor text

This will give you a comprehensive view of the top 10 cards by toughness, including their abilities and flavor text for more complete card information.

```sql
SELECT 
    c.CardName AS "Card Name",
    c.Toughness AS "Toughness",
    c.Power AS "Power",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    c.Abilities AS "Abilities",
    c.FlavorText AS "Flavor Text",
    s.SetName AS "Set Name",
    r.RarityName AS "Rarity"
FROM Card c
JOIN CardSet s ON c.SetID = s.SetID
JOIN Rarity r ON c.RarityID = r.RarityID
WHERE c.Toughness IS NOT NULL 
    AND c.Toughness != ''
    AND c.Toughness != '*'
ORDER BY CAST(c.Toughness AS INTEGER) DESC
LIMIT 10;
```

