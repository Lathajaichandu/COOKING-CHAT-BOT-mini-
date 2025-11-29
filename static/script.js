// -------------------- Search Recipe --------------------
const searchRecipe = async () => {
    const query = document.getElementById("q").value.trim();
    if (!query) return;

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p style='color:#fff;'>Searching... 🔍</p>";

    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (data.error) {
            resultsDiv.innerHTML = `<p style='color:#fff;'>${data.error}</p>`;
            return;
        }

        const recipe = data.result;
        if (!recipe) {
            resultsDiv.innerHTML = "<p style='color:#fff;'>No recipe found.</p>";
            return;
        }

        // Fetch a valid image if the default placeholder was returned
        if (recipe.image === "/static/noimage.png") {
            const imgRes = await fetch(`/api/recipe/${recipe.id}`);
            const imgData = await imgRes.json();
            recipe.image = imgData.image || "/static/noimage.png";
        }

        resultsDiv.innerHTML = "";

        const card = document.createElement("div");
        card.className = "recipe";
        card.innerHTML = `
            <img 
                src="${recipe.image}" 
                alt="${recipe.name}" 
                onerror="this.src='/static/noimage.png'" 
            />
            <div class="meta">
                <h3>${recipe.name}</h3>
                ${recipe.total_time ? `<p><strong>Time:</strong> ${recipe.total_time}</p>` : ''}
                <p><strong>Ingredients:</strong> ${recipe.ingredients.replace(/\n/g, '<br>')}</p>
                <p><strong>Instructions:</strong> ${recipe.instructions.replace(/\n/g, '<br>')}</p>
            </div>
        `;
        resultsDiv.appendChild(card);

    } catch (err) {
        console.error(err);
        resultsDiv.innerHTML = "<p style='color:#fff;'>Something went wrong. Please try again.</p>";
    }
};

// -------- Trigger search on button click or Enter key --------
document.getElementById("ask").addEventListener("click", searchRecipe);
document.getElementById("q").addEventListener("keyup", e => {
    if (e.key === "Enter") searchRecipe();
});

// -------------------- Voice Input (Telugu + English) --------------------
const micBtn = document.getElementById("mic");
let recognition = null;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    recognition = new SpeechRecognition();

    recognition.lang = "te-IN";  // Telugu (India)
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.style.display = "inline-block";

    micBtn.addEventListener("click", () => {
        recognition.start();
        micBtn.textContent = "🎙️ Listening...";
        micBtn.disabled = true;
    });

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        document.getElementById("q").value = text;

        micBtn.textContent = "🎤";
        micBtn.disabled = false;

        // Automatically perform search after speech input
        searchRecipe();
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        micBtn.textContent = "🎤";
        micBtn.disabled = false;
        alert("There was an issue with the microphone. Please try again.");
    };

    recognition.onend = () => {
        micBtn.textContent = "🎤";
        micBtn.disabled = false;
    };

} else {
    // Hide microphone button when speech recognition is unsupported
    micBtn.style.display = "none";
}
