selectedBox = null;

function is_english(word) {
    return [...word].every(c => " ?...~!abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".includes(c));
}

// Function to add click event listeners to boxes
function addBoxEventListeners() {
    document.querySelectorAll('.box').forEach(box => {
        box.addEventListener('click', function () {
            removeBoxStyles();

            // enable the add to core button
            document.getElementById('add-to-core-button').disabled = false;

            // Store the selected box
            selectedBox = {
                line: this.closest('.row').getAttribute('data-line'),
                position: this.getAttribute('data-position'),
                element: this
            };

            if (is_english(this.querySelector('.middle').innerText)) {
                // if the word is english etc, do not select it
                removeBoxStyles();
                document.getElementById('add-to-core-button').disabled = true;
                selectedBox = null;
                return;
            }

            // this.style.border = '2px solid red'; // Example highlight
            // better highlight that doesn't change the box size
            this.style.boxShadow = '0 0 0 2px red';
            // make shadow more important
            this.style.zIndex = '1';

            // request word info from server
            const word = this.querySelector('.middle').innerText;
            fetch('/word-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ word: word }),
            }).then(
                response => response.json()
            ).then(data => {
                document.getElementById('word-info').innerText = data['info'];
            });
        });
    });
}

document.getElementById('add-to-core-button').disabled = true;

function removeBoxStyles() {
    // document.querySelectorAll('.box').forEach(b => {
    //     b.style.boxShadow = 'none';
    //     b.style.zIndex = '0';
    // });
    if (selectedBox) {
        selectedBox.element.style.boxShadow = 'none';
        selectedBox.element.style.zIndex = '0';
        document.getElementById('word-info').innerText = '...';
    }
}

// remove box styles when you press esc
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        removeBoxStyles();
        document.getElementById('add-to-core-button').disabled = true;
        selectedBox = null;
    }
    if (event.key === "c") {
        if (selectedBox) {
            // get the middle word that is currently selected
            let word = selectedBox.element.querySelector('.middle').innerText;
            if (readingModeEnabled) {
                addWordToCore(word);
            } else {
                readingModeEnabled = true;
                readingModeUpdate();
            }
        }
    }
    if (event.key === "m") {
        readingModeEnabled = !readingModeEnabled;
        readingModeUpdate();
    }
});

function addWordToCore(word) {
    fetch('/add-to-core', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word: word }),
    })
    .then(response => response.json())
    .then(data => {
        requestChosenSong();
        console.log(`Added word to core: ${word}`);
    });
}

document.getElementById('add-to-core-button').addEventListener('click', function () {
    if (selectedBox) {
        // get the middle word that is currently selected
        let word = selectedBox.element.querySelector('.middle').innerText;
        addWordToCore(word);
    }
});

function get_tones_from(pinyin) {
    let answer = [];
    words = pinyin.split(" ");
    for (let i = 0; i < words.length; i++) {
        let word = words[i];
        if (" ?...;~!".includes(word)) {
            continue;
        }
        let tone = "|";
        for (let j = 0; j < word.length; j++) {
            let c = word[j];
            // "aeiouü"
            if ("āēīōūǖ".includes(c)) {
                tone = "—";
                break;
            } else if ("áéíóúǘ".includes(c)) {
                tone = "⟋";
                break;
            } else if ("ǎěǐǒǔǚ".includes(c)) {
                tone = "⟍⟋";
                break;
            } else if ("àèìòùǜ".includes(c)) {
                tone = "⟍";
                break;
            }
        }
        answer.push(tone);
    }

    return answer.join("       ");
}

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
        document.querySelector('#container').innerHTML = '';

        // Render the new rows
        data.forEach((row, lineIndex) => {
            // Insert the full line's lyrics above the row
            const lyricsElement = document.createElement('div');
            lyricsElement.classList.add('full-lyrics');
            lyricsElement.innerText = row[1];  // **Insert the full line's lyrics**
            document.querySelector('#container').appendChild(lyricsElement);  // Append the lyrics above the row

            const rowElement = document.createElement('div');
            rowElement.classList.add('row');
            rowElement.setAttribute('data-line', lineIndex);

            row[0].forEach((chunk, positionIndex) => {
                const boxElement = document.createElement('div');
                boxElement.classList.add('box');
                boxElement.setAttribute('data-position', positionIndex);

                boxElement.innerHTML = `
                    <div class="tones">${get_tones_from(chunk[0])}</div>
                    <div class="top">${chunk[0]}</div>
                    <div class="middle">${chunk[1]}</div>
                    <div class="bottom">${chunk[2]}</div>
                `;

                rowElement.appendChild(boxElement);
            });

            document.querySelector('#container').appendChild(rowElement);
        });

        // Re-assign event listeners to the newly added boxes
        addBoxEventListeners();

        // Add footer:
        const footer = document.createElement('div');
        footer.classList.add('footer');
        document.querySelector('#container').appendChild(footer);

        readingModeUpdate();
    });
}

const readingCheckbox = document.getElementById("reading-checkbox");
let readingModeEnabled = true;

const upsideDownCheckbox = document.getElementById("upside-down-checkbox");
let upsideDownModeEnabled = false;

function readingModeUpdate() {
    readingCheckbox.checked = readingModeEnabled;
    var elements = document.querySelectorAll(".row");
    elements.forEach(function(element) {
        if (readingCheckbox.checked) {
            element.classList.add("active");
        } else {
            element.classList.remove("active");
        }
    }, readingCheckbox);
}
// is reading mode enabled?
readingCheckbox.checked = readingModeEnabled;

// is upside down mode enabled?
upsideDownCheckbox.checked = upsideDownModeEnabled;

readingCheckbox.addEventListener('change', function() {
    readingModeEnabled = readingCheckbox.checked;
    readingModeUpdate();
});

upsideDownCheckbox.addEventListener('change', function() {
    upsideDownModeEnabled = upsideDownCheckbox.checked;
    upsideDownModeUpdate();
});

function upsideDownModeUpdate() {
    container = document.getElementById("container");
    upsideDownCheckbox.checked = upsideDownModeEnabled;
    if (upsideDownCheckbox.checked) {
        container.classList.add("flipped");
    } else {
        container.classList.remove("flipped");
    }
}

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

