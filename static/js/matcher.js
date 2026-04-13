// ===================== MATCHER.JS =====================
// Handles swipe left/right logic for "Book Matcher" Tinder-like interface.

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".swipe-card");
  const likeBtn = document.getElementById("like");
  const dislikeBtn = document.getElementById("dislike");

  let currentIndex = 0;

  // Function to show the next card
  const showNextCard = () => {
    if (currentIndex < cards.length - 1) {
      cards[currentIndex].style.display = "none";
      currentIndex++;
    } else {
      document.getElementById("card-stack").innerHTML = "<h3>✨ No more books! Try refreshing ✨</h3>";
    }
  };

  // Function to send like/dislike to backend
  const sendReaction = (bookId, liked) => {
    fetch(`/matcher/reaction/${bookId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ liked })
    }).then(res => res.json())
      .then(data => console.log(data))
      .catch(err => console.error(err));
  };

  // Like button
  likeBtn.addEventListener("click", () => {
    const currentCard = cards[currentIndex];
    if (!currentCard) return;

    const bookId = currentCard.getAttribute("data-id");
    currentCard.style.animation = "swipeRight 0.6s forwards";
    sendReaction(bookId, true);
    setTimeout(showNextCard, 500);
  });

  // Dislike button
  dislikeBtn.addEventListener("click", () => {
    const currentCard = cards[currentIndex];
    if (!currentCard) return;

    const bookId = currentCard.getAttribute("data-id");
    currentCard.style.animation = "swipeLeft 0.6s forwards";
    sendReaction(bookId, false);
    setTimeout(showNextCard, 500);
  });
});
