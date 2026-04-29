// API Configuration
const API_BASE_URL = "http://localhost:8000";

// DOM Elements
const videoUrlInput = document.getElementById("videoUrl");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusDiv = document.getElementById("status");
const resultsSection = document.getElementById("resultsSection");
const errorSection = document.getElementById("errorSection");
const errorMessage = document.getElementById("errorMessage");

// Event Listeners
analyzeBtn.addEventListener("click", handleAnalyze);
videoUrlInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleAnalyze();
});

// Main Analysis Handler
async function handleAnalyze() {
    const url = videoUrlInput.value.trim();

    if (!url) {
        showStatus("Please enter a YouTube URL", "error");
        return;
    }

    try {
        showStatus("Initializing analysis...", "loading");
        analyzeBtn.disabled = true;
        resultsSection.style.display = "none";
        errorSection.style.display = "none";

        // Check Ollama connection
        await checkOllamaConnection();

        // Send analysis request
        showStatus("Analyzing video... This may take a minute.", "loading");
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                url: url,
                use_cache: true,
            }),
        });

        const data = await response.json();

        if (data.status === "success") {
            displayResults(data.data);
            showStatus("Analysis complete! ✓", "success");
            resultsSection.style.display = "block";
            errorSection.style.display = "none";
        } else {
            throw new Error(data.error || "Analysis failed");
        }
    } catch (error) {
        showError(error.message);
        errorSection.style.display = "block";
        resultsSection.style.display = "none";
    } finally {
        analyzeBtn.disabled = false;
    }
}

// Check Ollama Connection
async function checkOllamaConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error(
                "Ollama is not running. Start it with: ollama serve"
            );
        }
    } catch (error) {
        throw new Error(
            "Cannot connect to API. Make sure the backend is running: python src/main.py"
        );
    }
}

// Display Results
function displayResults(data) {
    const { summary, insights, fact_check, metadata, quality_metrics } = data;

    // Summary
    document.getElementById("summaryContent").innerHTML = `
        <p><strong>Summary:</strong></p>
        <p>${summary.short_summary}</p>
    `;

    // Bullet Points
    document.getElementById("bulletPoints").innerHTML = summary.bullet_points
        .map((point) => `<li>${point}</li>`)
        .join("");

    // Key Takeaways
    document.getElementById("takeaways").innerHTML = summary.key_takeaways
        .map((takeaway) => `<li>${takeaway}</li>`)
        .join("");

    // Insights
    document.getElementById("patterns").innerHTML = insights.patterns
        .map((pattern) => `<li>${pattern}</li>`)
        .join("");

    document.getElementById("actionItems").innerHTML = insights.action_items
        .map((item) => `<li>${item}</li>`)
        .join("");

    document.getElementById("relatedTopics").innerHTML = insights.related_topics
        .map((topic) => `<li>${topic}</li>`)
        .join("");

    // Fact Check Summary
    const factSummary = fact_check.summary;
    document.getElementById("factCheckSummary").innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <strong>Support Percentage:</strong> ${factSummary.support_percentage}%
            </div>
            <div>
                <strong>Average Confidence:</strong> ${(factSummary.average_confidence * 100).toFixed(1)}%
            </div>
            <div>
                <strong>Facts Checked:</strong> ${factSummary.total_facts_checked}
            </div>
            <div>
                <strong>Supported:</strong> ${factSummary.supported_facts}/${factSummary.total_facts_checked}
            </div>
        </div>
    `;

    // Fact Check Details
    document.getElementById("factCheckDetails").innerHTML = fact_check.detailed_results
        .slice(0, 5)  // Show first 5
        .map(
            (result) => `
        <div class="fact-item ${result.supported ? "" : "unsupported"}">
            <strong>${result.supported ? "✓" : "✗"} ${result.claim}</strong><br>
            <small>Confidence: ${(result.confidence * 100).toFixed(1)}% | Timestamp: ${result.timestamp}</small>
        </div>
    `
        )
        .join("");

    // Quality Metrics
    document.getElementById("confidenceScore").textContent = `${(
        quality_metrics.overall_confidence * 100
    ).toFixed(1)}%`;
    document.getElementById("supportPercentage").textContent =
        factSummary.support_percentage + "%";

    // Metadata
    document.getElementById("metadata").innerHTML = `
        <div class="metadata-item">
            <span class="metadata-label">Video ID:</span>
            <span class="metadata-value">${metadata.video_id}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Title:</span>
            <span class="metadata-value">${metadata.title}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Duration:</span>
            <span class="metadata-value">${formatSeconds(metadata.duration_seconds)}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Segments:</span>
            <span class="metadata-value">${metadata.transcript_segments_count}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">URL:</span>
            <span class="metadata-value"><a href="${metadata.url}" target="_blank">View on YouTube</a></span>
        </div>
    `;
}

// Load History
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history?limit=10`);
        const data = await response.json();

        if (data.status === "success") {
            const historyList = document.getElementById("historyList");
            historyList.innerHTML = data.data
                .reverse()
                .map(
                    (item) => `
                <div class="history-item" onclick="loadAnalysisFromHistory('${item.metadata.video_id}')">
                    <div>
                        <strong>${item.metadata.title}</strong><br>
                        <small>Video ID: ${item.metadata.video_id}</small>
                    </div>
                    <small>${new Date(item.saved_at).toLocaleDateString()}</small>
                </div>
            `
                )
                .join("");
        }
    } catch (error) {
        console.error("Failed to load history:", error);
    }
}

// Load Analysis from History
async function loadAnalysisFromHistory(videoId) {
    try {
        const response = await fetch(`${API_BASE_URL}/similar/${videoId}`);
        const data = await response.json();

        if (data.status === "success" && data.data.length > 0) {
            displayResults(data.data[0]);
            resultsSection.style.display = "block";
            errorSection.style.display = "none";
        }
    } catch (error) {
        console.error("Failed to load analysis:", error);
    }
}

// Utility Functions
function showStatus(message, type = "info") {
    statusDiv.textContent = message;
    statusDiv.className = `status show ${type}`;
}

function showError(message) {
    errorMessage.textContent = message;
    statusDiv.textContent = "";
    statusDiv.className = "status";
}

function resetForm() {
    videoUrlInput.value = "";
    resultsSection.style.display = "none";
    errorSection.style.display = "none";
    statusDiv.textContent = "";
    statusDiv.className = "status";
}

function formatSeconds(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    }
    return `${minutes}m ${secs}s`;
}

// Load history on page load
document.addEventListener("DOMContentLoaded", loadHistory);
