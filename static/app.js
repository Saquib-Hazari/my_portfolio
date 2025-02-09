document.querySelectorAll(".expanded").forEach((button) => {
  button.addEventListener("click", function () {
    const card = this.closest(".card"); // Get the nearest card
    const allCards = document.querySelectorAll(".card"); // Get all cards

    allCards.forEach((c) => {
      if (c !== card) {
        c.classList.remove("active"); // Close other expanded cards
      }
    });

    card.classList.toggle("active"); // Toggle only the clicked card
  });
});

// Form submit
document
  .getElementById("contactForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    let formData = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      message: document.getElementById("message").value,
    };

    let response = await fetch("http://127.0.0.1:5000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    let result = await response.json();

    if (response.ok) {
      document.getElementById("thankYouMessage").style.display = "block"; // Show Thank You message
      document.getElementById("contactForm").reset(); // Clear the form
    } else {
      alert("Something went wrong! Please try again.");
    }
  });
