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
                console.log('Image clicked!');
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

// Move the escape key event listener outside the function to avoid duplicates
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

// Load filters when page loads
loadFilters();

document.addEventListener('click', (e) => {
  const img = e.target.closest('.card-image img');
  if (img) {
    console.log('Delegated image click:', img);
  }
});
