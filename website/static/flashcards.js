document.addEventListener('DOMContentLoaded', () => {
    const flashcard = document.getElementById('flashcard');
    let question = "";
    let answer = "";

    let frontOfCard = true;
    let card_no = 0;

    function newFlashcard() {
        fetch(
            '/flashcards/get?card=' + card_no,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        ).then(response => response.json())
        .then(data => {
            question = data.question;
            answer = data.answer;
            // Update flashcard content
            document.getElementById('front').innerText = question|| 'No question available';
            document.getElementById('back').innerText = answer || 'No answer available';
        });
    }

    flashcard.addEventListener('click', async () => {
        // Flip the card
        flashcard.classList.toggle('flip');
    });

    // add event listener for none button
    document.getElementById('none').addEventListener('click', () => {
        // if the card is flipped, flip it back
        if (flashcard.classList.contains('flip')) {
            flashcard.classList.toggle('flip');
        }
        frontOfCard = true;
        // get a new flashcard
        card_no++;
        newFlashcard();
    });
});
