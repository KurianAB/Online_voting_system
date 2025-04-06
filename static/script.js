// Tab Switching Functionality
function openTab(evt, tabName) {
    let tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";  // Hide all tab content
    }
    
    let tablinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    
    document.getElementById(tabName).style.display = "block"; // Show selected tab
    evt.currentTarget.classList.add("active");
}

// Show default tab (Generate Code) on page load
document.addEventListener("DOMContentLoaded", function () {
    document.getElementsByClassName("tab-link")[0].click();
});


// Generate Code Function
function generateCode() {
    fetch('/generate_code', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById("generated-code").textContent =  data.code;
        });
}



document.getElementById("getAnalysisBtn").addEventListener("click", function() {
    fetch("/get_vote_analysis")
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                document.getElementById("analysisResult").innerHTML = `<p>Error: ${data.error}</p>`;
                return;
            }

            const totalVotes = data.total_votes;
            let resultsHTML = `<h3>Total Votes: ${totalVotes}</h3>`;
            let highestVotes = 0;
            let winner = [];

            resultsHTML += `<h4>Votes per Candidate:</h4><ul>`;

            for (let candidate in data.candidate_votes) {
                let votes = data.candidate_votes[candidate].votes;
                let percentage = totalVotes > 0 ? ((votes / totalVotes) * 100).toFixed(2) : 0;

                resultsHTML += `<div>${candidate}: ${votes} votes (${percentage}%)</div>`;

                // Determine winner(s)
                if (votes > highestVotes) {
                    highestVotes = votes;
                    winner = [candidate];
                } else if (votes === highestVotes) {
                    winner.push(candidate);
                }
            }

            resultsHTML += `</ul>`;

            // Display the winner
            if (winner.length === 1) {
                resultsHTML += `<h3>Winner: ${winner[0]} with ${highestVotes} votes!</h3>`;
            } else {
                resultsHTML += `<h3>Tie between: ${winner.join(", ")} with ${highestVotes} votes each!</h3>`;
            }

            document.getElementById("analysisResult").innerHTML = resultsHTML;
        })
        .catch(error => {
            document.getElementById("analysisResult").innerHTML = `<p>Error fetching analysis.</p>`;
            console.error(error);
        });
});



document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabs.forEach((tab) => {
        tab.addEventListener("click", function () {
            // Remove active class from all tabs
            tabs.forEach((t) => t.classList.remove("active"));
            // Hide all tab contents
            tabContents.forEach((content) => content.style.display = "none");

            // Activate the clicked tab
            this.classList.add("active");
            const targetTab = this.getAttribute("data-tab");
            document.getElementById(targetTab).style.display = "block";
        });
    });

    // Show the first tab by default
    tabs[0].classList.add("active");
    tabContents[0].style.display = "block";
});


document.addEventListener("DOMContentLoaded", function() {
    const numCandidatesSelect = document.getElementById("num-candidates");
    const candidateList = document.getElementById("candidate-list");
    
    numCandidatesSelect.addEventListener("change", function() {
        candidateList.innerHTML = "";
        let numCandidates = parseInt(numCandidatesSelect.value);
        
        for (let i = 1; i <= numCandidates; i++) {
            let input = document.createElement("input");
            input.type = "text";
            input.className = "candidate-name";
            input.placeholder = `Candidate ${i} Name`;
            input.required = true;
            candidateList.appendChild(input);
            candidateList.appendChild(document.createElement("br"));
        }
    });

    document.getElementById("start-voting").addEventListener("click", function() {
        let sessionName = document.getElementById("session-name").value.trim();
        let candidateInputs = document.querySelectorAll(".candidate-name");
        let candidates = [];

        candidateInputs.forEach(input => {
            let name = input.value.trim();
            if (name) candidates.push(name);
        });

        if (sessionName === "" || candidates.length < 2) {
            alert("Enter a session name and at least 2 candidates.");
            return;
        }

        fetch("/start_voting", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_name: sessionName, candidates: candidates })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                document.getElementById("voting-message").style.display = "block";
                document.getElementById("start-voting").disabled = true;
                document.getElementById("stop-voting").disabled = false;
            } else {
                alert("Error starting voting session.");
            }
        });
    });

    document.getElementById("stop-voting").addEventListener("click", function() {
        fetch("/stop_voting", { method: "POST" }).then(response => response.json()).then(data => {
            if (data.success) {
                document.getElementById("voting-message").style.display = "none";
                document.getElementById("start-voting").disabled = false;
                document.getElementById("stop-voting").disabled = true;
                alert("Voting session has ended.");
            }
        });
    });
});


