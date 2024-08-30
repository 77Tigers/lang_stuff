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

            removeBoxStyles();

            // this.style.border = '2px solid red'; // Example highlight
            // better highlight that doesn't change the box size
            this.style.boxShadow = '0 0 0 2px red';
            // make shadow more important
            this.style.zIndex = '1';
        });
    });
}

function removeBoxStyles() {
    // Highlight the selected box (optional)
    document.querySelectorAll('.box').forEach(b => {
        b.style.boxShadow = 'none';
        b.style.zIndex = '0';
    });
}

// remove box styles when you press esc
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        removeBoxStyles();
        selectedBox = null;
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

// document.getElementById('gpt-button').addEventListener('click', function () {
//     if (selectedBox) {
//         processAction('gpt');
//     }
// });

function requestChosenSong() {
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
            // Insert the full line's lyrics above the row
            const lyricsElement = document.createElement('div');
            lyricsElement.classList.add('full-lyrics');
            lyricsElement.innerText = row[1];  // **Insert the full line's lyrics**
            document.querySelector('.container').appendChild(lyricsElement);  // Append the lyrics above the row

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
        });

        // Re-assign event listeners to the newly added boxes
        addBoxEventListeners();

        // Add footer:
        const footer = document.createElement('div');
        footer.classList.add('footer');
        document.querySelector('.container').appendChild(footer);

        readingModeUpdate();
    });
}

const readingCheckbox = document.getElementById("toggle-checkbox");
function readingModeUpdate() {
    var elements = document.querySelectorAll(".top");
    elements.forEach(function(element) {
        if (readingCheckbox.checked) {
            element.classList.add("active");
        } else {
            element.classList.remove("active");
        }
    }, readingCheckbox);
}

readingCheckbox.addEventListener('change', readingModeUpdate);

document.addEventListener('keypress', function(event) {
    if (event.key === "r") {
        requestChosenSong();
    }
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

window.onload = function() {
    // get URL and check if the path is /songs/<song_name>
    const url = new URL(window.location.href);
    const path = url.pathname;
    const words = path.split('/');
    if (words[1] == 'songs' && words.length == 3) {
        const songName = words[2];
        document.getElementById('song-dropdown').value = songName;
        requestChosenSong();
    }

    const dropdown = document.getElementById('song-dropdown');
    dropdown.addEventListener('change', function() {
        const songName = dropdown.value;
        window.location.href = `/songs/${songName}`;
    });
};

