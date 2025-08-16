# Select cards with multiple colors and subtypes
_Exported on 8/15/2025 at 18:56:12 CDT from Cursor (1.4.5)_

---

**User**

I would liek to write a select statement that gets all cards that have multiple colors and subtypes

---

**Cursor**

I'll help you write a SELECT statement to get all cards that have multiple colors and subtypes. First, let me examine the database schema to understand the structure of the tables and how colors and subtypes are stored.


Perfect! Now I can see the database structure. Based on the schema, I can write a SELECT statement that finds cards with multiple colors and subtypes. The database uses junction tables (`Card_Color` and `Card_SubType`) to represent many-to-many relationships between cards and their colors/subtypes.

Here's a SELECT statement that will get all cards that have multiple colors AND multiple subtypes:

```sql
SELECT 
    c.CardID,
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    c.Power,
    c.Toughness,
    GROUP_CONCAT(DISTINCT col.Color) AS Colors,
    GROUP_CONCAT(DISTINCT st.SubTypeName) AS SubTypes,
    COUNT(DISTINCT cc.ColorID) AS ColorCount,
    COUNT(DISTINCT cst.SubTypeID) AS SubTypeCount
FROM Card c
JOIN Card_Color cc ON c.CardID = cc.CardID
JOIN Color col ON cc.ColorID = col.ColorID
JOIN Card_SubType cst ON c.CardID = cst.CardID
JOIN SubType st ON cst.SubTypeID = st.SubTypeID
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost, c.Power, c.Toughness
HAVING COUNT(DISTINCT cc.ColorID) > 1 
   AND COUNT(DISTINCT cst.SubTypeID) > 1
ORDER BY c.CardName;
```

This query:

1. **Joins** the `Card` table with the junction tables for colors and subtypes
2. **Groups** the results by card to aggregate the colors and subtypes
3. **Uses HAVING** to filter for cards with more than 1 color AND more than 1 subtype
4. **Returns** useful information including the card details, all colors, all subtypes, and counts
5. **Orders** results alphabetically by card name

If you want a simpler version that just gets the card IDs and names:

```sql
SELECT DISTINCT c.CardID, c.CardName
FROM Card c
WHERE (
    SELECT COUNT(*) FROM Card_Color cc WHERE cc.CardID = c.CardID
) > 1
AND (
    SELECT COUNT(*) FROM Card_SubType cst WHERE cst.CardID = c.CardID
) > 1
ORDER BY c.CardName;
```

The first query gives you more detailed information, while the second is more concise if you just need the basic card identification.

```sql
SELECT 
    c.CardID,
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    c.Power,
    c.Toughness,
    GROUP_CONCAT(DISTINCT col.Color) AS Colors,
    GROUP_CONCAT(DISTINCT st.SubTypeName) AS SubTypes,
    COUNT(DISTINCT cc.ColorID) AS ColorCount,
    COUNT(DISTINCT cst.SubTypeID) AS SubTypeCount
FROM Card c
JOIN Card_Color cc ON c.CardID = cc.CardID
JOIN Color col ON cc.ColorID = col.ColorID
JOIN Card_SubType cst ON c.CardID = cst.CardID
JOIN SubType st ON cst.SubTypeID = st.SubTypeID
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost, c.Power, c.Toughness
HAVING COUNT(DISTINCT cc.ColorID) > 1 
   AND COUNT(DISTINCT cst.SubTypeID) > 1
ORDER BY c.CardName;
```

```sql
SELECT DISTINCT c.CardID, c.CardName
FROM Card c
WHERE (
    SELECT COUNT(*) FROM Card_Color cc WHERE cc.CardID = c.CardID
) > 1
AND (
    SELECT COUNT(*) FROM Card_SubType cst WHERE cst.CardID = c.CardID
) > 1
ORDER BY c.CardName;
```

---

**User**

I don't need the column for "CardID". Can we use the aliases "CardName" as "Card Name", "ManaCost" as "Mana Cost", "ConvertedManaCost" as "CMC", "ColorCount" as "Color Count" and "SubTypeCount" as "SubType Count"

---

**Cursor**

Perfect! Here's the updated SELECT statement with the aliases you requested and without the CardID column:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    c.Power,
    c.Toughness,
    GROUP_CONCAT(DISTINCT col.Color) AS Colors,
    GROUP_CONCAT(DISTINCT st.SubTypeName) AS SubTypes,
    COUNT(DISTINCT cc.ColorID) AS "Color Count",
    COUNT(DISTINCT cst.SubTypeID) AS "SubType Count"
FROM Card c
JOIN Card_Color cc ON c.CardID = cc.CardID
JOIN Color col ON cc.ColorID = col.ColorID
JOIN Card_SubType cst ON c.CardID = cst.CardID
JOIN SubType st ON cst.SubTypeID = st.SubTypeID
GROUP BY c.CardName, c.ManaCost, c.ConvertedManaCost, c.Power, c.Toughness
HAVING COUNT(DISTINCT cc.ColorID) > 1 
   AND COUNT(DISTINCT cst.SubTypeID) > 1
ORDER BY c.CardName;
```

The changes made:
- Removed `c.CardID` from the SELECT clause
- Added the aliases you requested:
  - `CardName` → `"Card Name"`
  - `ManaCost` → `"Mana Cost"`
  - `ConvertedManaCost` → `"CMC"`
  - `ColorCount` → `"Color Count"`
  - `SubTypeCount` → `"SubType Count"`
- Updated the GROUP BY clause to remove `c.CardID` since it's no longer in the SELECT

This will give you a clean result set with the column names formatted exactly as you specified.

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    c.Power,
    c.Toughness,
    GROUP_CONCAT(DISTINCT col.Color) AS Colors,
    GROUP_CONCAT(DISTINCT st.SubTypeName) AS SubTypes,
    COUNT(DISTINCT cc.ColorID) AS "Color Count",
    COUNT(DISTINCT cst.SubTypeID) AS "SubType Count"
FROM Card c
JOIN Card_Color cc ON c.CardID = cc.CardID
JOIN Color col ON cc.ColorID = col.ColorID
JOIN Card_SubType cst ON c.CardID = cst.CardID
JOIN SubType st ON cst.SubTypeID = st.SubTypeID
GROUP BY c.CardName, c.ManaCost, c.ConvertedManaCost, c.Power, c.Toughness
HAVING COUNT(DISTINCT cc.ColorID) > 1 
   AND COUNT(DISTINCT cst.SubTypeID) > 1
ORDER BY c.CardName;
```

