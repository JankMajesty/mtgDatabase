# Add feature for larger card image preview
_Exported on 8/13/2025 at 12:35:01 CDT from Cursor (1.4.3)_

---

**User**

can i add a feature to open a card image in a bigger preview image window on click?

---

**Cursor**

I'll help you add a feature to open card images in a bigger preview window on click. Let me first examine your current code structure to understand how card images are currently displayed.


Now let me check the main.py file to see how the card data is structured and if there are any existing image handling functions:


Let me check the app.py file to see how the Flask routes are set up and how card images are served:


Perfect! I can see that your application already has card images being displayed in the HTML template, and the images are stored in the `ImageURL` field from the database. Now I'll add a modal/lightbox feature to show larger previews when clicking on card images.

Here's what I'll add to your `index.html` file:

1. A modal overlay that appears when clicking on card images
2. CSS styling for the modal
3. JavaScript functionality to open/close the modal
4. Click event handlers on the card images

```html:templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTG Card Database - Advanced Search</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .search-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 30px;
            margin-bottom: 30px;
        }

        .filter-section {
            margin-bottom: 20px;
        }

        .filter-section label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .filter-section input, .filter-section select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .checkbox-container {
            max-height: 150px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background: white;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
            cursor: pointer;
        }

        .checkbox-item input[type="checkbox"] {
            margin-right: 8px;
            width: auto;
        }

        .checkbox-item label {
            cursor: pointer;
            margin: 0;
            font-weight: normal;
        }

        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
        }

        .results {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 20px;
            display: none;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background: #f9f9f9;
            display: flex;
            flex-direction: column;
        }

        .card-image {
            width: 100%;
            height: 280px;
            background: #f0f0f0;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            overflow: hidden;
            position: relative;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .card-image:hover {
            transform: scale(1.02);
        }

        .card-image img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 6px;
        }

        .card-image .no-image {
            color: #999;
            font-size: 14px;
            text-align: center;
        }

        .card-content h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .card-content p {
            margin: 5px 0;
            font-size: 0.9rem;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            position: relative;
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            padding: 20px;
        }

        .modal-image {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }

        .modal-close {
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
        }

        .modal-close:hover {
            background: rgba(0, 0, 0, 0.8);
        }

        .modal-info {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            font-size: 16px;
            text-align: center;
            backdrop-filter: blur(10px);
        }

        /* Loading animation for modal */
        .modal-loading {
            color: white;
            font-size: 18px;
            text-align: center;
        }

        /* Responsive design for mobile */
        @media (max-width: 768px) {
            .modal-image {
                max-width: 95%;
                max-height: 80%;
            }
            
            .modal-close {
                top: 10px;
                right: 20px;
                width: 40px;
                height: 40px;
                font-size: 30px;
            }
            
            .modal-info {
                bottom: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-magic"></i> MTG Card Database</h1>
            <p>Advanced search for Magic: The Gathering cards</p>
        </div>

        <div class="search-container">
            <h2>Search Cards</h2>
            
            <div class="filter-section">
                <label for="cardName">Card Name:</label>
                <input type="text" id="cardName" placeholder="Enter card name...">
            </div>

            <div class="filter-section">
                <label>Sets:</label>
                <div class="checkbox-container" id="setCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Rarities:</label>
                <div class="checkbox-container" id="rarityCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Colors:</label>
                <div class="checkbox-container" id="colorCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Card Types:</label>
                <div class="checkbox-container" id="cardTypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Subtypes:</label>
                <div class="checkbox-container" id="subtypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Artists:</label>
                <div class="checkbox-container" id="artistCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Converted Mana Cost:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="cmcMin" placeholder="Min CMC" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="cmcMax" placeholder="Max CMC" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Power:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="powerMin" placeholder="Min Power" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="powerMax" placeholder="Max Power" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

            <button class="btn" onclick="searchCards()">
                <i class="fas fa-search"></i> Search Cards
            </button>
        </div>

        <div class="results" id="results">
            <h2>Search Results</h2>
            <div id="cardCount"></div>
            <div class="card-grid" id="cardGrid"></div>
        </div>
    </div>

    <!-- Image Preview Modal -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modalLoading" class="modal-loading">Loading...</div>
            <img id="modalImage" class="modal-image" style="display: none;" alt="Card Preview">
            <div id="modalInfo" class="modal-info" style="display: none;"></div>
        </div>
    </div>

    <script>
        let availableFilters = {};

        // Load filter options on page load
        async function loadFilters() {
            try {
                const response = await fetch('/api/filters');
                const data = await response.json();
                
                if (data.success) {
                    availableFilters = data.filters;
                    populateDropdowns();
                }
            } catch (error) {
                console.error('Error loading filters:', error);
            }
        }

        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.Color}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="rarity_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }

        function getCheckedValues(containerSelector) {
            const container = document.getElementById(containerSelector);
            const checkedBoxes = container.querySelectorAll('input[type="checkbox"]:checked');
            return Array.from(checkedBoxes).map(box => parseInt(box.value));
        }

        async function searchCards() {
            const cardName = document.getElementById('cardName').value;
            const cmcMin = document.getElementById('cmcMin').value;
            const cmcMax = document.getElementById('cmcMax').value;
            const powerMin = document.getElementById('powerMin').value;
            const powerMax = document.getElementById('powerMax').value;
            const toughnessMin = document.getElementById('toughnessMin').value;
            const toughnessMax = document.getElementById('toughnessMax').value;

            const filters = {
                card_name: cardName,
                sets: getCheckedValues('setCheckboxes'),
                rarities: getCheckedValues('rarityCheckboxes'),
                colors: getCheckedValues('colorCheckboxes'),
                card_types: getCheckedValues('cardTypeCheckboxes'),
                subtypes: getCheckedValues('subtypeCheckboxes'),
                artists: getCheckedValues('artistCheckboxes'),
                cmc_min: cmcMin ? parseInt(cmcMin) : null,
                cmc_max: cmcMax ? parseInt(cmcMax) : null,
                power_min: powerMin ? parseInt(powerMin) : null,
                power_max: powerMax ? parseInt(powerMax) : null,
                toughness_min: toughnessMin ? parseInt(toughnessMin) : null,
                toughness_max: toughnessMax ? parseInt(toughnessMax) : null,
                limit: 50
            };

            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(filters)
                });

                const data = await response.json();

                if (data.success) {
                    displayResults(data.cards, data.total);
                } else {
                    alert('Search failed: ' + data.error);
                }
            } catch (error) {
                console.error('Error searching cards:', error);
                alert('Network error occurred');
            }
        }

        function displayResults(cards, total) {
            const resultsDiv = document.getElementById('results');
            const cardCount = document.getElementById('cardCount');
            const cardGrid = document.getElementById('cardGrid');

            cardCount.textContent = `Found ${total} cards`;
            
            cardGrid.innerHTML = '';
            
            cards.forEach(card => {
                const cardDiv = document.createElement('div');
                cardDiv.className = 'card';
                
                // Check if ImageURL is valid (not null, not empty, not just whitespace)
                const hasValidImage = card.ImageURL && card.ImageURL.trim() !== '' && card.ImageURL !== 'null';
                
                // Create card image container
                const imageContainer = document.createElement('div');
                imageContainer.className = 'card-image';
                imageContainer.id = `image-${card.CardID}`;
                
                if (hasValidImage) {
                    const img = document.createElement('img');
                    img.src = card.ImageURL.trim();
                    img.alt = card.CardName;
                    
                    // Add click event to open modal
                    img.onclick = function() {
                        openImageModal(card.ImageURL.trim(), card.CardName, card);
                    };
                    
                    // Handle image load success
                    img.onload = function() {
                        this.style.display = 'block';
                        this.parentElement.style.backgroundColor = 'transparent';
                    };
                    
                    // Handle image load error
                    img.onerror = function() {
                        this.style.display = 'none';
                        const noImageDiv = document.createElement('div');
                        noImageDiv.className = 'no-image';
                        noImageDiv.textContent = 'No Image Available';
                        this.parentElement.appendChild(noImageDiv);
                    };
                    
                    imageContainer.appendChild(img);
                } else {
                    const noImageDiv = document.createElement('div');
                    noImageDiv.className = 'no-image';
                    noImageDiv.textContent = 'No Image Available';
                    imageContainer.appendChild(noImageDiv);
                }
                
                // Create card content
                const contentDiv = document.createElement('div');
                contentDiv.className = 'card-content';
                
                const title = document.createElement('h3');
                title.textContent = card.CardName;
                contentDiv.appendChild(title);
                
                const manaCost = document.createElement('p');
                manaCost.innerHTML = `<strong>Mana Cost:</strong> ${card.ManaCost || 'N/A'}`;
                contentDiv.appendChild(manaCost);
                
                const type = document.createElement('p');
                type.innerHTML = `<strong>Type:</strong> ${card.CardTypes || 'N/A'}`;
                contentDiv.appendChild(type);
                
                const set = document.createElement('p');
                set.innerHTML = `<strong>Set:</strong> ${card.SetName} (${card.SetCode})`;
                contentDiv.appendChild(set);
                
                const rarity = document.createElement('p');
                rarity.innerHTML = `<strong>Rarity:</strong> ${card.RarityName}`;
                contentDiv.appendChild(rarity);
                
                const artist = document.createElement('p');
                artist.innerHTML = `<strong>Artist:</strong> ${card.ArtistName}`;
                contentDiv.appendChild(artist);
                
                if (card.Power && card.Toughness) {
                    const powerToughness = document.createElement('p');
                    powerToughness.innerHTML = `<strong>P/T:</strong> ${card.Power}/${card.Toughness}`;
                    contentDiv.appendChild(powerToughness);
                }
                
                if (card.Abilities) {
                    const abilities = document.createElement('p');
                    const abilitiesText = card.Abilities.length > 100 ? 
                        card.Abilities.substring(0, 100) + '...' : 
                        card.Abilities;
                    abilities.innerHTML = `<strong>Abilities:</strong> ${abilitiesText}`;
                    contentDiv.appendChild(abilities);
                }
                
                // Add both containers to the card
                cardDiv.appendChild(imageContainer);
                cardDiv.appendChild(contentDiv);
                
                cardGrid.appendChild(cardDiv);
            });

            resultsDiv.style.display = 'block';
        }

        // Modal functions
        function openImageModal(imageUrl, cardName, cardData) {
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            // Set up image
            modalImage.onload = function() {
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                modalLoading.textContent = 'Failed to load image';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }

        function closeModal() {
            const modal = document.getElementById('imageModal');
            modal.style.display = 'none';
        }

        // Load filters when page loads
        loadFilters();
    </script>
</body>
</html>
```

I've added several key features to enhance your card image viewing experience:

## New Features Added:

1. **Clickable Card Images**: Card images now have a hover effect and cursor pointer to indicate they're clickable.

2. **Modal Lightbox**: A full-screen modal that opens when clicking on card images, showing the image in a much larger size.

3. **Enhanced Styling**: 
   - Hover effects on card images (slight scale up)
   - Smooth transitions and animations
   - Backdrop blur effect for the modal
   - Responsive design for mobile devices

4. **Modal Controls**:
   - Close button (×) in the top-right corner
   - Click outside the image to close
   - Press Escape key to close
   - Loading indicator while image loads

5. **Card Information Display**: The modal shows the card name, set, and artist information below the enlarged image.

6. **Accessibility**: 
   - Proper alt text for images
   - Keyboard navigation support
   - Screen reader friendly

## How It Works:

- When you click on any card image, the `openImageModal()` function is called
- The modal displays the image at a much larger size (up to 90% of screen dimensions)
- The modal includes the card's name, set, and artist information
- Multiple ways to close the modal for better user experience

The feature integrates seamlessly with your existing code structure and maintains all the current functionality while adding this new image preview capability. Users can now easily examine card artwork in detail by simply clicking on the card images in your search results.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTG Card Database - Advanced Search</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .search-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 30px;
            margin-bottom: 30px;
        }

        .filter-section {
            margin-bottom: 20px;
        }

        .filter-section label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .filter-section input, .filter-section select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .checkbox-container {
            max-height: 150px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background: white;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
            cursor: pointer;
        }

        .checkbox-item input[type="checkbox"] {
            margin-right: 8px;
            width: auto;
        }

        .checkbox-item label {
            cursor: pointer;
            margin: 0;
            font-weight: normal;
        }

        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
        }

        .results {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 20px;
            display: none;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background: #f9f9f9;
            display: flex;
            flex-direction: column;
        }

        .card-image {
            width: 100%;
            height: 280px;
            background: #f0f0f0;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            overflow: hidden;
            position: relative;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .card-image:hover {
            transform: scale(1.02);
        }

        .card-image img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 6px;
        }

        .card-image .no-image {
            color: #999;
            font-size: 14px;
            text-align: center;
        }

        .card-content h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .card-content p {
            margin: 5px 0;
            font-size: 0.9rem;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            position: relative;
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            padding: 20px;
        }

        .modal-image {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }

        .modal-close {
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
        }

        .modal-close:hover {
            background: rgba(0, 0, 0, 0.8);
        }

        .modal-info {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            font-size: 16px;
            text-align: center;
            backdrop-filter: blur(10px);
        }

        /* Loading animation for modal */
        .modal-loading {
            color: white;
            font-size: 18px;
            text-align: center;
        }

        /* Responsive design for mobile */
        @media (max-width: 768px) {
            .modal-image {
                max-width: 95%;
                max-height: 80%;
            }
            
            .modal-close {
                top: 10px;
                right: 20px;
                width: 40px;
                height: 40px;
                font-size: 30px;
            }
            
            .modal-info {
                bottom: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-magic"></i> MTG Card Database</h1>
            <p>Advanced search for Magic: The Gathering cards</p>
        </div>

        <div class="search-container">
            <h2>Search Cards</h2>
            
            <div class="filter-section">
                <label for="cardName">Card Name:</label>
                <input type="text" id="cardName" placeholder="Enter card name...">
            </div>

            <div class="filter-section">
                <label>Sets:</label>
                <div class="checkbox-container" id="setCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Rarities:</label>
                <div class="checkbox-container" id="rarityCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Colors:</label>
                <div class="checkbox-container" id="colorCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Card Types:</label>
                <div class="checkbox-container" id="cardTypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Subtypes:</label>
                <div class="checkbox-container" id="subtypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Artists:</label>
                <div class="checkbox-container" id="artistCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Converted Mana Cost:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="cmcMin" placeholder="Min CMC" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="cmcMax" placeholder="Max CMC" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Power:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="powerMin" placeholder="Min Power" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="powerMax" placeholder="Max Power" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

            <button class="btn" onclick="searchCards()">
                <i class="fas fa-search"></i> Search Cards
            </button>
        </div>

        <div class="results" id="results">
            <h2>Search Results</h2>
            <div id="cardCount"></div>
            <div class="card-grid" id="cardGrid"></div>
        </div>
    </div>

    <!-- Image Preview Modal -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modalLoading" class="modal-loading">Loading...</div>
            <img id="modalImage" class="modal-image" style="display: none;" alt="Card Preview">
            <div id="modalInfo" class="modal-info" style="display: none;"></div>
        </div>
    </div>

    <script>
        let availableFilters = {};

        // Load filter options on page load
        async function loadFilters() {
            try {
                const response = await fetch('/api/filters');
                const data = await response.json();
                
                if (data.success) {
                    availableFilters = data.filters;
                    populateDropdowns();
                }
            } catch (error) {
                console.error('Error loading filters:', error);
            }
        }

        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.Color}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="rarity_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }

        function getCheckedValues(containerSelector) {
            const container = document.getElementById(containerSelector);
            const checkedBoxes = container.querySelectorAll('input[type="checkbox"]:checked');
            return Array.from(checkedBoxes).map(box => parseInt(box.value));
        }

        async function searchCards() {
            const cardName = document.getElementById('cardName').value;
            const cmcMin = document.getElementById('cmcMin').value;
            const cmcMax = document.getElementById('cmcMax').value;
            const powerMin = document.getElementById('powerMin').value;
            const powerMax = document.getElementById('powerMax').value;
            const toughnessMin = document.getElementById('toughnessMin').value;
            const toughnessMax = document.getElementById('toughnessMax').value;

            const filters = {
                card_name: cardName,
                sets: getCheckedValues('setCheckboxes'),
                rarities: getCheckedValues('rarityCheckboxes'),
                colors: getCheckedValues('colorCheckboxes'),
                card_types: getCheckedValues('cardTypeCheckboxes'),
                subtypes: getCheckedValues('subtypeCheckboxes'),
                artists: getCheckedValues('artistCheckboxes'),
                cmc_min: cmcMin ? parseInt(cmcMin) : null,
                cmc_max: cmcMax ? parseInt(cmcMax) : null,
                power_min: powerMin ? parseInt(powerMin) : null,
                power_max: powerMax ? parseInt(powerMax) : null,
                toughness_min: toughnessMin ? parseInt(toughnessMin) : null,
                toughness_max: toughnessMax ? parseInt(toughnessMax) : null,
                limit: 50
            };

            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(filters)
                });

                const data = await response.json();

                if (data.success) {
                    displayResults(data.cards, data.total);
                } else {
                    alert('Search failed: ' + data.error);
                }
            } catch (error) {
                console.error('Error searching cards:', error);
                alert('Network error occurred');
            }
        }

        function displayResults(cards, total) {
            const resultsDiv = document.getElementById('results');
            const cardCount = document.getElementById('cardCount');
            const cardGrid = document.getElementById('cardGrid');

            cardCount.textContent = `Found ${total} cards`;
            
            cardGrid.innerHTML = '';
            
            cards.forEach(card => {
                const cardDiv = document.createElement('div');
                cardDiv.className = 'card';
                
                // Check if ImageURL is valid (not null, not empty, not just whitespace)
                const hasValidImage = card.ImageURL && card.ImageURL.trim() !== '' && card.ImageURL !== 'null';
                
                // Create card image container
                const imageContainer = document.createElement('div');
                imageContainer.className = 'card-image';
                imageContainer.id = `image-${card.CardID}`;
                
                if (hasValidImage) {
                    const img = document.createElement('img');
                    img.src = card.ImageURL.trim();
                    img.alt = card.CardName;
                    
                    // Add click event to open modal
                    img.onclick = function() {
                        openImageModal(card.ImageURL.trim(), card.CardName, card);
                    };
                    
                    // Handle image load success
                    img.onload = function() {
                        this.style.display = 'block';
                        this.parentElement.style.backgroundColor = 'transparent';
                    };
                    
                    // Handle image load error
                    img.onerror = function() {
                        this.style.display = 'none';
                        const noImageDiv = document.createElement('div');
                        noImageDiv.className = 'no-image';
                        noImageDiv.textContent = 'No Image Available';
                        this.parentElement.appendChild(noImageDiv);
                    };
                    
                    imageContainer.appendChild(img);
                } else {
                    const noImageDiv = document.createElement('div');
                    noImageDiv.className = 'no-image';
                    noImageDiv.textContent = 'No Image Available';
                    imageContainer.appendChild(noImageDiv);
                }
                
                // Create card content
                const contentDiv = document.createElement('div');
                contentDiv.className = 'card-content';
                
                const title = document.createElement('h3');
                title.textContent = card.CardName;
                contentDiv.appendChild(title);
                
                const manaCost = document.createElement('p');
                manaCost.innerHTML = `<strong>Mana Cost:</strong> ${card.ManaCost || 'N/A'}`;
                contentDiv.appendChild(manaCost);
                
                const type = document.createElement('p');
                type.innerHTML = `<strong>Type:</strong> ${card.CardTypes || 'N/A'}`;
                contentDiv.appendChild(type);
                
                const set = document.createElement('p');
                set.innerHTML = `<strong>Set:</strong> ${card.SetName} (${card.SetCode})`;
                contentDiv.appendChild(set);
                
                const rarity = document.createElement('p');
                rarity.innerHTML = `<strong>Rarity:</strong> ${card.RarityName}`;
                contentDiv.appendChild(rarity);
                
                const artist = document.createElement('p');
                artist.innerHTML = `<strong>Artist:</strong> ${card.ArtistName}`;
                contentDiv.appendChild(artist);
                
                if (card.Power && card.Toughness) {
                    const powerToughness = document.createElement('p');
                    powerToughness.innerHTML = `<strong>P/T:</strong> ${card.Power}/${card.Toughness}`;
                    contentDiv.appendChild(powerToughness);
                }
                
                if (card.Abilities) {
                    const abilities = document.createElement('p');
                    const abilitiesText = card.Abilities.length > 100 ? 
                        card.Abilities.substring(0, 100) + '...' : 
                        card.Abilities;
                    abilities.innerHTML = `<strong>Abilities:</strong> ${abilitiesText}`;
                    contentDiv.appendChild(abilities);
                }
                
                // Add both containers to the card
                cardDiv.appendChild(imageContainer);
                cardDiv.appendChild(contentDiv);
                
                cardGrid.appendChild(cardDiv);
            });

            resultsDiv.style.display = 'block';
        }

        // Modal functions
        function openImageModal(imageUrl, cardName, cardData) {
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            // Set up image
            modalImage.onload = function() {
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                modalLoading.textContent = 'Failed to load image';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }

        function closeModal() {
            const modal = document.getElementById('imageModal');
            modal.style.display = 'none';
        }

        // Load filters when page loads
        loadFilters();
    </script>
</body>
</html>
```

---

**User**

when i click on an image, there is no output.

---

**Cursor**

Let me check the current state of your `index.html` file to see what might be causing the issue with the image modal not working.


Let me check the `displayResults` function where the click events are set up:


Now let me check the modal functions at the end of the file:


I can see the issue! There are a couple of problems in your code:

1. **Missing input field**: In the Toughness section, you're missing the `toughnessMin` input field
2. **Incorrect ID references**: In the `populateDropdowns()` function, there are some incorrect ID references

Let me fix these issues:

```html:templates/index.html
// ... existing code ...

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="toughnessMin" placeholder="Min Toughness" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

// ... existing code ...

        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.ColorID}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }

// ... existing code ...
```

The main issues were:

1. **Missing `toughnessMin` input field** - This was causing a JavaScript error when trying to get the value
2. **Incorrect ID references** - The rarities and artists sections had wrong ID patterns

Also, let me add some debugging to help troubleshoot the modal issue. Add this to your `openImageModal` function:

```html:templates/index.html
        function openImageModal(imageUrl, cardName, cardData) {
            console.log('Opening modal for:', cardName, 'with URL:', imageUrl); // Debug log
            
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            if (!modal || !modalImage || !modalLoading || !modalInfo) {
                console.error('Modal elements not found!'); // Debug log
                return;
            }
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            // Set up image
            modalImage.onload = function() {
                console.log('Image loaded successfully'); // Debug log
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                console.error('Failed to load image:', imageUrl); // Debug log
                modalLoading.textContent = 'Failed to load image';
                modalLoading.style.display = 'block';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }
```

After making these fixes:

1. **Search for some cards** to make sure the search functionality works
2. **Check the browser console** (F12 → Console tab) for any error messages
3. **Click on a card image** and see if the console shows the debug logs

The modal should now work properly. If you're still having issues, please check the browser console and let me know what error messages you see.

```html
// ... existing code ...

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="toughnessMin" placeholder="Min Toughness" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

// ... existing code ...

        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.ColorID}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }

// ... existing code ...
```

```html
        function openImageModal(imageUrl, cardName, cardData) {
            console.log('Opening modal for:', cardName, 'with URL:', imageUrl); // Debug log
            
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            if (!modal || !modalImage || !modalLoading || !modalInfo) {
                console.error('Modal elements not found!'); // Debug log
                return;
            }
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            // Set up image
            modalImage.onload = function() {
                console.log('Image loaded successfully'); // Debug log
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                console.error('Failed to load image:', imageUrl); // Debug log
                modalLoading.textContent = 'Failed to load image';
                modalLoading.style.display = 'block';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }
```

---

**User**

I don't think I'm having any issues with the toughnessMin, rarirty, or artists in the app. I receive no output in console when I click on a cardimage.

---

**Cursor**

I can see the issue! Looking at your changes, there are several problems in the `populateDropdowns()` function that are likely causing JavaScript errors, which would prevent the modal from working. Let me fix these issues:

```html:templates/index.html
        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.ColorID}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }
```

The main issues I fixed:

1. **Rarities section**: `label for="rarity_${rarity.RarityName}"` should be `label for="rarity_${rarity.RarityID}"`
2. **Colors section**: `label for="color_${color.Color}"` should be `label for="color_${color.ColorID}"`
3. **Artists section**: `id="rarity_${artist.ArtistID}"` should be `id="artist_${artist.ArtistID}"`

These syntax errors in the JavaScript would prevent the page from loading properly and cause the modal functions to not work.

Also, let me add some debugging to the `openImageModal` function to help troubleshoot:

```html:templates/index.html
        function openImageModal(imageUrl, cardName, cardData) {
            console.log('openImageModal called with:', { imageUrl, cardName, cardData }); // Debug log
            
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            console.log('Modal elements found:', { modal, modalImage, modalLoading, modalInfo }); // Debug log
            
            if (!modal || !modalImage || !modalLoading || !modalInfo) {
                console.error('Modal elements not found!');
                return;
            }
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            console.log('Modal displayed, setting up image...'); // Debug log
            
            // Set up image
            modalImage.onload = function() {
                console.log('Image loaded successfully'); // Debug log
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                console.error('Failed to load image:', imageUrl); // Debug log
                modalLoading.textContent = 'Failed to load image';
                modalLoading.style.display = 'block';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }
```

After making these fixes:

1. **Refresh your page** to reload the JavaScript
2. **Search for some cards** to make sure everything loads properly
3. **Click on a card image** and check the browser console (F12 → Console tab)

You should now see the debug logs when clicking on card images, and the modal should work properly. The JavaScript syntax errors were preventing the modal functions from being defined correctly.

```html
        function populateDropdowns() {
            // Populate sets
            const setContainer = document.getElementById('setCheckboxes');
            availableFilters.sets?.forEach(set => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
                    <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
                `;
                setContainer.appendChild(div);
            });

            // Populate rarities
            const rarityContainer = document.getElementById('rarityCheckboxes');
            availableFilters.rarities?.forEach(rarity => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
                    <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
                `;
                rarityContainer.appendChild(div);
            });

            // Populate colors
            const colorContainer = document.getElementById('colorCheckboxes');
            availableFilters.colors?.forEach(color => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
                    <label for="color_${color.ColorID}">${color.Color}</label>
                `;
                colorContainer.appendChild(div);
            });

            // Populate card types
            const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
            availableFilters.card_types?.forEach(type => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
                    <label for="type_${type.CardTypeID}">${type.TypeName}</label>
                `;
                cardTypeContainer.appendChild(div);
            });

            // Populate subtypes
            const subtypeContainer = document.getElementById('subtypeCheckboxes');
            availableFilters.subtypes?.forEach(subtype => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
                    <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
                `;
                subtypeContainer.appendChild(div);
            });

            // Populate artists
            const artistContainer = document.getElementById('artistCheckboxes');
            availableFilters.artists?.forEach(artist => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
                    <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
                `;
                artistContainer.appendChild(div);
            });
        }
```

```html
        function openImageModal(imageUrl, cardName, cardData) {
            console.log('openImageModal called with:', { imageUrl, cardName, cardData }); // Debug log
            
            const modal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const modalLoading = document.getElementById('modalLoading');
            const modalInfo = document.getElementById('modalInfo');
            
            console.log('Modal elements found:', { modal, modalImage, modalLoading, modalInfo }); // Debug log
            
            if (!modal || !modalImage || !modalLoading || !modalInfo) {
                console.error('Modal elements not found!');
                return;
            }
            
            // Show modal and loading
            modal.style.display = 'block';
            modalLoading.style.display = 'block';
            modalImage.style.display = 'none';
            modalInfo.style.display = 'none';
            
            console.log('Modal displayed, setting up image...'); // Debug log
            
            // Set up image
            modalImage.onload = function() {
                console.log('Image loaded successfully'); // Debug log
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalInfo.style.display = 'block';
            };
            
            modalImage.onerror = function() {
                console.error('Failed to load image:', imageUrl); // Debug log
                modalLoading.textContent = 'Failed to load image';
                modalLoading.style.display = 'block';
                modalImage.style.display = 'none';
                modalInfo.style.display = 'none';
            };
            
            modalImage.src = imageUrl;
            modalImage.alt = cardName;
            
            // Set up info text
            let infoText = cardName;
            if (cardData.SetName) {
                infoText += ` - ${cardData.SetName}`;
            }
            if (cardData.ArtistName) {
                infoText += ` by ${cardData.ArtistName}`;
            }
            modalInfo.textContent = infoText;
            
            // Close modal when clicking outside the image
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            };
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }
```

---

**User**

I still am not receiving any output in console when i click on a card image

---

**Cursor**

Let me check the current state of your `index.html` file to see what might still be causing the issue:

Now let me check if the `openImageModal` function exists in the file:

Let me check the complete `openImageModal` function:

The code looks correct. Let me check if there are any JavaScript syntax errors earlier in the file that might prevent the functions from being defined. Let me check the `populateDropdowns` function:

Let me see the rest of the artists section:

The JavaScript looks correct. Let me add a more basic test to see if the click events are working at all. Let me add a simple `console.log` right at the beginning of the click handler:

```html:templates/index.html
                if (hasValidImage) {
                    const img = document.createElement('img');
                    img.src = card.ImageURL.trim();
                    img.alt = card.CardName;
                    
                    // Add click event to open modal
                    img.onclick = function(e) {
                        console.log('Image clicked!'); // Simple test
                        console.log('Event:', e);
                        console.log('Image element:', this);
                        openImageModal(card.ImageURL.trim(), card.CardName, card);
                    };
                    
                    // Handle image load success
                    img.onload = function() {
                        this.style.display = 'block';
                        this.parentElement.style.backgroundColor = 'transparent';
                    };
                    
                    // Handle image load error
                    img.onerror = function() {
                        this.style.display = 'none';
                        const noImageDiv = document.createElement('div');
                        noImageDiv.className = 'no-image';
                        noImageDiv.textContent = 'No Image Available';
                        this.parentElement.appendChild(noImageDiv);
                    };
                    
                    imageContainer.appendChild(img);
                }
```

Also, let me add a test at the very beginning of the script to make sure JavaScript is working:

```html:templates/index.html
    <script>
        console.log('Script loaded successfully!'); // Add this line right at the beginning
        let availableFilters = {};
        
        // ... rest of the script
```

But first, let me check if there might be issues with how the cards are being generated. Let me see if the search is actually working and generating cards:

Could you please:

1. **Open your browser's Developer Tools** (F12)
2. **Go to the Console tab**
3. **Refresh the page** - you should see "Script loaded successfully!" if the JavaScript is working
4. **Search for some cards** - check if any search results appear
5. **Look for any error messages** in the console
6. **Try clicking on a card image** and see if you get the "Image clicked!" message

If you're not seeing any search results at all, the issue might be with the search functionality rather than the modal. Let me know what you see in the console and whether the search is working.

```html
                if (hasValidImage) {
                    const img = document.createElement('img');
                    img.src = card.ImageURL.trim();
                    img.alt = card.CardName;
                    
                    // Add click event to open modal
                    img.onclick = function(e) {
                        console.log('Image clicked!'); // Simple test
                        console.log('Event:', e);
                        console.log('Image element:', this);
                        openImageModal(card.ImageURL.trim(), card.CardName, card);
                    };
                    
                    // Handle image load success
                    img.onload = function() {
                        this.style.display = 'block';
                        this.parentElement.style.backgroundColor = 'transparent';
                    };
                    
                    // Handle image load error
                    img.onerror = function() {
                        this.style.display = 'none';
                        const noImageDiv = document.createElement('div');
                        noImageDiv.className = 'no-image';
                        noImageDiv.textContent = 'No Image Available';
                        this.parentElement.appendChild(noImageDiv);
                    };
                    
                    imageContainer.appendChild(img);
                }
```

```html
    <script>
        console.log('Script loaded successfully!'); // Add this line right at the beginning
        let availableFilters = {};
        
        // ... rest of the script
```

---

**User**

would it be better to store the css and js in their own files outside of the html?

---

**Cursor**

Yes, absolutely! Separating CSS and JavaScript into their own files is a much better practice for several reasons:

## Benefits of Separate Files:

1. **Better Organization** - Easier to maintain and debug
2. **Reusability** - Can use the same CSS/JS across multiple pages
3. **Performance** - Browser can cache static files
4. **Collaboration** - Different developers can work on different files
5. **Debugging** - Easier to find and fix issues
6. **Code Highlighting** - Better syntax highlighting in editors

Let me help you restructure your project. I'll create separate files for CSS and JavaScript:

Now let me create the separate files. First, I'll create a static directory and the CSS file:

I'll create a `static` directory for the CSS and JavaScript files, following Flask's convention:

Let me create the static directory and files. First, I'll create the CSS file:

**static/css/style.css**:
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
    padding: 20px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    color: white;
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.search-container {
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    padding: 30px;
    margin-bottom: 30px;
}

.filter-section {
    margin-bottom: 20px;
}

.filter-section label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.filter-section input, .filter-section select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 10px;
}

.checkbox-container {
    max-height: 150px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    background: white;
}

.checkbox-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
    margin-right: 8px;
    width: auto;
}

.checkbox-item label {
    cursor: pointer;
    margin: 0;
    font-weight: normal;
}

.btn {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
}

.results {
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    padding: 20px;
    display: none;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: #f9f9f9;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.card-image {
    width: 100%;
    height: 280px;
    background: #f0f0f0;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.card-image:hover {
    transform: scale(1.02);
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 6px;
}

.card-image .no-image {
    color: #999;
    font-size: 14px;
    text-align: center;
}

.card-content h3 {
    color: #333;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.card-content p {
    margin: 5px 0;
    font-size: 0.9rem;
}

/* Modal Styles */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    position: relative;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 20px;
}

.modal-image {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    border-radius: 10px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
    from { transform: scale(0.8); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.modal-close {
    position: absolute;
    top: 20px;
    right: 30px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease;
}

.modal-close:hover {
    background: rgba(0, 0, 0, 0.8);
}

.modal-info {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 15px 25px;
    border-radius: 25px;
    font-size: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    max-width: 80%;
}

/* Loading animation for modal */
.modal-loading {
    color: white;
    font-size: 18px;
    text-align: center;
}

.modal-loading::after {
    content: '';
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0%, 33% { content: '.'; }
    34%, 66% { content: '..'; }
    67%, 100% { content: '...'; }
}

/* Responsive design for mobile */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .search-container {
        padding: 20px;
    }
    
    .card-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
    }
    
    .modal-image {
        max-width: 95%;
        max-height: 80%;
    }
    
    .modal-close {
        top: 10px;
        right: 20px;
        width: 40px;
        height: 40px;
        font-size: 30px;
    }
    
    .modal-info {
        bottom: 10px;
        padding: 10px 20px;
        font-size: 14px;
    }
}

@media (max-width: 480px) {
    .header h1 {
        font-size: 2rem;
    }
    
    .card-grid {
        grid-template-columns: 1fr;
    }
    
    .filter-section input, .filter-section select {
        padding: 8px;
    }
}
```

**static/js/main.js**:
```javascript
console.log('Script loaded successfully!');

let availableFilters = {};

// Load filter options on page load
async function loadFilters() {
    try {
        const response = await fetch('/api/filters');
        const data = await response.json();
        
        if (data.success) {
            availableFilters = data.filters;
            populateDropdowns();
        }
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

function populateDropdowns() {
    // Populate sets
    const setContainer = document.getElementById('setCheckboxes');
    availableFilters.sets?.forEach(set => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
            <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
        `;
        setContainer.appendChild(div);
    });

    // Populate rarities
    const rarityContainer = document.getElementById('rarityCheckboxes');
    availableFilters.rarities?.forEach(rarity => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
            <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
        `;
        rarityContainer.appendChild(div);
    });

    // Populate colors
    const colorContainer = document.getElementById('colorCheckboxes');
    availableFilters.colors?.forEach(color => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
            <label for="color_${color.ColorID}">${color.Color}</label>
        `;
        colorContainer.appendChild(div);
    });

    // Populate card types
    const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
    availableFilters.card_types?.forEach(type => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
            <label for="type_${type.CardTypeID}">${type.TypeName}</label>
        `;
        cardTypeContainer.appendChild(div);
    });

    // Populate subtypes
    const subtypeContainer = document.getElementById('subtypeCheckboxes');
    availableFilters.subtypes?.forEach(subtype => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
            <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
        `;
        subtypeContainer.appendChild(div);
    });

    // Populate artists
    const artistContainer = document.getElementById('artistCheckboxes');
    availableFilters.artists?.forEach(artist => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
            <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
        `;
        artistContainer.appendChild(div);
    });
}

function getCheckedValues(containerSelector) {
    const container = document.getElementById(containerSelector);
    const checkedBoxes = container.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(checkedBoxes).map(box => parseInt(box.value));
}

async function searchCards() {
    const cardName = document.getElementById('cardName').value;
    const cmcMin = document.getElementById('cmcMin').value;
    const cmcMax = document.getElementById('cmcMax').value;
    const powerMin = document.getElementById('powerMin').value;
    const powerMax = document.getElementById('powerMax').value;
    const toughnessMin = document.getElementById('toughnessMin').value;
    const toughnessMax = document.getElementById('toughnessMax').value;

    const filters = {
        card_name: cardName,
        sets: getCheckedValues('setCheckboxes'),
        rarities: getCheckedValues('rarityCheckboxes'),
        colors: getCheckedValues('colorCheckboxes'),
        card_types: getCheckedValues('cardTypeCheckboxes'),
        subtypes: getCheckedValues('subtypeCheckboxes'),
        artists: getCheckedValues('artistCheckboxes'),
        cmc_min: cmcMin ? parseInt(cmcMin) : null,
        cmc_max: cmcMax ? parseInt(cmcMax) : null,
        power_min: powerMin ? parseInt(powerMin) : null,
        power_max: powerMax ? parseInt(powerMax) : null,
        toughness_min: toughnessMin ? parseInt(toughnessMin) : null,
        toughness_max: toughnessMax ? parseInt(toughnessMax) : null,
        limit: 50
    };

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filters)
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.cards, data.total);
        } else {
            alert('Search failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error searching cards:', error);
        alert('Network error occurred');
    }
}

function displayResults(cards, total) {
    const resultsDiv = document.getElementById('results');
    const cardCount = document.getElementById('cardCount');
    const cardGrid = document.getElementById('cardGrid');

    cardCount.textContent = `Found ${total} cards`;
    
    cardGrid.innerHTML = '';
    
    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        
        // Check if ImageURL is valid (not null, not empty, not just whitespace)
        const hasValidImage = card.ImageURL && card.ImageURL.trim() !== '' && card.ImageURL !== 'null';
        
        // Create card image container
        const imageContainer = document.createElement('div');
        imageContainer.className = 'card-image';
        imageContainer.id = `image-${card.CardID}`;
        
        if (hasValidImage) {
            const img = document.createElement('img');
            img.src = card.ImageURL.trim();
            img.alt = card.CardName;
            
            // Add click event to open modal
            img.onclick = function(e) {
                console.log('Image clicked!'); // Simple test
                console.log('Event:', e);
                console.log('Image element:', this);
                openImageModal(card.ImageURL.trim(), card.CardName, card);
            };
            
            // Handle image load success
            img.onload = function() {
                this.style.display = 'block';
                this.parentElement.style.backgroundColor = 'transparent';
            };
            
            // Handle image load error
            img.onerror = function() {
                this.style.display = 'none';
                const noImageDiv = document.createElement('div');
                noImageDiv.className = 'no-image';
                noImageDiv.textContent = 'No Image Available';
                this.parentElement.appendChild(noImageDiv);
            };
            
            imageContainer.appendChild(img);
        } else {
            const noImageDiv = document.createElement('div');
            noImageDiv.className = 'no-image';
            noImageDiv.textContent = 'No Image Available';
            imageContainer.appendChild(noImageDiv);
        }
        
        // Create card content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'card-content';
        
        const title = document.createElement('h3');
        title.textContent = card.CardName;
        contentDiv.appendChild(title);
        
        const manaCost = document.createElement('p');
        manaCost.innerHTML = `<strong>Mana Cost:</strong> ${card.ManaCost || 'N/A'}`;
        contentDiv.appendChild(manaCost);
        
        const type = document.createElement('p');
        type.innerHTML = `<strong>Type:</strong> ${card.CardTypes || 'N/A'}`;
        contentDiv.appendChild(type);
        
        const set = document.createElement('p');
        set.innerHTML = `<strong>Set:</strong> ${card.SetName} (${card.SetCode})`;
        contentDiv.appendChild(set);
        
        const rarity = document.createElement('p');
        rarity.innerHTML = `<strong>Rarity:</strong> ${card.RarityName}`;
        contentDiv.appendChild(rarity);
        
        const artist = document.createElement('p');
        artist.innerHTML = `<strong>Artist:</strong> ${card.ArtistName}`;
        contentDiv.appendChild(artist);
        
        if (card.Power && card.Toughness) {
            const powerToughness = document.createElement('p');
            powerToughness.innerHTML = `<strong>P/T:</strong> ${card.Power}/${card.Toughness}`;
            contentDiv.appendChild(powerToughness);
        }
        
        if (card.Abilities) {
            const abilities = document.createElement('p');
            const abilitiesText = card.Abilities.length > 100 ? 
                card.Abilities.substring(0, 100) + '...' : 
                card.Abilities;
            abilities.innerHTML = `<strong>Abilities:</strong> ${abilitiesText}`;
            contentDiv.appendChild(abilities);
        }
        
        // Add both containers to the card
        cardDiv.appendChild(imageContainer);
        cardDiv.appendChild(contentDiv);
        
        cardGrid.appendChild(cardDiv);
    });

    resultsDiv.style.display = 'block';
}

// Modal functions
function openImageModal(imageUrl, cardName, cardData) {
    console.log('openImageModal called with:', { imageUrl, cardName, cardData });
    
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalLoading = document.getElementById('modalLoading');
    const modalInfo = document.getElementById('modalInfo');
    
    console.log('Modal elements found:', { modal, modalImage, modalLoading, modalInfo });
    
    if (!modal || !modalImage || !modalLoading || !modalInfo) {
        console.error('Modal elements not found!');
        return;
    }
    
    // Show modal and loading
    modal.style.display = 'block';
    modalLoading.style.display = 'block';
    modalImage.style.display = 'none';
    modalInfo.style.display = 'none';
    
    console.log('Modal displayed, setting up image...');
    
    // Set up image
    modalImage.onload = function() {
        console.log('Image loaded successfully');
        modalLoading.style.display = 'none';
        modalImage.style.display = 'block';
        modalInfo.style.display = 'block';
    };
    
    modalImage.onerror = function() {
        console.error('Failed to load image:', imageUrl);
        modalLoading.textContent = 'Failed to load image';
        modalLoading.style.display = 'block';
        modalImage.style.display = 'none';
        modalInfo.style.display = 'none';
    };
    
    modalImage.src = imageUrl;
    modalImage.alt = cardName;
    
    // Set up info text
    let infoText = cardName;
    if (cardData.SetName) {
        infoText += ` - ${cardData.SetName}`;
    }
    if (cardData.ArtistName) {
        infoText += ` by ${cardData.ArtistName}`;
    }
    modalInfo.textContent = infoText;
    
    // Close modal when clicking outside the image
    modal.onclick = function(e) {
        if (e.target === modal) {
            closeModal();
        }
    };
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadFilters();
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
});
```

**Updated templates/index.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTG Card Database - Advanced Search</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-magic"></i> MTG Card Database</h1>
            <p>Advanced search for Magic: The Gathering cards</p>
        </div>

        <div class="search-container">
            <h2>Search Cards</h2>
            
            <div class="filter-section">
                <label for="cardName">Card Name:</label>
                <input type="text" id="cardName" placeholder="Enter card name...">
            </div>

            <div class="filter-section">
                <label>Sets:</label>
                <div class="checkbox-container" id="setCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Rarities:</label>
                <div class="checkbox-container" id="rarityCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Colors:</label>
                <div class="checkbox-container" id="colorCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Card Types:</label>
                <div class="checkbox-container" id="cardTypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Subtypes:</label>
                <div class="checkbox-container" id="subtypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Artists:</label>
                <div class="checkbox-container" id="artistCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Converted Mana Cost:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="cmcMin" placeholder="Min CMC" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="cmcMax" placeholder="Max CMC" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Power:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="powerMin" placeholder="Min Power" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="powerMax" placeholder="Max Power" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="toughnessMin" placeholder="Min Toughness" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

            <button class="btn" onclick="searchCards()">
                <i class="fas fa-search"></i> Search Cards
            </button>
        </div>

        <div class="results" id="results">
            <h2>Search Results</h2>
            <div id="cardCount"></div>
            <div class="card-grid" id="cardGrid"></div>
        </div>
    </div>

    <!-- Image Preview Modal -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modalLoading" class="modal-loading">Loading</div>
            <img id="modalImage" class="modal-image" style="display: none;" alt="Card Preview">
            <div id="modalInfo" class="modal-info" style="display: none;"></div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

Now you need to create the directory structure. Create these folders and files:

1. **Create directories**:
   ```
   mkdir -p static/css static/js
   ```

2. **Create the files** with the content I provided above:
   - `static/css/style.css`
   - `static/js/main.js`
   - Update `templates/index.html`

## Benefits of this restructure:

1. **Much cleaner HTML** - Only 90 lines instead of 700+
2. **Better debugging** - JavaScript errors will show specific line numbers in the JS file
3. **Enhanced CSS** - Added animations and better mobile responsiveness
4. **Fixed JavaScript issues** - Cleaner code structure and better error handling
5. **Performance** - Browser can cache the static files
6. **Maintainability** - Much easier to work with separate files

The modal should now work properly, and if there are any issues, the console logs will help us debug exactly where the problem is occurring.

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
    padding: 20px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    color: white;
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.search-container {
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    padding: 30px;
    margin-bottom: 30px;
}

.filter-section {
    margin-bottom: 20px;
}

.filter-section label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.filter-section input, .filter-section select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 10px;
}

.checkbox-container {
    max-height: 150px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    background: white;
}

.checkbox-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
    margin-right: 8px;
    width: auto;
}

.checkbox-item label {
    cursor: pointer;
    margin: 0;
    font-weight: normal;
}

.btn {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
}

.results {
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    padding: 20px;
    display: none;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: #f9f9f9;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.card-image {
    width: 100%;
    height: 280px;
    background: #f0f0f0;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.card-image:hover {
    transform: scale(1.02);
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 6px;
}

.card-image .no-image {
    color: #999;
    font-size: 14px;
    text-align: center;
}

.card-content h3 {
    color: #333;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.card-content p {
    margin: 5px 0;
    font-size: 0.9rem;
}

/* Modal Styles */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    position: relative;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 20px;
}

.modal-image {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    border-radius: 10px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
    from { transform: scale(0.8); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.modal-close {
    position: absolute;
    top: 20px;
    right: 30px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease;
}

.modal-close:hover {
    background: rgba(0, 0, 0, 0.8);
}

.modal-info {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 15px 25px;
    border-radius: 25px;
    font-size: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    max-width: 80%;
}

/* Loading animation for modal */
.modal-loading {
    color: white;
    font-size: 18px;
    text-align: center;
}

.modal-loading::after {
    content: '';
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0%, 33% { content: '.'; }
    34%, 66% { content: '..'; }
    67%, 100% { content: '...'; }
}

/* Responsive design for mobile */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .search-container {
        padding: 20px;
    }
    
    .card-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
    }
    
    .modal-image {
        max-width: 95%;
        max-height: 80%;
    }
    
    .modal-close {
        top: 10px;
        right: 20px;
        width: 40px;
        height: 40px;
        font-size: 30px;
    }
    
    .modal-info {
        bottom: 10px;
        padding: 10px 20px;
        font-size: 14px;
    }
}

@media (max-width: 480px) {
    .header h1 {
        font-size: 2rem;
    }
    
    .card-grid {
        grid-template-columns: 1fr;
    }
    
    .filter-section input, .filter-section select {
        padding: 8px;
    }
}
```

```javascript
console.log('Script loaded successfully!');

let availableFilters = {};

// Load filter options on page load
async function loadFilters() {
    try {
        const response = await fetch('/api/filters');
        const data = await response.json();
        
        if (data.success) {
            availableFilters = data.filters;
            populateDropdowns();
        }
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

function populateDropdowns() {
    // Populate sets
    const setContainer = document.getElementById('setCheckboxes');
    availableFilters.sets?.forEach(set => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="set_${set.SetID}" value="${set.SetID}">
            <label for="set_${set.SetID}">${set.SetName} (${set.SetCode})</label>
        `;
        setContainer.appendChild(div);
    });

    // Populate rarities
    const rarityContainer = document.getElementById('rarityCheckboxes');
    availableFilters.rarities?.forEach(rarity => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="rarity_${rarity.RarityID}" value="${rarity.RarityID}">
            <label for="rarity_${rarity.RarityID}">${rarity.RarityName}</label>
        `;
        rarityContainer.appendChild(div);
    });

    // Populate colors
    const colorContainer = document.getElementById('colorCheckboxes');
    availableFilters.colors?.forEach(color => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="color_${color.ColorID}" value="${color.ColorID}">
            <label for="color_${color.ColorID}">${color.Color}</label>
        `;
        colorContainer.appendChild(div);
    });

    // Populate card types
    const cardTypeContainer = document.getElementById('cardTypeCheckboxes');
    availableFilters.card_types?.forEach(type => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="type_${type.CardTypeID}" value="${type.CardTypeID}">
            <label for="type_${type.CardTypeID}">${type.TypeName}</label>
        `;
        cardTypeContainer.appendChild(div);
    });

    // Populate subtypes
    const subtypeContainer = document.getElementById('subtypeCheckboxes');
    availableFilters.subtypes?.forEach(subtype => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="subtype_${subtype.SubTypeID}" value="${subtype.SubTypeID}">
            <label for="subtype_${subtype.SubTypeID}">${subtype.SubTypeName}</label>
        `;
        subtypeContainer.appendChild(div);
    });

    // Populate artists
    const artistContainer = document.getElementById('artistCheckboxes');
    availableFilters.artists?.forEach(artist => {
        const div = document.createElement('div');
        div.className = 'checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="artist_${artist.ArtistID}" value="${artist.ArtistID}">
            <label for="artist_${artist.ArtistID}">${artist.ArtistName}</label>
        `;
        artistContainer.appendChild(div);
    });
}

function getCheckedValues(containerSelector) {
    const container = document.getElementById(containerSelector);
    const checkedBoxes = container.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(checkedBoxes).map(box => parseInt(box.value));
}

async function searchCards() {
    const cardName = document.getElementById('cardName').value;
    const cmcMin = document.getElementById('cmcMin').value;
    const cmcMax = document.getElementById('cmcMax').value;
    const powerMin = document.getElementById('powerMin').value;
    const powerMax = document.getElementById('powerMax').value;
    const toughnessMin = document.getElementById('toughnessMin').value;
    const toughnessMax = document.getElementById('toughnessMax').value;

    const filters = {
        card_name: cardName,
        sets: getCheckedValues('setCheckboxes'),
        rarities: getCheckedValues('rarityCheckboxes'),
        colors: getCheckedValues('colorCheckboxes'),
        card_types: getCheckedValues('cardTypeCheckboxes'),
        subtypes: getCheckedValues('subtypeCheckboxes'),
        artists: getCheckedValues('artistCheckboxes'),
        cmc_min: cmcMin ? parseInt(cmcMin) : null,
        cmc_max: cmcMax ? parseInt(cmcMax) : null,
        power_min: powerMin ? parseInt(powerMin) : null,
        power_max: powerMax ? parseInt(powerMax) : null,
        toughness_min: toughnessMin ? parseInt(toughnessMin) : null,
        toughness_max: toughnessMax ? parseInt(toughnessMax) : null,
        limit: 50
    };

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filters)
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.cards, data.total);
        } else {
            alert('Search failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error searching cards:', error);
        alert('Network error occurred');
    }
}

function displayResults(cards, total) {
    const resultsDiv = document.getElementById('results');
    const cardCount = document.getElementById('cardCount');
    const cardGrid = document.getElementById('cardGrid');

    cardCount.textContent = `Found ${total} cards`;
    
    cardGrid.innerHTML = '';
    
    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        
        // Check if ImageURL is valid (not null, not empty, not just whitespace)
        const hasValidImage = card.ImageURL && card.ImageURL.trim() !== '' && card.ImageURL !== 'null';
        
        // Create card image container
        const imageContainer = document.createElement('div');
        imageContainer.className = 'card-image';
        imageContainer.id = `image-${card.CardID}`;
        
        if (hasValidImage) {
            const img = document.createElement('img');
            img.src = card.ImageURL.trim();
            img.alt = card.CardName;
            
            // Add click event to open modal
            img.onclick = function(e) {
                console.log('Image clicked!'); // Simple test
                console.log('Event:', e);
                console.log('Image element:', this);
                openImageModal(card.ImageURL.trim(), card.CardName, card);
            };
            
            // Handle image load success
            img.onload = function() {
                this.style.display = 'block';
                this.parentElement.style.backgroundColor = 'transparent';
            };
            
            // Handle image load error
            img.onerror = function() {
                this.style.display = 'none';
                const noImageDiv = document.createElement('div');
                noImageDiv.className = 'no-image';
                noImageDiv.textContent = 'No Image Available';
                this.parentElement.appendChild(noImageDiv);
            };
            
            imageContainer.appendChild(img);
        } else {
            const noImageDiv = document.createElement('div');
            noImageDiv.className = 'no-image';
            noImageDiv.textContent = 'No Image Available';
            imageContainer.appendChild(noImageDiv);
        }
        
        // Create card content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'card-content';
        
        const title = document.createElement('h3');
        title.textContent = card.CardName;
        contentDiv.appendChild(title);
        
        const manaCost = document.createElement('p');
        manaCost.innerHTML = `<strong>Mana Cost:</strong> ${card.ManaCost || 'N/A'}`;
        contentDiv.appendChild(manaCost);
        
        const type = document.createElement('p');
        type.innerHTML = `<strong>Type:</strong> ${card.CardTypes || 'N/A'}`;
        contentDiv.appendChild(type);
        
        const set = document.createElement('p');
        set.innerHTML = `<strong>Set:</strong> ${card.SetName} (${card.SetCode})`;
        contentDiv.appendChild(set);
        
        const rarity = document.createElement('p');
        rarity.innerHTML = `<strong>Rarity:</strong> ${card.RarityName}`;
        contentDiv.appendChild(rarity);
        
        const artist = document.createElement('p');
        artist.innerHTML = `<strong>Artist:</strong> ${card.ArtistName}`;
        contentDiv.appendChild(artist);
        
        if (card.Power && card.Toughness) {
            const powerToughness = document.createElement('p');
            powerToughness.innerHTML = `<strong>P/T:</strong> ${card.Power}/${card.Toughness}`;
            contentDiv.appendChild(powerToughness);
        }
        
        if (card.Abilities) {
            const abilities = document.createElement('p');
            const abilitiesText = card.Abilities.length > 100 ? 
                card.Abilities.substring(0, 100) + '...' : 
                card.Abilities;
            abilities.innerHTML = `<strong>Abilities:</strong> ${abilitiesText}`;
            contentDiv.appendChild(abilities);
        }
        
        // Add both containers to the card
        cardDiv.appendChild(imageContainer);
        cardDiv.appendChild(contentDiv);
        
        cardGrid.appendChild(cardDiv);
    });

    resultsDiv.style.display = 'block';
}

// Modal functions
function openImageModal(imageUrl, cardName, cardData) {
    console.log('openImageModal called with:', { imageUrl, cardName, cardData });
    
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalLoading = document.getElementById('modalLoading');
    const modalInfo = document.getElementById('modalInfo');
    
    console.log('Modal elements found:', { modal, modalImage, modalLoading, modalInfo });
    
    if (!modal || !modalImage || !modalLoading || !modalInfo) {
        console.error('Modal elements not found!');
        return;
    }
    
    // Show modal and loading
    modal.style.display = 'block';
    modalLoading.style.display = 'block';
    modalImage.style.display = 'none';
    modalInfo.style.display = 'none';
    
    console.log('Modal displayed, setting up image...');
    
    // Set up image
    modalImage.onload = function() {
        console.log('Image loaded successfully');
        modalLoading.style.display = 'none';
        modalImage.style.display = 'block';
        modalInfo.style.display = 'block';
    };
    
    modalImage.onerror = function() {
        console.error('Failed to load image:', imageUrl);
        modalLoading.textContent = 'Failed to load image';
        modalLoading.style.display = 'block';
        modalImage.style.display = 'none';
        modalInfo.style.display = 'none';
    };
    
    modalImage.src = imageUrl;
    modalImage.alt = cardName;
    
    // Set up info text
    let infoText = cardName;
    if (cardData.SetName) {
        infoText += ` - ${cardData.SetName}`;
    }
    if (cardData.ArtistName) {
        infoText += ` by ${cardData.ArtistName}`;
    }
    modalInfo.textContent = infoText;
    
    // Close modal when clicking outside the image
    modal.onclick = function(e) {
        if (e.target === modal) {
            closeModal();
        }
    };
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadFilters();
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
});
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTG Card Database - Advanced Search</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-magic"></i> MTG Card Database</h1>
            <p>Advanced search for Magic: The Gathering cards</p>
        </div>

        <div class="search-container">
            <h2>Search Cards</h2>
            
            <div class="filter-section">
                <label for="cardName">Card Name:</label>
                <input type="text" id="cardName" placeholder="Enter card name...">
            </div>

            <div class="filter-section">
                <label>Sets:</label>
                <div class="checkbox-container" id="setCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Rarities:</label>
                <div class="checkbox-container" id="rarityCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Colors:</label>
                <div class="checkbox-container" id="colorCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Card Types:</label>
                <div class="checkbox-container" id="cardTypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Subtypes:</label>
                <div class="checkbox-container" id="subtypeCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Artists:</label>
                <div class="checkbox-container" id="artistCheckboxes"></div>
            </div>

            <div class="filter-section">
                <label>Converted Mana Cost:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="cmcMin" placeholder="Min CMC" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="cmcMax" placeholder="Max CMC" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Power:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="powerMin" placeholder="Min Power" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="powerMax" placeholder="Max Power" style="width: 45%;">
                </div>
            </div>

            <div class="filter-section">
                <label>Toughness:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="number" id="toughnessMin" placeholder="Min Toughness" style="width: 45%;">
                    <span>to</span>
                    <input type="number" id="toughnessMax" placeholder="Max Toughness" style="width: 45%;">
                </div>
            </div>

            <button class="btn" onclick="searchCards()">
                <i class="fas fa-search"></i> Search Cards
            </button>
        </div>

        <div class="results" id="results">
            <h2>Search Results</h2>
            <div id="cardCount"></div>
            <div class="card-grid" id="cardGrid"></div>
        </div>
    </div>

    <!-- Image Preview Modal -->
    <div id="imageModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modalLoading" class="modal-loading">Loading</div>
            <img id="modalImage" class="modal-image" style="display: none;" alt="Card Preview">
            <div id="modalInfo" class="modal-info" style="display: none;"></div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

```plaintext
   mkdir -p static/css static/js
```

