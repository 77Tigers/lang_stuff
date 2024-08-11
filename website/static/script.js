// Function to add click event listeners to boxes
function addBoxEventListeners() {
    document.querySelectorAll('.box').forEach(box => {
        box.addEventListener('click', function () {
            // Store the selected box
            selectedBox = {
                line: this.closest('.row').getAttribute('data-line'),
                position: this.getAttribute('data-position'),
                element: this
            };

            // Highlight the selected box (optional)
            document.querySelectorAll('.box').forEach(b => b.style.border = 'none');
            this.style.border = '2px solid red'; // Example highlight
        });
    });
}

// Initial event listener setup
addBoxEventListeners();

// Handle button clicks on the side panel
document.getElementById('hide-button').addEventListener('click', function () {
    if (selectedBox) {
        processAction('hide');
    }
});

document.getElementById('add-to-core-button').addEventListener('click', function () {
    if (selectedBox) {
        // get the middle word that is currently selected
        let word = selectedBox.element.querySelector('.middle').innerText;
        fetch('/add-to-core', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                word: word,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Added word to core: ${word}`);
        });
    }
});

document.getElementById('gpt-button').addEventListener('click', function () {
    if (selectedBox) {
        processAction('gpt');
    }
});

// Handle song request
document.getElementById('request-button').addEventListener('click', function () {
    const songName = document.getElementById('song-dropdown').value;

    fetch('/request-song', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ song: songName }),
    })
    .then(response => response.json())
    .then(data => {
        // Clear existing rows
        document.querySelector('.container').innerHTML = '';

        // Render the new rows
        data.forEach((row, lineIndex) => {
            const rowElement = document.createElement('div');
            rowElement.classList.add('row');
            rowElement.setAttribute('data-line', lineIndex);

            row[0].forEach((chunk, positionIndex) => {
                const boxElement = document.createElement('div');
                boxElement.classList.add('box');
                boxElement.setAttribute('data-position', positionIndex);

                boxElement.innerHTML = `
                    <div class="top">${chunk[0]}</div>
                    <div class="middle">${chunk[1]}</div>
                    <div class="bottom">${chunk[2]}</div>
                `;

                rowElement.appendChild(boxElement);
            });

            document.querySelector('.container').appendChild(rowElement);

            // Insert the full line's lyrics below the row
            const lyricsElement = document.createElement('div');
            lyricsElement.classList.add('full-lyrics');
            //lyricsElement.style.color = 'white';  // Style for lyrics text
            //lyricsElement.style.marginBottom = '10px'; // Space after lyrics
            lyricsElement.innerText = row[1];  // **Insert the full line's lyrics**

            document.querySelector('.container').appendChild(lyricsElement);  // Append the lyrics below the row
        });

        // Re-assign event listeners to the newly added boxes
        addBoxEventListeners();
    });
});

// Process action for the side panel buttons
function processAction(action) {
    fetch('/process-action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            line: selectedBox.line,
            position: selectedBox.position,
            action: action
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(`Action processed: ${action} on line ${data.line}, position ${data.position}`);
    });
}