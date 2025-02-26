document.getElementById("check-code").addEventListener("click", function() {
    fetch("/check_voting_status").then(response => response.json()).then(data => {
        if (data.active) {
            document.getElementById("status-message").style.display = "none";
            document.getElementById("vote-section").style.display = "block";

            let candidates = data.candidates;
            let candidateButtons = document.getElementById("candidate-buttons");
            candidateButtons.innerHTML = "";

            candidates.forEach(candidate => {
                let button = document.createElement("button");
                button.textContent = candidate;
                button.onclick = function() {
                    fetch("/vote", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ candidate: candidate })
                    }).then(() => {
                        document.getElementById("status-message").textContent = "Your vote has been recorded.";
                        document.getElementById("vote-section").style.display = "none";
                        document.getElementById("status-message").style.display = "block";
                    });
                };
                candidateButtons.appendChild(button);
            });
        } else {
            alert("Voting session has not started.");
        }
    });
});
