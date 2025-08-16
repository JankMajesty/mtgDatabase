# Select cards by artist and color
_Exported on 8/15/2025 at 18:56:04 CDT from Cursor (1.4.5)_

---

**User**

I want to write a select statement thats gets all cards by artist rk post along with the cards color.

---

**Cursor**

I'll help you write a SELECT statement to get all cards by artist "rk post" along with their colors. First, let me examine the database schema to understand the table structure.


Based on the schema, I can see that:
1. Cards are stored in the `Card` table with an `ArtistID` foreign key
2. Artists are stored in the `Artist` table
3. Colors are stored in the `Color` table
4. The relationship between cards and colors is through the `Card_Color` junction table

Here's the SELECT statement to get all cards by artist "rk post" along with their colors:

```sql
SELECT 
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    GROUP_CONCAT(col.Color) AS Colors
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost;
```

This query:
1. Joins the `Card` table with the `Artist` table to get artist information
2. Uses LEFT JOINs with the `Card_Color` and `Color` tables to get color information (LEFT JOIN ensures we get cards even if they have no colors)
3. Filters for cards by artist "rk post"
4. Groups the results by card to combine multiple colors into a single row
5. Uses `GROUP_CONCAT` to concatenate all colors for each card into a single field

If you want to see the colors as separate rows instead of concatenated, you could use this alternative:

```sql
SELECT 
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    col.Color
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

This second version will show each color on a separate row, which might be more useful for analysis purposes.

```sql
SELECT 
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    GROUP_CONCAT(col.Color) AS Colors
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost;
```

```sql
SELECT 
    c.CardName,
    c.ManaCost,
    c.ConvertedManaCost,
    col.Color
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

---

**User**

can we use the aliases "CardName" as "Card Name", "ManaCost" as "Mana Cost", "ConvertedManaCost" as "CMC", and "Colors" as "Color"

---

**Cursor**

Absolutely! Here's the SELECT statement with the aliases you requested:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    GROUP_CONCAT(col.Color) AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost;
```

And here's the alternative version that shows colors as separate rows:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    col.Color AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

The aliases will make the output more readable with column headers like "Card Name", "Mana Cost", "CMC", and "Color" instead of the database field names.

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    GROUP_CONCAT(col.Color) AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost;
```

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    col.Color AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

---

**User**

Can we also get a column for "ArtistName" as "Artist"

---

**Cursor**

Yes! Here's the SELECT statement with the additional "Artist" column:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    a.ArtistName AS "Artist",
    GROUP_CONCAT(col.Color) AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost, a.ArtistName;
```

And here's the version that shows colors as separate rows:

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    a.ArtistName AS "Artist",
    col.Color AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

Now you'll have all five columns: "Card Name", "Mana Cost", "CMC", "Artist", and "Color".

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    a.ArtistName AS "Artist",
    GROUP_CONCAT(col.Color) AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
GROUP BY c.CardID, c.CardName, c.ManaCost, c.ConvertedManaCost, a.ArtistName;
```

```sql
SELECT 
    c.CardName AS "Card Name",
    c.ManaCost AS "Mana Cost",
    c.ConvertedManaCost AS "CMC",
    a.ArtistName AS "Artist",
    col.Color AS "Color"
FROM Card c
JOIN Artist a ON c.ArtistID = a.ArtistID
LEFT JOIN Card_Color cc ON c.CardID = cc.CardID
LEFT JOIN Color col ON cc.ColorID = col.ColorID
WHERE a.ArtistName = 'rk post'
ORDER BY c.CardName, col.Color;
```

